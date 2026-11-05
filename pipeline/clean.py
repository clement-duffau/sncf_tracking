"""Tables propres : extrémités, liaisons (non orientées) et mesures mensuelles par liaison × sens.

- TGV : services National et International additionnés ; mois à 0 train prévu ignorés ;
  circulés = prévus − annulés ; gravité > 30 / > 60 min mise à NULL si invalide (mois déclarés
  `gravite_invalide` dans events.yaml, valeurs négatives ou hiérarchie rompue) ; causes converties
  en nombres de trains (% × trains en retard), NULL quand elles ne sont pas renseignées.
- Intercités : libellés composites normalisés (« BRIVE/CAHORS » = « CAHORS/BRIVE »), doublons du même
  mois additionnés, mois à 0 train programmé ignorés.
"""

from __future__ import annotations

from datetime import date

import duckdb

from . import config
from .events import Evenement, debut_rupture_causes, mois_effet

CAUSES = ["externe", "infra", "gestion_trafic", "materiel_roulant", "gestion_gare", "prise_en_charge_voyageurs"]


def _extremites(con: duckdb.DuckDBPyConnection) -> None:
    """Extrémité = une gare (TGV) ou un groupe de gares (libellé Intercités composite)."""
    con.sql("""
    create or replace table extremite_libelle as
    with libs as (
      select distinct g libelle from (select gare_depart g from tgv_aqst union select gare_arrivee from tgv_aqst
                                      union select depart from intercites union select arrivee from intercites)),
    morceaux as (select libelle, unnest(string_split(libelle, '/')) morceau from libs)
    select m.libelle, list_sort(list_distinct(list(lg.gare))) gares
    from morceaux m join libelle_gare lg on lg.libelle = m.morceau group by 1
    """)
    con.sql("""
    create or replace table extremite as
    select distinct gares, array_to_string(gares, '+') id from extremite_libelle
    """)
    lignes = []
    for ext_id, gares in con.sql("select id, gares from extremite").fetchall():
        infos = con.execute(
            "select nom, region, pays from gare where list_contains(?, id) order by nom", [gares]).fetchall()
        lignes.append((ext_id, gares, " / ".join(r[0] for r in infos),
                       sorted({r[1] for r in infos if r[1]}), sorted({r[2] for r in infos})))
    con.sql("""create or replace table extremite (id varchar primary key, gares varchar[], nom varchar,
               regions varchar[], pays varchar[])""")
    con.executemany("insert into extremite values (?, ?, ?, ?, ?)", lignes)
    con.sql("""create or replace table extremite_libelle as
               select el.libelle, e.id extremite from extremite_libelle el
               join extremite e on e.id = array_to_string(el.gares, '+')""")


def construire(con: duckdb.DuckDBPyConnection, evts: list[Evenement]) -> None:
    _extremites(con)

    gravite_ko = sorted(mois_effet(evts, "TGV", "gravite_invalide"))
    con.sql("create or replace table mois_gravite_ko (date date)")
    if gravite_ko:
        con.executemany("insert into mois_gravite_ko values (?)", [(d,) for d in gravite_ko])
    rupture = debut_rupture_causes(evts) or date(9999, 1, 1)

    somme_causes = " + ".join(f"prct_cause_{c}" for c in CAUSES)
    causes_trains = ",\n".join(
        f"sum(case when causes_ok then prct_cause_{c} * nb_train_retard_arrivee / 100 end) cause_{c}" for c in CAUSES)

    con.sql(f"""
    create or replace table mesure_orientee as
    with t as (
      select *, date::date mois,
        ({somme_causes}) > 0 as causes_ok,
        not (date::date in (select date from mois_gravite_ko)
             or nb_train_retard_sup_30 < 0 or nb_train_retard_sup_60 < 0
             or nb_train_retard_sup_30 < nb_train_retard_sup_60
             or nb_train_retard_sup_15 < nb_train_retard_sup_30) as gravite_ok
      from tgv_aqst where nb_train_prevu > 0)
    select 'TGV' type, d.extremite dep, a.extremite arr, mois,
      sum(nb_train_prevu)::bigint prevus, sum(nb_annulation)::bigint annules,
      sum(greatest(nb_train_prevu - nb_annulation, 0))::bigint circules,
      sum(nb_train_retard_arrivee)::bigint retards,
      sum(nb_train_retard_sup_15)::bigint sup15,
      case when bool_and(gravite_ok) then sum(nb_train_retard_sup_30) end::bigint sup30,
      case when bool_and(gravite_ok) then sum(nb_train_retard_sup_60) end::bigint sup60,
      sum(nb_train_prevu * duree_moyenne) / sum(nb_train_prevu) duree,
      sum(case when causes_ok then nb_train_retard_arrivee else 0 end)::bigint retards_avec_causes,
      {causes_trains},
      case when mois >= DATE '{rupture}' then 2 else 1 end nomenclature_causes
    from t join extremite_libelle d on d.libelle = t.gare_depart join extremite_libelle a on a.libelle = t.gare_arrivee
    group by all
    union all by name
    select 'Intercités' type, d.extremite dep, a.extremite arr, date::date mois,
      sum(nombre_de_trains_programmes)::bigint prevus, sum(nombre_de_trains_annules)::bigint annules,
      sum(nombre_de_trains_ayant_circule)::bigint circules, sum(nombre_de_trains_en_retard_a_l_arrivee)::bigint retards
    from intercites i join extremite_libelle d on d.libelle = i.depart join extremite_libelle a on a.libelle = i.arrivee
    where nombre_de_trains_programmes > 0
    group by all
    """)

    # Liaisons non orientées
    pre = " ".join(f"when '{t}' then '{p}'" for t, p in config.PREFIXE_TYPE.items())
    con.sql(f"""
    create or replace table mesure as
    select (case type {pre} end) || '-' || least(dep, arr) || '--' || greatest(dep, arr) liaison,
      least(dep, arr) a, greatest(dep, arr) b,
      case when dep < arr then 'ab' else 'ba' end sens, * exclude (dep, arr)
    from mesure_orientee
    """)
    con.sql("""
    create or replace table liaison as
    with base as (
      select liaison, type, any_value(a) a, any_value(b) b, min(mois) premier_mois, max(mois) dernier_mois,
        count(distinct mois) nb_mois,
        sum(prevus * duree) filter (where duree > 0) / nullif(sum(prevus) filter (where duree > 0), 0) duree
      from mesure group by liaison, type),
    fin as (select type, max(mois) fin from mesure group by 1)
    select b.liaison id, b.type, b.a, b.b, ea.nom nom_a, eb.nom nom_b, ea.nom || ' – ' || eb.nom nom,
      list_sort(list_distinct(list_concat(ea.regions, eb.regions))) regions,
      list_sort(list_distinct(list_concat(ea.pays, eb.pays))) pays,
      not list_has_all(['France'], list_distinct(list_concat(ea.pays, eb.pays))) international,
      round(b.duree)::integer duree, b.premier_mois, b.dernier_mois, b.nb_mois,
      b.dernier_mois > f.fin - interval (12) month active
    from base b join extremite ea on ea.id = b.a join extremite eb on eb.id = b.b join fin f on f.type = b.type
    """)


def verifier_doublons(con: duckdb.DuckDBPyConnection) -> None:
    n = con.execute("select count(*) from (select liaison, sens, mois from mesure group by all having count(*) > 1)").fetchall()[0][0]
    if n:
        raise AssertionError(f"{n} doublons liaison × sens × mois dans la table mesure")


def identifiant(type_train: str, a: str, b: str) -> str:
    a, b = sorted((a, b))
    return f"{config.PREFIXE_TYPE[type_train]}-{a}--{b}"

