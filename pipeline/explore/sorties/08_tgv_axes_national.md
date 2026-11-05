# Exploration — TGV par axe et TGV global

_Généré par `pipeline/explore/08_tgv_axes_national.py`._

## Régularité mensuelle TGV par axe (tgv_axes)

- Licence : Open Database License (ODbL)
- Dernière modification des données : 2026-10-02T10:06:13+00:00
- Enregistrements : 835
- Champs : `date` (date), `axe` (text), `regularite_composite` (double), `ponctualite_origine` (double)

## Régularité mensuelle TGV globale (tgv_national)

- Licence : Open Database License (ODbL)
- Dernière modification des données : 2026-10-02T10:03:46+00:00
- Enregistrements : 141
- Champs : `date` (date), `regularite_composite` (double), `ponctualite_origine` (double)

### TGV par axe : couverture par axe

| axe | mois | premier | dernier | reg_moy | reg_null | ponct_null |
|---|---|---|---|---|---|---|
| Atlantique | 141 | 2015-01-01 | 2026-09-01 | 88.7 | 0 | 0 |
| Est | 141 | 2015-01-01 | 2026-09-01 | 90.6 | 0 | 0 |
| Europe | 141 | 2015-01-01 | 2026-09-01 | 87 | 0 | 0 |
| Nord | 141 | 2015-01-01 | 2026-09-01 | 88.3 | 0 | 0 |
| OUIGO | 130 | 2015-12-01 | 2026-09-01 | 87.7 | 1 | 1 |
| Sud-Est | 141 | 2015-01-01 | 2026-09-01 | 88.2 | 0 | 0 |

### TGV par axe : régularité sur les 12 derniers mois (moyenne simple des mois)

| axe | reg | ponct_origine |
|---|---|---|
| Atlantique | 87.1 | 84.2 |
| Est | 84.2 | 75.8 |
| OUIGO | 83.6 | 78.5 |
| Sud-Est | 83.3 | 82.4 |
| Nord | 81.9 | 78.9 |
| Europe | 76.5 | 56.1 |

### TGV global : couverture

| premier | dernier | mois | attendus | reg_min | reg_max |
|---|---|---|---|---|---|
| 2015-01-01 | 2026-09-01 | 141 | 141 | 77.85 | 94.56 |

### TGV global : moyenne annuelle (moyenne simple des mois)

| annee | regularite | ponctualite_origine | mois |
|---|---|---|---|
| 2015 | 90.4 | 84.4 | 12 |
| 2016 | 89.5 | 83.6 | 12 |
| 2017 | 88.7 | 81.9 | 12 |
| 2018 | 87.7 | 80.7 | 12 |
| 2019 | 90 | 85.1 | 12 |
| 2020 | 90.8 | 86.6 | 12 |
| 2021 | 90.6 | 86.7 | 12 |
| 2022 | 88 | 81.3 | 12 |
| 2023 | 87.5 | 80.9 | 12 |
| 2024 | 88.1 | 83.4 | 12 |
| 2025 | 86.6 | 82.1 | 12 |
| 2026 | 83.3 | 78.1 | 9 |

