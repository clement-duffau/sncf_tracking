"""Phase 2 — calibrage du score de fiabilité et comparaison de variantes sur les vraies données.

Usage : python pipeline/explore/06_score_variantes.py
Prérequis : tgv_aqst, intercites dans data/raw/

Méthode (détaillée dans docs/PLAN.md) :
- unité = liaison non orientée (A–B et B–A fusionnés, services National/International sommés) ;
- composantes : R = part des trains circulés à l'heure, A = part des trains prévus annulés,
  G30 / G60 = part des trains circulés en retard > 30 / > 60 min (TGV uniquement) ;
- rétrécissement bayésien (bêta-binomial) de chaque taux vers la moyenne du type de train :
      taux_lissé = (x + M·μ) / (n + M)
  avec M (en trains) = m · D, où D = surdispersion (les retards d'un même mois sont corrélés)
  et m = force du prior estimée par Bayes empirique (méthode des moments).
"""

from commun import Rapport, connexion

con = connexion()
r = Rapport("06_score_variantes", "Phase 2 — calibrage et variantes du score de fiabilité", con)

# ------------------------------------------------------------------ données au grain liaison × mois
con.sql("""
create or replace table lm as
-- TGV : fusion des sens et des services
select 'TGV' type, date, least(gare_depart, gare_arrivee) a, greatest(gare_depart, gare_arrivee) b,
  sum(nb_train_prevu)::double prevus, sum(nb_annulation)::double annules,
  sum(greatest(nb_train_prevu - nb_annulation, 0))::double circules, sum(nb_train_retard_arrivee)::double retards,
  sum(nb_train_retard_sup_30)::double s30, sum(nb_train_retard_sup_60)::double s60
from tgv_aqst
where nb_train_prevu > 0
group by all
union all
-- Intercités : libellés composites normalisés (ALBI/RODEZ = RODEZ/ALBI), sens fusionnés, doublons sommés
select 'Intercités', date,
  least(list_aggregate(list_sort(string_split(depart, '/')), 'string_agg', '/'), list_aggregate(list_sort(string_split(arrivee, '/')), 'string_agg', '/')),
  greatest(list_aggregate(list_sort(string_split(depart, '/')), 'string_agg', '/'), list_aggregate(list_sort(string_split(arrivee, '/')), 'string_agg', '/')),
  sum(nombre_de_trains_programmes), sum(nombre_de_trains_annules), sum(nombre_de_trains_ayant_circule),
  sum(nombre_de_trains_en_retard_a_l_arrivee), null, null
from intercites
where nombre_de_trains_programmes > 0
group by all
""")
con.sql("""
create or replace table fenetre as
select type, max(date) fin, max(date) - interval 11 month debut from lm group by 1
""")
r.section("Fenêtre d'évaluation : 12 derniers mois disponibles par type")
r.table("Fenêtres", "select type, debut::date debut, fin::date fin from fenetre order by 1")

# ------------------------------------------------------------------ surdispersion D
r.section("1. Surdispersion : les trains d'une même liaison ne sont pas indépendants")
r.texte("Pour chaque liaison, on compare la variance observée du taux mensuel à la variance qu'aurait un tirage "
        "binomial (trains indépendants) : D = variance observée / variance binomiale. Calcul sur les 24 derniers "
        "mois, liaisons-mois d'au moins 20 trains circulés.")
con.sql("""
create or replace table surdisp as
with base as (
  select l.*, f.fin from lm l join fenetre f using (type) where l.date > f.fin - interval 24 month and circules >= 20),
taux as (
  select type, a, b, 'retard' metrique, retards / circules p, circules n from base
  union all select type, a, b, 'annulation', annules / prevus, prevus from base
  union all select type, a, b, 'retard > 30 min', s30 / circules, circules from base where type = 'TGV'),
par_liaison as (
  select type, metrique, a, b, var_samp(p) v_obs, avg(p) pbar, avg(1 / n) inv_n, count(*) k from taux group by all having k >= 12)
select type, metrique, count(*) liaisons,
  median(v_obs / nullif(pbar * (1 - pbar) * inv_n, 0)) D_mediane,
  quantile_cont(v_obs / nullif(pbar * (1 - pbar) * inv_n, 0), 0.25) D_q25,
  quantile_cont(v_obs / nullif(pbar * (1 - pbar) * inv_n, 0), 0.75) D_q75
from par_liaison group by all
""")
r.table("Facteur de surdispersion D par type et métrique", "select * from surdisp order by type, metrique")

# ------------------------------------------------------------------ Bayes empirique
r.section("2. Force du prior par Bayes empirique (méthode des moments)")
r.texte("Sur la fenêtre de 12 mois : variance inter-liaisons observée des taux = variance « vraie » τ² + bruit "
        "d'échantillonnage (μ(1−μ)·D/n). Pour une loi bêta de moyenne μ et de variance τ², la concentration vaut "
        "m = μ(1−μ)/τ² − 1 (en trains « effectifs »). En trains réels : M = m·D.")
con.sql("""
create or replace table periode as
select l.type, a, b, sum(prevus) prevus, sum(annules) annules, sum(circules) circules, sum(retards) retards,
  sum(s30) s30, sum(s60) s60, count(*) mois
from lm l join fenetre f using (type) where l.date between f.debut and f.fin group by all
""")
con.sql("""
create or replace table prior as
with t as (
  select type, 'retard' metrique, retards x, circules n from periode
  union all select type, 'annulation', annules, prevus from periode
  union all select type, 'retard > 30 min', s30, circules from periode where type = 'TGV'
  union all select type, 'retard > 60 min', s60, circules from periode where type = 'TGV'),
mu as (select type, metrique, sum(x) / sum(n) mu, count(*) k, var_samp(x / n) v_obs, avg(1 / n) inv_n from t group by all),
-- Pour > 60 min, on réutilise le D mesuré sur > 30 min
d as (select mu.*, coalesce(s.D_mediane, s30.D_mediane) D from mu
      left join surdisp s using (type, metrique)
      left join (select type, D_mediane from surdisp where metrique = 'retard > 30 min') s30 using (type))
select d.*, v_obs - mu * (1 - mu) * D * inv_n tau2,
  mu * (1 - mu) / (v_obs - mu * (1 - mu) * D * inv_n) - 1 m_eff,
  (mu * (1 - mu) / (v_obs - mu * (1 - mu) * D * inv_n) - 1) * D M_trains
from d
""")
r.table("Prior par type et métrique", """
select type, metrique, round(100 * mu, 2) mu_pct, k liaisons, round(D, 1) D, round(sqrt(tau2) * 100, 2) tau_pct, round(m_eff) m_eff, round(M_trains) M_trains
from prior order by type, metrique""")
r.table("Ordre de grandeur : trains circulés par liaison et par mois (médiane, fenêtre de 12 mois)", """
select type, median(circules / mois) mediane_circules_par_mois, min(circules / mois) min_par_mois, max(circules / mois) max_par_mois
from periode group by 1""")

# Valeur retenue pour la suite : M = M_trains de la métrique « retard » arrondi, par type
con.sql("""
create or replace table M as
select type, round(M_trains, -1) M from prior where metrique = 'retard'
""")
r.table("M retenu (arrondi à la dizaine) — appliqué à toutes les composantes d'un type", "select * from M order by 1")

# ------------------------------------------------------------------ composantes lissées
con.sql("""
create or replace table compo as
with mu as (select type, metrique, mu from prior)
select p.*, M.M,
  retards / circules R_brut_retard, annules / prevus A_brut, s30 / circules G30_brut, s60 / circules G60_brut,
  (retards + M.M * (select mu from mu where mu.type = p.type and metrique = 'retard')) / (circules + M.M) ret_l,
  (annules + M.M * (select mu from mu where mu.type = p.type and metrique = 'annulation')) / (prevus + M.M) ann_l,
  (s30 + M.M * (select mu from mu where mu.type = p.type and metrique = 'retard > 30 min')) / (circules + M.M) g30_l,
  (s60 + M.M * (select mu from mu where mu.type = p.type and metrique = 'retard > 60 min')) / (circules + M.M) g60_l
from periode p join M using (type)
""")

# ------------------------------------------------------------------ variantes
con.sql("""
create or replace table scores as
select type, a || ' – ' || b liaison, circules, mois,
  round(100 * (1 - retards / circules), 1) regularite_brute, round(100 * annules / prevus, 2) annul_brut,
  round(100 * s30 / circules, 1) g30_brut,
  -- V1 : probabilité qu'un train prévu arrive à l'heure (annulé = échec)
  100 * (1 - ann_l) * (1 - ret_l) V1,
  -- V2 : pénalité graduée par train prévu, normalisée sur 0–100
  --   à l'heure 0 ; retard ≤ 30 min 1 ; 30–60 min 2 ; > 60 min 3 ; annulé 3
  100 * (1 - ((1 - ann_l) * ((ret_l - g30_l) * 1 + (g30_l - g60_l) * 2 + g60_l * 3) + ann_l * 3) / 3) V2,
  -- V3 : moyenne pondérée de rangs-centiles (50 % régularité, 25 % annulations, 25 % gravité > 30 min)
  100 * (0.5 * percent_rank() over (partition by type order by ret_l desc)
       + 0.25 * percent_rank() over (partition by type order by ann_l desc)
       + 0.25 * percent_rank() over (partition by type order by g30_l desc)) V3,
  -- Sans lissage (pour mesurer l'effet du prior)
  100 * (1 - annules / prevus) * (1 - retards / circules) V1_sans_lissage
from compo
""")

for type_ in ["TGV", "Intercités"]:
    r.section(f"3. Classements {type_} sur 12 mois — variantes calculables")
    variantes = ["V1", "V2", "V3"] if type_ == "TGV" else ["V1"]
    for v in variantes:
        cols = "liaison, round(circules) circules, regularite_brute, annul_brut, g30_brut, round(V1, 1) V1, round(V2, 1) V2, round(V3, 1) V3"
        if type_ == "Intercités":
            cols = "liaison, round(circules) circules, regularite_brute, annul_brut, round(V1, 1) V1, round(V1_sans_lissage, 1) V1_sans_lissage"
        lim = 10 if type_ == "TGV" else 100
        r.table(f"{type_} — {v} : haut du classement", f"select row_number() over (order by {v} desc) rang, {cols} from scores where type = '{type_}' order by {v} desc limit {lim}")
        if type_ == "TGV":
            r.table(f"{type_} — {v} : bas du classement", f"select rang, * exclude (rang) from (select row_number() over (order by {v} desc) rang, {cols} from scores where type = '{type_}') order by rang desc limit 10")

r.section("4. Concordance des variantes (TGV, corrélation de rang de Spearman)")
r.table("Corrélations entre variantes", """
with rk as (select rank() over (order by V1) r1, rank() over (order by V2) r2, rank() over (order by V3) r3,
  rank() over (order by regularite_brute) r0 from scores where type = 'TGV')
select round(corr(r1, r2), 3) V1_V2, round(corr(r1, r3), 3) V1_V3, round(corr(r2, r3), 3) V2_V3, round(corr(r0, r1), 3) regularite_brute_V1 from rk""")
r.table("Plus grands écarts de rang entre V1 et V2 (TGV)", """
with rk as (select liaison, rank() over (order by V1 desc) rang_V1, rank() over (order by V2 desc) rang_V2, rank() over (order by V3 desc) rang_V3,
  regularite_brute, annul_brut, g30_brut from scores where type = 'TGV')
select * from rk order by abs(rang_V1 - rang_V2) desc limit 8""")

# ------------------------------------------------------------------ effet du lissage sur un mois isolé
r.section("5. Effet du lissage sur un mois isolé (petites liaisons)")
r.texte("Sur un seul mois, une petite liaison (≈ 20–60 trains) peut afficher une régularité extrême par hasard. "
        "On compare le classement brut et lissé (V1) du dernier mois TGV.")
con.sql("""
create or replace table mois_isole as
with f as (select fin from fenetre where type = 'TGV'), mu as (select mu from prior where type = 'TGV' and metrique = 'retard'),
mua as (select mu from prior where type = 'TGV' and metrique = 'annulation'), M_ as (select M from M where type = 'TGV')
select a || ' – ' || b liaison, circules, round(100 * (1 - retards / circules), 1) regularite_brute,
  100 * (1 - annules / prevus) * (1 - retards / circules) V1_brut,
  100 * (1 - (annules + (select M from M_) * (select mu from mua)) / (prevus + (select M from M_)))
      * (1 - (retards + (select M from M_) * (select mu from mu)) / (circules + (select M from M_))) V1_lisse
from lm where type = 'TGV' and date = (select fin from f)
""")
r.table("Dernier mois TGV — top 8 brut", "select row_number() over (order by V1_brut desc) rang_brut, liaison, round(circules) circules, regularite_brute, round(V1_brut, 1) V1_brut, round(V1_lisse, 1) V1_lisse from mois_isole order by V1_brut desc limit 8")
r.table("Dernier mois TGV — top 8 lissé", "select row_number() over (order by V1_lisse desc) rang_lisse, liaison, round(circules) circules, regularite_brute, round(V1_brut, 1) V1_brut, round(V1_lisse, 1) V1_lisse from mois_isole order by V1_lisse desc limit 8")
r.table("Dernier mois TGV — 8 derniers lissé", "select liaison, round(circules) circules, regularite_brute, round(V1_brut, 1) V1_brut, round(V1_lisse, 1) V1_lisse from mois_isole order by V1_lisse limit 8")

# ------------------------------------------------------------------ sensibilité à M
r.section("6. Sensibilité au choix de M (TGV, V2, 12 mois)")
for facteur in [0, 1, 3, 10]:
    con.sql(f"""
    create or replace table sens_{facteur} as
    with mu as (select metrique, mu from prior where type = 'TGV'), M_ as (select M * {facteur} M from M where type = 'TGV'),
    c as (select a || ' – ' || b liaison,
      (retards + (select M from M_) * (select mu from mu where metrique = 'retard')) / (circules + (select M from M_)) ret_l,
      (annules + (select M from M_) * (select mu from mu where metrique = 'annulation')) / (prevus + (select M from M_)) ann_l,
      (s30 + (select M from M_) * (select mu from mu where metrique = 'retard > 30 min')) / (circules + (select M from M_)) g30_l,
      (s60 + (select M from M_) * (select mu from mu where metrique = 'retard > 60 min')) / (circules + (select M from M_)) g60_l
      from periode where type = 'TGV')
    select liaison, 100 * (1 - ((1 - ann_l) * ((ret_l - g30_l) + (g30_l - g60_l) * 2 + g60_l * 3) + ann_l * 3) / 3) V2 from c""")
r.table("Rang des 3 liaisons les moins fréquentées et du 1er / dernier selon M (×0, ×1, ×3, ×10)", """
with rk as (
  select liaison, rank() over (order by s0.V2 desc) r0, rank() over (order by s1.V2 desc) r1,
    rank() over (order by s3.V2 desc) r3, rank() over (order by s10.V2 desc) r10
  from sens_0 s0 join sens_1 s1 using (liaison) join sens_3 s3 using (liaison) join sens_10 s10 using (liaison))
select rk.*, round(p.circules) circules from rk join (select a || ' – ' || b liaison, circules from periode where type = 'TGV') p using (liaison)
where liaison in (select a || ' – ' || b from periode where type = 'TGV' order by circules limit 3) or r1 in (1, (select max(r1) from rk))
order by r1""")

r.ecrire()
