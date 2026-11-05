# Phase 2 — essais tendances et « Mon trajet »

_Généré par `pipeline/explore/07_tendances_mon_trajet.py`._

## 1. Tendances : 12 derniers mois vs 12 mois précédents (liaisons non orientées)

### Répartition des liaisons selon |z| (seuil proposé : |z| ≥ 2 et |Δ| ≥ 2 points)

| type | liaisons | amelioration_significative | degradation_significative | stable_ou_incertain | significatif_mais_faible |
|---|---|---|---|---|---|
| TGV | 61 | 0 | 29 | 32 | 0 |
| Intercités | 18 | 0 | 4 | 14 | 1 |

### Tendance relative : Δ liaison − Δ du type (le réseau entier a pu bouger)

| type | delta_type_pts | liaisons | mieux_que_le_reseau | pire_que_le_reseau |
|---|---|---|---|---|
| TGV | -4.2 | 61 | 1 | 0 |
| Intercités | -3 | 18 | 0 | 0 |

### Plus fortes améliorations (TGV)

| liaison | trains_12m | reg_avant | reg_12m | delta_pts | z |
|---|---|---|---|---|---|
| LILLE – LYON PART DIEU | 8502 | 77.3 | 77.6 | 0.3 | 0.2 |
| PARIS EST – REIMS | 5246 | 89.8 | 89.2 | -0.6 | -0.3 |
| PARIS LYON – SAINT ETIENNE CHATEAUCREUX | 2688 | 84 | 82.6 | -1.3 | -0.4 |
| PARIS LYON – ZURICH | 2883 | 89.5 | 88 | -1.5 | -0.6 |
| PARIS MONTPARNASSE – ST MALO | 2465 | 89.1 | 87.3 | -1.8 | -0.6 |
| PARIS MONTPARNASSE – TOURS | 3712 | 85.6 | 83.6 | -2 | -0.8 |
| BORDEAUX ST JEAN – TOURCOING | 634 | 86.1 | 83.9 | -2.2 | -0.4 |
| LYON PART DIEU – MONTPELLIER | 5335 | 79.2 | 77 | -2.2 | -0.9 |

### Plus fortes dégradations (TGV)

| liaison | trains_12m | reg_avant | reg_12m | delta_pts | z |
|---|---|---|---|---|---|
| PARIS EST – STUTTGART | 3050 | 69.5 | 59.4 | -10.1 | -2.7 |
| ITALIE – PARIS LYON | 1819 | 77.6 | 69.3 | -8.3 | -1.7 |
| DOUAI – PARIS NORD | 3391 | 82 | 74 | -8 | -2.6 |
| FRANCFORT – PARIS EST | 4456 | 78.5 | 70.7 | -7.9 | -2.7 |
| ARRAS – PARIS NORD | 10884 | 83.7 | 76.5 | -7.2 | -4.4 |
| NICE VILLE – PARIS LYON | 5081 | 82.3 | 75.7 | -6.6 | -2.7 |
| NANTES – STRASBOURG | 1363 | 89.6 | 83.3 | -6.3 | -1.6 |
| CHAMBERY CHALLES LES EAUX – PARIS LYON | 6155 | 77.4 | 71.3 | -6.1 | -2.5 |

### Intercités : toutes les liaisons

| liaison | trains_12m | reg_avant | reg_12m | delta_pts | z |
|---|---|---|---|---|---|
| ALBI/RODEZ – PARIS-AUSTERLITZ | 301 | 78.3 | 83.1 | 4.8 | 1 |
| AURILLAC – PARIS-AUSTERLITZ | 546 | 84.2 | 86.1 | 1.9 | 0.5 |
| BRIANÇON – PARIS-AUSTERLITZ | 482 | 66.6 | 67.4 | 0.8 | 0.2 |
| NICE-VILLE – PARIS-AUSTERLITZ | 612 | 73.1 | 73 | -0.1 | -0 |
| PARIS-AUSTERLITZ – RODEZ/ALBI | 303 | 95.1 | 94.7 | -0.4 | -0.1 |
| BORDEAUX-ST-JEAN – NANTES | 2828 | 86.5 | 84.9 | -1.7 | -1.2 |
| HENDAYE – TOULOUSE-MATABIAU | 2700 | 87.6 | 85.9 | -1.7 | -1.2 |
| PARIS-AUSTERLITZ – TOULOUSE-MATABIAU | 2256 | 87.9 | 86 | -1.9 | -1.3 |
| CLERMONT-FERRAND – PARIS-BERCY | 5098 | 90.2 | 88.3 | -1.9 | -2 |
| PARIS-AUSTERLITZ – TARBES | 441 | 89.7 | 87.1 | -2.6 | -0.8 |
| LYON – NANCY | 731 | 91 | 88.1 | -3 | -1 |
| BÉZIERS – CLERMONT-FERRAND | 725 | 96.4 | 93.1 | -3.3 | -1.9 |
| CAHORS/BRIVE – PARIS-AUSTERLITZ | 2186 | 90.3 | 86.5 | -3.9 | -2.7 |
| BRIVE/CAHORS – PARIS-AUSTERLITZ | 1967 | 90.6 | 86.5 | -4 | -2.7 |
| CERBERE – PARIS-AUSTERLITZ | 336 | 85.6 | 81 | -4.6 | -1.1 |
| LATOUR-DE-CAROL – PARIS-AUSTERLITZ | 292 | 89 | 84.2 | -4.8 | -1.2 |
| BORDEAUX-ST-JEAN – MARSEILLE-ST-CHARLES | 4632 | 69.6 | 64.6 | -5 | -3.4 |
| LYON – NANTES | 2022 | 84.7 | 78.8 | -5.9 | -3.2 |

Remarque : les liaisons Intercités sont ici orientées-fusionnées sans normaliser les libellés composites (« ALBI/RODEZ » et « RODEZ/ALBI » restent séparés) ; le pipeline de production normalisera.

## 2. Pente sur 36 mois (régression du taux mensuel désaisonnalisé) — exemple TGV

### Effet saisonnier moyen (points de régularité vs moyenne de l'année)

| mois | tgv | intercites |
|---|---|---|
| 1 | 0.8 | 1.7 |
| 2 | 1.6 | 1 |
| 3 | 2.5 | 3.4 |
| 4 | 1.9 | 1.8 |
| 5 | 2.1 | 0.6 |
| 6 | -2.4 | -2.6 |
| 7 | -4.1 | -2.5 |
| 8 | 0.1 | 0.7 |
| 9 | 0.6 | 2.2 |
| 10 | -0.4 | -0.6 |
| 11 | -1.8 | -4 |
| 12 | -0.8 | -1.6 |

### Pente (points / an) sur 36 mois, désaisonnalisée — 5 plus fortes hausses et baisses TGV

| sens | liaison | pts_par_an | r2 | n |
|---|---|---|---|---|
| hausse | LILLE – LYON PART DIEU | 0.7 | 0.02 | 36 |
| hausse | PARIS EST – REIMS | 0.6 | 0.02 | 36 |
| hausse | PARIS MONTPARNASSE – ST MALO | -0.1 | 0 | 36 |
| hausse | BREST – PARIS MONTPARNASSE | -0.2 | 0.01 | 36 |
| hausse | BORDEAUX ST JEAN – TOURCOING | -0.3 | 0 | 36 |
| baisse | ITALIE – PARIS LYON | -8.8 | 0.6 | 32 |
| baisse | PARIS EST – STUTTGART | -7.7 | 0.21 | 36 |
| baisse | FRANCFORT – PARIS EST | -4.6 | 0.21 | 36 |
| baisse | MACON LOCHE – PARIS LYON | -3.9 | 0.47 | 36 |
| baisse | BARCELONA – PARIS LYON | -3.7 | 0.32 | 36 |

## 3. « Mon trajet » : exemples

Probabilité qu'un **train prévu** arrive à l'heure (annulé = pas à l'heure), sens choisi, mois calendaire choisi. On prend ce mois sur les 5 dernières années disponibles hors 2020. Prior bêta centré sur (niveau de la liaison sur 24 mois + effet saisonnier), de force m = 60 trains effectifs (cf. 06). Intervalle de crédibilité à 80 %. On donne aussi la dispersion d'une année sur l'autre, qui est la vraie incertitude pour un voyage futur.

_Quantiles bêta approchés par une loi normale de même moyenne et variance (pas de `qbeta` natif dans DuckDB)._

### TGV PARIS MONTPARNASSE → TOULOUSE MATABIAU, mois 7

| trajet | mois | annees_liste | trains_prevus_obs | D | prior_pct | proba_pct | ic80_bas | ic80_haut | pire_annee | meilleure_annee |
|---|---|---|---|---|---|---|---|---|---|---|
| PARIS MONTPARNASSE → TOULOUSE MATABIAU | 7 | 2026,2025,2024,2023,2022 | 1086 | 9.4 | 76.6 | 77.5 | 73.5 | 81.6 | 70.4 | 86.9 |

### TGV PARIS MONTPARNASSE → TOULOUSE MATABIAU, mois 10

| trajet | mois | annees_liste | trains_prevus_obs | D | prior_pct | proba_pct | ic80_bas | ic80_haut | pire_annee | meilleure_annee |
|---|---|---|---|---|---|---|---|---|---|---|
| PARIS MONTPARNASSE → TOULOUSE MATABIAU | 10 | 2025,2024,2023,2022,2021 | 1099 | 9.4 | 80.3 | 82.5 | 78.9 | 86.2 | 80.2 | 87.2 |

### TGV PARIS EST → REIMS, mois 12

| trajet | mois | annees_liste | trains_prevus_obs | D | prior_pct | proba_pct | ic80_bas | ic80_haut | pire_annee | meilleure_annee |
|---|---|---|---|---|---|---|---|---|---|---|
| PARIS EST → REIMS | 12 | 2025,2024,2023,2022,2021 | 1117 | 9.4 | 88.6 | 88 | 84.9 | 91.1 | 76.5 | 95 |

### TGV MARSEILLE ST CHARLES → TOURCOING, mois 8

| trajet | mois | annees_liste | trains_prevus_obs | D | prior_pct | proba_pct | ic80_bas | ic80_haut | pire_annee | meilleure_annee |
|---|---|---|---|---|---|---|---|---|---|---|
| MARSEILLE ST CHARLES → TOURCOING | 8 | 2026,2025,2024,2023,2022 | 156 | 9.4 | 78.1 | 76.8 | 70.6 | 82.9 | 50 | 83.9 |

### TGV PARIS LYON → BARCELONA, mois 7

| trajet | mois | annees_liste | trains_prevus_obs | D | prior_pct | proba_pct | ic80_bas | ic80_haut | pire_annee | meilleure_annee |
|---|---|---|---|---|---|---|---|---|---|---|
| PARIS LYON → BARCELONA | 7 | 2026,2025,2024,2023,2022 | 415 | 9.4 | 81 | 77 | 71.8 | 82.3 | 53.2 | 85.2 |

### Intercités PARIS-AUSTERLITZ → BRIANÇON, mois 2

| trajet | mois | annees_liste | trains_prevus_obs | D | prior_pct | proba_pct | ic80_bas | ic80_haut | pire_annee | meilleure_annee |
|---|---|---|---|---|---|---|---|---|---|---|
| PARIS-AUSTERLITZ → BRIANÇON | 2 | 2026,2025,2024,2023,2022 | 129 | 2.3 | 65.2 | 56.9 | 51 | 62.8 | 10.3 | 75 |

### Intercités BORDEAUX-ST-JEAN → MARSEILLE-ST-CHARLES, mois 7

| trajet | mois | annees_liste | trains_prevus_obs | D | prior_pct | proba_pct | ic80_bas | ic80_haut | pire_annee | meilleure_annee |
|---|---|---|---|---|---|---|---|---|---|---|
| BORDEAUX-ST-JEAN → MARSEILLE-ST-CHARLES | 7 | 2025,2024,2023,2022,2021 | 1095 | 2.3 | 62.8 | 60.3 | 57.6 | 63 | 45.6 | 73.3 |

## 4. Variabilité d'une année sur l'autre pour un même trajet et un même mois

### Écart-type inter-annuel de la probabilité d'être à l'heure (trajet orienté × mois calendaire, ≥ 4 années hors 2020, ≥ 50 trains/mois)

| type | cellules | sd_mediane_pts | sd_q90_pts | sd_binomiale_mediane_pts |
|---|---|---|---|---|
| TGV | 1414 | 6.7 | 13.3 | 2.4 |
| Intercités | 565 | 5.4 | 9.7 | 2.9 |

