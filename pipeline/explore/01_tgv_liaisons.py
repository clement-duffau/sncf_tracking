"""Profilage du jeu « Régularité mensuelle TGV par liaisons » (AQST).

Usage : python pipeline/explore/01_tgv_liaisons.py
Prérequis : data/raw/tgv_aqst.parquet (python pipeline/download.py tgv_aqst)
"""

import json

from commun import RAW, Rapport, connexion

con = connexion()
r = Rapport("01_tgv_liaisons", "Exploration — TGV par liaisons (regularite-mensuelle-tgv-aqst)", con)

# Vue de travail : circulés = prévus - annulés (hypothèse vérifiée plus bas)
con.sql("""
create or replace view t as
select *, nb_train_prevu - nb_annulation as circules,
  prct_cause_externe + prct_cause_infra + prct_cause_gestion_trafic + prct_cause_materiel_roulant
  + prct_cause_gestion_gare + prct_cause_prise_en_charge_voyageurs as somme_causes,
  case when duree_moyenne < 90 then '1. < 1h30 (seuil 5 min)'
       when duree_moyenne <= 180 then '2. 1h30–3h (seuil 10 min)'
       else '3. > 3h (seuil 15 min)' end as tranche_duree
from tgv_aqst
""")

# ---------------------------------------------------------------- métadonnées
meta = json.loads((RAW / "tgv_aqst.meta.json").read_text())
m = meta["metas"]["default"]
r.section("Métadonnées du portail")
r.texte(f"- Titre : {m['title']}\n- Éditeur : {m.get('publisher')}\n- Licence : {m.get('license')}\n"
        f"- Dernière modification des données : {m.get('data_processed')}\n- Nombre d'enregistrements : {m.get('records_count')}")
r.lignes += ["| champ | type | libellé | description |", "|---|---|---|---|"]
for f in meta["fields"]:
    r.lignes.append(f"| {f['name']} | {f['type']} | {f.get('label','')} | {(f.get('description') or '').replace('|','/')} |")
r.lignes.append("")

# ---------------------------------------------------------------- couverture
r.section("Couverture temporelle")
r.table("Période, lignes, liaisons", """
select min(date) premier_mois, max(date) dernier_mois, count(distinct date) nb_mois,
  datediff('month', min(date), max(date)) + 1 nb_mois_attendus, count(*) lignes,
  count(distinct (gare_depart, gare_arrivee)) liaisons_orientees,
  count(distinct (least(gare_depart, gare_arrivee), greatest(gare_depart, gare_arrivee))) liaisons_non_orientees
from t""")
r.table("Mois manquants dans la série", """
select m.d mois_manquant from (select unnest(generate_series((select min(date) from t), (select max(date) from t), interval 1 month))::date d) m
where m.d not in (select distinct date from t)""")
r.table("Nombre de lignes par mois (distribution)", """
select n lignes_par_mois, count(*) nb_mois, min(date) premier, max(date) dernier
from (select date, count(*) n from t group by 1) group by 1 order by 1""")
r.table("Lignes par service", "select service, count(*) lignes, count(distinct (gare_depart, gare_arrivee)) liaisons from t group by 1")

# ---------------------------------------------------------------- liaisons
r.section("Liaisons")
r.table("Liaisons dont la couverture n'est pas complète (apparitions / disparitions / reclassements)", """
with tot as (select count(distinct date) n from t)
select service, gare_depart, gare_arrivee, count(*) nb_mois, min(date) premier, max(date) dernier
from t group by all having count(*) < (select n from tot) order by premier, gare_depart""")
r.table("Liaisons orientées sans liaison retour", """
select service, gare_depart, gare_arrivee from (select distinct service, gare_depart, gare_arrivee from t) a
where not exists (select 1 from t b where b.gare_depart = a.gare_arrivee and b.gare_arrivee = a.gare_depart)""")
r.table("Asymétries de couverture entre aller et retour (toutes services confondus)", """
with c as (select gare_depart a, gare_arrivee b, count(distinct date) n, min(date) d1, max(date) d2 from t group by all)
select x.a, x.b, x.n mois_aller, y.n mois_retour, x.d1, x.d2, y.d1 d1_retour, y.d2 d2_retour
from c x join c y on x.a = y.b and x.b = y.a where x.n <> y.n and x.a < x.b""")
r.table("Gares citées (59) : nombre de lignes et période", """
select gare, count(*) lignes, count(distinct date) mois, min(date) premier, max(date) dernier
from (select gare_depart gare, date from t union all select gare_arrivee, date from t) group by 1 order by 1""")
r.table("Gares « parisiennes » et pseudo-gares", """
select distinct gare from (select gare_depart gare from t union select gare_arrivee from t)
where gare like 'PARIS%' or gare in ('ITALIE', 'MARNE LA VALLEE') order by 1""")
r.table("Liaisons présentes sous les deux services le même mois", """
select a.date, a.gare_depart, a.gare_arrivee, a.nb_train_prevu prevus_national, b.nb_train_prevu prevus_international,
  a.nb_train_retard_arrivee retards_national, b.nb_train_retard_arrivee retards_international
from t a join t b using (date, gare_depart, gare_arrivee)
where a.service = 'National' and b.service = 'International' order by 2, 3, 1""")
r.table("Volume habituel des liaisons Paris–Bellegarde/Mulhouse/Strasbourg autour de l'épisode jul.–sept. 2025", """
select gare_depart, gare_arrivee, date, sum(nb_train_prevu) filter (where service='National') prevus_nat,
  sum(nb_train_prevu) filter (where service='International') prevus_int, sum(nb_train_prevu) prevus_total
from t where gare_depart = 'PARIS LYON' and gare_arrivee in ('BELLEGARDE (AIN)', 'MULHOUSE VILLE')
  and date between '2025-05-01' and '2025-11-01' group by all order by 2, 3""")

# ---------------------------------------------------------------- qualité
r.section("Valeurs manquantes et aberrantes")
cols = [c[0] for c in con.sql("describe tgv_aqst").fetchall()]
r.table("Valeurs nulles par colonne", "select " + ", ".join(f"count(*) - count({c}) as {c}" for c in cols) + " from tgv_aqst")
r.table("Commentaires de retard à l'arrivée : nombre par année (seul champ commentaire renseigné)", """
select year(date) annee, count(commentaires_retard_arrivee) avec_commentaire, count(*) lignes,
  count(*) filter (where regexp_matches(lower(commentaires_retard_arrivee), 'gr[eè]ve|mouvement social')) mentionnant_greve
from t group by 1 order by 1""")
r.table("Exemple de commentaire (tronqué à 300 caractères)", """
select date, gare_depart, gare_arrivee, left(commentaires_retard_arrivee, 300) commentaire
from t where commentaires_retard_arrivee is not null order by date, gare_depart limit 3""")
r.table("Mois avec 0 train prévu", """
select date, count(*) liaisons, sum(nb_annulation) annulations_declarees, sum((circules < 0)::int) circules_negatifs
from t where nb_train_prevu = 0 group by 1 order by 1""")
r.table("Bornes des grandeurs numériques", """
select min(duree_moyenne) duree_min, max(duree_moyenne) duree_max, min(nb_train_prevu) prevus_min, max(nb_train_prevu) prevus_max,
  min(retard_moyen_arrivee) retard_moyen_arr_min, max(retard_moyen_arrivee) retard_moyen_arr_max,
  min(retard_moyen_tous_trains_arrivee) moy_tous_min, max(retard_moyen_tous_trains_arrivee) moy_tous_max,
  min(nb_train_retard_sup_30) sup30_min, count(*) filter (where nb_train_retard_sup_30 < 0) sup30_negatifs,
  count(*) filter (where retard_moyen_tous_trains_arrivee < 0) moy_tous_negatif
from t""")
r.table("Lignes avec un retard moyen « tous trains » fortement négatif (avance ?)", """
select date, gare_depart, gare_arrivee, nb_train_prevu, nb_annulation, retard_moyen_tous_trains_arrivee
from t where retard_moyen_tous_trains_arrivee < -5 order by retard_moyen_tous_trains_arrivee limit 10""")

# ---------------------------------------------------------------- définition « à l'heure »
r.section("Seuils composites : vérification avec les comptes > 15 min")
r.texte("Pour un trajet > 3 h, le seuil « à l'heure » est 15 min : `nb_train_retard_arrivee` devrait alors "
        "égaler `nb_train_retard_sup_15`. Pour les trajets plus courts, il devrait lui être supérieur ou égal.")
r.table("Cohérence retard composite vs > 15 min, par tranche de durée moyenne", """
select tranche_duree, count(*) lignes,
  count(*) filter (where nb_train_retard_arrivee = nb_train_retard_sup_15) egal_sup15,
  count(*) filter (where nb_train_retard_arrivee > nb_train_retard_sup_15) superieur,
  count(*) filter (where nb_train_retard_arrivee < nb_train_retard_sup_15) inferieur,
  count(*) filter (where retard_moyen_arrivee = retard_moyen_trains_retard_sup15) retard_moyen_identique
from t where circules > 0 group by 1 order by 1""")

# ---------------------------------------------------------------- gravité
r.section("Gravité des retards (> 15 / > 30 / > 60 min)")
r.table("Hiérarchie retards ≥ >15 ≥ >30 ≥ >60, par année", """
select year(date) annee, count(*) lignes,
  count(*) filter (where nb_train_retard_sup_15 < nb_train_retard_sup_30) sup15_lt_sup30,
  count(*) filter (where nb_train_retard_sup_30 < nb_train_retard_sup_60) sup30_lt_sup60,
  count(*) filter (where nb_train_retard_sup_30 < 0) sup30_negatif,
  sum(nb_train_retard_arrivee) retards, sum(nb_train_retard_sup_15) sup15, sum(nb_train_retard_sup_30) sup30, sum(nb_train_retard_sup_60) sup60
from t group by 1 order by 1""")
r.table("Mois où la hiérarchie est rompue", """
select date, count(*) lignes, count(*) filter (where nb_train_retard_sup_30 < nb_train_retard_sup_60) sup30_lt_sup60,
  count(*) filter (where nb_train_retard_sup_30 <= 0) sup30_nul_ou_negatif,
  sum(nb_train_retard_sup_15) sup15, sum(nb_train_retard_sup_30) sup30, sum(nb_train_retard_sup_60) sup60
from t group by 1 having count(*) filter (where nb_train_retard_sup_30 < nb_train_retard_sup_60) > 0 order by 1""")
r.table("Exemple : Paris Montparnasse → Bordeaux, nov. 2024 – mai 2025", """
select date, nb_train_retard_arrivee retards, nb_train_retard_sup_15 sup15, nb_train_retard_sup_30 sup30, nb_train_retard_sup_60 sup60
from t where gare_depart = 'PARIS MONTPARNASSE' and gare_arrivee = 'BORDEAUX ST JEAN' and date between '2024-11-01' and '2025-05-01' order by date""")
r.table("Part des trains circulés en retard > 15 / > 30 / > 60 min (hors janv.–mars 2025)", """
select round(100 * sum(nb_train_retard_sup_15) / sum(circules), 2) pct_sup15,
       round(100 * sum(nb_train_retard_sup_30) / sum(circules), 2) pct_sup30,
       round(100 * sum(nb_train_retard_sup_60) / sum(circules), 2) pct_sup60
from t where not (date between '2025-01-01' and '2025-03-01')""")

# ---------------------------------------------------------------- causes
r.section("Causes de retard")
r.texte("Les six colonnes `prct_cause_*` sont des pourcentages **des trains en retard à l'arrivée** "
        "(libellés du portail). Vérification de leur somme :")
r.table("Distribution de la somme des 6 pourcentages (arrondie)", """
select round(somme_causes) somme, count(*) lignes, count(*) filter (where nb_train_retard_arrivee > 0) dont_avec_retards
from t group by 1 order by 2 desc""")
r.table("Lignes avec retards mais causes toutes à 0, par année", """
select year(date) annee, count(*) lignes, sum(nb_train_retard_arrivee) retards_concernes
from t where somme_causes = 0 and nb_train_retard_arrivee > 0 group by 1 order by 1""")
r.table("Lignes avec retards mais causes à 0 : répartition par service (2018)", """
select service, count(*) from t where somme_causes = 0 and nb_train_retard_arrivee > 0 and year(date) = 2018 group by 1""")
r.table("Répartition moyenne des causes, pondérée par le nombre de trains en retard, par année", """
select year(date) annee,
  round(sum(prct_cause_externe * nb_train_retard_arrivee) / sum(nb_train_retard_arrivee), 1) externe,
  round(sum(prct_cause_infra * nb_train_retard_arrivee) / sum(nb_train_retard_arrivee), 1) infra,
  round(sum(prct_cause_gestion_trafic * nb_train_retard_arrivee) / sum(nb_train_retard_arrivee), 1) gestion_trafic,
  round(sum(prct_cause_materiel_roulant * nb_train_retard_arrivee) / sum(nb_train_retard_arrivee), 1) materiel,
  round(sum(prct_cause_gestion_gare * nb_train_retard_arrivee) / sum(nb_train_retard_arrivee), 1) gare,
  round(sum(prct_cause_prise_en_charge_voyageurs * nb_train_retard_arrivee) / sum(nb_train_retard_arrivee), 1) voyageurs
from t where somme_causes > 0 group by 1 order by 1""")
r.table("Répartition mensuelle des causes depuis juin 2025 (rupture visible en mai 2026)", """
select date,
  round(sum(prct_cause_externe * nb_train_retard_arrivee) / sum(nb_train_retard_arrivee), 1) externe,
  round(sum(prct_cause_infra * nb_train_retard_arrivee) / sum(nb_train_retard_arrivee), 1) infra,
  round(sum(prct_cause_gestion_trafic * nb_train_retard_arrivee) / sum(nb_train_retard_arrivee), 1) gestion_trafic,
  round(sum(prct_cause_materiel_roulant * nb_train_retard_arrivee) / sum(nb_train_retard_arrivee), 1) materiel,
  round(sum(prct_cause_gestion_gare * nb_train_retard_arrivee) / sum(nb_train_retard_arrivee), 1) gare,
  round(sum(prct_cause_prise_en_charge_voyageurs * nb_train_retard_arrivee) / sum(nb_train_retard_arrivee), 1) voyageurs
from t where somme_causes > 0 and date >= '2025-06-01' group by 1 order by 1""")
r.table("Granularité des pourcentages de causes (nb de valeurs distinctes, part des valeurs entières)", """
select count(distinct prct_cause_externe) distinctes, round(100 * avg((prct_cause_externe = round(prct_cause_externe))::int), 1) pct_entieres from t""")

# ---------------------------------------------------------------- annulations
r.section("Prévus, annulés, circulés")
r.texte("Il n'y a pas de colonne « circulés » : on la calcule comme `prévus − annulés`. "
        "Les 73 lignes à 0 prévu avec annulations > 0 (avril–mai 2020) montrent que la convention n'est "
        "pas parfaitement tenue au plus fort du confinement.")
r.table("Totaux mensuels, service National (régularité recalculée sur circulés)", """
select date, sum(nb_train_prevu) prevus, sum(nb_annulation) annules, round(100 * sum(nb_annulation) / sum(nb_train_prevu), 1) pct_annules,
  sum(nb_train_retard_arrivee) retards,
  round(100 * (1 - sum(nb_train_retard_arrivee) / sum(greatest(circules, 0))), 1) regularite_recalculee
from t where service = 'National' group by 1 order by 1""", max_lignes=300)

# ---------------------------------------------------------------- comparaison au global
r.section("Comparaison avec la régularité TGV globale officielle")
r.texte("La régularité « globale » publiée n'est pas la moyenne des liaisons (un train compte dans plusieurs "
        "liaisons, et le global inclut des trains absents du jeu par liaisons). On mesure l'écart.")
r.table("Écart régularité agrégée des liaisons (tous services) vs régularité globale publiée, par année", """
with l as (select date, 100 * (1 - sum(nb_train_retard_arrivee) / sum(greatest(circules, 0))) reg_liaisons from t group by 1)
select year(date) annee, round(avg(reg_liaisons), 1) reg_liaisons_moy, round(avg(regularite_composite), 1) reg_globale_moy,
  round(avg(reg_liaisons - regularite_composite), 2) ecart_moyen, round(corr(reg_liaisons, regularite_composite), 3) correlation
from l join tgv_national using (date) group by 1 order by 1""")

# ---------------------------------------------------------------- volumes
r.section("Volumes par liaison-mois (utile pour le poids bayésien)")
r.table("Quantiles du nombre de trains circulés par liaison-mois (circulés > 0)", """
select quantile_cont(circules, [0.05, 0.1, 0.25, 0.5, 0.75, 0.9]) quantiles, min(circules), max(circules), avg(circules)
from t where circules > 0""")
r.table("Liaisons les moins fréquentées (moyenne de trains circulés par mois, 12 derniers mois)", """
select gare_depart, gare_arrivee, round(avg(c)) circules_par_mois from
 (select gare_depart, gare_arrivee, date, sum(circules) c from t where date > (select max(date) from t) - interval 12 month group by all)
group by all order by 3 limit 10""")

r.ecrire()
