# Phase 2 — calibrage et variantes du score de fiabilité

_Généré par `pipeline/explore/06_score_variantes.py`._

## Fenêtre d'évaluation : 12 derniers mois disponibles par type

### Fenêtres

| type | debut | fin |
|---|---|---|
| Intercités | 2025-06-01 | 2026-05-01 |
| TGV | 2025-10-01 | 2026-09-01 |

## 1. Surdispersion : les trains d'une même liaison ne sont pas indépendants

Pour chaque liaison, on compare la variance observée du taux mensuel à la variance qu'aurait un tirage binomial (trains indépendants) : D = variance observée / variance binomiale. Calcul sur les 24 derniers mois, liaisons-mois d'au moins 20 trains circulés.

### Facteur de surdispersion D par type et métrique

| type | metrique | liaisons | D_mediane | D_q25 | D_q75 |
|---|---|---|---|---|---|
| Intercités | annulation | 16 | 3.23 | 1.76 | 4.52 |
| Intercités | retard | 16 | 2.3 | 1.53 | 5.43 |
| TGV | annulation | 61 | 7.35 | 4.46 | 14.91 |
| TGV | retard | 61 | 9.43 | 5.88 | 14.63 |
| TGV | retard > 30 min | 61 | 11.68 | 7.69 | 16.84 |

## 2. Force du prior par Bayes empirique (méthode des moments)

Sur la fenêtre de 12 mois : variance inter-liaisons observée des taux = variance « vraie » τ² + bruit d'échantillonnage (μ(1−μ)·D/n). Pour une loi bêta de moyenne μ et de variance τ², la concentration vaut m = μ(1−μ)/τ² − 1 (en trains « effectifs »). En trains réels : M = m·D.

### Prior par type et métrique

| type | metrique | mu_pct | liaisons | D | tau_pct | m_eff | M_trains |
|---|---|---|---|---|---|---|---|
| Intercités | annulation | 1.78 | 16 | 3.2 | 1.65 | 63 | 203 |
| Intercités | retard | 17.98 | 16 | 2.3 | 7.68 | 24 | 55 |
| TGV | annulation | 1.16 | 61 | 7.4 | 0.78 | 190 | 1394 |
| TGV | retard | 18.38 | 61 | 9.4 | 4.98 | 60 | 561 |
| TGV | retard > 30 min | 7.33 | 61 | 11.7 | 2.92 | 78 | 916 |
| TGV | retard > 60 min | 3.03 | 61 | 11.7 | 1.13 | 229 | 2669 |

### Ordre de grandeur : trains circulés par liaison et par mois (médiane, fenêtre de 12 mois)

| type | mediane_circules_par_mois | min_par_mois | max_par_mois |
|---|---|---|---|
| TGV | 483 | 21.83 | 2036.83 |
| Intercités | 60.67 | 28 | 424.83 |

### M retenu (arrondi à la dizaine) — appliqué à toutes les composantes d'un type

| type | M |
|---|---|
| Intercités | 60 |
| TGV | 560 |

## 3. Classements TGV sur 12 mois — variantes calculables

### TGV — V1 : haut du classement

| rang | liaison | circules | regularite_brute | annul_brut | g30_brut | V1 | V2 | V3 |
|---|---|---|---|---|---|---|---|---|
| 1 | PARIS EST – REIMS | 5246 | 89.2 | 0.19 | 3.3 | 88.2 | 94.2 | 99.2 |
| 2 | BREST – PARIS MONTPARNASSE | 6488 | 89.6 | 2.08 | 5.1 | 87.1 | 92 | 72.9 |
| 3 | LYON PART DIEU – PARIS LYON | 15112 | 86.8 | 0.36 | 5.4 | 86.3 | 92.6 | 90.8 |
| 4 | NANCY – PARIS EST | 6526 | 87 | 0.38 | 5 | 86.2 | 92.7 | 90 |
| 5 | PARIS LYON – ZURICH | 2883 | 88 | 1.23 | 6.3 | 85.9 | 91.5 | 74.2 |
| 6 | DIJON VILLE – PARIS LYON | 8465 | 86.8 | 0.68 | 5.9 | 85.9 | 91.9 | 81.3 |
| 7 | LAUSANNE – PARIS LYON | 2331 | 87.8 | 1.4 | 6 | 85.4 | 91.2 | 71.7 |
| 8 | PARIS MONTPARNASSE – ST MALO | 2465 | 87.3 | 1.2 | 4.6 | 85.2 | 92 | 75.4 |
| 9 | BESANCON FRANCHE COMTE TGV – PARIS LYON | 3626 | 86.6 | 1.04 | 6.4 | 85 | 91.1 | 71.7 |
| 10 | LYON PART DIEU – RENNES | 2206 | 86.4 | 0.41 | 6.6 | 85 | 91.4 | 77.1 |

### TGV — V1 : bas du classement

| rang | liaison | circules | regularite_brute | annul_brut | g30_brut | V1 | V2 | V3 |
|---|---|---|---|---|---|---|---|---|
| 61 | PARIS EST – STUTTGART | 3050 | 59.4 | 3.3 | 16.7 | 61 | 78.7 | 0.8 |
| 60 | FRANCFORT – PARIS EST | 4456 | 70.7 | 3.03 | 14.7 | 69.9 | 82.1 | 3.3 |
| 59 | ITALIE – PARIS LYON | 1819 | 69.3 | 0.55 | 16.7 | 71.7 | 83.3 | 22.1 |
| 58 | CHAMBERY CHALLES LES EAUX – PARIS LYON | 6155 | 71.3 | 0.37 | 10.9 | 71.9 | 85.6 | 30 |
| 57 | DOUAI – PARIS NORD | 3391 | 74 | 2.95 | 4.7 | 73 | 87 | 28.3 |
| 56 | LYON PART DIEU – MARNE LA VALLEE | 9011 | 73.4 | 0.73 | 8.8 | 73.4 | 86.7 | 30.4 |
| 55 | ARRAS – PARIS NORD | 10884 | 76.5 | 2.85 | 4.3 | 74.7 | 87.8 | 33.3 |
| 54 | MARNE LA VALLEE – MARSEILLE ST CHARLES | 6435 | 75.3 | 1.3 | 12.3 | 74.8 | 85.1 | 15.8 |
| 53 | NICE VILLE – PARIS LYON | 5081 | 75.7 | 1.51 | 14.7 | 75.2 | 84 | 13.7 |
| 52 | LILLE – MARSEILLE ST CHARLES | 5342 | 75.6 | 1.13 | 12.1 | 75.3 | 85.5 | 20.4 |

### TGV — V2 : haut du classement

| rang | liaison | circules | regularite_brute | annul_brut | g30_brut | V1 | V2 | V3 |
|---|---|---|---|---|---|---|---|---|
| 1 | PARIS EST – REIMS | 5246 | 89.2 | 0.19 | 3.3 | 88.2 | 94.2 | 99.2 |
| 2 | NANCY – PARIS EST | 6526 | 87 | 0.38 | 5 | 86.2 | 92.7 | 90 |
| 3 | LYON PART DIEU – PARIS LYON | 15112 | 86.8 | 0.36 | 5.4 | 86.3 | 92.6 | 90.8 |
| 4 | LE CREUSOT MONTCEAU MONTCHANIN – PARIS LYON | 4802 | 83.8 | 0.25 | 4.1 | 83.2 | 92.2 | 81.7 |
| 5 | BREST – PARIS MONTPARNASSE | 6488 | 89.6 | 2.08 | 5.1 | 87.1 | 92 | 72.9 |
| 6 | PARIS MONTPARNASSE – ST MALO | 2465 | 87.3 | 1.2 | 4.6 | 85.2 | 92 | 75.4 |
| 7 | DIJON VILLE – PARIS LYON | 8465 | 86.8 | 0.68 | 5.9 | 85.9 | 91.9 | 81.3 |
| 8 | PARIS LYON – ZURICH | 2883 | 88 | 1.23 | 6.3 | 85.9 | 91.5 | 74.2 |
| 9 | PARIS MONTPARNASSE – RENNES | 19636 | 83.9 | 0.91 | 4.9 | 83 | 91.5 | 74.2 |
| 10 | LYON PART DIEU – RENNES | 2206 | 86.4 | 0.41 | 6.6 | 85 | 91.4 | 77.1 |

### TGV — V2 : bas du classement

| rang | liaison | circules | regularite_brute | annul_brut | g30_brut | V1 | V2 | V3 |
|---|---|---|---|---|---|---|---|---|
| 61 | PARIS EST – STUTTGART | 3050 | 59.4 | 3.3 | 16.7 | 61 | 78.7 | 0.8 |
| 60 | FRANCFORT – PARIS EST | 4456 | 70.7 | 3.03 | 14.7 | 69.9 | 82.1 | 3.3 |
| 59 | ITALIE – PARIS LYON | 1819 | 69.3 | 0.55 | 16.7 | 71.7 | 83.3 | 22.1 |
| 58 | NICE VILLE – PARIS LYON | 5081 | 75.7 | 1.51 | 14.7 | 75.2 | 84 | 13.7 |
| 57 | MARNE LA VALLEE – MARSEILLE ST CHARLES | 6435 | 75.3 | 1.3 | 12.3 | 74.8 | 85.1 | 15.8 |
| 56 | LILLE – MARSEILLE ST CHARLES | 5342 | 75.6 | 1.13 | 12.1 | 75.3 | 85.5 | 20.4 |
| 55 | CHAMBERY CHALLES LES EAUX – PARIS LYON | 6155 | 71.3 | 0.37 | 10.9 | 71.9 | 85.6 | 30 |
| 54 | PARIS LYON – TOULON | 6346 | 78.8 | 0.77 | 13.3 | 78.4 | 86.1 | 30.4 |
| 53 | PARIS MONTPARNASSE – TOULOUSE MATABIAU | 4768 | 80.5 | 1.99 | 12.2 | 79.1 | 86.2 | 22.9 |
| 52 | LYON PART DIEU – MARNE LA VALLEE | 9011 | 73.4 | 0.73 | 8.8 | 73.4 | 86.7 | 30.4 |

### TGV — V3 : haut du classement

| rang | liaison | circules | regularite_brute | annul_brut | g30_brut | V1 | V2 | V3 |
|---|---|---|---|---|---|---|---|---|
| 1 | PARIS EST – REIMS | 5246 | 89.2 | 0.19 | 3.3 | 88.2 | 94.2 | 99.2 |
| 2 | LYON PART DIEU – PARIS LYON | 15112 | 86.8 | 0.36 | 5.4 | 86.3 | 92.6 | 90.8 |
| 3 | NANCY – PARIS EST | 6526 | 87 | 0.38 | 5 | 86.2 | 92.7 | 90 |
| 4 | LE CREUSOT MONTCEAU MONTCHANIN – PARIS LYON | 4802 | 83.8 | 0.25 | 4.1 | 83.2 | 92.2 | 81.7 |
| 5 | DIJON VILLE – PARIS LYON | 8465 | 86.8 | 0.68 | 5.9 | 85.9 | 91.9 | 81.3 |
| 6 | LYON PART DIEU – RENNES | 2206 | 86.4 | 0.41 | 6.6 | 85 | 91.4 | 77.1 |
| 7 | PARIS MONTPARNASSE – ST MALO | 2465 | 87.3 | 1.2 | 4.6 | 85.2 | 92 | 75.4 |
| 8 | PARIS LYON – ZURICH | 2883 | 88 | 1.23 | 6.3 | 85.9 | 91.5 | 74.2 |
| 9 | PARIS MONTPARNASSE – RENNES | 19636 | 83.9 | 0.91 | 4.9 | 83 | 91.5 | 74.2 |
| 10 | BREST – PARIS MONTPARNASSE | 6488 | 89.6 | 2.08 | 5.1 | 87.1 | 92 | 72.9 |

### TGV — V3 : bas du classement

| rang | liaison | circules | regularite_brute | annul_brut | g30_brut | V1 | V2 | V3 |
|---|---|---|---|---|---|---|---|---|
| 61 | PARIS EST – STUTTGART | 3050 | 59.4 | 3.3 | 16.7 | 61 | 78.7 | 0.8 |
| 60 | FRANCFORT – PARIS EST | 4456 | 70.7 | 3.03 | 14.7 | 69.9 | 82.1 | 3.3 |
| 59 | NICE VILLE – PARIS LYON | 5081 | 75.7 | 1.51 | 14.7 | 75.2 | 84 | 13.7 |
| 58 | MARNE LA VALLEE – MARSEILLE ST CHARLES | 6435 | 75.3 | 1.3 | 12.3 | 74.8 | 85.1 | 15.8 |
| 57 | LILLE – MARSEILLE ST CHARLES | 5342 | 75.6 | 1.13 | 12.1 | 75.3 | 85.5 | 20.4 |
| 56 | ITALIE – PARIS LYON | 1819 | 69.3 | 0.55 | 16.7 | 71.7 | 83.3 | 22.1 |
| 55 | PARIS MONTPARNASSE – TOULOUSE MATABIAU | 4768 | 80.5 | 1.99 | 12.2 | 79.1 | 86.2 | 22.9 |
| 54 | MARSEILLE ST CHARLES – TOURCOING | 262 | 76.7 | 2.6 | 13 | 78.8 | 87.5 | 26.7 |
| 53 | PARIS LYON – PERPIGNAN | 4923 | 80.5 | 1.42 | 11.4 | 79.5 | 86.8 | 27.9 |
| 52 | DOUAI – PARIS NORD | 3391 | 74 | 2.95 | 4.7 | 73 | 87 | 28.3 |

## 3. Classements Intercités sur 12 mois — variantes calculables

### Intercités — V1 : haut du classement

| rang | liaison | circules | regularite_brute | annul_brut | V1 | V1_sans_lissage |
|---|---|---|---|---|---|---|
| 1 | BÉZIERS – CLERMONT-FERRAND | 725 | 93.1 | 0.68 | 91.5 | 92.5 |
| 2 | CLERMONT-FERRAND – PARIS-BERCY | 5098 | 88.3 | 1.09 | 87.3 | 87.4 |
| 3 | LYON – NANCY | 731 | 88.1 | 0.27 | 87.3 | 87.9 |
| 4 | BRIVE/CAHORS – PARIS-AUSTERLITZ | 4153 | 86.5 | 0.72 | 85.8 | 85.9 |
| 5 | PARIS-AUSTERLITZ – TOULOUSE-MATABIAU | 2256 | 86 | 1.1 | 84.9 | 85.1 |
| 6 | ALBI/RODEZ – PARIS-AUSTERLITZ | 604 | 88.9 | 5.03 | 84.1 | 84.4 |
| 7 | HENDAYE – TOULOUSE-MATABIAU | 2700 | 85.9 | 2.24 | 83.9 | 83.9 |
| 8 | BORDEAUX-ST-JEAN – NANTES | 2828 | 84.9 | 1.36 | 83.6 | 83.7 |
| 9 | PARIS-AUSTERLITZ – TARBES | 441 | 87.1 | 4.13 | 83.1 | 83.5 |
| 10 | LATOUR-DE-CAROL – PARIS-AUSTERLITZ | 292 | 84.2 | 1.02 | 82.9 | 83.4 |
| 11 | AURILLAC – PARIS-AUSTERLITZ | 546 | 86.1 | 7.14 | 80 | 79.9 |
| 12 | CERBERE – PARIS-AUSTERLITZ | 336 | 81 | 1.47 | 79.9 | 79.8 |
| 13 | LYON – NANTES | 2022 | 78.8 | 1.37 | 77.8 | 77.8 |
| 14 | NICE-VILLE – PARIS-AUSTERLITZ | 612 | 73 | 2.86 | 71.8 | 71 |
| 15 | BRIANÇON – PARIS-AUSTERLITZ | 482 | 67.4 | 1.43 | 68 | 66.5 |
| 16 | BORDEAUX-ST-JEAN – MARSEILLE-ST-CHARLES | 4632 | 64.6 | 2.97 | 62.9 | 62.7 |

## 4. Concordance des variantes (TGV, corrélation de rang de Spearman)

### Corrélations entre variantes

| V1_V2 | V1_V3 | V2_V3 | regularite_brute_V1 |
|---|---|---|---|
| 0.91 | 0.96 | 0.96 | 0.97 |

### Plus grands écarts de rang entre V1 et V2 (TGV)

| liaison | rang_V1 | rang_V2 | rang_V3 | regularite_brute | annul_brut | g30_brut |
|---|---|---|---|---|---|---|
| LILLE – PARIS NORD | 39 | 18 | 35 | 81.6 | 1.82 | 3.6 |
| MARSEILLE ST CHARLES – PARIS LYON | 13 | 31 | 15 | 84.1 | 0.7 | 9.3 |
| AIX EN PROVENCE TGV – PARIS LYON | 19 | 35 | 26 | 83.1 | 0.79 | 9.5 |
| MONTPELLIER – PARIS LYON | 26 | 39 | 32 | 81.8 | 0.48 | 10.5 |
| LE MANS – PARIS MONTPARNASSE | 34 | 22 | 28 | 81.7 | 1.25 | 5.1 |
| ARRAS – PARIS NORD | 55 | 43 | 47 | 76.5 | 2.85 | 4.3 |
| PARIS MONTPARNASSE – ST PIERRE DES CORPS | 25 | 14 | 20 | 82.6 | 1.4 | 4.1 |
| NANTES – STRASBOURG | 22 | 33 | 28 | 83.3 | 1.16 | 8.7 |

## 5. Effet du lissage sur un mois isolé (petites liaisons)

Sur un seul mois, une petite liaison (≈ 20–60 trains) peut afficher une régularité extrême par hasard. On compare le classement brut et lissé (V1) du dernier mois TGV.

### Dernier mois TGV — top 8 brut

| rang_brut | liaison | circules | regularite_brute | V1_brut | V1_lisse |
|---|---|---|---|---|---|
| 1 | LYON PART DIEU – PARIS LYON | 1257 | 91.5 | 91.4 | 88.1 |
| 2 | BREST – PARIS MONTPARNASSE | 569 | 91.4 | 91.2 | 86 |
| 3 | BARCELONA – PARIS LYON | 132 | 90.9 | 90.9 | 82.6 |
| 4 | LAUSANNE – PARIS LYON | 142 | 90.8 | 90.8 | 82.7 |
| 5 | PARIS MONTPARNASSE – ST MALO | 195 | 90.8 | 90.8 | 83.3 |
| 6 | LYON PART DIEU – RENNES | 180 | 89.4 | 89.4 | 82.8 |
| 7 | NANTES – PARIS MONTPARNASSE | 1228 | 88.9 | 88.8 | 86.2 |
| 8 | PARIS MONTPARNASSE – QUIMPER | 523 | 88.5 | 88.5 | 84.4 |

### Dernier mois TGV — top 8 lissé

| rang_lisse | liaison | circules | regularite_brute | V1_brut | V1_lisse |
|---|---|---|---|---|---|
| 1 | LYON PART DIEU – PARIS LYON | 1257 | 91.5 | 91.4 | 88.1 |
| 2 | NANTES – PARIS MONTPARNASSE | 1228 | 88.9 | 88.8 | 86.2 |
| 3 | BREST – PARIS MONTPARNASSE | 569 | 91.4 | 91.2 | 86 |
| 4 | PARIS MONTPARNASSE – RENNES | 1720 | 87.4 | 87.4 | 85.7 |
| 5 | MARSEILLE ST CHARLES – PARIS LYON | 1099 | 87.6 | 87.6 | 85.3 |
| 6 | AIX EN PROVENCE TGV – PARIS LYON | 928 | 87.6 | 87.3 | 84.8 |
| 7 | ANGERS SAINT LAUD – PARIS MONTPARNASSE | 1086 | 87.1 | 86.9 | 84.8 |
| 8 | PARIS LYON – VALENCE ALIXAN TGV | 760 | 87.4 | 87.3 | 84.4 |

### Dernier mois TGV — 8 derniers lissé

| liaison | circules | regularite_brute | V1_brut | V1_lisse |
|---|---|---|---|---|
| ARRAS – PARIS NORD | 866 | 71.5 | 70.3 | 74.4 |
| LYON PART DIEU – MARNE LA VALLEE | 736 | 73 | 71.7 | 75.6 |
| DOUAI – PARIS NORD | 282 | 67.4 | 66.2 | 75.8 |
| PARIS EST – STUTTGART | 199 | 63.3 | 63 | 76.1 |
| LILLE – LYON PART DIEU | 699 | 74.7 | 73.2 | 76.5 |
| LILLE – PARIS NORD | 1200 | 75.7 | 74.7 | 76.6 |
| LYON PART DIEU – MONTPELLIER | 417 | 73.6 | 72.7 | 77.3 |
| LILLE – MARSEILLE ST CHARLES | 450 | 74.9 | 73.7 | 77.6 |

## 6. Sensibilité au choix de M (TGV, V2, 12 mois)

### Rang des 3 liaisons les moins fréquentées et du 1er / dernier selon M (×0, ×1, ×3, ×10)

| liaison | r0 | r1 | r3 | r10 | circules |
|---|---|---|---|---|---|
| PARIS EST – REIMS | 1 | 1 | 1 | 1 | 5246 |
| NANTES – STRASBOURG | 35 | 33 | 33 | 33 | 1363 |
| MARSEILLE ST CHARLES – TOURCOING | 57 | 46 | 40 | 37 | 262 |
| BORDEAUX ST JEAN – TOURCOING | 53 | 48 | 42 | 39 | 634 |
| PARIS EST – STUTTGART | 61 | 61 | 61 | 61 | 3050 |

