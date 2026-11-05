"""Profilage du jeu « Régularité mensuelle TER » (agrégé par région).

Usage : python pipeline/explore/03_ter.py
Prérequis : data/raw/ter.parquet
"""

import json

from commun import RAW, Rapport, connexion

con = connexion()
r = Rapport("03_ter", "Exploration — TER par région (regularite-mensuelle-ter)", con)

meta = json.loads((RAW / "ter.meta.json").read_text())
m = meta["metas"]["default"]
r.section("Métadonnées du portail")
r.texte(f"- Titre : {m['title']}\n- Éditeur : {m.get('publisher')}\n- Licence : {m.get('license')}\n"
        f"- Dernière modification des données : {m.get('data_processed')}\n- Nombre d'enregistrements : {m.get('records_count')}")
r.lignes += ["| champ | type | libellé | description |", "|---|---|---|---|"]
for f in meta["fields"]:
    r.lignes.append(f"| {f['name']} | {f['type']} | {f.get('label','')} | {(f.get('description') or '').replace('|','/')} |")
r.lignes.append("")

r.section("Couverture")
r.table("Période et volumes", """
select min(date) premier_mois, max(date) dernier_mois, count(distinct date) nb_mois,
  datediff('month', min(date), max(date)) + 1 nb_mois_attendus, count(*) lignes, count(distinct region) libelles_region
from ter""")
r.table("Libellés de région : période couverte", """
select region, count(*) mois, min(date) premier, max(date) dernier, round(avg(nombre_de_trains_programmes)) programmes_par_mois
from ter group by 1 order by premier, region""")
r.table("Régions-mois en double", "select date, region, count(*) from ter group by all having count(*) > 1")
r.table("Nombre de libellés par mois : paliers", """
select n libelles, count(*) nb_mois, min(date) premier, max(date) dernier
from (select date, count(*) n from ter group by 1) group by 1 order by premier""")

r.section("Cohérence des colonnes")
r.table("Contrôles", """
select count(*) lignes,
  count(*) filter (where nombre_de_trains_programmes - nombre_de_trains_annules <> nombre_de_trains_ayant_circule) circules_incoherents,
  count(*) filter (where abs(taux_de_regularite - 100 * (nombre_de_trains_ayant_circule - nombre_de_trains_en_retard_a_l_arrivee)
                     / nullif(nombre_de_trains_ayant_circule, 0)) > 0.05) taux_incoherents,
  count(*) - count(taux_de_regularite) taux_null, count(commentaires) avec_commentaire
from ter""")
r.table("Lignes où programmés − annulés ≠ circulés (échantillon récent)", """
select date, region, nombre_de_trains_programmes programmes, nombre_de_trains_annules annules, nombre_de_trains_ayant_circule circules,
  nombre_de_trains_programmes - nombre_de_trains_annules - nombre_de_trains_ayant_circule ecart
from ter where nombre_de_trains_programmes - nombre_de_trains_annules <> nombre_de_trains_ayant_circule order by date desc limit 15""")
r.table("Écart programmés − annulés − circulés : à partir de quand ?", """
select year(date) annee, count(*) lignes, count(*) filter (where nombre_de_trains_programmes - nombre_de_trains_annules <> nombre_de_trains_ayant_circule) incoherentes
from ter group by 1 order by 1""")
r.table("Commentaires : nombre par année et mentions de grève / mouvement social", """
select year(date) annee, count(commentaires) avec_commentaire, count(*) lignes,
  count(*) filter (where regexp_matches(lower(commentaires), 'gr[eè]ve|mouvement social|social')) mentionnant_greve
from ter group by 1 order by 1""")
r.table("Exemples de commentaires mentionnant une grève (20 premiers)", """
select date, region, left(commentaires, 200) commentaire from ter
where regexp_matches(lower(commentaires), 'gr[eè]ve|mouvement social') order by date limit 20""")
r.table("Mois où au moins 3 régions mentionnent une grève (candidats pour data/events.yaml)", """
select date, count(*) regions from ter where regexp_matches(lower(commentaires), 'gr[eè]ve|mouvement social')
group by 1 having count(*) >= 3 order by 1""")

r.section("Série nationale TER (somme des régions)")
r.table("Régularité et annulations par année", """
select year(date) annee, sum(nombre_de_trains_programmes) programmes,
  round(100 * sum(nombre_de_trains_annules) / sum(nombre_de_trains_programmes), 1) pct_annules,
  round(100 * (1 - sum(nombre_de_trains_en_retard_a_l_arrivee) / sum(nombre_de_trains_ayant_circule)), 1) regularite
from ter group by 1 order by 1""")
r.table("Régularité des régions actuelles sur les 12 derniers mois", """
select region, sum(nombre_de_trains_ayant_circule) circules,
  round(100 * (1 - sum(nombre_de_trains_en_retard_a_l_arrivee) / sum(nombre_de_trains_ayant_circule)), 1) regularite,
  round(100 * sum(nombre_de_trains_annules) / sum(nombre_de_trains_programmes), 1) pct_annules
from ter where date > (select max(date) from ter) - interval 12 month group by 1 order by regularite desc""")

r.ecrire()
