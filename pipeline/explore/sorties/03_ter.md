# Exploration — TER par région (regularite-mensuelle-ter)

_Généré par `pipeline/explore/03_ter.py`._

## Métadonnées du portail

- Titre : Régularité mensuelle TER
- Éditeur : SNCF Voyageurs
- Licence : Open Database License (ODbL)
- Dernière modification des données : 2026-09-10T14:06:29+00:00
- Nombre d'enregistrements : 2380

| champ | type | libellé | description |
|---|---|---|---|
| date | date | Date |  |
| region | text | Région |  |
| nombre_de_trains_programmes | int | Nombre de trains programmés |  |
| nombre_de_trains_ayant_circule | int | Nombre de trains ayant circulé |  |
| nombre_de_trains_annules | int | Nombre de trains annulés |  |
| nombre_de_trains_en_retard_a_l_arrivee | int | Nombre de trains en retard à l'arrivée |  |
| taux_de_regularite | double | Taux de régularité |  |
| nombre_de_trains_a_l_heure_pour_un_train_en_retard_a_l_arrivee | double | Nombre de trains à l'heure pour un train en retard à l'arrivée |  |
| commentaires | text | Commentaires |  |

## Couverture

### Période et volumes

| premier_mois | dernier_mois | nb_mois | nb_mois_attendus | lignes | libelles_region |
|---|---|---|---|---|---|
| 2013-01-01 | 2026-08-01 | 164 | 164 | 2380 | 31 |

### Libellés de région : période couverte

| region | mois | premier | dernier | programmes_par_mois |
|---|---|---|---|---|
| Alsace | 48 | 2013-01-01 | 2016-12-01 | 18286 |
| Aquitaine | 92 | 2013-01-01 | 2020-08-01 | 10598 |
| Auvergne | 60 | 2013-01-01 | 2017-12-01 | 5213 |
| Basse Normandie | 60 | 2013-01-01 | 2017-12-01 | 3207 |
| Bourgogne | 60 | 2013-01-01 | 2017-12-01 | 7376 |
| Bretagne | 164 | 2013-01-01 | 2026-08-01 | 8494 |
| Centre | 92 | 2013-01-01 | 2020-08-01 | 9083 |
| Champagne Ardenne | 48 | 2013-01-01 | 2016-12-01 | 5980 |
| Franche Comté | 60 | 2013-01-01 | 2017-12-01 | 5504 |
| Haute Normandie | 60 | 2013-01-01 | 2017-12-01 | 5716 |
| Languedoc Roussillon | 60 | 2013-01-01 | 2017-12-01 | 4571 |
| Limousin | 60 | 2013-01-01 | 2017-12-01 | 3981 |
| Lorraine | 48 | 2013-01-01 | 2016-12-01 | 13198 |
| Midi Pyrénées | 66 | 2013-01-01 | 2018-06-01 | 8238 |
| Nord Pas de Calais | 60 | 2013-01-01 | 2017-12-01 | 18108 |
| Pays-de-la-Loire | 164 | 2013-01-01 | 2026-08-01 | 11720 |
| Picardie | 60 | 2013-01-01 | 2017-12-01 | 10569 |
| Poitou Charentes | 60 | 2013-01-01 | 2017-12-01 | 3393 |
| Provence Alpes Côte d'Azur | 164 | 2013-01-01 | 2026-08-01 | 13498 |
| Rhône Alpes | 60 | 2013-01-01 | 2017-12-01 | 27531 |
| Grand Est | 116 | 2017-01-01 | 2026-08-01 | 40514 |
| Auvergne-Rhône-Alpes | 104 | 2018-01-01 | 2026-08-01 | 33879 |
| Bourgogne-Franche-Comté | 104 | 2018-01-01 | 2026-08-01 | 13739 |
| Hauts-de-France | 104 | 2018-01-01 | 2026-08-01 | 26187 |
| Normandie | 104 | 2018-01-01 | 2026-08-01 | 9345 |
| Occitanie | 98 | 2018-07-01 | 2026-08-01 | 12212 |
| Centre Val-de-Loire | 72 | 2020-09-01 | 2026-08-01 | 10214 |
| Nouvelle Aquitaine | 72 | 2020-09-01 | 2026-08-01 | 17494 |
| Etoile Amiens | 20 | 2025-01-01 | 2026-08-01 | 4454 |
| Loire Océan | 20 | 2025-01-01 | 2026-08-01 | 2516 |
| Sud Azur | 20 | 2025-01-01 | 2026-08-01 | 5179 |

### Régions-mois en double

| date | region | count_star() |
|---|---|---|

### Nombre de libellés par mois : paliers

| libelles | nb_mois | premier | dernier |
|---|---|---|---|
| 20 | 48 | 2013-01-01 | 2016-12-01 |
| 18 | 12 | 2017-01-01 | 2017-12-01 |
| 11 | 84 | 2018-01-01 | 2024-12-01 |
| 14 | 20 | 2025-01-01 | 2026-08-01 |

## Cohérence des colonnes

### Contrôles

| lignes | circules_incoherents | taux_incoherents | taux_null | avec_commentaire |
|---|---|---|---|---|
| 2380 | 343 | 13 | 37 | 926 |

### Lignes où programmés − annulés ≠ circulés (échantillon récent)

| date | region | programmes | annules | circules | ecart |
|---|---|---|---|---|---|
| 2026-08-01 | Auvergne-Rhône-Alpes | 38215 | 1003 | 37568 | -356 |
| 2026-08-01 | Grand Est | 39764 | 1392 | 38246 | 126 |
| 2026-08-01 | Normandie | 9941 | 123 | 9854 | -36 |
| 2026-08-01 | Sud Azur | 5631 | 390 | 5549 | -308 |
| 2026-08-01 | Hauts-de-France | 23238 | 487 | 22825 | -74 |
| 2026-08-01 | Provence Alpes Côte d'Azur | 10964 | 293 | 10771 | -100 |
| 2026-08-01 | Loire Océan | 2027 | 14 | 2014 | -1 |
| 2026-08-01 | Occitanie | 14475 | 613 | 14068 | -206 |
| 2026-08-01 | Nouvelle Aquitaine | 18611 | 719 | 18080 | -188 |
| 2026-08-01 | Pays-de-la-Loire | 11413 | 252 | 11239 | -78 |
| 2026-08-01 | Etoile Amiens | 4045 | 72 | 3984 | -11 |
| 2026-08-01 | Bourgogne-Franche-Comté | 16094 | 276 | 15807 | 11 |
| 2026-08-01 | Centre Val-de-Loire | 10819 | 381 | 10594 | -156 |
| 2026-07-01 | Bourgogne-Franche-Comté | 16036 | 218 | 15869 | -51 |
| 2026-07-01 | Occitanie | 14511 | 741 | 13992 | -222 |

### Écart programmés − annulés − circulés : à partir de quand ?

| annee | lignes | incoherentes |
|---|---|---|
| 2013 | 240 | 0 |
| 2014 | 240 | 4 |
| 2015 | 240 | 1 |
| 2016 | 240 | 1 |
| 2017 | 216 | 4 |
| 2018 | 132 | 2 |
| 2019 | 132 | 0 |
| 2020 | 132 | 0 |
| 2021 | 132 | 0 |
| 2022 | 132 | 22 |
| 2023 | 132 | 0 |
| 2024 | 132 | 33 |
| 2025 | 168 | 165 |
| 2026 | 112 | 111 |

### Commentaires : nombre par année et mentions de grève / mouvement social

| annee | avec_commentaire | lignes | mentionnant_greve |
|---|---|---|---|
| 2013 | 169 | 240 | 34 |
| 2014 | 143 | 240 | 23 |
| 2015 | 131 | 240 | 2 |
| 2016 | 178 | 240 | 16 |
| 2017 | 177 | 216 | 7 |
| 2018 | 96 | 132 | 20 |
| 2019 | 32 | 132 | 0 |
| 2020 | 0 | 132 | 0 |
| 2021 | 0 | 132 | 0 |
| 2022 | 0 | 132 | 0 |
| 2023 | 0 | 132 | 0 |
| 2024 | 0 | 132 | 0 |
| 2025 | 0 | 168 | 0 |
| 2026 | 0 | 112 | 0 |

### Exemples de commentaires mentionnant une grève (20 premiers)

| date | region | commentaire |
|---|---|---|
| 2013-03-01 | Languedoc Roussillon | Mouvement social et nouvel arrêt de travail spontané suite l'agression d'un agent du service commercial train. |
| 2013-04-01 | Nord Pas de Calais | Grève nationale le 13. |
| 2013-04-01 | Languedoc Roussillon | Intempéries et mouvement social. |
| 2013-05-01 | Languedoc Roussillon | Intempéries et mouvement social. |
| 2013-06-01 | Alsace | Mouvement social et travaux à Vendenheim pour la deuxième phase du TGV Est. |
| 2013-06-01 | Centre | Grève nationale. |
| 2013-06-01 | Champagne Ardenne | Mouvement social national le 13/06/2013. |
| 2013-06-01 | Poitou Charentes | Mouvement social le 13/06. Importants travaux avec des limitations de vitesse, ainsi que de nombreux dérangements d'installation |
| 2013-06-01 | Nord Pas de Calais | Grève le 13. |
| 2013-09-01 | Centre | Grève nationale. |
| 2013-09-01 | Champagne Ardenne | Mouvement social national interprofessionnel le 10/09 ; mouvement social local les 28 et 29/09 |
| 2013-09-01 | Languedoc Roussillon | Malveillance et mouvement social. |
| 2013-09-01 | Basse Normandie | Mouvement social le 10. |
| 2013-09-01 | Bourgogne | Mouvement social interprofessionnel national le 10 et droit de retrait suite à une agression de contrôleur le 21 ayant entraîné d'importantes annulations de trains. |
| 2013-09-01 | Poitou Charentes | Mouvement social le 10/09. Importants travaux avec des limitations de vitesse (raccordement LGV SEA à Villognon). |
| 2013-09-01 | Haute Normandie | Mouvement social. |
| 2013-10-01 | Provence Alpes Côte d'Azur | Mouvement social interprofessionnel. |
| 2013-10-01 | Languedoc Roussillon | Intempéries, malveillance et mouvement social. |
| 2013-10-01 | Centre | Grève, intempéries et travaux. |
| 2013-10-01 | Champagne Ardenne | Mouvement social local le 5 et 6, mouvement social national le 9, collision entre un train et une camionnette à un passage à niveau le 19, agression d'un contrôleur dans un train ayant entraîné une fo |

### Mois où au moins 3 régions mentionnent une grève (candidats pour data/events.yaml)

| date | regions |
|---|---|
| 2013-06-01 | 5 |
| 2013-09-01 | 7 |
| 2013-10-01 | 7 |
| 2013-12-01 | 9 |
| 2014-06-01 | 14 |
| 2014-12-01 | 3 |
| 2016-05-01 | 3 |
| 2016-06-01 | 7 |
| 2018-04-01 | 3 |
| 2018-05-01 | 5 |
| 2018-06-01 | 3 |

## Série nationale TER (somme des régions)

### Régularité et annulations par année

| annee | programmes | pct_annules | regularite |
|---|---|---|---|
| 2013 | 2136139 | 2.4 | 90.9 |
| 2014 | 2096950 | 2.1 | 91.5 |
| 2015 | 2172702 | 1.8 | 91.1 |
| 2016 | 2249086 | 1.9 | 90.6 |
| 2017 | 2390822 | 1.8 | 91 |
| 2018 | 2178346 | 2.1 | 90.6 |
| 2019 | 2245097 | 2.2 | 92.4 |
| 2020 | 1912839 | 2 | 92.6 |
| 2021 | 2321010 | 2.3 | 93 |
| 2022 | 2480185 | 2.5 | 92.1 |
| 2023 | 2418367 | 2.5 | 90.8 |
| 2024 | 2619162 | 2.3 | 91.7 |
| 2025 | 2680004 | 2.4 | 91.3 |
| 2026 | 1774397 | 2.9 | 90.1 |

### Régularité des régions actuelles sur les 12 derniers mois

| region | circules | regularite | pct_annules |
|---|---|---|---|
| Loire Océan | 29650 | 94.6 | 2.3 |
| Bretagne | 116400 | 94.1 | 1.8 |
| Grand Est | 516747 | 93.3 | 3.1 |
| Bourgogne-Franche-Comté | 189511 | 93.1 | 1.2 |
| Etoile Amiens | 52537 | 91.6 | 1.8 |
| Normandie | 114560 | 89.7 | 1.5 |
| Provence Alpes Côte d'Azur | 137010 | 89.6 | 2.4 |
| Auvergne-Rhône-Alpes | 465670 | 89.4 | 2.5 |
| Pays-de-la-Loire | 138144 | 89.3 | 2.4 |
| Hauts-de-France | 300088 | 89 | 2.6 |
| Centre Val-de-Loire | 124609 | 88.8 | 2 |
| Nouvelle Aquitaine | 216214 | 87.9 | 4 |
| Sud Azur | 62713 | 86.4 | 6.7 |
| Occitanie | 162893 | 84.9 | 4.7 |

