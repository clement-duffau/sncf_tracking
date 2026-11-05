"""Phase 2 — essais des méthodes « tendances » et « Mon trajet » sur les vraies données.

Usage : python pipeline/explore/07_tendances_mon_trajet.py
Prérequis : tgv_aqst, intercites dans data/raw/

Tendances : régularité des 12 derniers mois vs 12 mois précédents, par liaison non orientée.
  Test z avec variance binomiale gonflée par la surdispersion D (≈ 9,4 TGV, ≈ 2,3 Intercités,
  cf. 06_score_variantes) : z = Δ / sqrt(D·(p1(1−p1)/n1 + p0(1−p0)/n0)).
Mon trajet : probabilité qu'un train prévu (sens choisi, mois calendaire choisi) arrive à l'heure.
  Données = ce mois calendaire sur les années disponibles ; prior = niveau de la liaison
  (toutes saisons) × effet saisonnier du type ; posterior bêta avec n effectif = n / D.
"""

from commun import Rapport, connexion

D = {"TGV": 9.4, "Intercités": 2.3}

con = connexion()
r = Rapport("07_tendances_mon_trajet", "Phase 2 — essais tendances et « Mon trajet »", con)

con.sql("""
create or replace table lm as
select 'TGV' type, date, gare_depart dep, gare_arrivee arr,
  sum(nb_train_prevu)::double prevus, sum(nb_annulation)::double annules,
  sum(greatest(nb_train_prevu - nb_annulation, 0))::double circules, sum(nb_train_retard_arrivee)::double retards
from tgv_aqst where nb_train_prevu > 0 group by all
union all
select 'Intercités', date, depart, arrivee, sum(nombre_de_trains_programmes), sum(nombre_de_trains_annules),
  sum(nombre_de_trains_ayant_circule), sum(nombre_de_trains_en_retard_a_l_arrivee)
from intercites where nombre_de_trains_programmes > 0 group by all
""")
con.sql("create or replace table dtab (type varchar, D double)")
for k, v in D.items():
    con.execute("insert into dtab values (?, ?)", [k, v])

# ------------------------------------------------------------------ tendances
r.section("1. Tendances : 12 derniers mois vs 12 mois précédents (liaisons non orientées)")
con.sql("""
create or replace table tend as
with f as (select type, max(date) fin from lm group by 1),
x as (
  select l.type, least(dep, arr) a, greatest(dep, arr) b,
    sum(circules) filter (where date > fin - interval 12 month) n1,
    sum(retards) filter (where date > fin - interval 12 month) k1,
    sum(circules) filter (where date <= fin - interval 12 month and date > fin - interval 24 month) n0,
    sum(retards) filter (where date <= fin - interval 12 month and date > fin - interval 24 month) k0
  from lm l join f using (type) group by all)
select x.*, 1 - k1 / n1 p1, 1 - k0 / n0 p0, (1 - k1 / n1) - (1 - k0 / n0) delta,
  ((1 - k1 / n1) - (1 - k0 / n0)) / sqrt(D * ((1 - k1 / n1) * (k1 / n1) / n1 + (1 - k0 / n0) * (k0 / n0) / n0)) z
from x join dtab using (type) where n1 > 0 and n0 > 0
""")
r.table("Répartition des liaisons selon |z| (seuil proposé : |z| ≥ 2 et |Δ| ≥ 2 points)", """
select type, count(*) liaisons,
  count(*) filter (where z >= 2 and delta >= 0.02) amelioration_significative,
  count(*) filter (where z <= -2 and delta <= -0.02) degradation_significative,
  count(*) filter (where abs(z) < 2 or abs(delta) < 0.02) stable_ou_incertain,
  count(*) filter (where abs(z) >= 2 and abs(delta) < 0.02) significatif_mais_faible
from tend group by 1""")
r.table("Tendance relative : Δ liaison − Δ du type (le réseau entier a pu bouger)", """
with dt as (select type, 1 - sum(k1) / sum(n1) - (1 - sum(k0) / sum(n0)) delta_type from tend group by 1),
x as (select t.*, dt.delta_type, delta - delta_type rel, (delta - delta_type) / sqrt(D * (p1 * (1 - p1) / n1 + p0 * (1 - p0) / n0)) zr
      from tend t join dt using (type) join dtab using (type))
select type, round(100 * any_value(delta_type), 1) delta_type_pts, count(*) liaisons,
  count(*) filter (where zr >= 2 and rel >= 0.02) mieux_que_le_reseau,
  count(*) filter (where zr <= -2 and rel <= -0.02) pire_que_le_reseau
from x group by 1""")
r.table("Plus fortes améliorations (TGV)", """
select a || ' – ' || b liaison, round(n1) trains_12m, round(100 * p0, 1) reg_avant, round(100 * p1, 1) reg_12m, round(100 * delta, 1) delta_pts, round(z, 1) z
from tend where type = 'TGV' order by delta desc limit 8""")
r.table("Plus fortes dégradations (TGV)", """
select a || ' – ' || b liaison, round(n1) trains_12m, round(100 * p0, 1) reg_avant, round(100 * p1, 1) reg_12m, round(100 * delta, 1) delta_pts, round(z, 1) z
from tend where type = 'TGV' order by delta limit 8""")
r.table("Intercités : toutes les liaisons", """
select a || ' – ' || b liaison, round(n1) trains_12m, round(100 * p0, 1) reg_avant, round(100 * p1, 1) reg_12m, round(100 * delta, 1) delta_pts, round(z, 1) z
from tend where type = 'Intercités' order by delta desc""")
r.texte("Remarque : les liaisons Intercités sont ici orientées-fusionnées sans normaliser les libellés composites "
        "(« ALBI/RODEZ » et « RODEZ/ALBI » restent séparés) ; le pipeline de production normalisera.")

r.section("2. Pente sur 36 mois (régression du taux mensuel désaisonnalisé) — exemple TGV")
con.sql("""
create or replace table saison as
-- effet saisonnier du type : écart moyen du mois calendaire à la moyenne annuelle (2018–2025 hors 2020)
with m as (select type, date, 1 - sum(retards) / sum(circules) reg from lm group by all),
a as (select type, year(date) y, avg(reg) reg_an from m group by all)
select m.type, month(date) mois, avg(reg - reg_an) effet from m join a on a.type = m.type and a.y = year(m.date)
where year(date) between 2018 and 2025 and year(date) <> 2020 group by all
""")
r.table("Effet saisonnier moyen (points de régularité vs moyenne de l'année)", """
select mois, round(100 * max(effet) filter (where type = 'TGV'), 1) tgv, round(100 * max(effet) filter (where type = 'Intercités'), 1) intercites
from saison group by mois order by mois""")
r.table("Pente (points / an) sur 36 mois, désaisonnalisée — 5 plus fortes hausses et baisses TGV", """
with f as (select max(date) fin from lm where type = 'TGV'),
m as (select least(dep, arr) a, greatest(dep, arr) b, date, 1 - sum(retards) / sum(circules) reg
      from lm where type = 'TGV' and date > (select fin from f) - interval 36 month group by all),
d as (select m.*, reg - s.effet reg_ds, datediff('month', (select fin from f) - interval 36 month, date) / 12.0 t
      from m join saison s on s.type = 'TGV' and s.mois = month(m.date)),
p as (select a || ' – ' || b liaison, regr_slope(reg_ds, t) pente, regr_r2(reg_ds, t) r2, count(*) n from d group by all)
(select 'hausse' sens, liaison, round(100 * pente, 1) pts_par_an, round(r2, 2) r2, n from p order by pente desc limit 5)
union all
(select 'baisse', liaison, round(100 * pente, 1), round(r2, 2), n from p order by pente limit 5)""")

# ------------------------------------------------------------------ Mon trajet
r.section("3. « Mon trajet » : exemples")
r.texte("Probabilité qu'un **train prévu** arrive à l'heure (annulé = pas à l'heure), sens choisi, mois calendaire "
        "choisi. On prend ce mois sur les 5 dernières années disponibles hors 2020. Prior bêta centré sur "
        "(niveau de la liaison sur 24 mois + effet saisonnier), de force m = 60 trains effectifs (cf. 06). "
        "Intervalle de crédibilité à 80 %. On donne aussi la dispersion d'une année sur l'autre, qui est la "
        "vraie incertitude pour un voyage futur.")
try:
    con.sql("select qbeta(0.5, 2, 2)").fetchall()
    has_qbeta = True
except Exception:
    has_qbeta = False
if not has_qbeta:
    # DuckDB n'a pas de quantile bêta natif : approximation normale de la loi bêta (suffisante pour l'essai)
    con.sql("""create or replace macro qbeta(q, al, be) as
      al / (al + be) + (case when q < 0.5 then -1.2816 else 1.2816 end) * sqrt(al * be / ((al + be) ^ 2 * (al + be + 1)))""")
    r.texte("_Quantiles bêta approchés par une loi normale de même moyenne et variance (pas de `qbeta` natif dans DuckDB)._")
con.sql("""
create or replace macro mon_trajet(p_type, p_dep, p_arr, p_mois) as table
with f as (select max(date) fin from lm where type = p_type),
niveau as (select 1 - (sum(retards) + sum(annules)) / sum(prevus) p from lm
           where type = p_type and dep = p_dep and arr = p_arr and date > (select fin from f) - interval 24 month),
s as (select effet from saison where type = p_type and mois = p_mois),
obs as (select date, prevus, prevus - annules - retards a_l_heure from lm
        where type = p_type and dep = p_dep and arr = p_arr and month(date) = p_mois and year(date) <> 2020
        order by date desc limit 5),
agg as (select sum(prevus) n, sum(a_l_heure) k, count(*) annees,
          min(a_l_heure / prevus) pire, max(a_l_heure / prevus) meilleure, string_agg(year(date)::varchar, ',') annees_liste from obs),
post as (select n, k, annees, annees_liste, pire, meilleure, (select D from dtab where type = p_type) D,
           least(greatest((select p from niveau) + (select effet from s), 0.01), 0.99) prior_moy from agg)
select p_dep || ' → ' || p_arr trajet, p_mois mois, annees_liste, round(n) trains_prevus_obs, D,
  round(100 * prior_moy, 1) prior_pct,
  round(100 * (k / D + 60 * prior_moy) / (n / D + 60), 1) proba_pct,
  round(100 * qbeta(0.10, k / D + 60 * prior_moy, (n - k) / D + 60 * (1 - prior_moy)), 1) ic80_bas,
  round(100 * qbeta(0.90, k / D + 60 * prior_moy, (n - k) / D + 60 * (1 - prior_moy)), 1) ic80_haut,
  round(100 * pire, 1) pire_annee, round(100 * meilleure, 1) meilleure_annee
from post
""")
exemples = [
    ("TGV", "PARIS MONTPARNASSE", "TOULOUSE MATABIAU", 7),
    ("TGV", "PARIS MONTPARNASSE", "TOULOUSE MATABIAU", 10),
    ("TGV", "PARIS EST", "REIMS", 12),
    ("TGV", "MARSEILLE ST CHARLES", "TOURCOING", 8),
    ("TGV", "PARIS LYON", "BARCELONA", 7),
    ("Intercités", "PARIS-AUSTERLITZ", "BRIANÇON", 2),
    ("Intercités", "BORDEAUX-ST-JEAN", "MARSEILLE-ST-CHARLES", 7),
]
for t, d, a, mois in exemples:
    r.table(f"{t} {d} → {a}, mois {mois}", f"select * from mon_trajet('{t}', '{d}', '{a}', {mois})")

r.section("4. Variabilité d'une année sur l'autre pour un même trajet et un même mois")
r.table("Écart-type inter-annuel de la probabilité d'être à l'heure (trajet orienté × mois calendaire, ≥ 4 années hors 2020, ≥ 50 trains/mois)", """
with x as (select type, dep, arr, month(date) mois, 1 - (retards + annules) / prevus p, prevus from lm
           where year(date) <> 2020 and prevus >= 50),
g as (select type, dep, arr, mois, stddev_samp(p) sd, avg(p) moy, avg(prevus) n, count(*) annees from x group by all having count(*) >= 4)
select type, count(*) cellules, round(100 * median(sd), 1) sd_mediane_pts, round(100 * quantile_cont(sd, 0.9), 1) sd_q90_pts,
  round(100 * median(sqrt(moy * (1 - moy) / n)), 1) sd_binomiale_mediane_pts
from g group by 1""")
r.ecrire()
