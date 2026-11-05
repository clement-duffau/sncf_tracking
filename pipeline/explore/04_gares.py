"""Rattachement des gares TGV / Intercités au référentiel « Gares de voyageurs » et à une région.

Usage : python pipeline/explore/04_gares.py
Prérequis : tgv_aqst, intercites, gares_voyageurs (parquet + csv) dans data/raw/

Méthode de correspondance des noms (mesurée ici, à reprendre dans le pipeline) :
  1. normalisation : majuscules, accents retirés, ponctuation → espace, « ST » → « SAINT » ;
  2. égalité exacte des noms normalisés ;
  3. sinon : tous les mots du libellé source sont contenus dans le nom du référentiel
     (ex. « PARIS LYON » ⊂ « PARIS GARE DE LYON ») — on garde le candidat le plus proche
     (Jaro-Winkler), en privilégiant les gares de segment A (grandes gares) ;
  4. le reste est non rattaché (gares étrangères, pseudo-gare « ITALIE »…).
La région est déduite du code INSEE de la commune (2 premiers caractères = département).
"""

from commun import RAW, Rapport, connexion

# Départements → régions (COG INSEE, régions issues de la réforme de 2016)
DEP_REGION = {
    "Auvergne-Rhône-Alpes": "01 03 07 15 26 38 42 43 63 69 73 74",
    "Bourgogne-Franche-Comté": "21 25 39 58 70 71 89 90",
    "Bretagne": "22 29 35 56",
    "Centre-Val de Loire": "18 28 36 37 41 45",
    "Corse": "2A 2B",
    "Grand Est": "08 10 51 52 54 55 57 67 68 88",
    "Hauts-de-France": "02 59 60 62 80",
    "Île-de-France": "75 77 78 91 92 93 94 95",
    "Normandie": "14 27 50 61 76",
    "Nouvelle-Aquitaine": "16 17 19 23 24 33 40 47 64 79 86 87",
    "Occitanie": "09 11 12 30 31 32 34 46 48 65 66 81 82",
    "Pays de la Loire": "44 49 53 72 85",
    "Provence-Alpes-Côte d'Azur": "04 05 06 13 83 84",
}

con = connexion()
r = Rapport("04_gares", "Exploration — rattachement des gares au référentiel et aux régions", con)

con.sql("create or replace table dep_region (dep varchar, region varchar)")
for region, deps in DEP_REGION.items():
    for d in deps.split():
        con.execute("insert into dep_region values (?, ?)", [d, region])

norm = """trim(regexp_replace(regexp_replace(regexp_replace(upper(strip_accents({x})), '[^A-Z0-9]+', ' ', 'g'),
          '(^| )ST( |$)', '\\1SAINT\\2', 'g'), '(^| )STE( |$)', '\\1SAINTE\\2', 'g'))"""

con.sql(f"""
create or replace table ref as
select nom, libellecourt trigramme, segment_drg, codeinsee, codes_uic,
  {norm.format(x='nom')} nom_norm,
  string_split(position_geographique, ',')[1]::double lat, string_split(position_geographique, ',')[2]::double lon,
  case when codeinsee like '97%' then left(codeinsee, 3) else left(codeinsee, 2) end dep
from read_csv('{(RAW / 'gares_voyageurs.csv').as_posix()}', delim = ';', header = true, all_varchar = true)
""")

r.section("Référentiel « Gares de voyageurs » (Gares & Connexions)")
r.table("Volumes", """
select count(*) gares, count(distinct nom) noms_distincts, count(distinct nom_norm) noms_normalises_distincts,
  count(*) filter (where lat is null) sans_coordonnees, count(*) filter (where codeinsee is null) sans_insee,
  count(*) filter (where segment_drg like '%A%') segment_A
from ref""")
r.table("Gares dont le département n'est pas rattaché à une région métropolitaine", """
select dep, count(*) gares, min(nom) exemple from ref left join dep_region using (dep) where region is null group by 1 order by 1""")

# Gares sources (libellés bruts), avec découpage des libellés composites Intercités « A/B »
con.sql("""
create or replace table src as
select distinct 'TGV' source, g morceau from (select gare_depart g from tgv_aqst union select gare_arrivee from tgv_aqst)
union
select distinct 'Intercités', unnest(string_split(g, '/')) from (select depart g from intercites union select arrivee from intercites)
""")
# Forme normalisée sans contenu entre parenthèses ni suffixe « VILLE » (« NICE VILLE » → « NICE »)
con.sql(f"""create or replace table src2 as
select *, regexp_replace({norm.format(x="regexp_replace(morceau, '\\(.*\\)', '')")}, ' VILLE$', '') morceau_norm from src""")

con.sql("""
create or replace table corresp as
with exact as (
  select s.*, r.nom, r.dep, 'exact' methode, 1.0 score from src2 s join ref r on r.nom_norm = s.morceau_norm),
inclus as (
  select s.*, r.nom, r.dep, 'mots inclus' methode, jaro_winkler_similarity(s.morceau_norm, r.nom_norm) score,
    row_number() over (partition by s.source, s.morceau
                       order by (r.segment_drg like '%A%') desc, jaro_winkler_similarity(s.morceau_norm, r.nom_norm) desc) rn
  from src2 s join ref r
    on list_has_all(string_split(r.nom_norm, ' '), string_split(s.morceau_norm, ' '))
  where not exists (select 1 from exact e where e.source = s.source and e.morceau = s.morceau))
select source, morceau, nom, dep, methode, score from exact
union all select source, morceau, nom, dep, methode, score from inclus where rn = 1
union all
select source, morceau, null, null, 'non rattaché', null from src2 s
where not exists (select 1 from exact e where e.source = s.source and e.morceau = s.morceau)
  and not exists (select 1 from inclus i where i.source = s.source and i.morceau = s.morceau)
""")

r.section("Taux de correspondance")
r.table("Par source et méthode (unités = gares, libellés composites découpés)", """
with c as (select source, methode, count(*) gares from corresp group by all)
select source, methode, gares, round(100 * gares / sum(gares) over (partition by source), 1) pct from c order by source, methode""")
r.table("Correspondances obtenues par « mots inclus » (à valider à la main)", """
select source, morceau libelle_source, nom gare_referentiel, round(score, 3) jaro_winkler from corresp where methode = 'mots inclus' order by source, morceau""")
r.table("Gares non rattachées", "select source, morceau from corresp where methode = 'non rattaché' order by source, morceau")
r.table("Villes ayant plusieurs gares de segment A dans le référentiel (ambiguïté possible du libellé source)", """
select split_part(nom_norm, ' ', 1) ville, string_agg(nom, ' ; ' order by nom) gares from ref
where segment_drg like '%A%' and split_part(nom_norm, ' ', 1) in ('PARIS', 'LYON', 'LILLE', 'MONTPELLIER', 'MARSEILLE', 'NICE', 'BORDEAUX', 'TOULOUSE', 'NANTES', 'ROUEN', 'VALENCE', 'AVIGNON', 'AIX', 'BESANCON', 'NIMES', 'LIMOGES')
group by 1 having count(*) > 1 order by 1""")
r.table("Correspondances exactes (contrôle)", """
select source, morceau libelle_source, nom gare_referentiel from corresp where methode = 'exact' order by source, morceau""")

r.section("Résolution des 2 gares françaises non rattachées via « Liste des gares » (SNCF Réseau, codes UIC)")
if (RAW / "liste_gares.parquet").exists():
    r.table("Valence TGV (commune d'Alixan) et Paris-Vaugirard : code UIC puis gare de voyageurs correspondante", f"""
    with lg as (select distinct code_uic, libelle, commune, departemen from liste_gares
                where libelle in ('Valence-TGV', 'Paris-Vaugirard'))
    select lg.libelle libelle_reseau, lg.commune, lg.departemen, lg.code_uic, r.nom gare_voyageurs, r.codes_uic
    from lg left join ref r on r.codes_uic like '%' || lg.code_uic || '%'""")
else:
    r.texte("_liste_gares.parquet absent : section non calculée._")

r.section("Régions des liaisons (12 derniers mois)")
con.sql("create or replace table gare_region as select c.*, d.region from corresp c left join dep_region d using (dep)")
r.table("Régions des gares TGV rattachées", """
select region, count(distinct morceau) gares, string_agg(distinct morceau, ', ') liste from gare_region where source = 'TGV' group by 1 order by 1""")
r.table("Régions des gares Intercités rattachées", """
select region, count(distinct morceau) gares, string_agg(distinct morceau, ', ') liste from gare_region where source = 'Intercités' group by 1 order by 1""")
r.table("Nombre de liaisons TGV (non orientées, 12 derniers mois) touchant chaque région", """
with l as (select distinct least(gare_depart, gare_arrivee) a, greatest(gare_depart, gare_arrivee) b from tgv_aqst
           where date > (select max(date) from tgv_aqst) - interval 12 month),
lr as (select a, b, ga.region ra, gb.region rb from l
       left join (select morceau, region from gare_region where source = 'TGV') ga on ga.morceau = a
       left join (select morceau, region from gare_region where source = 'TGV') gb on gb.morceau = b)
select region, count(*) liaisons from (select a, b, ra region from lr union select a, b, rb from lr) group by 1 order by 2 desc""")

r.ecrire()
