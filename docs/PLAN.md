# Plan — « Le classement des liaisons ferroviaires » (phase 2)

Ce plan s'appuie sur l'exploration décrite dans [`DATA.md`](DATA.md). Les chiffres cités viennent des rapports
`pipeline/explore/sorties/06_score_variantes.md` (score) et `07_tendances_mon_trajet.md` (tendances, « Mon trajet »),
calculés sur les données du 5 novembre 2026.

> **Statut : plan validé avec les recommandations (5 novembre 2026).** Étape 1 (pipeline de production, tests,
> `data/events.yaml`) réalisée ; voir « Mise en œuvre » ci-dessous pour les précisions apportées en cours de route.

### Mise en œuvre de l'étape 1 : précisions et écarts

- **Gares** : aucune correspondance automatique approximative en production. Seules l'égalité des noms normalisés,
  `pipeline/refs/gares_alias.csv` (22 libellés relus) et `gares_etrangeres.csv` (8) sont utilisées ; un libellé
  inconnu fait échouer le build avec des candidats suggérés.
- **Paris-Vaugirard** reste une gare distincte (même code UIC que Montparnasse, mais ses 622 trains de 2018 vers
  Bordeaux s'ajoutaient à ceux de Montparnasse, qui ne les a pas absorbés en 2019 : fusionner créerait une marche).
- **Lille, Montpellier** (TGV) et **Lyon** (Intercités depuis 2018) sont rattachés à la ville (`precision: ville`),
  la gare exacte n'étant pas connue ; la région n'en dépend pas.
- **Gravité imputée des Intercités** : parts TGV des mêmes mois ; avant 2018 (pas de données TGV par liaison),
  parts TGV de tout l'historique.
- **Couverture partielle** : moins de 6 mois de données dans la période (ou moins que la durée de la période si
  elle est plus courte).
- **« Mon trajet »** est calculé pour les liaisons ayant des données dans les 24 derniers mois du type.
- **Tendance du réseau** : −3,7 points pour le TGV (et non −4,2 comme dans l'essai de phase 2), car la grève de
  juin 2026 est maintenant exclue des tendances ; 27 liaisons TGV « en dégradation » en absolu, une seule se
  distingue du réseau.
- **Mois anormaux non annotés** (signalés à chaque build, faute de source fiable sur leur cause) : Intercités
  décembre 2017 (programmés −20,6 % à périmètre constant) et TGV juillet 2018 (5,4 % d'annulations, fin de la grève
  du printemps ?). À compléter dans `data/events.yaml` si une source est trouvée.
- **Étape 3 (fiche liaison)** : les causes sont montrées en barres empilées par année (plutôt qu'en aires), l'année
  2026 coupée en deux à la rupture de nomenclature ; la saisonnalité et « Mon trajet » condensé sont réunis dans
  un seul graphique (probabilité d'arriver à l'heure pour chaque mois, avec la fourchette d'une année sur l'autre).
  Les couleurs des graphiques sont validées par script (daltonisme, contrastes) dans les deux thèmes ; les trois
  niveaux de retard forment une rampe ordinale d'une seule teinte.
- **Question 8 tranchée** : code sous licence MIT, site à l'URL par défaut https://clement-duffau.github.io/sncf_tracking/.

## Sommaire

1. [Périmètre recommandé](#1-périmètre-recommandé)
2. [Modèle de données](#2-modèle-de-données)
3. [Score de fiabilité](#3-score-de-fiabilité)
4. [Périodes et filtres](#4-périodes-et-filtres)
5. [Tendances et saisonnalité](#5-tendances-et-saisonnalité)
6. [« Mon trajet »](#6-mon-trajet)
7. [Grèves et événements : `data/events.yaml`](#7-grèves-et-événements--dataeventsyaml)
8. [Pages, composants, design](#8-pages-composants-design)
9. [GitHub Actions](#9-github-actions)
10. [Méthodologie, sources, ODbL](#10-méthodologie-sources-odbl)
11. [Découpage en étapes](#11-découpage-en-étapes)
12. [Questions ouvertes](#12-questions-ouvertes)

---

## 1. Périmètre recommandé

| Type | Recommandation | Justification (DATA.md) |
|---|---|---|
| **TGV** (national + international SNCF) | **v1, cœur du site** | 61 liaisons non orientées actives, 105 mois sans trou, régularité + annulations + gravité + causes |
| **Intercités** | **v1**, classement séparé (onglet), vue « Tous » possible | Même seuil de retard que le TGV ; 16 liaisons actives, historique depuis 2014 ; pas de causes ni de gravité ; annulations non comparables |
| **TER** | **v2** : page « Régions TER » à part, jamais mélangée aux liaisons | Agrégé par région, seuil fixe de 5 min, historique cassé par la réforme territoriale, 3 lots non régionaux depuis 2025 |
| Transilien | Hors périmètre | Comme demandé |

Les liaisons **historiques** (Normandie avant 2020, Madrid, Paris-Vaugirard, Intercités supprimés…) restent
consultables dans « Tout l'historique » et sur leur fiche, mais n'apparaissent pas dans le classement des
12 derniers mois.

**Unité du classement : la liaison non orientée** (Paris – Toulouse). A→B et B→A sont fusionnés pour le score ;
la fiche montre chaque sens, et « Mon trajet » travaille toujours dans le sens choisi. Pour le TGV, les services
National et International sont sommés (épisode juillet–septembre 2025, reclassement de Barcelone).

## 2. Modèle de données

### Pipeline (Python + DuckDB, sur le modèle de l'Atlas des antennes)

```
pipeline/
  __main__.py      python -m pipeline build [--offline] [--force]
  fetch.py         API Explore v2.1 : métadonnées (data_processed, schéma) + exports Parquet, avec reprises
  schemas.py       schéma attendu de chaque jeu (noms et types) → échec explicite si une source change
  load.py          vues DuckDB sur data/raw/*.parquet
  gares.py         normalisation des libellés, rattachement au référentiel, régions
  clean.py         fusion des sens et des services, normalisation Intercités, drapeaux de qualité
  score.py         prior, rétrécissement bayésien, scores par période
  trends.py        tendances, saisonnalité, « Mon trajet »
  events.py        lecture et validation de data/events.yaml
  export.py        fichiers JSON du site
  refs/
    gares_alias.csv        libellé source → id de gare (les ~10 cas manuels : Valence Alixan, Vaugirard, Lille…)
    gares_etrangeres.csv   gares étrangères et pseudo-gares : pays, coordonnées saisies à la main
    departements.csv       département → région (COG INSEE)
tests/             pytest sur un mini-jeu synthétique (fusion des sens, Intercités, prior, anomalies)
```

### Tables DuckDB (en mémoire, non versionnées)

| Table | Grain | Colonnes principales |
|---|---|---|
| `gare` | gare | `id` (slug), `nom` affiché, `nom_referentiel`, `uic`, `lat`, `lon`, `region`, `pays` |
| `liaison` | liaison non orientée × type | `id` (`paris-montparnasse--toulouse-matabiau`), `type`, `gare_a`, `gare_b` (ordre alphabétique), `regions[]`, `international`, `duree_min` moyenne, `premier_mois`, `dernier_mois`, `active` |
| `mesure` | liaison × sens × mois | `prevus`, `annules`, `circules`, `retards`, `sup15`, `sup30`, `sup60` (NULL si inexploitable), `cause_*` en **nombre de trains** (= % × retards), `nomenclature_causes` (`v1` avant mai 2026, `v2` après), drapeaux `gravite_ok`, `causes_ok` |
| `contexte` | type × mois | régularité TGV globale et par axe (officielles), totaux Intercités, totaux TER |
| `evenement` | événement | issu de `data/events.yaml` |
| `prior` | type × période × composante | `mu`, `M` |
| `score` | liaison × période | composantes brutes et lissées, score, rang, intervalle |
| `trajet` | liaison × sens × mois calendaire | probabilité, intervalle, années utilisées |

### Fichiers produits (`site/public/data/`, non versionnés, reconstruits par la CI)

| Fichier | Contenu | Taille estimée (brut / gzip) | Chargement |
|---|---|---|---|
| `meta.json` | dates de données (`data_processed`), fenêtres par type, paramètres du score (μ, M), version de méthode | 3 Ko / 1 Ko | au démarrage |
| `classement.json` | liaisons (id, libellés, type, régions, durée) + scores précalculés pour les périodes standard (12 mois, chaque année, tout l'historique) : score, intervalle, régularité, annulations, > 30 min, trains, tendance, sparkline 12 mois | ≈ 80 Ko / 20 Ko | au démarrage |
| `mensuel-tgv.json`, `mensuel-intercites.json` | comptes par liaison × sens × mois, **en colonnes** (gares en dictionnaire) : ce qu'il faut pour recalculer n'importe quelle période ou n'importe quel mois dans le navigateur | mesuré : 990 Ko / 176 Ko pour l'ensemble (dont ≈ 85 % TGV) | à la demande (mois précis, période libre, page Statistiques) |
| `liaison/<id>.json` | fiche : séries par sens, causes, gravité, saisonnalité, tendance, table « Mon trajet » (12 mois × 2 sens), événements touchant la liaison | mesuré : 19 Ko / 3 Ko | au clic |
| `stats.json` | séries nationales officielles, axes, Intercités, causes agrégées, distribution des scores, records | ≈ 60 Ko / 15 Ko | page Statistiques |
| `gares.json` | gares desservies (nom, région, coordonnées) pour la recherche et « Mon trajet » | ≈ 8 Ko / 3 Ko | au démarrage |
| `evenements.json` | événements annotés | ≈ 5 Ko | au démarrage |
| `donnees/*.csv` | export ouvert des tables dérivées (ODbL) | ≈ 1,5 Mo | téléchargement |
| `regions-ter.json` (v2) | régions TER × mois | ≈ 60 Ko / 12 Ko | page Régions |

Premier affichage sur mobile : HTML + JS (≈ 40 Ko gzip, graphiques SVG faits main comme l'Atlas) + `classement.json`
+ `meta.json` + `gares.json` ≈ **70 Ko gzip**. Les comptes mensuels ne sont chargés que si l'on quitte les périodes
standard.

## 3. Score de fiabilité

### Composantes (par liaison et par période, sens fusionnés)

| Composante | Définition | Disponible |
|---|---|---|
| R : retard | trains en retard (seuil composite 5/10/15 min) / trains circulés | TGV, Intercités |
| A : annulation | trains annulés / trains prévus (programmés pour Intercités) | TGV, Intercités (définitions différentes) |
| G30, G60 : gravité | trains > 30 min / > 60 min de retard / trains circulés | TGV seulement ; manquante en janv.–mars 2025 |

### Rétrécissement bayésien

Chaque taux est lissé vers la moyenne de son type de train, sur la **même période** :

```
taux lissé = (x + M · μ) / (n + M)
```

- `x` = nombre d'événements (retards, annulations…), `n` = trains concernés (circulés ou prévus) ;
- `μ` = taux moyen du type (TGV ou Intercités) sur la période (somme des événements / somme des trains) ;
- `M` = poids du prior, **en trains**.

**Choix de M (Bayes empirique corrigé de la surdispersion, → 06).** Les retards d'un même mois sont fortement
corrélés (une panne, une canicule touchent tous les trains) : la variance mensuelle observée est **9,4 fois** la
variance binomiale pour le TGV (2,3 pour les Intercités). On mesure ce facteur D, puis on estime la dispersion « vraie »
entre liaisons τ² par la méthode des moments, et la force du prior vaut m = μ(1−μ)/τ² − 1 en trains « effectifs »,
soit **M = m · D** en trains réels :

| Type | μ retard (12 mois) | D | τ (écart entre liaisons) | M (trains) | Repère |
|---|---|---|---|---|---|
| TGV | 18,4 % | 9,4 | 5,0 pts | **≈ 560** | ≈ 1,2 mois d'une liaison médiane (483 trains/mois) |
| Intercités | 18,0 % | 2,3 | 7,7 pts | **≈ 60** | ≈ 1 mois d'une liaison médiane (61 trains/mois) |

Effet concret : sur 12 mois, une liaison médiane (≈ 5 800 trains) n'est rétrécie que de 9 % vers la moyenne ; sur un
seul mois, Barcelone – Paris (132 trains, 90,9 % brut) descend à 82,6 % et sort du top 8, alors que Lyon – Paris
(1 257 trains) reste premier (→ 06, § 5). Sur 12 mois, entre M = 0 et M = 560, les deux liaisons de Tourcoing
(≈ 22–27 trains par mois et par sens) gagnent 11 et 5 places, Nantes – Strasbourg (57) en gagne 2 ; le premier et
le dernier ne bougent pas (→ 06, § 6).

On applique le même M à toutes les composantes d'un type (les M estimés séparément vont de 560 à 2 670 trains pour
le TGV ; un seul M est plus simple à expliquer, et l'effet sur le classement est faible). **M est figé dans
`pipeline/config.py`** et recalibré une fois par an par le script 06, pour que les scores ne bougent pas à cause de
l'estimation elle-même.

### Formule recommandée : V2, « note moyenne d'un train prévu »

Chaque train prévu reçoit des points, et le score est la moyenne sur 100 :

| Issue du train | Points |
|---|---|
| à l'heure | 100 |
| en retard, au plus 30 min | 67 |
| en retard de 30 à 60 min | 33 |
| en retard de plus de 60 min | 0 |
| annulé | 0 |

```
score = 100 − 100/3 · [ (1−Ã) · ( (R̃−G̃30)·1 + (G̃30−G̃60)·2 + G̃60·3 ) + Ã·3 ]
```

(composantes lissées, notées ~). Avantages : une seule échelle, lisible (« un train annulé compte comme un retard
de plus d'une heure »), qui combine les trois dimensions sans pondérations arbitraires entre taux d'ordres de
grandeur très différents (1 % d'annulations contre 18 % de retards).

**Intercités (pas de gravité)** : leurs trains en retard sont répartis comme la moyenne TGV de la même période
(39,9 % de plus de 30 min et 16,5 % de plus de 60 min **parmi les trains en retard**, → 06 § 3 bis). Cela revient à
les classer sur les retards et les annulations, sur la même échelle que le TGV. La fiche l'indique (« gravité non
publiée, estimée »). Dans la vue « Tous types », un avertissement rappelle que les annulations Intercités ne
comptent pas les suppressions annoncées la veille.

### Variantes comparées (TGV, 12 mois oct. 2025 – sept. 2026, liaisons non orientées)

- **V1, « probabilité d'arriver à l'heure »** = (1 − Ã)·(1 − R̃). Simple, c'est exactement la quantité de « Mon trajet »,
  mais ignore la gravité.
- **V2, « note moyenne d'un train prévu »** (recommandée), ci-dessus.
- **V3, « centiles pondérés »** = 50 % rang-centile de R̃ + 25 % de Ã + 25 % de G̃30. Relative (un rang, pas un niveau),
  sensible à la composition du classement, difficile à comparer d'une année sur l'autre.

Top 10 :

| Rang | V1 | V2 (recommandée) | V3 |
|---|---|---|---|
| 1 | Paris Est – Reims (88,2) | Paris Est – Reims (94,2) | Paris Est – Reims (99,2) |
| 2 | Brest – Paris Montparnasse (87,1) | Nancy – Paris Est (92,7) | Lyon Part-Dieu – Paris Lyon (90,8) |
| 3 | Lyon Part-Dieu – Paris Lyon (86,3) | Lyon Part-Dieu – Paris Lyon (92,6) | Nancy – Paris Est (90,0) |
| 4 | Nancy – Paris Est (86,2) | Le Creusot – Paris Lyon (92,2) | Le Creusot – Paris Lyon (81,7) |
| 5 | Paris Lyon – Zurich (85,9) | Brest – Paris Montparnasse (92,0) | Dijon – Paris Lyon (81,3) |
| 6 | Dijon – Paris Lyon (85,9) | Paris Montparnasse – St-Malo (92,0) | Lyon Part-Dieu – Rennes (77,1) |
| 7 | Lausanne – Paris Lyon (85,4) | Dijon – Paris Lyon (91,9) | Paris Montparnasse – St-Malo (75,4) |
| 8 | Paris Montparnasse – St-Malo (85,2) | Paris Lyon – Zurich (91,5) | Paris Lyon – Zurich (74,2) |
| 9 | Besançon TGV – Paris Lyon (85,0) | Paris Montparnasse – Rennes (91,5) | Paris Montparnasse – Rennes (74,2) |
| 10 | Lyon Part-Dieu – Rennes (85,0) | Lyon Part-Dieu – Rennes (91,4) | Brest – Paris Montparnasse (72,9) |

Bas du classement (du dernier au 5e avant-dernier) :

| Rang | V1 | V2 (recommandée) | V3 |
|---|---|---|---|
| 61 | Paris Est – Stuttgart (61,0) | Paris Est – Stuttgart (78,7) | Paris Est – Stuttgart (0,8) |
| 60 | Francfort – Paris Est (69,9) | Francfort – Paris Est (82,1) | Francfort – Paris Est (3,3) |
| 59 | Italie – Paris Lyon (71,7) | Italie – Paris Lyon (83,3) | Nice – Paris Lyon (13,7) |
| 58 | Chambéry – Paris Lyon (71,9) | Nice – Paris Lyon (84,0) | Marne-la-Vallée – Marseille (15,8) |
| 57 | Douai – Paris Nord (73,0) | Marne-la-Vallée – Marseille (85,1) | Lille – Marseille (20,4) |

Les trois variantes sont très corrélées (Spearman 0,91 à 0,96, → 06 § 4). V2 se distingue en remontant les
liaisons courtes aux retards légers (Lille – Paris : 39e en V1, 18e en V2) et en descendant les longues liaisons du
Sud-Est aux retards graves (Marseille – Paris : 13e → 31e ; Montpellier – Paris : 26e → 39e). C'est l'effet voulu,
« un retard de 5 min n'est pas un retard d'une heure », mais il pénalise mécaniquement les trajets longs : à
signaler dans la méthodologie.

Intercités (V2, gravité imputée) : 1. Béziers – Clermont-Ferrand (95,2), 2. Lyon – Nancy (93,2),
3. Clermont-Ferrand – Paris-Bercy (92,9) … 14. Nice – Paris-Austerlitz (84,0), 15. Briançon – Paris-Austerlitz (82,6),
16. Bordeaux – Marseille (79,3).

### Incertitude affichée

Intervalle à 80 % par simulation simple côté pipeline : composantes tirées dans leurs lois bêta a posteriori avec
`n / D` trains effectifs, puis score recalculé. Le classement affiche le score arrondi à l'entier et une barre
d'intervalle ; deux liaisons dont les intervalles se chevauchent largement sont présentées comme « au coude à coude »
(pas de tri par décimale invisible).

## 4. Périodes et filtres

### Périodes

| Période | Définition | Calcul |
|---|---|---|
| **12 derniers mois** (défaut) | 12 mois glissants jusqu'au **dernier mois publié du type** (TGV sept. 2026, Intercités mai 2026). Les deux fenêtres sont affichées | précalculé |
| Année civile | 2018 → 2026 (TGV), 2014 → 2026 (Intercités) ; année en cours marquée « partielle » | précalculé |
| Tout l'historique | depuis le premier mois de la liaison | précalculé |
| Mois précis | un mois ; le lissage pèse alors beaucoup pour les petites liaisons (voulu) | navigateur, à partir de `mensuel-*.json` |
| Période libre (option) | du mois X au mois Y | navigateur |

Une liaison n'apparaît dans une période que si elle a au moins un mois de données ; si elle en a moins de 6 sur
12, elle est marquée « couverture partielle ». Le prior μ est toujours celui du type sur la période, **même quand
on filtre** (filtrer « Bretagne » ne change pas la référence).

### Filtres (barre de puces, combinables, reflétés dans l'URL)

- **Type** : TGV, Intercités, tous.
- **Région** : une liaison appartient aux régions de ses deux extrémités ; « International » pour les 7 liaisons TGV
  avec une gare étrangère.
- **Gare** : recherche (« toutes les liaisons de Rennes »).
- **Durée** : < 1 h 30, 1 h 30–3 h, > 3 h (ce sont aussi les tranches de seuil « à l'heure »).
- **Fréquentation** (comme « popularité » sur bestalbums) : trains par mois en tranches (< 50, 50–200, 200–500,
  > 500) et seuil minimal de trains.
- **Tendance** : en amélioration, en dégradation, stable.
- **Tri** : score, régularité, annulations, retards > 30 min, trains, tendance, ordre alphabétique.

## 5. Tendances et saisonnalité

### Tendance d'une liaison

- Régularité des 12 derniers mois comparée aux 12 précédents, test z avec variance binomiale **gonflée par D** :
  `z = Δ / sqrt(D · (p₁(1−p₁)/n₁ + p₀(1−p₀)/n₀))`.
- Étiquette « en amélioration / en dégradation » si **|z| ≥ 2 et |Δ| ≥ 2 points**, sinon « stable ».
- **Tendance relative au réseau** en plus : Δ liaison − Δ du type. Le test sur les vraies données montre pourquoi
  c'est indispensable : sur 12 mois, la régularité TGV globale a perdu 4,2 points ; **29 liaisons TGV sur 61 se
  « dégradent » significativement, aucune ne s'améliore**, mais une fois l'évolution du réseau retirée, **une seule
  liaison se distingue** (→ 07). La page Tendances doit dire d'abord « tout le réseau a reculé », puis montrer les
  liaisons qui s'écartent de cette évolution.
- Sur la fiche : courbe mensuelle désaisonnalisée sur 36 mois et pente en points par an (exemple : Italie – Paris
  −8,8 pts/an, Paris – Stuttgart −7,7, Francfort – Paris −4,6, → 07 § 2).
- Les mois marqués `exclure: tendances` dans `events.yaml` (COVID) sont retirés des deux fenêtres.

### Saisonnalité

- Profil du type : écart moyen de chaque mois calendaire à la moyenne de son année (2018–2025, hors 2020). TGV :
  mars +2,5 pts, mai +2,1, juin −2,4, **juillet −4,1**, novembre −1,8 (→ 07). Intercités : mars +3,4, novembre −4,0.
- Profil d'une liaison : même calcul, **rétréci vers le profil du type** (la variabilité d'une année sur l'autre
  d'un même mois est grande : écart-type médian de 6,7 points pour le TGV).
- Affichage : 12 barres sur la fiche, et une carte de chaleur liaison × mois sur la page Tendances.

## 6. « Mon trajet »

**Question posée** : « Je prends un train de A vers B en juillet : quelle est la probabilité qu'il arrive à l'heure ? »
La réponse porte sur un **train prévu** (un train annulé n'est pas « à l'heure ») et sur une liaison suivie par les
données : les ≈ 61 liaisons TGV et 16 Intercités actives, dans les deux sens. Pas de calcul par horaire ou par train :
les données n'existent pas.

**Méthode (testée → 07 § 3) :**

1. Données : le mois calendaire choisi sur les **5 dernières années disponibles**, hors mois exclus par `events.yaml`
   (COVID), dans le **sens choisi**. Comptes `k` (trains prévus à l'heure) sur `n` (trains prévus).
2. Prior bêta centré sur (niveau de la liaison dans ce sens sur 24 mois + effet saisonnier du type), de force
   m = 60 trains effectifs (cohérent avec le § 3).
3. Posterior bêta avec n effectif = n / D → probabilité moyenne et **intervalle de crédibilité à 80 %**.
4. **Intervalle de prédiction** : l'incertitude d'un voyage futur est dominée par la variabilité d'une année sur
   l'autre (écart-type médian 6,7 points TGV, 5,4 Intercités, contre 2,4 pour le seul aléa binomial, → 07 § 4).
   On ajoute donc à la variance du posterior une variance inter-annuelle estimée par type (rétrécie vers la cellule).

**Affichage** : « **77 %** de chances d'arriver à l'heure (le plus souvent entre 70 et 84 %) », avec les valeurs des
5 derniers mois de juillet en petites barres (pire et meilleure année), plus la probabilité d'annulation et de retard
> 30 min (TGV). Exemples réels : Paris Montparnasse → Toulouse en juillet : 77,5 % (pire année 70,4 %, meilleure
86,9 %) ; en octobre : 82,5 %. Paris-Austerlitz → Briançon en février : 56,9 %, avec une pire année à 10,3 %.

**Peu de données** :
- moins de 3 années ou moins de 100 trains prévus pour ce mois → message « estimation surtout fondée sur la moyenne
  de la liaison » et intervalle élargi ;
- paire absente des données → pas de chiffre inventé : on propose les liaisons suivies au départ ou à l'arrivée de
  ces gares (« Paris → Orange n'est pas suivi ; Paris → Avignon TGV l'est ») ;
- trajet avec correspondance : hors périmètre v1 (question ouverte).

## 7. Grèves et événements : `data/events.yaml`

Fichier versionné, rempli à la main et relu (avec une source pour chaque entrée) :

```yaml
- id: greve-printemps-2018
  titre: Grève contre la réforme ferroviaire
  type: greve            # greve | covid | travaux | meteo | incident | donnees
  debut: 2018-04
  fin: 2018-06
  perimetre: national    # national | axe:<Sud-Est> | liaisons: [paris-lyon--marseille-st-charles, …]
  types: [TGV, Intercités]
  exclure: [tendances, saisonnalite, mon_trajet]   # jamais du score : c'est la réalité vécue par les voyageurs
  source: https://…
- id: causes-nomenclature-2026
  titre: Changement probable de nomenclature des causes de retard
  type: donnees
  debut: 2026-05
  types: [TGV]
  note: Infrastructure et gestion du trafic passent d'environ 20 % à 5 % du jour au lendemain
```

Utilisation :
- **bandes grisées** sur tous les graphiques temporels, avec infobulle ;
- **exclusions** : tendances, saisonnalité et « Mon trajet » ignorent les mois marqués ; le score les garde (option
  « hors grèves » en question ouverte) ;
- **chronologie** sur la page Statistiques ;
- les événements `donnees` documentent les ruptures de séries (gravité janv.–mars 2025, causes mai 2026, transfert
  Normandie 2020, reclassements de service 2025) et désactivent les calculs concernés ;
- **aide au remplissage** : le pipeline signale dans le journal de la CI les mois candidats (annulations TGV > 5 % ;
  programmés Intercités ou TER en baisse de plus de 20 % sur un an) **absents** du fichier, sans jamais l'écrire
  lui-même. Candidats déjà détectés : 2018-04 à 07, 2019-12, 2020-01, 2020-03 à 06, 2020-11 et 12, 2021-04 et 05,
  2022-12, 2023-01, 2023-03 (→ 05).

## 8. Pages, composants, design

### Pages (routeur par hash, URL partageables)

| Route | Page | Contenu |
|---|---|---|
| `#/` | **Classement** | barre de filtres (puces) ; tableau : rang, liaison, type, score + barre d'intervalle, régularité, annulations, > 30 min, trains/mois, tendance (flèche), courbe des 12 derniers mois ; sur mobile, une carte par liaison |
| `#/liaison/<id>` | **Fiche liaison** | en-tête (score, rang, intervalle, comparaison au type) ; choix du sens ; historique mensuel avec la moyenne du type et les événements ; annulations ; gravité (barres empilées) ; causes (aires empilées, rupture de 2026 signalée) ; saisonnalité ; tendance ; « Mon trajet » condensé ; petite carte SVG des deux gares ; tableau des données et export CSV |
| `#/mon-trajet` | **Mon trajet** | départ, arrivée (recherche dans les gares desservies), mois, type si besoin → probabilité, intervalle, années précédentes, liaisons proches |
| `#/tendances` | **Tendances** | évolution du réseau, puis liaisons qui s'en écartent ; carte de chaleur saisonnière ; chronologie des événements |
| `#/statistiques` | **Statistiques** | régularité TGV officielle depuis 2015, axes, Intercités ; distribution des scores ; causes dans le temps ; meilleurs et pires mois ; records |
| `#/regions` | Régions TER (v2) | classement des régions, séries, avertissements sur le découpage |
| `#/methodologie` | **Méthodologie et sources** | voir § 10 |

### Composants Svelte 5 (mêmes conventions que l'Atlas)

- `lib/ui/` : `DataTable` (tri, ligne cliquable, vue cartes sur mobile), `FilterBar` / `Chips`, `Select`,
  `SearchBox` (gares), `MonthPicker`, `PeriodPicker`, `Tooltip`, `Section`, `Badge` (type, tendance), `ScoreBar`
  (score + intervalle).
- `lib/charts/` (SVG faits main, sans dépendance) : `LineChart` (avec bandes d'événements et courbe de référence),
  `StackedBars`, `StackedArea`, `Sparkline`, `SeasonBars`, `Heatmap`, `YearDots` (« Mon trajet »), `MiniMap`
  (contour de la France + points).
- `lib/score.ts` : formules du § 3, **identiques au pipeline**, vérifiées par Vitest sur des valeurs exportées par
  le pipeline (même score à 0,01 près) ; `lib/period.ts`, `lib/data.ts` (chargement paresseux), `lib/router.svelte.ts`,
  `lib/format.ts` (nombres et dates en français).

### Design

- **Esprit bestalbums** : un classement dense et numéroté, un score très visible, des sous-scores en colonnes, des
  filtres riches mais repliables, un seuil minimal (« trains minimum », l'équivalent des « votes minimum »), une page
  Statistiques fournie, aucune fioriture.
- Sobre, typographie lisible (Archivo, comme l'Atlas), thèmes clair et sombre, couleur réservée au score (échelle
  séquentielle) et aux types de train.
- Mobile d'abord : cartes empilées pour le classement, filtres dans un panneau, graphiques pleine largeur.
- Accessibilité : contrastes vérifiés, navigation au clavier, tableau de données en alternative à chaque graphique,
  mouvement réduit respecté.
- Tout en français, nombres au format français (« 87,3 % »).

## 9. GitHub Actions

- `ci.yml` (push hors `main`, pull requests) : pytest, `svelte-check`, Vitest, build.
- `deploy.yml` :
  - **déclencheurs** : push sur `main`, à la demande, et planifié **chaque lundi à 6 h 17 UTC**. Les publications
    sont irrégulières (TGV autour du 2 du mois, TER le 10, Intercités avec 2 mois de retard) : un passage hebdomadaire
    coûte peu et évite un mois de retard ;
  - **détection de nouvelles données** : on lit `data_processed` de chaque jeu (API métadonnées, quelques Ko) et on
    compare au fichier versionné `data/sources.lock.json`. Rien de nouveau et pas de push de code → arrêt immédiat,
    pas de déploiement. Sinon : téléchargement, build, tests, déploiement, puis commit du nouveau `sources.lock.json`
    sur `main` (un push fait avec `GITHUB_TOKEN` ne relance pas le workflow) ;
  - **échec propre si une source change** : `schemas.py` vérifie les noms et types de colonnes ; des contrôles de
    cohérence vérifient que le nombre de lignes ne baisse pas de plus de 5 %, que le dernier mois ne recule pas, que
    les causes somment à 100 % ± 2 dans au moins 95 % des lignes et que les gares sont toutes rattachées. Le message
    d'erreur nomme le jeu et la colonne. En cas d'échec, **le site déjà publié reste en place** (le déploiement est la
    dernière étape) et GitHub envoie la notification d'échec habituelle ;
  - une **nouvelle gare non rattachée** fait aussi échouer le build, avec le libellé à ajouter dans
    `pipeline/refs/gares_alias.csv`.

## 10. Méthodologie, sources, ODbL

Page `#/methodologie`, aussi reprise dans le README :

- **Sources** : liens vers les 5 jeux de régularité et les 2 référentiels, avec la date de dernière mise à jour lue
  dans `meta.json`.
- **Attribution** (pied de page de toutes les pages et méthodologie) : « Données : SNCF Voyageurs (régularité TGV,
  Intercités, TER), SNCF Gares & Connexions (gares de voyageurs), SNCF Réseau (liste des gares) —
  ressources.data.sncf.com, licence ODbL. »
- **Définitions** : seuils 5/10/15 min (TGV, Intercités) et 5 min (TER) ; arrondi à la minute inférieure ; « prévus »
  et « programmés » ; trains supprimés la veille avant 16 h ; sélection AQST ; la régularité globale officielle n'est
  pas la moyenne des liaisons.
- **Méthode** : score V2 et barème, rétrécissement bayésien (formule, μ, M, D), gravité imputée pour les Intercités,
  intervalles, tendances, « Mon trajet », événements.
- **Limites connues** : anomalies et ruptures de DATA.md (gravité début 2025, causes mai 2026, Lille / Montpellier
  ambigus, OUIGO non identifiable, Intercités « LYON »…).
- **ODbL** : les fichiers de `site/public/data/` forment une **base de données dérivée**. Ils sont publiés sous ODbL,
  avec un fichier `LICENSE-DONNEES` et un lien de téléchargement en CSV (`donnees/`) depuis la page méthodologie. Le
  site et ses graphiques sont des « œuvres produites » : ils portent la mention d'attribution ci-dessus. Le **code**
  est sous une licence distincte (question ouverte).

## 11. Découpage en étapes

| Étape | Contenu |
|---|---|
| 1 | Pipeline de production (fetch, schémas, gares, clean, score, export) + tests + `events.yaml` initial |
| 2 | Site : classement + filtres + périodes standard ; méthodologie ; déploiement Pages |
| 3 | Fiche liaison (historique, causes, gravité, saisonnalité, tendance, carte) |
| 4 | Mon trajet |
| 5 | Tendances et Statistiques ; périodes libres et mois précis (comptes mensuels chargés à la demande) |
| 6 | Régions TER (v2), finitions, accessibilité |

## 12. Questions ouvertes

1. **Formule du score** : V2 (note moyenne d'un train, recommandée) ou V1 (probabilité d'arriver à l'heure, plus
   simple et identique à « Mon trajet ») ? Le barème 100 / 67 / 33 / 0 / 0 vous convient-il ? Un annulé doit-il valoir
   comme un retard de plus d'une heure ?
2. **Intercités** : gravité imputée (même échelle que le TGV, recommandé) ou score sans gravité affiché à part ?
   Vue « Tous types » proposée ou seulement des onglets séparés ?
3. **Grèves dans le score** : les garder (recommandé : c'est ce que vivent les voyageurs) ou proposer un interrupteur
   « hors grèves » ?
4. **Liaison fusionnée ou par sens** dans le classement : la fusion est recommandée ; un filtre « par sens » vous
   serait-il utile ?
5. **Liaisons internationales** (7 sur 61) : dans le classement principal (recommandé, avec un filtre) ou à part ?
6. **« Mon trajet »** : se limiter aux paires suivies (recommandé) ou tenter des trajets avec correspondance en
   combinant deux liaisons (fragile : retards non indépendants, pas d'horaires) ?
7. **TER** : v2 comme proposé, ou dès la v1 ?
8. **Licence du code** (MIT ? même licence que l'Atlas ?) et **nom de domaine / URL** GitHub Pages.
9. **Petite carte** : SVG minimal (proposé, aucune dépendance) ou MapLibre comme l'Atlas (≈ 280 Ko) ?
10. **`events.yaml`** : je peux préparer une première version (événements nationaux 2014–2026 avec sources) à
    relire, ou vous préférez la remplir vous-même ?
