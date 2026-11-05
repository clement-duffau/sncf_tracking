"""Profilage des jeux « Régularité mensuelle TGV par axe » et « TGV globale ».

Usage : python pipeline/explore/08_tgv_axes_national.py
"""

import json

from commun import RAW, Rapport, connexion

con = connexion()
r = Rapport("08_tgv_axes_national", "Exploration — TGV par axe et TGV global", con)

for cle in ["tgv_axes", "tgv_national"]:
    meta = json.loads((RAW / f"{cle}.meta.json").read_text())
    m = meta["metas"]["default"]
    r.section(f"{m['title']} ({cle})")
    r.texte(f"- Licence : {m.get('license')}\n- Dernière modification des données : {m.get('data_processed')}\n"
            f"- Enregistrements : {m.get('records_count')}\n- Champs : " + ", ".join(f"`{f['name']}` ({f['type']})" for f in meta["fields"]))

r.table("TGV par axe : couverture par axe", """
select axe, count(*) mois, min(date) premier, max(date) dernier, round(avg(regularite_composite), 1) reg_moy,
  count(*) - count(regularite_composite) reg_null, count(*) - count(ponctualite_origine) ponct_null
from tgv_axes group by 1 order by 1""")
r.table("TGV par axe : régularité sur les 12 derniers mois (moyenne simple des mois)", """
select axe, round(avg(regularite_composite), 1) reg, round(avg(ponctualite_origine), 1) ponct_origine
from tgv_axes where date > (select max(date) from tgv_axes) - interval 12 month group by 1 order by 2 desc""")
r.table("TGV global : couverture", """
select min(date) premier, max(date) dernier, count(*) mois, datediff('month', min(date), max(date)) + 1 attendus,
  min(regularite_composite) reg_min, max(regularite_composite) reg_max from tgv_national""")
r.table("TGV global : moyenne annuelle (moyenne simple des mois)", """
select year(date) annee, round(avg(regularite_composite), 1) regularite, round(avg(ponctualite_origine), 1) ponctualite_origine, count(*) mois
from tgv_national group by 1 order by 1""")
r.ecrire()
