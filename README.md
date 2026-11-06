# Le classement des liaisons ferroviaires

Site statique sur la **régularité des trains en France** à partir des données open data SNCF :
un classement des liaisons TGV et Intercités avec un score de fiabilité pondéré façon bayésienne, une fiche par
liaison (historique, causes, gravité des retards), les tendances, une page « Mon trajet » et des statistiques
globales. Publié sur GitHub Pages, sans backend : **https://clement-duffau.github.io/sncf_tracking/**

## État d'avancement

| Étape | Contenu | État |
|---|---|---|
| Phase 1 | Exploration des données : [`docs/DATA.md`](docs/DATA.md) | fait |
| Phase 2 | Plan : [`docs/PLAN.md`](docs/PLAN.md) | validé |
| 1 | Pipeline de production, tests, `data/events.yaml` | fait |
| 2 | Site : classement, filtres, méthodologie ; déploiement Pages | fait |
| 3 | Fiche liaison | fait |
| 4 | Mon trajet | à faire |
| 5 | Tendances, Statistiques, périodes libres | à faire |
| 6 | Régions TER (v2), finitions | à faire |

## Démarrage rapide

Prérequis : Python 3.11+ et Node.js 20+.

```bash
python -m venv .venv && source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
python -m pipeline build
```

```bash
cd site && npm install && npm run dev
```

`python -m pipeline build` télécharge les jeux SNCF (≈ 5 Mo, avec reprises automatiques si la connexion est
coupée) dans `data/raw/`, vérifie leur format, calcule les scores, tendances et probabilités « Mon trajet », puis
écrit les fichiers du site dans `site/public/data/` (une dizaine de secondes une fois les fichiers téléchargés).

### Commandes du pipeline

| Commande | Effet |
|---|---|
| `python -m pipeline build` | télécharge les données et produit `site/public/data/` |
| `python -m pipeline build --hors-ligne` | réutilise `data/raw/` sans réseau |
| `python -m pipeline build --sans-lock` | ne met pas à jour `data/sources.lock.json` |
| `python -m pipeline verifier` | indique si un jeu a été republié depuis le dernier build (pour la GitHub Action) |
| `python -m pytest -q tests` | tests du pipeline sur un mini-jeu synthétique |
| `python pipeline/download.py` | télécharge aussi les jeux annexes utilisés par l'exploration |
| `python pipeline/explore/01_tgv_liaisons.py` (… `08`) | régénère un rapport d'exploration dans `pipeline/explore/sorties/` |

### Commandes du site (`site/`)

| Commande | Effet |
|---|---|
| `npm run dev` | serveur de développement (lit `site/public/data/`, produit par le pipeline) |
| `npm run check` | vérification des types (svelte-check) |
| `npm test` | tests unitaires (Vitest : classement, filtres, formats, fiche, égalité du score avec le pipeline) |
| `npm run build` | site statique dans `site/dist/` |

Un build **échoue avec un message explicite** si une source change de format (colonne absente ou de type
différent), si le nombre de lignes baisse de plus de 5 % ou si le dernier mois publié recule par rapport à
`data/sources.lock.json`, si les causes de retard ne somment plus à 100 %, ou si une gare n'est pas rattachée au
référentiel (il faut alors l'ajouter dans `pipeline/refs/gares_alias.csv`). Les mois anormaux qu'aucune entrée de
`data/events.yaml` ne couvre sont signalés en avertissement.

## Architecture

```
pipeline/                 Python + DuckDB
  config.py               chemins, jeux de données, paramètres de la méthode (M, D, barème, seuils)
  fetch.py                API Explore v2.1 du portail SNCF : métadonnées et exports, avec reprises
  schemas.py              colonnes et types attendus de chaque jeu
  load.py                 vues DuckDB sur data/raw/
  checks.py               contrôles de cohérence, data/sources.lock.json
  events.py               lecture et validation de data/events.yaml, mois anormaux non annotés
  gares.py                rattachement des libellés au référentiel « Gares de voyageurs », régions
  clean.py                liaisons non orientées, mesures mensuelles par sens (fusion des services,
                          libellés Intercités composites, gravité invalide, causes en nombre de trains)
  score.py                score V2, rétrécissement bayésien, intervalle à 80 %, rangs par période
  trends.py               tendances (absolue et relative au réseau), saisonnalité, pentes, « Mon trajet »
  export.py               fichiers JSON du site et CSV ouverts
  refs/                   departements.csv, gares_alias.csv, gares_etrangeres.csv (relus à la main)
  explore/                scripts et rapports d'exploration (phases 1 et 2)
data/
  events.yaml             grèves, COVID, ruptures de séries (versionné, sourcé)
  sources.lock.json       date de publication et volume de chaque jeu au dernier build (versionné)
  raw/                    données téléchargées (non versionné)
site/                     Vite + Svelte 5 + TypeScript, sans backend
  src/pages/              Classement, fiche liaison, Méthodologie et sources
  src/lib/classement.ts   lignes d'une période, filtres, tris, « coude à coude » (testé par Vitest)
  src/lib/fiche.ts        fiche : fusion des sens, issues et causes par année, export CSV (testé par Vitest)
  src/lib/score.ts        score V2, même formule que le pipeline (vérifié par Vitest sur les valeurs exportées)
  src/lib/charts/         SVG faits main : barre de score « voie », courbes, barres segmentées, mois de l'année
  src/lib/carte/          petite carte de situation (contour IGN Admin Express simplifié, Licence Ouverte)
  src/lib/router.svelte.ts routeur par hash ; filtres reflétés dans l'URL (#/?type=TGV&periode=2025&region=Bretagne)
tests/                    pytest
docs/                     DATA.md (exploration), PLAN.md (plan validé)
.github/workflows/        ci.yml (tests + build), deploy.yml (données hebdomadaires + Pages)
```

### Fichiers produits (`site/public/data/`, non versionnés)

| Fichier | Contenu | Taille (brut / gzip) |
|---|---|---|
| `meta.json` | dates des données, fenêtres « 12 derniers mois », périodes, paramètres du score | 4 Ko / 1 Ko |
| `classement.json` | liaisons (identité, régions, tendance, courbe des 12 derniers mois) et scores par type × période | 135 Ko / 31 Ko |
| `mensuel-tgv.json`, `mensuel-intercites.json` | comptes par liaison × sens × mois, en colonnes (périodes libres, statistiques) | 580 Ko / 140 Ko et 120 Ko / 17 Ko |
| `liaison/<id>.json` | fiche : séries par sens, scores, causes, gravité, saisonnalité, tendance, « Mon trajet » (112 fiches) | ≈ 16 Ko / 4–6 Ko chacune |
| `stats.json` | séries nationales (TGV officiel et par axe, totaux TGV, Intercités, TER), causes TGV, saisonnalité | 38 Ko / 14 Ko |
| `gares.json` | gares desservies avec région, coordonnées et liaisons | 15 Ko / 3 Ko |
| `evenements.json` | événements de `data/events.yaml` | 10 Ko / 3 Ko |
| `donnees/*.csv` | export ouvert (ODbL) : mesures mensuelles, scores, liaisons, gares, « Mon trajet » | ≈ 3 Mo |

## Déploiement

1. Dans le dépôt GitHub : *Settings → Pages → Build and deployment → Source : **GitHub Actions***.
2. Le workflow `deploy.yml` s'exécute à chaque push sur `main`, chaque lundi à 6 h 17 UTC et à la demande
   (onglet *Actions*). Le passage du lundi s'arrête tôt si la SNCF n'a rien republié depuis le dernier build ;
   sinon il reconstruit les données, enregistre `data/sources.lock.json` sur `main` et publie le site.
3. Si une source change de format, le build échoue avec un message explicite et le site déjà publié reste en place.

## Méthode en bref

Détails et justification chiffrée dans [`docs/PLAN.md`](docs/PLAN.md).

- **Unité** : liaison non orientée (A→B et B→A fusionnés), services National et International additionnés.
- **Score** : note moyenne d'un train prévu sur 100 (à l'heure 100, retard ≤ 30 min 67, 30–60 min 33,
  > 60 min ou annulé 0). Pour les Intercités, la gravité n'est pas publiée : leurs retards sont répartis comme la
  moyenne TGV de la même période.
- **Rétrécissement bayésien** : chaque taux est tiré vers la moyenne du type, avec un poids de 560 trains (TGV)
  ou 60 trains (Intercités), environ un mois d'une liaison médiane.
- **Grèves** : comptées dans le score, exclues des tendances, de la saisonnalité et de « Mon trajet ».

## Sources et licence des données

Données : **SNCF Voyageurs** (régularité mensuelle TGV par liaisons, par axe et globale ; Intercités ; TER) et
**SNCF Gares & Connexions** (gares de voyageurs), via [ressources.data.sncf.com](https://ressources.data.sncf.com),
sous licence [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/1-0/). Les données dérivées
produites par le pipeline (`site/public/data/`, dont `donnees/*.csv`) sont diffusées sous la même licence.

Contour de la France de la petite carte : [france-geojson](https://github.com/gregoiredavid/france-geojson),
d'après Admin Express (IGN), Licence Ouverte Etalab.

Code : licence [MIT](LICENSE).
