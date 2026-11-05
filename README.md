# Le classement des liaisons ferroviaires

Site statique (à venir) sur la **régularité des trains en France** à partir des données open data SNCF : un
classement des liaisons TGV et Intercités avec un score de fiabilité pondéré façon bayésienne, une fiche par liaison
(historique, causes, gravité des retards), les tendances, une page « Mon trajet » et des statistiques globales.
Publication prévue sur GitHub Pages, sans backend.

## État d'avancement

| Phase | Contenu | État |
|---|---|---|
| 1 | Exploration des données : [`docs/DATA.md`](docs/DATA.md) | fait |
| 2 | Proposition de plan : [`docs/PLAN.md`](docs/PLAN.md) | **en attente de validation** |
| 3+ | Pipeline de production, site, GitHub Action | pas commencé |

## Reproduire l'exploration

Prérequis : Python 3.11 ou plus récent.

```bash
python -m venv .venv && source .venv/bin/activate
```

```bash
pip install -r pipeline/requirements.txt
```

```bash
python pipeline/download.py
```

`download.py` interroge l'API Explore v2.1 du portail [ressources.data.sncf.com](https://ressources.data.sncf.com)
et écrit dans `data/raw/` (non versionné, ≈ 10 Mo) l'export Parquet, l'export CSV et les métadonnées de chaque jeu.
Les connexions coupées sont retentées automatiquement. On peut ne télécharger qu'un jeu :
`python pipeline/download.py tgv_aqst` (clés : `tgv_aqst`, `tgv_axes`, `tgv_national`, `intercites`, `ter`,
`gares_voyageurs`, `liste_gares`, `temps_parcours`, `frequentation_gares`).

Puis lancer les scripts d'exploration, chacun écrivant un rapport Markdown dans `pipeline/explore/sorties/` :

```bash
for f in pipeline/explore/0*.py; do python "$f" > /dev/null; done
```

| Script | Contenu |
|---|---|
| `01_tgv_liaisons.py` | TGV par liaisons : colonnes, couverture, liaisons, anomalies, gravité, causes |
| `02_intercites.py` | Intercités : libellés, doublons, cohérence |
| `03_ter.py` | TER par région : libellés, incohérences, commentaires |
| `04_gares.py` | rattachement des gares au référentiel et aux régions |
| `05_evenements.py` | grèves, COVID, transfert Normandie, saisonnalité |
| `06_score_variantes.py` | calibrage bayésien et variantes du score (phase 2) |
| `07_tendances_mon_trajet.py` | essais des tendances et de « Mon trajet » (phase 2) |
| `08_tgv_axes_national.py` | TGV par axe et TGV global |

## Organisation

```
pipeline/
  download.py         téléchargement des jeux SNCF (API Opendatasoft)
  requirements.txt
  explore/            scripts d'exploration DuckDB et leurs rapports (sorties/)
docs/
  DATA.md             description des données, qualité, pièges, faisabilité
  PLAN.md             proposition de plan (score, modèle de données, pages, CI)
data/raw/             données téléchargées (non versionné)
```

## Sources et licence des données

Données : **SNCF Voyageurs** (régularité mensuelle TGV par liaisons, par axe et globale ; Intercités ; TER),
**SNCF Gares & Connexions** (gares de voyageurs), **SNCF Réseau** (liste des gares), via
[ressources.data.sncf.com](https://ressources.data.sncf.com), sous licence
[Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/1-0/). Les données dérivées que publiera
le site seront diffusées sous la même licence.
