"""Profilage du jeu « Régularité mensuelle Intercités ».

Usage : python pipeline/explore/02_intercites.py
Prérequis : data/raw/intercites.parquet
"""

import json

from commun import RAW, Rapport, connexion

con = connexion()
r = Rapport("02_intercites", "Exploration — Intercités (regularite-mensuelle-intercites)", con)
con.sql("create or replace view i as select * from intercites")

meta = json.loads((RAW / "intercites.meta.json").read_text())
m = meta["metas"]["default"]
r.section("Métadonnées du portail")
r.texte(f"- Titre : {m['title']}\n- Éditeur : {m.get('publisher')}\n- Licence : {m.get('license')}\n"
        f"- Dernière modification des données : {m.get('data_processed')}\n- Nombre d'enregistrements : {m.get('records_count')}")
r.lignes += ["| champ | type | libellé | description |", "|---|---|---|---|"]
for f in meta["fields"]:
    r.lignes.append(f"| {f['name']} | {f['type']} | {f.get('label','')} | {(f.get('description') or '').replace('|','/')} |")
r.lignes.append("")

r.section("Couverture temporelle")
r.table("Période, lignes, liaisons", """
select min(date) premier_mois, max(date) dernier_mois, count(distinct date) nb_mois,
  datediff('month', min(date), max(date)) + 1 nb_mois_attendus, count(*) lignes,
  count(distinct (depart, arrivee)) libelles_liaisons_orientees
from i""")
r.table("Nombre de lignes par mois : paliers", """
select n lignes_par_mois, count(*) nb_mois, min(date) premier, max(date) dernier
from (select date, count(*) n from i group by 1) group by 1 order by premier""")

r.section("Liaisons et libellés")
r.table("Liste des libellés de liaisons (orientés)", """
select depart, arrivee, count(*) lignes, count(distinct date) mois, min(date) premier, max(date) dernier,
  round(avg(nombre_de_trains_programmes)) programmes_par_mois,
  exists (select 1 from i b where b.depart = a.arrivee and b.arrivee = a.depart) retour_avec_meme_libelle
from i a group by all order by depart, arrivee""")
r.table("Noms de gares/libellés composites (contenant « / »)", """
select distinct g from (select depart g from i union select arrivee from i) where g like '%/%' order by 1""")
r.table("Liaisons ayant plusieurs lignes le même mois (doublons apparents)", """
select depart, arrivee, count(*) mois_concernes, min(date) premier, max(date) dernier
from (select date, depart, arrivee from i group by all having count(*) > 1) group by all order by depart, arrivee""")
r.table("Exemple de doublon : Paris-Austerlitz → Toulouse, 2 mois", """
select * from i where depart = 'PARIS-AUSTERLITZ' and arrivee = 'TOULOUSE-MATABIAU' and date in ('2022-01-01', '2026-05-01') order by date""")
r.table("Liaisons présentes sur les 12 derniers mois disponibles", """
select depart, arrivee, sum(nombre_de_trains_programmes) programmes, sum(nombre_de_trains_ayant_circule) circules
from i where date > (select max(date) from i) - interval 12 month group by all order by depart, arrivee""")

r.section("Cohérence des colonnes")
r.table("Contrôles", """
select count(*) lignes,
  count(*) filter (where nombre_de_trains_programmes - nombre_de_trains_annules <> nombre_de_trains_ayant_circule) circules_incoherents,
  count(*) filter (where abs(taux_de_regularite - 100 * (nombre_de_trains_ayant_circule - nombre_de_trains_en_retard_a_l_arrivee)
                     / nullif(nombre_de_trains_ayant_circule, 0)) > 0.05) taux_incoherents,
  count(*) filter (where abs(nombre_de_trains_a_l_heure_pour_un_train_en_retard_a_l_arrivee
                     - (nombre_de_trains_ayant_circule - nombre_de_trains_en_retard_a_l_arrivee) / nullif(nombre_de_trains_en_retard_a_l_arrivee, 0)) > 0.01) ratio_incoherent,
  count(*) filter (where nombre_de_trains_ayant_circule = 0) circules_zero,
  count(*) filter (where nombre_de_trains_programmes = 0) programmes_zero,
  count(*) - count(taux_de_regularite) taux_null
from i""")
r.table("Lignes à 0 train circulé, par mois", """
select date, count(*) lignes, sum(nombre_de_trains_programmes) programmes, sum(nombre_de_trains_annules) annules
from i where nombre_de_trains_ayant_circule = 0 group by 1 order by 1""")
r.table("Valeurs de taux_de_regularite quand 0 train a circulé", """
select taux_de_regularite, nombre_de_trains_a_l_heure_pour_un_train_en_retard_a_l_arrivee ratio, count(*) from i
where nombre_de_trains_ayant_circule = 0 group by all""")
r.table("Ratio « trains à l'heure pour un train en retard » quand 0 retard", """
select nombre_de_trains_a_l_heure_pour_un_train_en_retard_a_l_arrivee ratio, count(*) from i
where nombre_de_trains_en_retard_a_l_arrivee = 0 and nombre_de_trains_ayant_circule > 0 group by all order by 1""")

r.section("Séries mensuelles")
r.table("Totaux mensuels", """
select date, sum(nombre_de_trains_programmes) programmes, sum(nombre_de_trains_annules) annules,
  round(100 * sum(nombre_de_trains_annules) / nullif(sum(nombre_de_trains_programmes), 0), 1) pct_annules,
  sum(nombre_de_trains_en_retard_a_l_arrivee) retards,
  round(100 * (1 - sum(nombre_de_trains_en_retard_a_l_arrivee) / nullif(sum(nombre_de_trains_ayant_circule), 0)), 1) regularite
from i group by 1 order by 1""", max_lignes=300)

r.section("Volumes (pour le poids bayésien)")
r.table("Quantiles du nombre de trains circulés par liaison-mois (> 0), 2020 et après", """
select quantile_cont(nombre_de_trains_ayant_circule, [0.05, 0.1, 0.25, 0.5, 0.75, 0.9]) quantiles, avg(nombre_de_trains_ayant_circule) moyenne
from i where nombre_de_trains_ayant_circule > 0 and date >= '2020-01-01'""")

r.section("Gares communes avec le jeu TGV (libellés bruts)")
r.table("Gares Intercités dont le libellé, ponctuation retirée, existe aussi dans le jeu TGV", """
with ic as (select distinct g from (select depart g from i union select arrivee from i)),
     tg as (select distinct g from (select gare_depart g from tgv_aqst union select gare_arrivee from tgv_aqst))
select ic.g gare_intercites, tg.g gare_tgv from ic left join tg
  on regexp_replace(upper(ic.g), '[^A-Z]', '', 'g') = regexp_replace(upper(tg.g), '[^A-Z]', '', 'g')
order by tg.g nulls last, ic.g""")

r.ecrire()
