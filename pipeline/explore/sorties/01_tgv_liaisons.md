# Exploration — TGV par liaisons (regularite-mensuelle-tgv-aqst)

_Généré par `pipeline/explore/01_tgv_liaisons.py`._

## Métadonnées du portail

- Titre : Régularité mensuelle TGV par liaisons
- Éditeur : SNCF Voyageurs
- Licence : Open Database License (ODbL)
- Dernière modification des données : 2026-10-02T10:10:31+00:00
- Nombre d'enregistrements : 12907

| champ | type | libellé | description |
|---|---|---|---|
| date | date | Date |  |
| service | text | Service | National / international |
| gare_depart | text | Gare de départ |  |
| gare_arrivee | text | Gare d'arrivée |  |
| duree_moyenne | int | Durée moyenne du trajet | Durée moyenne prévue du trajet, en min |
| nb_train_prevu | int | Nombre de circulations prévues |  |
| nb_annulation | int | Nombre de trains annulés |  |
| commentaire_annulation | text | Commentaire annulations | Facultatif |
| nb_train_depart_retard | int | Nombre de trains en retard au départ |  |
| retard_moyen_depart | double | Retard moyen des trains en retard au départ | En min |
| retard_moyen_tous_trains_depart | double | Retard moyen de tous les trains au départ | Retard moyen de tous les trains au départ, en min |
| commentaire_retards_depart | text | Commentaire retards au départ | Facultatif |
| nb_train_retard_arrivee | int | Nombre de trains en retard à l'arrivée |  |
| retard_moyen_arrivee | double | Retard moyen des trains en retard à l'arrivée | Retard moyen des trains en retard à l'arrivée, en min |
| retard_moyen_tous_trains_arrivee | double | Retard moyen de tous les trains à l'arrivée | En min |
| commentaires_retard_arrivee | text | Commentaire retards à l'arrivée | Facultatif |
| nb_train_retard_sup_15 | int | Nombre trains en retard > 15min | Nombre de trains en retard supérieur à 15min (si liaison concurrencée par vol) |
| retard_moyen_trains_retard_sup15 | double | Retard moyen trains en retard > 15 (si liaison concurrencée par vol) | Retard moyen (en min) des trains en retard supérieur à 15min (si liaison concurrencée par vol) |
| nb_train_retard_sup_30 | int | Nombre trains en retard > 30min | Nombre de trains en retard supérieur à 30 min |
| nb_train_retard_sup_60 | int | Nombre trains en retard > 60min | Nombre de trains en retard supérieur à 60 min |
| prct_cause_externe | double | Prct retard pour causes externes | Pourcentage de trains en retard pour causes externes (météo, obstacles, colis suspects, malveillance, mouvements sociaux, etc.) |
| prct_cause_infra | double | Prct retard pour cause infrastructure | Pourcentage de trains en retard pour cause infrastructure ferroviaire (maintenance, travaux) |
| prct_cause_gestion_trafic | double | Prct retard pour cause gestion trafic | Pourcentage de trains en retard pour cause gestion du trafic % trains en retard pour cause de gestion trafic (circulation sur ligne ferroviaire, interactions réseaux) |
| prct_cause_materiel_roulant | double | Prct retard pour cause matériel roulant | Pourcentage de trains en retard pour cause matériel roulant |
| prct_cause_gestion_gare | double | Prct retard pour cause gestion en gare et réutilisation de matériel | Pourcentage de trains en retard pour cause de gestion en gare et réutilisation de matériel |
| prct_cause_prise_en_charge_voyageurs | double | Prct retard pour cause prise en compte voyageurs (affluence, gestions PSH, correspondances) | Pourcentage de trains en retard pour cause de prise en compte voyageurs (affluence, gestions PSH, correspondances) |

## Couverture temporelle

### Période, lignes, liaisons

| premier_mois | dernier_mois | nb_mois | nb_mois_attendus | lignes | liaisons_orientees | liaisons_non_orientees |
|---|---|---|---|---|---|---|
| 2018-01-01 | 2026-09-01 | 105 | 105 | 12907 | 130 | 65 |

### Mois manquants dans la série

| mois_manquant |
|---|

### Nombre de lignes par mois (distribution)

| lignes_par_mois | nb_mois | premier | dernier |
|---|---|---|---|
| 118 | 1 | 2021-04-01 | 2021-04-01 |
| 119 | 4 | 2023-10-01 | 2024-06-01 |
| 121 | 54 | 2021-01-01 | 2026-09-01 |
| 123 | 30 | 2019-01-01 | 2022-12-01 |
| 124 | 1 | 2022-08-01 | 2022-08-01 |
| 130 | 12 | 2018-01-01 | 2018-12-01 |
| 135 | 3 | 2025-07-01 | 2025-09-01 |

### Lignes par service

| service | lignes | liaisons |
|---|---|---|
| National | 11339 | 116 |
| International | 1568 | 30 |

## Liaisons

### Liaisons dont la couverture n'est pas complète (apparitions / disparitions / reclassements)

| service | gare_depart | gare_arrivee | nb_mois | premier | dernier |
|---|---|---|---|---|---|
| International | BARCELONA | PARIS LYON | 93 | 2018-01-01 | 2025-09-01 |
| National | BORDEAUX ST JEAN | PARIS VAUGIRARD | 12 | 2018-01-01 | 2018-12-01 |
| National | BORDEAUX ST JEAN | TOURCOING | 103 | 2018-01-01 | 2026-09-01 |
| International | ITALIE | PARIS LYON | 101 | 2018-01-01 | 2026-09-01 |
| International | MADRID | MARSEILLE ST CHARLES | 45 | 2018-01-01 | 2022-12-01 |
| International | MARSEILLE ST CHARLES | MADRID | 45 | 2018-01-01 | 2022-12-01 |
| National | MARSEILLE ST CHARLES | TOURCOING | 104 | 2018-01-01 | 2026-09-01 |
| National | NANTES | PARIS VAUGIRARD | 12 | 2018-01-01 | 2018-12-01 |
| International | PARIS LYON | BARCELONA | 93 | 2018-01-01 | 2025-09-01 |
| International | PARIS LYON | ITALIE | 101 | 2018-01-01 | 2026-09-01 |
| International | PARIS LYON | ZURICH | 104 | 2018-01-01 | 2026-09-01 |
| National | PARIS VAUGIRARD | BORDEAUX ST JEAN | 12 | 2018-01-01 | 2018-12-01 |
| National | PARIS VAUGIRARD | NANTES | 12 | 2018-01-01 | 2018-12-01 |
| National | PARIS VAUGIRARD | RENNES | 12 | 2018-01-01 | 2018-12-01 |
| National | RENNES | PARIS VAUGIRARD | 12 | 2018-01-01 | 2018-12-01 |
| National | TOURCOING | BORDEAUX ST JEAN | 103 | 2018-01-01 | 2026-09-01 |
| National | TOURCOING | MARSEILLE ST CHARLES | 13 | 2018-01-01 | 2022-08-01 |
| International | ZURICH | PARIS LYON | 104 | 2018-01-01 | 2026-09-01 |
| International | BELLEGARDE (AIN) | PARIS LYON | 3 | 2025-07-01 | 2025-09-01 |
| International | CHAMBERY CHALLES LES EAUX | PARIS LYON | 3 | 2025-07-01 | 2025-09-01 |
| International | DIJON VILLE | PARIS LYON | 3 | 2025-07-01 | 2025-09-01 |
| International | LYON PART DIEU | MARSEILLE ST CHARLES | 3 | 2025-07-01 | 2025-09-01 |
| International | MACON LOCHE | PARIS LYON | 3 | 2025-07-01 | 2025-09-01 |
| International | MARSEILLE ST CHARLES | LYON PART DIEU | 3 | 2025-07-01 | 2025-09-01 |
| International | MULHOUSE VILLE | PARIS LYON | 3 | 2025-07-01 | 2025-09-01 |
| International | PARIS EST | STRASBOURG | 3 | 2025-07-01 | 2025-09-01 |
| International | PARIS LYON | BELLEGARDE (AIN) | 3 | 2025-07-01 | 2025-09-01 |
| International | PARIS LYON | CHAMBERY CHALLES LES EAUX | 3 | 2025-07-01 | 2025-09-01 |
| International | PARIS LYON | DIJON VILLE | 3 | 2025-07-01 | 2025-09-01 |
| International | PARIS LYON | MACON LOCHE | 3 | 2025-07-01 | 2025-09-01 |
| International | PARIS LYON | MULHOUSE VILLE | 3 | 2025-07-01 | 2025-09-01 |
| International | STRASBOURG | PARIS EST | 3 | 2025-07-01 | 2025-09-01 |
| National | BARCELONA | PARIS LYON | 12 | 2025-10-01 | 2026-09-01 |
| National | PARIS LYON | BARCELONA | 12 | 2025-10-01 | 2026-09-01 |

### Liaisons orientées sans liaison retour

| service | gare_depart | gare_arrivee |
|---|---|---|

### Asymétries de couverture entre aller et retour (toutes services confondus)

| a | b | mois_aller | mois_retour | d1 | d2 | d1_retour | d2_retour |
|---|---|---|---|---|---|---|---|
| MARSEILLE ST CHARLES | TOURCOING | 104 | 13 | 2018-01-01 | 2026-09-01 | 2018-01-01 | 2022-08-01 |

### Gares citées (59) : nombre de lignes et période

| gare | lignes | mois | premier | dernier |
|---|---|---|---|---|
| AIX EN PROVENCE TGV | 210 | 105 | 2018-01-01 | 2026-09-01 |
| ANGERS SAINT LAUD | 210 | 105 | 2018-01-01 | 2026-09-01 |
| ANGOULEME | 210 | 105 | 2018-01-01 | 2026-09-01 |
| ANNECY | 210 | 105 | 2018-01-01 | 2026-09-01 |
| ARRAS | 210 | 105 | 2018-01-01 | 2026-09-01 |
| AVIGNON TGV | 210 | 105 | 2018-01-01 | 2026-09-01 |
| BARCELONA | 210 | 105 | 2018-01-01 | 2026-09-01 |
| BELLEGARDE (AIN) | 216 | 105 | 2018-01-01 | 2026-09-01 |
| BESANCON FRANCHE COMTE TGV | 210 | 105 | 2018-01-01 | 2026-09-01 |
| BORDEAUX ST JEAN | 440 | 105 | 2018-01-01 | 2026-09-01 |
| BREST | 210 | 105 | 2018-01-01 | 2026-09-01 |
| CHAMBERY CHALLES LES EAUX | 216 | 105 | 2018-01-01 | 2026-09-01 |
| DIJON VILLE | 216 | 105 | 2018-01-01 | 2026-09-01 |
| DOUAI | 210 | 105 | 2018-01-01 | 2026-09-01 |
| DUNKERQUE | 210 | 105 | 2018-01-01 | 2026-09-01 |
| FRANCFORT | 210 | 105 | 2018-01-01 | 2026-09-01 |
| GENEVE | 210 | 105 | 2018-01-01 | 2026-09-01 |
| GRENOBLE | 210 | 105 | 2018-01-01 | 2026-09-01 |
| ITALIE | 202 | 101 | 2018-01-01 | 2026-09-01 |
| LA ROCHELLE VILLE | 210 | 105 | 2018-01-01 | 2026-09-01 |
| LAUSANNE | 210 | 105 | 2018-01-01 | 2026-09-01 |
| LAVAL | 210 | 105 | 2018-01-01 | 2026-09-01 |
| LE CREUSOT MONTCEAU MONTCHANIN | 210 | 105 | 2018-01-01 | 2026-09-01 |
| LE MANS | 210 | 105 | 2018-01-01 | 2026-09-01 |
| LILLE | 630 | 105 | 2018-01-01 | 2026-09-01 |
| LYON PART DIEU | 1266 | 105 | 2018-01-01 | 2026-09-01 |
| MACON LOCHE | 216 | 105 | 2018-01-01 | 2026-09-01 |
| MADRID | 90 | 45 | 2018-01-01 | 2022-12-01 |
| MARNE LA VALLEE | 420 | 105 | 2018-01-01 | 2026-09-01 |
| MARSEILLE ST CHARLES | 1053 | 105 | 2018-01-01 | 2026-09-01 |
| METZ | 210 | 105 | 2018-01-01 | 2026-09-01 |
| MONTPELLIER | 420 | 105 | 2018-01-01 | 2026-09-01 |
| MULHOUSE VILLE | 216 | 105 | 2018-01-01 | 2026-09-01 |
| NANCY | 210 | 105 | 2018-01-01 | 2026-09-01 |
| NANTES | 444 | 105 | 2018-01-01 | 2026-09-01 |
| NICE VILLE | 210 | 105 | 2018-01-01 | 2026-09-01 |
| NIMES | 210 | 105 | 2018-01-01 | 2026-09-01 |
| PARIS EST | 1266 | 105 | 2018-01-01 | 2026-09-01 |
| PARIS LYON | 5270 | 105 | 2018-01-01 | 2026-09-01 |
| PARIS MONTPARNASSE | 3360 | 105 | 2018-01-01 | 2026-09-01 |
| PARIS NORD | 840 | 105 | 2018-01-01 | 2026-09-01 |
| PARIS VAUGIRARD | 72 | 12 | 2018-01-01 | 2018-12-01 |
| PERPIGNAN | 210 | 105 | 2018-01-01 | 2026-09-01 |
| POITIERS | 210 | 105 | 2018-01-01 | 2026-09-01 |
| QUIMPER | 210 | 105 | 2018-01-01 | 2026-09-01 |
| REIMS | 210 | 105 | 2018-01-01 | 2026-09-01 |
| RENNES | 444 | 105 | 2018-01-01 | 2026-09-01 |
| SAINT ETIENNE CHATEAUCREUX | 210 | 105 | 2018-01-01 | 2026-09-01 |
| ST MALO | 210 | 105 | 2018-01-01 | 2026-09-01 |
| ST PIERRE DES CORPS | 210 | 105 | 2018-01-01 | 2026-09-01 |
| STRASBOURG | 426 | 105 | 2018-01-01 | 2026-09-01 |
| STUTTGART | 210 | 105 | 2018-01-01 | 2026-09-01 |
| TOULON | 210 | 105 | 2018-01-01 | 2026-09-01 |
| TOULOUSE MATABIAU | 210 | 105 | 2018-01-01 | 2026-09-01 |
| TOURCOING | 323 | 104 | 2018-01-01 | 2026-09-01 |
| TOURS | 210 | 105 | 2018-01-01 | 2026-09-01 |
| VALENCE ALIXAN TGV | 210 | 105 | 2018-01-01 | 2026-09-01 |
| VANNES | 210 | 105 | 2018-01-01 | 2026-09-01 |
| ZURICH | 208 | 104 | 2018-01-01 | 2026-09-01 |

### Gares « parisiennes » et pseudo-gares

| gare |
|---|
| ITALIE |
| MARNE LA VALLEE |
| PARIS EST |
| PARIS LYON |
| PARIS MONTPARNASSE |
| PARIS NORD |
| PARIS VAUGIRARD |

### Liaisons présentes sous les deux services le même mois

| date | gare_depart | gare_arrivee | prevus_national | prevus_international | retards_national | retards_international |
|---|---|---|---|---|---|---|
| 2025-07-01 | BELLEGARDE (AIN) | PARIS LYON | 22 | 231 | 1 | 47 |
| 2025-08-01 | BELLEGARDE (AIN) | PARIS LYON | 25 | 228 | 2 | 26 |
| 2025-09-01 | BELLEGARDE (AIN) | PARIS LYON | 8 | 244 | 2 | 33 |
| 2025-07-01 | CHAMBERY CHALLES LES EAUX | PARIS LYON | 148 | 96 | 50 | 37 |
| 2025-08-01 | CHAMBERY CHALLES LES EAUX | PARIS LYON | 144 | 96 | 41 | 37 |
| 2025-09-01 | CHAMBERY CHALLES LES EAUX | PARIS LYON | 149 | 88 | 39 | 32 |
| 2025-07-01 | DIJON VILLE | PARIS LYON | 220 | 186 | 16 | 22 |
| 2025-08-01 | DIJON VILLE | PARIS LYON | 202 | 152 | 23 | 24 |
| 2025-09-01 | DIJON VILLE | PARIS LYON | 202 | 120 | 29 | 23 |
| 2025-07-01 | LYON PART DIEU | MARSEILLE ST CHARLES | 495 | 62 | 134 | 18 |
| 2025-08-01 | LYON PART DIEU | MARSEILLE ST CHARLES | 510 | 55 | 147 | 13 |
| 2025-09-01 | LYON PART DIEU | MARSEILLE ST CHARLES | 437 | 30 | 87 | 16 |
| 2025-07-01 | MACON LOCHE | PARIS LYON | 163 | 65 | 54 | 33 |
| 2025-08-01 | MACON LOCHE | PARIS LYON | 157 | 65 | 44 | 32 |
| 2025-09-01 | MACON LOCHE | PARIS LYON | 172 | 60 | 46 | 32 |
| 2025-07-01 | MARSEILLE ST CHARLES | LYON PART DIEU | 520 | 62 | 110 | 8 |
| 2025-08-01 | MARSEILLE ST CHARLES | LYON PART DIEU | 534 | 55 | 135 | 4 |
| 2025-09-01 | MARSEILLE ST CHARLES | LYON PART DIEU | 431 | 30 | 51 | 1 |
| 2025-07-01 | MULHOUSE VILLE | PARIS LYON | 136 | 196 | 12 | 22 |
| 2025-08-01 | MULHOUSE VILLE | PARIS LYON | 121 | 158 | 10 | 22 |
| 2025-09-01 | MULHOUSE VILLE | PARIS LYON | 124 | 143 | 15 | 20 |
| 2025-07-01 | PARIS EST | STRASBOURG | 352 | 252 | 58 | 36 |
| 2025-08-01 | PARIS EST | STRASBOURG | 336 | 237 | 30 | 18 |
| 2025-09-01 | PARIS EST | STRASBOURG | 420 | 232 | 30 | 17 |
| 2025-07-01 | PARIS LYON | BELLEGARDE (AIN) | 17 | 230 | 3 | 46 |
| 2025-08-01 | PARIS LYON | BELLEGARDE (AIN) | 21 | 230 | 2 | 29 |
| 2025-09-01 | PARIS LYON | BELLEGARDE (AIN) | 4 | 248 | 0 | 53 |
| 2025-07-01 | PARIS LYON | CHAMBERY CHALLES LES EAUX | 143 | 96 | 37 | 17 |
| 2025-08-01 | PARIS LYON | CHAMBERY CHALLES LES EAUX | 143 | 96 | 24 | 10 |
| 2025-09-01 | PARIS LYON | CHAMBERY CHALLES LES EAUX | 150 | 88 | 32 | 21 |
| 2025-07-01 | PARIS LYON | DIJON VILLE | 217 | 194 | 36 | 25 |
| 2025-08-01 | PARIS LYON | DIJON VILLE | 181 | 153 | 19 | 11 |
| 2025-09-01 | PARIS LYON | DIJON VILLE | 166 | 118 | 25 | 17 |
| 2025-07-01 | PARIS LYON | MACON LOCHE | 189 | 63 | 28 | 6 |
| 2025-08-01 | PARIS LYON | MACON LOCHE | 183 | 63 | 20 | 4 |
| 2025-09-01 | PARIS LYON | MACON LOCHE | 205 | 55 | 26 | 7 |
| 2025-07-01 | PARIS LYON | MULHOUSE VILLE | 131 | 193 | 27 | 33 |
| 2025-08-01 | PARIS LYON | MULHOUSE VILLE | 115 | 158 | 11 | 13 |
| 2025-09-01 | PARIS LYON | MULHOUSE VILLE | 124 | 142 | 19 | 19 |
| 2025-07-01 | STRASBOURG | PARIS EST | 338 | 252 | 56 | 91 |
| 2025-08-01 | STRASBOURG | PARIS EST | 313 | 242 | 42 | 71 |
| 2025-09-01 | STRASBOURG | PARIS EST | 408 | 233 | 35 | 68 |

### Volume habituel des liaisons Paris–Bellegarde/Mulhouse/Strasbourg autour de l'épisode jul.–sept. 2025

| gare_depart | gare_arrivee | date | prevus_nat | prevus_int | prevus_total |
|---|---|---|---|---|---|
| PARIS LYON | BELLEGARDE (AIN) | 2025-05-01 | 252 |  | 252 |
| PARIS LYON | BELLEGARDE (AIN) | 2025-06-01 | 237 |  | 237 |
| PARIS LYON | BELLEGARDE (AIN) | 2025-07-01 | 17 | 230 | 247 |
| PARIS LYON | BELLEGARDE (AIN) | 2025-08-01 | 21 | 230 | 251 |
| PARIS LYON | BELLEGARDE (AIN) | 2025-09-01 | 4 | 248 | 252 |
| PARIS LYON | BELLEGARDE (AIN) | 2025-10-01 | 264 |  | 264 |
| PARIS LYON | BELLEGARDE (AIN) | 2025-11-01 | 249 |  | 249 |
| PARIS LYON | MULHOUSE VILLE | 2025-05-01 | 326 |  | 326 |
| PARIS LYON | MULHOUSE VILLE | 2025-06-01 | 312 |  | 312 |
| PARIS LYON | MULHOUSE VILLE | 2025-07-01 | 131 | 193 | 324 |
| PARIS LYON | MULHOUSE VILLE | 2025-08-01 | 115 | 158 | 273 |
| PARIS LYON | MULHOUSE VILLE | 2025-09-01 | 124 | 142 | 266 |
| PARIS LYON | MULHOUSE VILLE | 2025-10-01 | 244 |  | 244 |
| PARIS LYON | MULHOUSE VILLE | 2025-11-01 | 259 |  | 259 |

## Valeurs manquantes et aberrantes

### Valeurs nulles par colonne

| date | service | gare_depart | gare_arrivee | duree_moyenne | nb_train_prevu | nb_annulation | commentaire_annulation | nb_train_depart_retard | retard_moyen_depart | retard_moyen_tous_trains_depart | commentaire_retards_depart | nb_train_retard_arrivee | retard_moyen_arrivee | retard_moyen_tous_trains_arrivee | commentaires_retard_arrivee | nb_train_retard_sup_15 | retard_moyen_trains_retard_sup15 | nb_train_retard_sup_30 | nb_train_retard_sup_60 | prct_cause_externe | prct_cause_infra | prct_cause_gestion_trafic | prct_cause_materiel_roulant | prct_cause_gestion_gare | prct_cause_prise_en_charge_voyageurs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 12907 | 0 | 0 | 0 | 12907 | 0 | 0 | 0 | 12209 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### Commentaires de retard à l'arrivée : nombre par année (seul champ commentaire renseigné)

| annee | avec_commentaire | lignes | mentionnant_greve |
|---|---|---|---|
| 2018 | 457 | 1560 | 30 |
| 2019 | 241 | 1476 | 0 |
| 2020 | 0 | 1476 | 0 |
| 2021 | 0 | 1449 | 0 |
| 2022 | 0 | 1467 | 0 |
| 2023 | 0 | 1446 | 0 |
| 2024 | 0 | 1450 | 0 |
| 2025 | 0 | 1494 | 0 |
| 2026 | 0 | 1089 | 0 |

### Exemple de commentaire (tronqué à 300 caractères)

| date | gare_depart | gare_arrivee | commentaire |
|---|---|---|---|
| 2018-01-01 | ANGOULEME | PARIS MONTPARNASSE | Ce mois-ci, l'OD a été touchée par les incidents suivants : Le 1er : Tempête Carmen sur la façade Atlantique  (52 TGV ; 1079mn) Le 3 : Tempête Eleonor sur l’ouest de la France (35 TGV ; 407mn) Le 5 : Dérangement d’une aiguille en gare de Massy TGV (57 TGV ; 1254mn) Le 7 : Dérangement du poste d’aigu |
| 2018-01-01 | ARRAS | PARIS NORD | Deux accidents de personne  se sont produits sur le secteur Nord, l’un à Fresnoy avec un train Eurostar le 16, et l’autre près de Lille Europe le 25 avec un train Ouigo.  Aussi en matière de causes retards, le domaine « Externe réseau » est bien le plus marquant avec quasiment cinq points, représent |
| 2018-01-01 | BORDEAUX ST JEAN | TOURCOING | 7660 du 7 +42: Dérangemetn d'insta MPW 7660 du 26 +68: Soin matériel roulant |

### Mois avec 0 train prévu

| date | liaisons | annulations_declarees | circules_negatifs |
|---|---|---|---|
| 2020-04-01 | 50 | 462 | 50 |
| 2020-05-01 | 9 | 17 | 9 |
| 2020-06-01 | 4 | 6 | 4 |
| 2020-08-01 | 2 | 0 | 0 |
| 2020-09-01 | 2 | 0 | 0 |
| 2020-10-01 | 2 | 0 | 0 |
| 2020-11-01 | 2 | 0 | 0 |
| 2020-12-01 | 2 | 0 | 0 |

### Bornes des grandeurs numériques

| duree_min | duree_max | prevus_min | prevus_max | retard_moyen_arr_min | retard_moyen_arr_max | moy_tous_min | moy_tous_max | sup30_min | sup30_negatifs | moy_tous_negatif |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 786 | 0 | 1104 | -40.11 | 299.6 | -472.64 | 92 | -44 | 43 | 122 |

### Lignes avec un retard moyen « tous trains » fortement négatif (avance ?)

| date | gare_depart | gare_arrivee | nb_train_prevu | nb_annulation | retard_moyen_tous_trains_arrivee |
|---|---|---|---|---|---|
| 2019-12-01 | STRASBOURG | NANTES | 10 | 4 | -472.64 |
| 2019-12-01 | LYON PART DIEU | MONTPELLIER | 75 | 20 | -173.08 |
| 2020-02-01 | PARIS EST | FRANCFORT | 165 | 7 | -163.04 |
| 2019-11-01 | NIMES | PARIS LYON | 226 | 11 | -151.29 |
| 2019-11-01 | MONTPELLIER | PARIS LYON | 227 | 11 | -150.56 |
| 2019-10-01 | NIMES | PARIS LYON | 266 | 12 | -90.63 |
| 2019-10-01 | MONTPELLIER | PARIS LYON | 263 | 12 | -80.86 |
| 2019-11-01 | VALENCE ALIXAN TGV | PARIS LYON | 233 | 11 | -71.53 |
| 2019-10-01 | VALENCE ALIXAN TGV | PARIS LYON | 265 | 11 | -68.93 |
| 2019-11-01 | PARIS LYON | MONTPELLIER | 138 | 15 | -15.19 |

## Seuils composites : vérification avec les comptes > 15 min

Pour un trajet > 3 h, le seuil « à l'heure » est 15 min : `nb_train_retard_arrivee` devrait alors égaler `nb_train_retard_sup_15`. Pour les trajets plus courts, il devrait lui être supérieur ou égal.

### Cohérence retard composite vs > 15 min, par tranche de durée moyenne

| tranche_duree | lignes | egal_sup15 | superieur | inferieur | retard_moyen_identique |
|---|---|---|---|---|---|
| 1. < 1h30 (seuil 5 min) | 2092 | 10 | 2082 | 0 | 6 |
| 2. 1h30–3h (seuil 10 min) | 5571 | 172 | 5393 | 6 | 114 |
| 3. > 3h (seuil 15 min) | 5171 | 4523 | 623 | 25 | 3038 |

## Gravité des retards (> 15 / > 30 / > 60 min)

### Hiérarchie retards ≥ >15 ≥ >30 ≥ >60, par année

| annee | lignes | sup15_lt_sup30 | sup30_lt_sup60 | sup30_negatif | retards | sup15 | sup30 | sup60 |
|---|---|---|---|---|---|---|---|---|
| 2018 | 1560 | 0 | 0 | 0 | 68199 | 46557 | 21351 | 7485 |
| 2019 | 1476 | 0 | 0 | 0 | 51012 | 35326 | 16530 | 6289 |
| 2020 | 1476 | 2 | 0 | 0 | 31079 | 20563 | 9226 | 2922 |
| 2021 | 1449 | 0 | 0 | 0 | 41341 | 30396 | 15028 | 5362 |
| 2022 | 1467 | 0 | 0 | 0 | 61739 | 45432 | 22232 | 8245 |
| 2023 | 1446 | 0 | 0 | 0 | 63119 | 46410 | 23048 | 9183 |
| 2024 | 1450 | 0 | 0 | 0 | 60218 | 43124 | 20556 | 8027 |
| 2025 | 1494 | 1 | 354 | 43 | 65412 | 49193 | 19928 | 13429 |
| 2026 | 1089 | 0 | 0 | 0 | 59638 | 45704 | 24130 | 9928 |

### Mois où la hiérarchie est rompue

| date | lignes | sup30_lt_sup60 | sup30_nul_ou_negatif | sup15 | sup30 | sup60 |
|---|---|---|---|---|---|---|
| 2025-01-01 | 121 | 118 | 117 | 3873 | -81 | 1882 |
| 2025-02-01 | 121 | 117 | 119 | 3106 | -74 | 1462 |
| 2025-03-01 | 121 | 119 | 111 | 3156 | -16 | 1586 |

### Exemple : Paris Montparnasse → Bordeaux, nov. 2024 – mai 2025

| date | retards | sup15 | sup30 | sup60 |
|---|---|---|---|---|
| 2024-11-01 | 126 | 90 | 43 | 17 |
| 2024-12-01 | 65 | 46 | 19 | 2 |
| 2025-01-01 | 162 | 124 | 0 | 55 |
| 2025-02-01 | 83 | 64 | 0 | 28 |
| 2025-03-01 | 93 | 52 | 0 | 21 |
| 2025-04-01 | 74 | 49 | 20 | 4 |
| 2025-05-01 | 79 | 57 | 32 | 12 |

### Part des trains circulés en retard > 15 / > 30 / > 60 min (hors janv.–mars 2025)

| pct_sup15 | pct_sup30 | pct_sup60 |
|---|---|---|
| 10.64 | 5.19 | 1.99 |

## Causes de retard

Les six colonnes `prct_cause_*` sont des pourcentages **des trains en retard à l'arrivée** (libellés du portail). Vérification de leur somme :

### Distribution de la somme des 6 pourcentages (arrondie)

| somme | lignes | dont_avec_retards |
|---|---|---|
| 100 | 12625 | 12625 |
| 0 | 272 | 80 |
| 98 | 4 | 4 |
| 99 | 3 | 3 |
| 85 | 1 | 1 |
| 87 | 1 | 1 |
| 88 | 1 | 1 |

### Lignes avec retards mais causes toutes à 0, par année

| annee | lignes | retards_concernes |
|---|---|---|
| 2018 | 66 | 1946 |
| 2019 | 2 | 24 |
| 2020 | 8 | 31 |
| 2023 | 1 | 1 |
| 2026 | 3 | 9 |

### Lignes avec retards mais causes à 0 : répartition par service (2018)

| service | count_star() |
|---|---|
| International | 65 |
| National | 1 |

### Répartition moyenne des causes, pondérée par le nombre de trains en retard, par année

| annee | externe | infra | gestion_trafic | materiel | gare | voyageurs |
|---|---|---|---|---|---|---|
| 2018 | 26.1 | 23.5 | 21.2 | 20.4 | 5.4 | 3.4 |
| 2019 | 25.1 | 23.7 | 23.2 | 18 | 6.3 | 3.7 |
| 2020 | 25.3 | 30 | 19.4 | 15.9 | 6.3 | 3.1 |
| 2021 | 25.2 | 19.1 | 15.2 | 16.2 | 8.6 | 15.7 |
| 2022 | 18.7 | 18 | 22.7 | 21.4 | 8.5 | 10.7 |
| 2023 | 16.6 | 20.9 | 23.2 | 20.3 | 9.6 | 9.4 |
| 2024 | 17.1 | 22.2 | 23.7 | 18.2 | 9 | 9.9 |
| 2025 | 19.8 | 21 | 24.5 | 17.7 | 9 | 8 |
| 2026 | 29.7 | 10.8 | 11.4 | 20.5 | 19.1 | 8.4 |

### Répartition mensuelle des causes depuis juin 2025 (rupture visible en mai 2026)

| date | externe | infra | gestion_trafic | materiel | gare | voyageurs |
|---|---|---|---|---|---|---|
| 2025-06-01 | 15.7 | 28.4 | 21.5 | 16.6 | 8.9 | 8.8 |
| 2025-07-01 | 19 | 20.1 | 25.8 | 18.6 | 9.1 | 7.4 |
| 2025-08-01 | 29.9 | 13.9 | 20.6 | 18 | 9.4 | 8.1 |
| 2025-09-01 | 22.2 | 26.9 | 20.9 | 16.3 | 7.2 | 6.5 |
| 2025-10-01 | 29 | 15.5 | 25.6 | 14.5 | 8.3 | 7.2 |
| 2025-11-01 | 19.5 | 16 | 26.7 | 20 | 11.3 | 6.4 |
| 2025-12-01 | 13 | 15 | 29.9 | 22.8 | 10.9 | 8.5 |
| 2026-01-01 | 32.6 | 16.6 | 21.9 | 16.5 | 7.7 | 4.7 |
| 2026-02-01 | 27.8 | 18.7 | 22.1 | 16.9 | 8 | 6.5 |
| 2026-03-01 | 23.8 | 18.7 | 25.8 | 18.1 | 7.5 | 6.2 |
| 2026-04-01 | 21.2 | 21.7 | 19.6 | 19.8 | 12 | 5.8 |
| 2026-05-01 | 34 | 5.9 | 5.7 | 24.7 | 20.9 | 8.8 |
| 2026-06-01 | 26.9 | 5.9 | 4.8 | 21.9 | 31.6 | 8.6 |
| 2026-07-01 | 34.7 | 5.8 | 3.6 | 19 | 27.4 | 9.6 |
| 2026-08-01 | 30.4 | 5.6 | 5 | 23.8 | 22.9 | 12.4 |
| 2026-09-01 | 31 | 6.8 | 4.5 | 23.3 | 22.8 | 11.6 |

### Granularité des pourcentages de causes (nb de valeurs distinctes, part des valeurs entières)

| distinctes | pct_entieres |
|---|---|
| 2759 | 22.4 |

## Prévus, annulés, circulés

Il n'y a pas de colonne « circulés » : on la calcule comme `prévus − annulés`. Les 73 lignes à 0 prévu avec annulations > 0 (avril–mai 2020) montrent que la convention n'est pas parfaitement tenue au plus fort du confinement.

### Totaux mensuels, service National (régularité recalculée sur circulés)

| date | prevus | annules | pct_annules | retards | regularite_recalculee |
|---|---|---|---|---|---|
| 2018-01-01 | 33273 | 238 | 0.7 | 4980 | 84.9 |
| 2018-02-01 | 30668 | 722 | 2.4 | 6645 | 77.8 |
| 2018-03-01 | 33602 | 904 | 2.7 | 4954 | 84.8 |
| 2018-04-01 | 34317 | 11283 | 32.9 | 3847 | 83.3 |
| 2018-05-01 | 34179 | 8564 | 25.1 | 4381 | 82.9 |
| 2018-06-01 | 34239 | 5267 | 15.4 | 5921 | 79.6 |
| 2018-07-01 | 33572 | 1899 | 5.7 | 8292 | 73.8 |
| 2018-08-01 | 31803 | 383 | 1.2 | 5328 | 83 |
| 2018-09-01 | 31352 | 156 | 0.5 | 4677 | 85 |
| 2018-10-01 | 31118 | 301 | 1 | 4971 | 83.9 |
| 2018-11-01 | 31756 | 342 | 1.1 | 5376 | 82.9 |
| 2018-12-01 | 31533 | 292 | 0.9 | 4702 | 84.9 |
| 2019-01-01 | 32265 | 446 | 1.4 | 4843 | 84.8 |
| 2019-02-01 | 29336 | 339 | 1.2 | 3430 | 88.2 |
| 2019-03-01 | 32303 | 334 | 1 | 3775 | 88.2 |
| 2019-04-01 | 30228 | 223 | 0.7 | 3346 | 88.8 |
| 2019-05-01 | 32108 | 648 | 2 | 3240 | 89.7 |
| 2019-06-01 | 31951 | 1128 | 3.5 | 5093 | 83.5 |
| 2019-07-01 | 33363 | 1526 | 4.6 | 5146 | 83.8 |
| 2019-08-01 | 30007 | 459 | 1.5 | 3747 | 87.3 |
| 2019-09-01 | 30666 | 282 | 0.9 | 3446 | 88.7 |
| 2019-10-01 | 30651 | 1008 | 3.3 | 5022 | 83.1 |
| 2019-11-01 | 28765 | 682 | 2.4 | 4557 | 83.8 |
| 2019-12-01 | 14609 | 2412 | 16.5 | 2151 | 82.4 |
| 2020-01-01 | 25235 | 1421 | 5.6 | 3601 | 84.9 |
| 2020-02-01 | 29153 | 302 | 1 | 3688 | 87.2 |
| 2020-03-01 | 19429 | 1893 | 9.7 | 2813 | 84 |
| 2020-04-01 | 3253 | 1931 | 59.4 | 548 | 68 |
| 2020-05-01 | 11745 | 1944 | 16.6 | 942 | 90.4 |
| 2020-06-01 | 21085 | 1257 | 6 | 1804 | 90.9 |
| 2020-07-01 | 28895 | 543 | 1.9 | 3365 | 88.1 |
| 2020-08-01 | 29017 | 272 | 0.9 | 3307 | 88.5 |
| 2020-09-01 | 29609 | 174 | 0.6 | 2903 | 90.1 |
| 2020-10-01 | 20329 | 344 | 1.7 | 3277 | 83.6 |
| 2020-11-01 | 9236 | 1511 | 16.4 | 1075 | 86.1 |
| 2020-12-01 | 23158 | 1474 | 6.4 | 2101 | 90.3 |
| 2021-01-01 | 28393 | 114 | 0.4 | 3510 | 87.6 |
| 2021-02-01 | 25261 | 218 | 0.9 | 2833 | 88.7 |
| 2021-03-01 | 26487 | 926 | 3.5 | 1721 | 93.3 |
| 2021-04-01 | 29892 | 11417 | 38.2 | 1117 | 94 |
| 2021-05-01 | 29713 | 1814 | 6.1 | 2671 | 90.4 |
| 2021-06-01 | 30447 | 40 | 0.1 | 3686 | 87.9 |
| 2021-07-01 | 33322 | 228 | 0.7 | 3954 | 88.1 |
| 2021-08-01 | 33468 | 36 | 0.1 | 3288 | 90.2 |
| 2021-09-01 | 31395 | 266 | 0.8 | 3644 | 88.3 |
| 2021-10-01 | 32244 | 375 | 1.2 | 4253 | 86.7 |
| 2021-11-01 | 31205 | 67 | 0.2 | 4770 | 84.7 |
| 2021-12-01 | 34104 | 569 | 1.7 | 4179 | 87.5 |
| 2022-01-01 | 33556 | 524 | 1.6 | 3094 | 90.6 |
| 2022-02-01 | 30608 | 230 | 0.8 | 2590 | 91.5 |
| 2022-03-01 | 34607 | 203 | 0.6 | 3694 | 89.3 |
| 2022-04-01 | 34799 | 81 | 0.2 | 4806 | 86.2 |
| 2022-05-01 | 35648 | 58 | 0.2 | 4503 | 87.3 |
| 2022-06-01 | 34845 | 189 | 0.5 | 6375 | 81.6 |
| 2022-07-01 | 36533 | 372 | 1 | 8646 | 76.1 |
| 2022-08-01 | 36281 | 88 | 0.2 | 6164 | 83 |
| 2022-09-01 | 34134 | 271 | 0.8 | 4023 | 88.1 |
| 2022-10-01 | 35232 | 266 | 0.8 | 5063 | 85.5 |
| 2022-11-01 | 33413 | 45 | 0.1 | 4204 | 87.4 |
| 2022-12-01 | 35849 | 4126 | 11.5 | 5055 | 84.1 |
| 2023-01-01 | 35558 | 1810 | 5.1 | 4255 | 87.4 |
| 2023-02-01 | 31709 | 1248 | 3.9 | 3337 | 89 |
| 2023-03-01 | 35753 | 8347 | 23.3 | 3638 | 86.7 |
| 2023-04-01 | 34544 | 1129 | 3.3 | 4748 | 85.8 |
| 2023-05-01 | 34868 | 344 | 1 | 4395 | 87.3 |
| 2023-06-01 | 35303 | 185 | 0.5 | 6192 | 82.4 |
| 2023-07-01 | 35766 | 90 | 0.3 | 5875 | 83.5 |
| 2023-08-01 | 36076 | 122 | 0.3 | 5580 | 84.5 |
| 2023-09-01 | 35866 | 135 | 0.4 | 5453 | 84.7 |
| 2023-10-01 | 36453 | 96 | 0.3 | 5440 | 85 |
| 2023-11-01 | 34593 | 660 | 1.9 | 5687 | 83.2 |
| 2023-12-01 | 36285 | 317 | 0.9 | 5209 | 85.5 |
| 2024-01-01 | 35733 | 325 | 0.9 | 5637 | 84.1 |
| 2024-02-01 | 33367 | 1514 | 4.5 | 3861 | 87.9 |
| 2024-03-01 | 35450 | 139 | 0.4 | 4813 | 86.4 |
| 2024-04-01 | 35305 | 49 | 0.1 | 4820 | 86.3 |
| 2024-05-01 | 35816 | 115 | 0.3 | 4187 | 88.3 |
| 2024-06-01 | 35550 | 150 | 0.4 | 4936 | 86.1 |
| 2024-07-01 | 36636 | 998 | 2.7 | 5839 | 83.6 |
| 2024-08-01 | 36125 | 136 | 0.4 | 4173 | 88.4 |
| 2024-09-01 | 35271 | 129 | 0.4 | 5057 | 85.6 |
| 2024-10-01 | 36384 | 149 | 0.4 | 4273 | 88.2 |
| 2024-11-01 | 32596 | 282 | 0.9 | 5343 | 83.5 |
| 2024-12-01 | 35322 | 206 | 0.6 | 4772 | 86.4 |
| 2025-01-01 | 35825 | 411 | 1.1 | 5147 | 85.5 |
| 2025-02-01 | 31878 | 305 | 1 | 4067 | 87.1 |
| 2025-03-01 | 35271 | 152 | 0.4 | 4036 | 88.5 |
| 2025-04-01 | 34587 | 252 | 0.7 | 3956 | 88.5 |
| 2025-05-01 | 34930 | 282 | 0.8 | 3773 | 89.1 |
| 2025-06-01 | 34544 | 131 | 0.4 | 5857 | 83 |
| 2025-07-01 | 33420 | 282 | 0.8 | 5789 | 82.5 |
| 2025-08-01 | 32842 | 169 | 0.5 | 5063 | 84.5 |
| 2025-09-01 | 32539 | 311 | 1 | 5034 | 84.4 |
| 2025-10-01 | 35507 | 301 | 0.8 | 5574 | 84.2 |
| 2025-11-01 | 33245 | 147 | 0.4 | 6184 | 81.3 |
| 2025-12-01 | 34549 | 132 | 0.4 | 5799 | 83.2 |
| 2026-01-01 | 34424 | 704 | 2 | 7540 | 77.6 |
| 2026-02-01 | 31160 | 412 | 1.3 | 4917 | 84 |
| 2026-03-01 | 34813 | 113 | 0.3 | 3777 | 89.1 |
| 2026-04-01 | 34902 | 137 | 0.4 | 5240 | 84.9 |
| 2026-05-01 | 33293 | 119 | 0.4 | 5987 | 82 |
| 2026-06-01 | 34660 | 1356 | 3.9 | 7818 | 76.5 |
| 2026-07-01 | 35760 | 763 | 2.1 | 8448 | 75.9 |
| 2026-08-01 | 35001 | 296 | 0.8 | 6888 | 80.2 |
| 2026-09-01 | 34175 | 174 | 0.5 | 5654 | 83.4 |

## Comparaison avec la régularité TGV globale officielle

La régularité « globale » publiée n'est pas la moyenne des liaisons (un train compte dans plusieurs liaisons, et le global inclut des trains absents du jeu par liaisons). On mesure l'écart.

### Écart régularité agrégée des liaisons (tous services) vs régularité globale publiée, par année

| annee | reg_liaisons_moy | reg_globale_moy | ecart_moyen | correlation |
|---|---|---|---|---|
| 2018 | 82.2 | 87.7 | -5.56 | 0.86 |
| 2019 | 86 | 90 | -4.05 | 0.87 |
| 2020 | 86 | 90.8 | -4.81 | 0.81 |
| 2021 | 89 | 90.6 | -1.62 | 1 |
| 2022 | 85.8 | 88 | -2.16 | 1 |
| 2023 | 85.4 | 87.5 | -2.14 | 0.99 |
| 2024 | 86.3 | 88.1 | -1.82 | 0.99 |
| 2025 | 85 | 86.6 | -1.61 | 0.97 |
| 2026 | 81.3 | 83.3 | -2.05 | 0.99 |

## Volumes par liaison-mois (utile pour le poids bayésien)

### Quantiles du nombre de trains circulés par liaison-mois (circulés > 0)

| quantiles | min(circules) | max(circules) | avg(circules) |
|---|---|---|---|
| [33.65000000000009, 67.0, 146.0, 225.0, 351.0, 520.0] | 1 | 1099 | 266.72 |

### Liaisons les moins fréquentées (moyenne de trains circulés par mois, 12 derniers mois)

| gare_depart | gare_arrivee | circules_par_mois |
|---|---|---|
| MARSEILLE ST CHARLES | TOURCOING | 22 |
| BORDEAUX ST JEAN | TOURCOING | 26 |
| TOURCOING | BORDEAUX ST JEAN | 27 |
| NANTES | STRASBOURG | 57 |
| STRASBOURG | NANTES | 57 |
| BARCELONA | PARIS LYON | 66 |
| PARIS LYON | BARCELONA | 67 |
| ITALIE | PARIS LYON | 76 |
| PARIS LYON | ITALIE | 76 |
| LYON PART DIEU | RENNES | 90 |

