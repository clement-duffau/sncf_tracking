"""Événements visibles dans les données : COVID, grèves, transfert Normandie, saisonnalité.

Usage : python pipeline/explore/05_evenements.py
Prérequis : tgv_aqst, tgv_national, intercites, ter dans data/raw/
"""

from commun import Rapport, connexion

con = connexion()
r = Rapport("05_evenements", "Exploration — événements visibles (COVID, grèves, Normandie, saisons)", con)

# Séries mensuelles nationales comparables
con.sql("""
create or replace view mens as
with tgv as (
  select date, sum(nb_train_prevu) prevus, sum(nb_annulation) annules,
    1 - sum(nb_train_retard_arrivee) / sum(greatest(nb_train_prevu - nb_annulation, 0)) reg
  from tgv_aqst group by 1),
ic as (
  select date, sum(nombre_de_trains_programmes) prevus, sum(nombre_de_trains_annules) annules,
    1 - sum(nombre_de_trains_en_retard_a_l_arrivee) / nullif(sum(nombre_de_trains_ayant_circule), 0) reg
  from intercites group by 1),
ter_ as (
  select date, sum(nombre_de_trains_programmes) prevus, sum(nombre_de_trains_annules) annules,
    1 - sum(nombre_de_trains_en_retard_a_l_arrivee) / nullif(sum(nombre_de_trains_ayant_circule), 0) reg
  from ter group by 1)
select coalesce(tgv.date, ic.date, ter_.date) date,
  tgv.prevus tgv_prevus, round(100 * tgv.annules / tgv.prevus, 1) tgv_pct_annul, round(100 * tgv.reg, 1) tgv_reg,
  ic.prevus ic_prevus, round(100 * ic.annules / ic.prevus, 1) ic_pct_annul, round(100 * ic.reg, 1) ic_reg,
  ter_.prevus ter_prevus, round(100 * ter_.annules / ter_.prevus, 1) ter_pct_annul, round(100 * ter_.reg, 1) ter_reg
from tgv full join ic using (date) full join ter_ using (date)
""")

r.section("Périodes candidates")
r.texte("Pour chaque période, on compare le mois aux mêmes mois de l'année précédente quand c'est utile. "
        "« prévus » = trains prévus (TGV) ou programmés (Intercités, TER). Pour Intercités et TER, les trains "
        "supprimés avant 16 h la veille ne sont pas comptés : une grève annoncée fait **baisser les programmés** "
        "au lieu d'augmenter les annulations.")
r.table("Grève du printemps 2018 (avril–juin 2018) et voisinage", """
select * from mens where date between '2018-02-01' and '2018-08-01' order by date""")
r.table("Grève contre la réforme des retraites (déc. 2019 – janv. 2020) et voisinage", """
select * from mens where date between '2019-10-01' and '2020-02-01' order by date""")
r.table("COVID-19 (mars 2020 – mai 2021)", """
select * from mens where date between '2020-02-01' and '2021-06-01' order by date""")
r.table("Grèves de fin 2022 et réforme des retraites 2023", """
select * from mens where date between '2022-10-01' and '2023-06-01' order by date""")
r.table("Mois où le TGV annule plus de 5 % des trains prévus", """
select date, tgv_prevus, tgv_pct_annul, tgv_reg, ic_prevus, ic_pct_annul, ter_pct_annul from mens where tgv_pct_annul > 5 order by date""")
r.table("Mois où les trains Intercités programmés chutent de plus de 20 % par rapport au même mois N−1 (à périmètre de liaisons non constant)", """
select a.date, a.ic_prevus, b.ic_prevus ic_prevus_n_moins_1, round(100 * (a.ic_prevus / b.ic_prevus - 1), 1) variation_pct
from mens a join mens b on b.date = a.date - interval 12 month
where a.ic_prevus < 0.8 * b.ic_prevus order by a.date""")
r.table("Même chose pour les TER (sommes nationales)", """
select a.date, a.ter_prevus, b.ter_prevus n_moins_1, round(100 * (a.ter_prevus / b.ter_prevus - 1), 1) variation_pct
from mens a join mens b on b.date = a.date - interval 12 month
where a.ter_prevus < 0.9 * b.ter_prevus order by a.date""")

r.section("Transfert des Intercités Normandie vers TER (1er janvier 2020)")
r.table("Liaisons Intercités normandes : dernier mois publié", """
select depart, arrivee, max(date) dernier_mois from intercites
where depart in ('PARIS-ST-LAZARE','PARIS-VAUGIRARD') or arrivee in ('PARIS-ST-LAZARE','PARIS-VAUGIRARD') or depart = 'CAEN' or arrivee = 'CAEN'
group by all order by 1, 2""")
r.table("TER Normandie : trains programmés par mois autour du transfert", """
select date, nombre_de_trains_programmes programmes, taux_de_regularite from ter where region = 'Normandie'
and date between '2019-09-01' and '2020-03-01' order by date""")

r.section("Saisonnalité (hors 2020 et avril 2018 / déc. 2019 – janv. 2020)")
r.table("Régularité moyenne par mois calendaire", """
select month(date) mois, round(avg(tgv_reg), 1) tgv, round(avg(ic_reg), 1) intercites, round(avg(ter_reg), 1) ter,
  round(avg(tgv_pct_annul), 2) tgv_pct_annul
from mens where year(date) <> 2020 and date not in ('2018-04-01', '2018-05-01', '2018-06-01', '2019-12-01', '2020-01-01')
group by 1 order by 1""")
r.table("Écart-type inter-annuel de la régularité TGV par mois calendaire (2018–2026, hors 2020)", """
select month(date) mois, round(stddev(tgv_reg), 1) ecart_type, round(min(tgv_reg), 1) min, round(max(tgv_reg), 1) max, count(*) annees
from mens where tgv_reg is not null and year(date) <> 2020 group by 1 order by 1""")

r.section("Séries complètes")
r.table("Séries mensuelles comparées (toutes années)", "select * from mens order by date", max_lignes=400)

r.ecrire()
