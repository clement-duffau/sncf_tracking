# Exploration — Intercités (regularite-mensuelle-intercites)

_Généré par `pipeline/explore/02_intercites.py`._

## Métadonnées du portail

- Titre : Régularité mensuelle Intercités
- Éditeur : SNCF Voyageurs
- Licence : Open Database License (ODbL)
- Dernière modification des données : 2026-07-27T14:46:56+00:00
- Nombre d'enregistrements : 5949

| champ | type | libellé | description |
|---|---|---|---|
| date | date | Date |  |
| depart | text | Départ |  |
| arrivee | text | Arrivée |  |
| nombre_de_trains_programmes | int | Nombre de trains programmés |  |
| nombre_de_trains_ayant_circule | int | Nombre de trains ayant circulé |  |
| nombre_de_trains_annules | int | Nombre de trains annulés |  |
| nombre_de_trains_en_retard_a_l_arrivee | int | Nombre de trains en retard à l'arrivée |  |
| taux_de_regularite | double | Taux de régularité |  |
| nombre_de_trains_a_l_heure_pour_un_train_en_retard_a_l_arrivee | double | Nombre de trains à l'heure pour un train en retard à l'arrivée |  |

## Couverture temporelle

### Période, lignes, liaisons

| premier_mois | dernier_mois | nb_mois | nb_mois_attendus | lignes | libelles_liaisons_orientees |
|---|---|---|---|---|---|
| 2014-01-01 | 2026-05-01 | 149 | 149 | 5949 | 97 |

### Nombre de lignes par mois : paliers

| lignes_par_mois | nb_mois | premier | dernier |
|---|---|---|---|
| 50 | 30 | 2014-01-01 | 2016-06-01 |
| 65 | 17 | 2016-07-01 | 2017-12-01 |
| 63 | 1 | 2017-04-01 | 2017-04-01 |
| 46 | 12 | 2018-01-01 | 2018-12-01 |
| 38 | 12 | 2019-01-01 | 2019-12-01 |
| 23 | 1 | 2020-01-01 | 2020-01-01 |
| 24 | 7 | 2020-02-01 | 2020-12-01 |
| 4 | 1 | 2020-04-01 | 2020-04-01 |
| 16 | 2 | 2020-05-01 | 2020-06-01 |
| 22 | 1 | 2020-07-01 | 2020-07-01 |
| 28 | 12 | 2021-01-01 | 2021-12-01 |
| 30 | 23 | 2022-01-01 | 2023-11-01 |
| 34 | 19 | 2023-12-01 | 2026-05-01 |
| 32 | 11 | 2024-01-01 | 2024-11-01 |

## Liaisons et libellés

### Liste des libellés de liaisons (orientés)

| depart | arrivee | lignes | mois | premier | dernier | programmes_par_mois | retour_avec_meme_libelle |
|---|---|---|---|---|---|---|---|
| ALBI/RODEZ | PARIS-AUSTERLITZ | 97 | 97 | 2018-01-01 | 2026-05-01 | 20 | False |
| AMIENS | PARIS-NORD | 60 | 60 | 2014-01-01 | 2018-12-01 | 187 | True |
| AURILLAC | PARIS-AUSTERLITZ | 30 | 30 | 2023-12-01 | 2026-05-01 | 18 | True |
| BAYONNE | TOULOUSE-MATABIAU | 29 | 29 | 2018-01-01 | 2020-12-01 | 76 | True |
| BELFORT | PARIS-EST | 48 | 48 | 2014-01-01 | 2017-12-01 | 116 | True |
| BORDEAUX-ST-JEAN | LIMOGES | 48 | 48 | 2014-01-01 | 2017-12-01 | 27 | True |
| BORDEAUX-ST-JEAN | MARSEILLE-ST-CHARLES | 100 | 100 | 2018-01-01 | 2026-05-01 | 194 | True |
| BORDEAUX-ST-JEAN | NANTES | 149 | 149 | 2014-01-01 | 2026-05-01 | 91 | True |
| BORDEAUX-ST-JEAN | NICE-VILLE | 48 | 48 | 2014-01-01 | 2017-12-01 | 189 | True |
| BOULOGNE-VILLE | PARIS-NORD | 60 | 60 | 2014-01-01 | 2018-12-01 | 129 | True |
| BOURG-ST-MAURICE/ST-GERVAIS | PARIS-AUSTERLITZ | 17 | 17 | 2016-07-01 | 2017-12-01 | 5 | True |
| BOURGES | PARIS-AUSTERLITZ | 48 | 48 | 2014-01-01 | 2017-12-01 | 116 | True |
| BRIANÇON | PARIS-AUSTERLITZ | 98 | 98 | 2018-01-01 | 2026-05-01 | 20 | True |
| BRIANÇON/NICE-VILLE | PARIS-AUSTERLITZ | 18 | 18 | 2016-07-01 | 2017-12-01 | 49 | False |
| BRIVE/CAHORS | PARIS-AUSTERLITZ | 18 | 18 | 2016-07-01 | 2017-12-01 | 163 | True |
| BÉZIERS | CLERMONT-FERRAND | 148 | 148 | 2014-01-01 | 2026-05-01 | 39 | True |
| CAEN | PARIS-ST-LAZARE | 72 | 72 | 2014-01-01 | 2019-12-01 | 187 | True |
| CAEN | TOURS | 72 | 72 | 2014-01-01 | 2019-12-01 | 65 | True |
| CAHORS/BRIVE | PARIS-AUSTERLITZ | 100 | 100 | 2018-01-01 | 2026-05-01 | 173 | False |
| CAMBRAI/MAUBEUGE | PARIS-NORD | 12 | 12 | 2018-01-01 | 2018-12-01 | 154 | False |
| CERBERE | PARIS-AUSTERLITZ | 99 | 99 | 2014-01-01 | 2026-05-01 | 57 | True |
| CERBERE/TOULOUSE | PARIS-AUSTERLITZ | 45 | 45 | 2018-01-01 | 2021-12-01 | 24 | False |
| CHERBOURG | PARIS-ST-LAZARE | 72 | 72 | 2014-01-01 | 2019-12-01 | 194 | True |
| CLERMONT-FERRAND | BÉZIERS | 148 | 148 | 2014-01-01 | 2026-05-01 | 41 | True |
| CLERMONT-FERRAND | NÎMES | 48 | 48 | 2014-01-01 | 2017-12-01 | 31 | True |
| CLERMONT-FERRAND | PARIS-BERCY | 149 | 149 | 2014-01-01 | 2026-05-01 | 207 | True |
| GRANVILLE | PARIS-VAUGIRARD | 72 | 72 | 2014-01-01 | 2019-12-01 | 155 | True |
| HENDAYE | PARIS-AUSTERLITZ | 18 | 18 | 2016-07-01 | 2017-12-01 | 9 | True |
| HENDAYE | TOULOUSE-MATABIAU | 119 | 119 | 2014-01-01 | 2026-05-01 | 95 | True |
| HENDAYE/LOURDES | PARIS-AUSTERLITZ | 24 | 24 | 2022-01-01 | 2023-12-01 | 18 | False |
| LATOUR-DE-CAROL | PARIS-AUSTERLITZ | 99 | 99 | 2017-02-01 | 2026-05-01 | 21 | True |
| LE HAVRE | PARIS-ST-LAZARE | 72 | 72 | 2014-01-01 | 2019-12-01 | 327 | True |
| LIMOGES | BORDEAUX-ST-JEAN | 48 | 48 | 2014-01-01 | 2017-12-01 | 29 | True |
| LIMOGES | PARIS-AUSTERLITZ | 18 | 18 | 2016-07-01 | 2017-12-01 | 36 | True |
| LYON | NANCY | 18 | 18 | 2024-12-01 | 2026-05-01 | 29 | True |
| LYON | NANTES | 100 | 100 | 2018-01-01 | 2026-05-01 | 66 | True |
| LYON-PART-DIEU | NANTES | 48 | 48 | 2014-01-01 | 2017-12-01 | 80 | True |
| MARSEILLE-ST-CHARLES | BORDEAUX-ST-JEAN | 118 | 118 | 2016-07-01 | 2026-05-01 | 191 | True |
| MAUBEUGE | PARIS-NORD | 48 | 48 | 2014-01-01 | 2017-12-01 | 265 | True |
| MODANE | PARIS-AUSTERLITZ | 12 | 12 | 2021-01-01 | 2021-12-01 | 18 | True |
| NANCY | LYON | 18 | 18 | 2024-12-01 | 2026-05-01 | 29 | True |
| NANTES | BORDEAUX-ST-JEAN | 149 | 149 | 2014-01-01 | 2026-05-01 | 92 | True |
| NANTES | LYON | 100 | 100 | 2018-01-01 | 2026-05-01 | 66 | True |
| NANTES | LYON-PART-DIEU | 48 | 48 | 2014-01-01 | 2017-12-01 | 40 | True |
| NEVERS | PARIS-BERCY | 48 | 48 | 2014-01-01 | 2017-12-01 | 143 | True |
| NICE-VILLE | BORDEAUX-ST-JEAN | 30 | 30 | 2014-01-01 | 2016-06-01 | 174 | True |
| NICE-VILLE | PARIS-AUSTERLITZ | 65 | 65 | 2021-01-01 | 2026-05-01 | 24 | True |
| NÎMES | CLERMONT-FERRAND | 48 | 48 | 2014-01-01 | 2017-12-01 | 33 | True |
| ORLÉANS | PARIS-AUSTERLITZ | 48 | 48 | 2014-01-01 | 2017-12-01 | 330 | True |
| PARIS-AUSTERLITZ | AURILLAC | 30 | 30 | 2023-12-01 | 2026-05-01 | 19 | True |
| PARIS-AUSTERLITZ | BOURG-ST-MAURICE/ST-GERVAIS | 17 | 17 | 2016-07-01 | 2017-12-01 | 5 | True |
| PARIS-AUSTERLITZ | BOURGES | 48 | 48 | 2014-01-01 | 2017-12-01 | 118 | True |
| PARIS-AUSTERLITZ | BRIANÇON | 116 | 116 | 2016-07-01 | 2026-05-01 | 21 | True |
| PARIS-AUSTERLITZ | BRIVE/CAHORS | 118 | 118 | 2016-07-01 | 2026-05-01 | 163 | True |
| PARIS-AUSTERLITZ | CERBERE | 99 | 99 | 2014-01-01 | 2026-05-01 | 54 | True |
| PARIS-AUSTERLITZ | HENDAYE | 18 | 18 | 2016-07-01 | 2017-12-01 | 9 | True |
| PARIS-AUSTERLITZ | LATOUR-DE-CAROL | 99 | 99 | 2017-02-01 | 2026-05-01 | 20 | True |
| PARIS-AUSTERLITZ | LIMOGES | 18 | 18 | 2016-07-01 | 2017-12-01 | 40 | True |
| PARIS-AUSTERLITZ | LOURDES/HENDAYE | 24 | 24 | 2022-01-01 | 2023-12-01 | 19 | False |
| PARIS-AUSTERLITZ | MODANE | 12 | 12 | 2021-01-01 | 2021-12-01 | 17 | True |
| PARIS-AUSTERLITZ | NICE-VILLE | 83 | 83 | 2016-07-01 | 2026-05-01 | 24 | True |
| PARIS-AUSTERLITZ | ORLÉANS | 48 | 48 | 2014-01-01 | 2017-12-01 | 318 | True |
| PARIS-AUSTERLITZ | RODEZ/ALBI | 98 | 98 | 2018-01-01 | 2026-05-01 | 20 | False |
| PARIS-AUSTERLITZ | TARBES | 30 | 30 | 2023-12-01 | 2026-05-01 | 19 | True |
| PARIS-AUSTERLITZ | TOULOUSE-MATABIAU | 157 | 104 | 2016-08-01 | 2026-05-01 | 61 | True |
| PARIS-AUSTERLITZ | TOULOUSE-MATABIAU/CERBERE | 59 | 59 | 2016-07-01 | 2021-12-01 | 41 | True |
| PARIS-AUSTERLITZ | TOULOUSE-MATABIAU/RODEZ | 18 | 18 | 2016-07-01 | 2017-12-01 | 64 | True |
| PARIS-AUSTERLITZ | TOURS | 48 | 48 | 2014-01-01 | 2017-12-01 | 119 | True |
| PARIS-BERCY | CLERMONT-FERRAND | 149 | 149 | 2014-01-01 | 2026-05-01 | 206 | True |
| PARIS-BERCY | NEVERS | 48 | 48 | 2014-01-01 | 2017-12-01 | 140 | True |
| PARIS-EST | BELFORT | 48 | 48 | 2014-01-01 | 2017-12-01 | 121 | True |
| PARIS-EST | TROYES | 48 | 48 | 2014-01-01 | 2017-12-01 | 233 | True |
| PARIS-NORD | AMIENS | 60 | 60 | 2014-01-01 | 2018-12-01 | 202 | True |
| PARIS-NORD | BOULOGNE-VILLE | 60 | 60 | 2014-01-01 | 2018-12-01 | 114 | True |
| PARIS-NORD | MAUBEUGE | 48 | 48 | 2014-01-01 | 2017-12-01 | 243 | True |
| PARIS-NORD | MAUBEUGE/CAMBRAI | 12 | 12 | 2018-01-01 | 2018-12-01 | 153 | False |
| PARIS-NORD | ST-QUENTIN | 12 | 12 | 2018-01-01 | 2018-12-01 | 115 | True |
| PARIS-ST-LAZARE | CAEN | 72 | 72 | 2014-01-01 | 2019-12-01 | 221 | True |
| PARIS-ST-LAZARE | CHERBOURG | 72 | 72 | 2014-01-01 | 2019-12-01 | 181 | True |
| PARIS-ST-LAZARE | LE HAVRE | 72 | 72 | 2014-01-01 | 2019-12-01 | 327 | True |
| PARIS-ST-LAZARE | ROUEN | 30 | 30 | 2014-01-01 | 2016-06-01 | 284 | True |
| PARIS-ST-LAZARE | ROUEN-RIVE-DROITE | 42 | 42 | 2016-07-01 | 2019-12-01 | 276 | True |
| PARIS-ST-LAZARE | TROUVILLE-DEAUVILLE | 72 | 72 | 2014-01-01 | 2019-12-01 | 85 | True |
| PARIS-VAUGIRARD | GRANVILLE | 72 | 72 | 2014-01-01 | 2019-12-01 | 153 | True |
| ROUEN | PARIS-ST-LAZARE | 30 | 30 | 2014-01-01 | 2016-06-01 | 276 | True |
| ROUEN-RIVE-DROITE | PARIS-ST-LAZARE | 42 | 42 | 2016-07-01 | 2019-12-01 | 274 | True |
| ST-QUENTIN | PARIS-NORD | 12 | 12 | 2018-01-01 | 2018-12-01 | 114 | True |
| TARBES | PARIS-AUSTERLITZ | 30 | 30 | 2023-12-01 | 2026-05-01 | 19 | True |
| TOULOUSE-MATABIAU | BAYONNE | 29 | 29 | 2018-01-01 | 2020-12-01 | 77 | True |
| TOULOUSE-MATABIAU | HENDAYE | 119 | 119 | 2014-01-01 | 2026-05-01 | 94 | True |
| TOULOUSE-MATABIAU | PARIS-AUSTERLITZ | 157 | 104 | 2016-08-01 | 2026-05-01 | 59 | True |
| TOULOUSE-MATABIAU/CERBERE | PARIS-AUSTERLITZ | 14 | 14 | 2016-07-01 | 2017-12-01 | 88 | True |
| TOULOUSE-MATABIAU/RODEZ | PARIS-AUSTERLITZ | 18 | 18 | 2016-07-01 | 2017-12-01 | 65 | True |
| TOURS | CAEN | 72 | 72 | 2014-01-01 | 2019-12-01 | 59 | True |
| TOURS | PARIS-AUSTERLITZ | 48 | 48 | 2014-01-01 | 2017-12-01 | 119 | True |
| TROUVILLE-DEAUVILLE | PARIS-ST-LAZARE | 72 | 72 | 2014-01-01 | 2019-12-01 | 83 | True |
| TROYES | PARIS-EST | 48 | 48 | 2014-01-01 | 2017-12-01 | 228 | True |

### Noms de gares/libellés composites (contenant « / »)

| g |
|---|
| ALBI/RODEZ |
| BOURG-ST-MAURICE/ST-GERVAIS |
| BRIANÇON/NICE-VILLE |
| BRIVE/CAHORS |
| CAHORS/BRIVE |
| CAMBRAI/MAUBEUGE |
| CERBERE/TOULOUSE |
| HENDAYE/LOURDES |
| LOURDES/HENDAYE |
| MAUBEUGE/CAMBRAI |
| RODEZ/ALBI |
| TOULOUSE-MATABIAU/CERBERE |
| TOULOUSE-MATABIAU/RODEZ |

### Liaisons ayant plusieurs lignes le même mois (doublons apparents)

| depart | arrivee | mois_concernes | premier | dernier |
|---|---|---|---|---|
| PARIS-AUSTERLITZ | TOULOUSE-MATABIAU | 53 | 2022-01-01 | 2026-05-01 |
| TOULOUSE-MATABIAU | PARIS-AUSTERLITZ | 53 | 2022-01-01 | 2026-05-01 |

### Exemple de doublon : Paris-Austerlitz → Toulouse, 2 mois

| date | depart | arrivee | nombre_de_trains_programmes | nombre_de_trains_ayant_circule | nombre_de_trains_annules | nombre_de_trains_en_retard_a_l_arrivee | taux_de_regularite | nombre_de_trains_a_l_heure_pour_un_train_en_retard_a_l_arrivee |
|---|---|---|---|---|---|---|---|---|
| 2022-01-01 | PARIS-AUSTERLITZ | TOULOUSE-MATABIAU | 81 | 81 | 0 | 19 | 76.54 | 3.26 |
| 2022-01-01 | PARIS-AUSTERLITZ | TOULOUSE-MATABIAU | 28 | 28 | 0 | 2 | 92.86 | 13 |
| 2026-05-01 | PARIS-AUSTERLITZ | TOULOUSE-MATABIAU | 66 | 66 | 0 | 8 | 87.88 | 7.25 |
| 2026-05-01 | PARIS-AUSTERLITZ | TOULOUSE-MATABIAU | 24 | 24 | 0 | 3 | 87.5 | 7 |

### Liaisons présentes sur les 12 derniers mois disponibles

| depart | arrivee | programmes | circules |
|---|---|---|---|
| ALBI/RODEZ | PARIS-AUSTERLITZ | 315 | 301 |
| AURILLAC | PARIS-AUSTERLITZ | 287 | 274 |
| BORDEAUX-ST-JEAN | MARSEILLE-ST-CHARLES | 2421 | 2353 |
| BORDEAUX-ST-JEAN | NANTES | 1432 | 1417 |
| BRIANÇON | PARIS-AUSTERLITZ | 245 | 240 |
| BÉZIERS | CLERMONT-FERRAND | 365 | 362 |
| CAHORS/BRIVE | PARIS-AUSTERLITZ | 2201 | 2186 |
| CERBERE | PARIS-AUSTERLITZ | 170 | 168 |
| CLERMONT-FERRAND | BÉZIERS | 365 | 363 |
| CLERMONT-FERRAND | PARIS-BERCY | 2579 | 2550 |
| HENDAYE | TOULOUSE-MATABIAU | 1392 | 1359 |
| LATOUR-DE-CAROL | PARIS-AUSTERLITZ | 147 | 146 |
| LYON | NANCY | 367 | 365 |
| LYON | NANTES | 1025 | 1009 |
| MARSEILLE-ST-CHARLES | BORDEAUX-ST-JEAN | 2353 | 2279 |
| NANCY | LYON | 366 | 366 |
| NANTES | BORDEAUX-ST-JEAN | 1435 | 1411 |
| NANTES | LYON | 1025 | 1013 |
| NICE-VILLE | PARIS-AUSTERLITZ | 314 | 304 |
| PARIS-AUSTERLITZ | AURILLAC | 301 | 272 |
| PARIS-AUSTERLITZ | BRIANÇON | 244 | 242 |
| PARIS-AUSTERLITZ | BRIVE/CAHORS | 1982 | 1967 |
| PARIS-AUSTERLITZ | CERBERE | 171 | 168 |
| PARIS-AUSTERLITZ | LATOUR-DE-CAROL | 148 | 146 |
| PARIS-AUSTERLITZ | NICE-VILLE | 316 | 308 |
| PARIS-AUSTERLITZ | RODEZ/ALBI | 321 | 303 |
| PARIS-AUSTERLITZ | TARBES | 231 | 222 |
| PARIS-AUSTERLITZ | TOULOUSE-MATABIAU | 1200 | 1190 |
| PARIS-BERCY | CLERMONT-FERRAND | 2575 | 2548 |
| TARBES | PARIS-AUSTERLITZ | 229 | 219 |
| TOULOUSE-MATABIAU | HENDAYE | 1370 | 1341 |
| TOULOUSE-MATABIAU | PARIS-AUSTERLITZ | 1081 | 1066 |

## Cohérence des colonnes

### Contrôles

| lignes | circules_incoherents | taux_incoherents | ratio_incoherent | circules_zero | programmes_zero | taux_null |
|---|---|---|---|---|---|---|
| 5949 | 0 | 0 | 190 | 161 | 158 | 0 |

### Lignes à 0 train circulé, par mois

| date | lignes | programmes | annules |
|---|---|---|---|
| 2015-04-01 | 1 | 0 | 0 |
| 2015-06-01 | 2 | 0 | 0 |
| 2015-07-01 | 1 | 0 | 0 |
| 2015-10-01 | 2 | 0 | 0 |
| 2015-11-01 | 2 | 0 | 0 |
| 2016-10-01 | 2 | 0 | 0 |
| 2016-11-01 | 6 | 0 | 0 |
| 2016-12-01 | 2 | 0 | 0 |
| 2017-01-01 | 2 | 0 | 0 |
| 2017-02-01 | 2 | 0 | 0 |
| 2017-03-01 | 2 | 0 | 0 |
| 2017-05-01 | 5 | 0 | 0 |
| 2017-06-01 | 6 | 0 | 0 |
| 2017-07-01 | 4 | 0 | 0 |
| 2017-08-01 | 6 | 0 | 0 |
| 2017-09-01 | 6 | 0 | 0 |
| 2017-10-01 | 6 | 0 | 0 |
| 2017-11-01 | 8 | 0 | 0 |
| 2017-12-01 | 6 | 0 | 0 |
| 2018-05-01 | 2 | 0 | 0 |
| 2018-11-01 | 2 | 0 | 0 |
| 2019-02-01 | 2 | 0 | 0 |
| 2019-04-01 | 2 | 0 | 0 |
| 2019-05-01 | 2 | 0 | 0 |
| 2019-06-01 | 2 | 0 | 0 |
| 2020-09-01 | 2 | 0 | 0 |
| 2020-10-01 | 2 | 0 | 0 |
| 2020-11-01 | 2 | 0 | 0 |
| 2021-01-01 | 4 | 0 | 0 |
| 2021-02-01 | 5 | 2 | 2 |
| 2021-03-01 | 4 | 0 | 0 |
| 2021-04-01 | 8 | 0 | 0 |
| 2021-05-01 | 2 | 0 | 0 |
| 2021-06-01 | 2 | 0 | 0 |
| 2021-07-01 | 2 | 0 | 0 |
| 2021-08-01 | 2 | 0 | 0 |
| 2021-09-01 | 2 | 0 | 0 |
| 2021-10-01 | 2 | 0 | 0 |
| 2021-11-01 | 2 | 0 | 0 |
| 2022-11-01 | 4 | 0 | 0 |
| 2022-12-01 | 4 | 0 | 0 |
| 2023-01-01 | 6 | 0 | 0 |
| 2023-02-01 | 6 | 0 | 0 |
| 2023-03-01 | 5 | 0 | 0 |
| 2023-04-01 | 2 | 0 | 0 |
| 2024-05-01 | 2 | 4 | 4 |
| 2024-06-01 | 2 | 0 | 0 |
| 2026-03-01 | 2 | 0 | 0 |
| 2026-04-01 | 2 | 0 | 0 |
| 2026-05-01 | 2 | 0 | 0 |

### Valeurs de taux_de_regularite quand 0 train a circulé

| taux_de_regularite | ratio | count_star() |
|---|---|---|
| 0 | 0 | 161 |

### Ratio « trains à l'heure pour un train en retard » quand 0 retard

| ratio | count_star() |
|---|---|
| 0 | 318 |
| 16 | 1 |
| 22 | 2 |
| 10 | 1 |
| 13 | 1 |
| 11 | 1 |
| 12 | 1 |

## Séries mensuelles

### Totaux mensuels

| date | programmes | annules | pct_annules | retards | regularite |
|---|---|---|---|---|---|
| 2014-01-01 | 8424 | 42 | 0.5 | 796 | 90.5 |
| 2014-02-01 | 7604 | 63 | 0.8 | 846 | 88.8 |
| 2014-03-01 | 8413 | 36 | 0.4 | 781 | 90.7 |
| 2014-04-01 | 8254 | 33 | 0.4 | 809 | 90.2 |
| 2014-05-01 | 8371 | 45 | 0.5 | 750 | 91 |
| 2014-06-01 | 6388 | 25 | 0.4 | 1041 | 83.6 |
| 2014-07-01 | 8624 | 242 | 2.8 | 1332 | 84.1 |
| 2014-08-01 | 8321 | 66 | 0.8 | 845 | 89.8 |
| 2014-09-01 | 8178 | 85 | 1 | 961 | 88.1 |
| 2014-10-01 | 8715 | 76 | 0.9 | 1376 | 84.1 |
| 2014-11-01 | 7597 | 65 | 0.9 | 1073 | 85.8 |
| 2014-12-01 | 7899 | 123 | 1.6 | 1205 | 84.5 |
| 2015-01-01 | 7361 | 99 | 1.3 | 777 | 89.3 |
| 2015-02-01 | 6698 | 116 | 1.7 | 746 | 88.7 |
| 2015-03-01 | 7442 | 62 | 0.8 | 695 | 90.6 |
| 2015-04-01 | 7094 | 94 | 1.3 | 730 | 89.6 |
| 2015-05-01 | 7216 | 28 | 0.4 | 652 | 90.9 |
| 2015-06-01 | 7340 | 60 | 0.8 | 1021 | 86 |
| 2015-07-01 | 7384 | 91 | 1.2 | 1177 | 83.9 |
| 2015-08-01 | 7444 | 60 | 0.8 | 946 | 87.2 |
| 2015-09-01 | 7548 | 83 | 1.1 | 847 | 88.7 |
| 2015-10-01 | 7493 | 58 | 0.8 | 976 | 86.9 |
| 2015-11-01 | 7071 | 93 | 1.3 | 1171 | 83.2 |
| 2015-12-01 | 7670 | 100 | 1.3 | 814 | 89.2 |
| 2016-01-01 | 7465 | 85 | 1.1 | 789 | 89.3 |
| 2016-02-01 | 7220 | 80 | 1.1 | 723 | 89.9 |
| 2016-03-01 | 7062 | 70 | 1 | 925 | 86.8 |
| 2016-04-01 | 7338 | 63 | 0.9 | 903 | 87.6 |
| 2016-05-01 | 6914 | 76 | 1.1 | 1139 | 83.3 |
| 2016-06-01 | 4404 | 56 | 1.3 | 1056 | 75.7 |
| 2016-07-01 | 8422 | 88 | 1 | 1304 | 84.4 |
| 2016-08-01 | 8308 | 87 | 1 | 1160 | 85.9 |
| 2016-09-01 | 8787 | 93 | 1.1 | 1103 | 87.3 |
| 2016-10-01 | 8552 | 64 | 0.7 | 1093 | 87.1 |
| 2016-11-01 | 8076 | 140 | 1.7 | 1694 | 78.7 |
| 2016-12-01 | 8749 | 78 | 0.9 | 1294 | 85.1 |
| 2017-01-01 | 8998 | 104 | 1.2 | 1346 | 84.9 |
| 2017-02-01 | 7986 | 68 | 0.9 | 956 | 87.9 |
| 2017-03-01 | 8926 | 78 | 0.9 | 987 | 88.8 |
| 2017-04-01 | 8456 | 73 | 0.9 | 1025 | 87.8 |
| 2017-05-01 | 8310 | 81 | 1 | 1121 | 86.4 |
| 2017-06-01 | 8274 | 93 | 1.1 | 1544 | 81.1 |
| 2017-07-01 | 8595 | 87 | 1 | 1456 | 82.9 |
| 2017-08-01 | 8828 | 77 | 0.9 | 1215 | 86.1 |
| 2017-09-01 | 8310 | 85 | 1 | 1127 | 86.3 |
| 2017-10-01 | 8493 | 75 | 0.9 | 1260 | 85 |
| 2017-11-01 | 8333 | 118 | 1.4 | 1409 | 82.8 |
| 2017-12-01 | 6943 | 123 | 1.8 | 1099 | 83.9 |
| 2018-01-01 | 6467 | 178 | 2.8 | 862 | 86.3 |
| 2018-02-01 | 5668 | 193 | 3.4 | 1107 | 79.8 |
| 2018-03-01 | 6353 | 98 | 1.5 | 778 | 87.6 |
| 2018-04-01 | 3398 | 26 | 0.8 | 641 | 81 |
| 2018-05-01 | 3747 | 62 | 1.7 | 689 | 81.3 |
| 2018-06-01 | 4584 | 54 | 1.2 | 994 | 78.1 |
| 2018-07-01 | 6011 | 115 | 1.9 | 1197 | 79.7 |
| 2018-08-01 | 6402 | 97 | 1.5 | 849 | 86.5 |
| 2018-09-01 | 6245 | 67 | 1.1 | 828 | 86.6 |
| 2018-10-01 | 6277 | 126 | 2 | 967 | 84.3 |
| 2018-11-01 | 7225 | 108 | 1.5 | 1776 | 75 |
| 2018-12-01 | 6227 | 112 | 1.8 | 903 | 85.2 |
| 2019-01-01 | 5062 | 99 | 2 | 552 | 88.9 |
| 2019-02-01 | 4560 | 49 | 1.1 | 409 | 90.9 |
| 2019-03-01 | 4933 | 62 | 1.3 | 528 | 89.2 |
| 2019-04-01 | 4949 | 47 | 0.9 | 457 | 90.7 |
| 2019-05-01 | 5078 | 57 | 1.1 | 542 | 89.2 |
| 2019-06-01 | 4932 | 113 | 2.3 | 876 | 81.8 |
| 2019-07-01 | 5182 | 61 | 1.2 | 831 | 83.8 |
| 2019-08-01 | 4590 | 48 | 1 | 542 | 88.1 |
| 2019-09-01 | 4928 | 64 | 1.3 | 550 | 88.7 |
| 2019-10-01 | 5028 | 360 | 7.2 | 724 | 84.5 |
| 2019-11-01 | 4694 | 109 | 2.3 | 816 | 82.2 |
| 2019-12-01 | 1924 | 63 | 3.3 | 401 | 78.5 |
| 2020-01-01 | 1340 | 31 | 2.3 | 252 | 80.7 |
| 2020-02-01 | 2087 | 50 | 2.4 | 344 | 83.1 |
| 2020-03-01 | 1247 | 47 | 3.8 | 201 | 83.3 |
| 2020-04-01 | 120 | 0 | 0 | 8 | 93.3 |
| 2020-05-01 | 507 | 8 | 1.6 | 99 | 80.2 |
| 2020-06-01 | 1189 | 22 | 1.9 | 204 | 82.5 |
| 2020-07-01 | 2047 | 31 | 1.5 | 387 | 80.8 |
| 2020-08-01 | 2165 | 30 | 1.4 | 379 | 82.2 |
| 2020-09-01 | 2034 | 66 | 3.2 | 324 | 83.5 |
| 2020-10-01 | 1960 | 89 | 4.5 | 400 | 78.6 |
| 2020-11-01 | 688 | 21 | 3.1 | 95 | 85.8 |
| 2020-12-01 | 1401 | 34 | 2.4 | 264 | 80.7 |
| 2021-01-01 | 1899 | 44 | 2.3 | 251 | 86.5 |
| 2021-02-01 | 1706 | 38 | 2.2 | 273 | 83.6 |
| 2021-03-01 | 1708 | 22 | 1.3 | 203 | 88 |
| 2021-04-01 | 1145 | 6 | 0.5 | 139 | 87.8 |
| 2021-05-01 | 1709 | 22 | 1.3 | 224 | 86.7 |
| 2021-06-01 | 1904 | 34 | 1.8 | 256 | 86.3 |
| 2021-07-01 | 2297 | 44 | 1.9 | 350 | 84.5 |
| 2021-08-01 | 2427 | 39 | 1.6 | 317 | 86.7 |
| 2021-09-01 | 2226 | 39 | 1.8 | 255 | 88.3 |
| 2021-10-01 | 2271 | 29 | 1.3 | 389 | 82.6 |
| 2021-11-01 | 2020 | 31 | 1.5 | 304 | 84.7 |
| 2021-12-01 | 2313 | 66 | 2.9 | 321 | 85.7 |
| 2022-01-01 | 2025 | 24 | 1.2 | 320 | 84 |
| 2022-02-01 | 2020 | 8 | 0.4 | 233 | 88.4 |
| 2022-03-01 | 2364 | 24 | 1 | 251 | 89.3 |
| 2022-04-01 | 2132 | 23 | 1.1 | 272 | 87.1 |
| 2022-05-01 | 2264 | 20 | 0.9 | 332 | 85.2 |
| 2022-06-01 | 2380 | 40 | 1.7 | 453 | 80.6 |
| 2022-07-01 | 2406 | 44 | 1.8 | 633 | 73.2 |
| 2022-08-01 | 2553 | 29 | 1.1 | 475 | 81.2 |
| 2022-09-01 | 2348 | 35 | 1.5 | 352 | 84.8 |
| 2022-10-01 | 2220 | 10 | 0.5 | 329 | 85.1 |
| 2022-11-01 | 1854 | 29 | 1.6 | 311 | 83 |
| 2022-12-01 | 1766 | 42 | 2.4 | 379 | 78 |
| 2023-01-01 | 2017 | 12 | 0.6 | 286 | 85.7 |
| 2023-02-01 | 1853 | 12 | 0.6 | 319 | 82.7 |
| 2023-03-01 | 1211 | 7 | 0.6 | 203 | 83.1 |
| 2023-04-01 | 1854 | 22 | 1.2 | 292 | 84.1 |
| 2023-05-01 | 2274 | 13 | 0.6 | 439 | 80.6 |
| 2023-06-01 | 2560 | 27 | 1.1 | 521 | 79.4 |
| 2023-07-01 | 2585 | 22 | 0.9 | 413 | 83.9 |
| 2023-08-01 | 2652 | 20 | 0.8 | 426 | 83.8 |
| 2023-09-01 | 2471 | 20 | 0.8 | 397 | 83.8 |
| 2023-10-01 | 2482 | 33 | 1.3 | 492 | 79.9 |
| 2023-11-01 | 2164 | 61 | 2.8 | 573 | 72.8 |
| 2023-12-01 | 2179 | 46 | 2.1 | 411 | 80.7 |
| 2024-01-01 | 2429 | 30 | 1.2 | 372 | 84.5 |
| 2024-02-01 | 2220 | 32 | 1.4 | 337 | 84.6 |
| 2024-03-01 | 2280 | 15 | 0.7 | 274 | 87.9 |
| 2024-04-01 | 2530 | 29 | 1.1 | 373 | 85.1 |
| 2024-05-01 | 2196 | 15 | 0.7 | 329 | 84.9 |
| 2024-06-01 | 2432 | 22 | 0.9 | 333 | 86.2 |
| 2024-07-01 | 2702 | 29 | 1.1 | 457 | 82.9 |
| 2024-08-01 | 2741 | 15 | 0.5 | 402 | 85.3 |
| 2024-09-01 | 2575 | 15 | 0.6 | 345 | 86.5 |
| 2024-10-01 | 2567 | 39 | 1.5 | 400 | 84.2 |
| 2024-11-01 | 2148 | 24 | 1.1 | 421 | 80.2 |
| 2024-12-01 | 2482 | 12 | 0.5 | 346 | 86 |
| 2025-01-01 | 2416 | 37 | 1.5 | 364 | 84.7 |
| 2025-02-01 | 2177 | 8 | 0.4 | 307 | 85.8 |
| 2025-03-01 | 2496 | 13 | 0.5 | 312 | 87.4 |
| 2025-04-01 | 2437 | 10 | 0.4 | 349 | 85.6 |
| 2025-05-01 | 2264 | 13 | 0.6 | 342 | 84.8 |
| 2025-06-01 | 2455 | 64 | 2.6 | 524 | 78.1 |
| 2025-07-01 | 2693 | 35 | 1.3 | 436 | 83.6 |
| 2025-08-01 | 2498 | 7 | 0.3 | 440 | 82.3 |
| 2025-09-01 | 2341 | 27 | 1.2 | 339 | 85.4 |
| 2025-10-01 | 2461 | 22 | 0.9 | 393 | 83.9 |
| 2025-11-01 | 2233 | 45 | 2 | 375 | 82.9 |
| 2025-12-01 | 2528 | 63 | 2.5 | 399 | 83.8 |
| 2026-01-01 | 2297 | 76 | 3.3 | 496 | 77.7 |
| 2026-02-01 | 2255 | 115 | 5.1 | 540 | 74.8 |
| 2026-03-01 | 2472 | 22 | 0.9 | 296 | 87.9 |
| 2026-04-01 | 2529 | 24 | 0.9 | 440 | 82.4 |
| 2026-05-01 | 2211 | 15 | 0.7 | 438 | 80.1 |

## Volumes (pour le poids bayésien)

### Quantiles du nombre de trains circulés par liaison-mois (> 0), 2020 et après

| quantiles | moyenne |
|---|---|
| [9.0, 14.0, 24.0, 31.0, 115.0, 192.60000000000014] | 73.24 |

## Gares communes avec le jeu TGV (libellés bruts)

### Gares Intercités dont le libellé, ponctuation retirée, existe aussi dans le jeu TGV

| gare_intercites | gare_tgv |
|---|---|
| BORDEAUX-ST-JEAN | BORDEAUX ST JEAN |
| LYON-PART-DIEU | LYON PART DIEU |
| MARSEILLE-ST-CHARLES | MARSEILLE ST CHARLES |
| NANCY | NANCY |
| NANTES | NANTES |
| NICE-VILLE | NICE VILLE |
| PARIS-EST | PARIS EST |
| PARIS-NORD | PARIS NORD |
| PARIS-VAUGIRARD | PARIS VAUGIRARD |
| TOULOUSE-MATABIAU | TOULOUSE MATABIAU |
| TOURS | TOURS |
| ALBI/RODEZ |  |
| AMIENS |  |
| AURILLAC |  |
| BAYONNE |  |
| BELFORT |  |
| BOULOGNE-VILLE |  |
| BOURG-ST-MAURICE/ST-GERVAIS |  |
| BOURGES |  |
| BRIANÇON |  |
| BRIANÇON/NICE-VILLE |  |
| BRIVE/CAHORS |  |
| BÉZIERS |  |
| CAEN |  |
| CAHORS/BRIVE |  |
| CAMBRAI/MAUBEUGE |  |
| CERBERE |  |
| CERBERE/TOULOUSE |  |
| CHERBOURG |  |
| CLERMONT-FERRAND |  |
| GRANVILLE |  |
| HENDAYE |  |
| HENDAYE/LOURDES |  |
| LATOUR-DE-CAROL |  |
| LE HAVRE |  |
| LIMOGES |  |
| LOURDES/HENDAYE |  |
| LYON |  |
| MAUBEUGE |  |
| MAUBEUGE/CAMBRAI |  |
| MODANE |  |
| NEVERS |  |
| NÎMES |  |
| ORLÉANS |  |
| PARIS-AUSTERLITZ |  |
| PARIS-BERCY |  |
| PARIS-ST-LAZARE |  |
| RODEZ/ALBI |  |
| ROUEN |  |
| ROUEN-RIVE-DROITE |  |
| ST-QUENTIN |  |
| TARBES |  |
| TOULOUSE-MATABIAU/CERBERE |  |
| TOULOUSE-MATABIAU/RODEZ |  |
| TROUVILLE-DEAUVILLE |  |
| TROYES |  |

