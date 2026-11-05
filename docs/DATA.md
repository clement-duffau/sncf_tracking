# Données — exploration (phase 1)

Ce document décrit les jeux open data utilisés par « Le classement des liaisons ferroviaires » : ce qu'ils contiennent,
leurs limites et ce qu'on peut en tirer. Tous les chiffres viennent des scripts `pipeline/explore/*.py`, exécutés sur
les données téléchargées le **5 novembre 2026**. Chaque script écrit son rapport complet dans
`pipeline/explore/sorties/*.md`, versionné ; les références « (→ 01) » renvoient à ces rapports.

Pour reproduire :

```bash
pip install -r pipeline/requirements.txt
python pipeline/download.py                     # tout (≈ 10 Mo) → data/raw/
python pipeline/explore/01_tgv_liaisons.py      # puis 02 … 08
```

## Sommaire

1. [Sources et accès](#1-sources-et-accès)
2. [TGV par liaisons (AQST)](#2-tgv-par-liaisons-aqst)
3. [TGV par axe et TGV global](#3-tgv-par-axe-et-tgv-global)
4. [Intercités](#4-intercités)
5. [TER (par région)](#5-ter-par-région)
6. [Référentiels de gares et rattachement aux régions](#6-référentiels-de-gares-et-rattachement-aux-régions)
7. [Définitions « à l'heure » : ce qui est comparable](#7-définitions--à-lheure--ce-qui-est-comparable)
8. [Événements visibles dans les données](#8-événements-visibles-dans-les-données)
9. [Faisabilité des fonctionnalités visées](#9-faisabilité-des-fonctionnalités-visées)

---

## 1. Sources et accès

| Clé locale | Jeu (portail SNCF) | Éditeur | Licence | Couverture | Lignes | Données modifiées le |
|---|---|---|---|---|---|---|
| `tgv_aqst` | [regularite-mensuelle-tgv-aqst](https://ressources.data.sncf.com/explore/dataset/regularite-mensuelle-tgv-aqst/) | SNCF Voyageurs | ODbL | janv. 2018 → sept. 2026 | 12 907 | 2026-10-02 |
| `tgv_axes` | [regularite-mensuelle-tgv-axes](https://ressources.data.sncf.com/explore/dataset/regularite-mensuelle-tgv-axes/) | SNCF Voyageurs | ODbL | janv. 2015 → sept. 2026 | 835 | 2026-10-02 |
| `tgv_national` | [reglarite-mensuelle-tgv-nationale](https://ressources.data.sncf.com/explore/dataset/reglarite-mensuelle-tgv-nationale/) (sic) | SNCF Voyageurs | ODbL | janv. 2015 → sept. 2026 | 141 | 2026-10-02 |
| `intercites` | [regularite-mensuelle-intercites](https://ressources.data.sncf.com/explore/dataset/regularite-mensuelle-intercites/) | SNCF Voyageurs | ODbL | janv. 2014 → mai 2026 | 5 949 | 2026-07-27 |
| `ter` | [regularite-mensuelle-ter](https://ressources.data.sncf.com/explore/dataset/regularite-mensuelle-ter/) | SNCF Voyageurs | ODbL | janv. 2013 → août 2026 | 2 380 | 2026-09-10 |
| `gares_voyageurs` | [gares-de-voyageurs](https://ressources.data.sncf.com/explore/dataset/gares-de-voyageurs/) | SNCF Gares & Connexions | ODbL | 2 792 gares | 2 792 | 2026-11-04 |
| `liste_gares` | [liste-des-gares](https://ressources.data.sncf.com/explore/dataset/liste-des-gares/) | SNCF Réseau | ODbL | 6 469 points | 6 469 | 2025-10-02 |

Repérés dans le catalogue mais **non profilés** (téléchargement non terminé au moment de l'exploration, et pas
nécessaires à la v1) : `meilleurs-temps-des-parcours-des-trains` (3 999 lignes), `frequentation-gares` (3 021),
`ponctualite-mensuelle-transilien` (2 087, hors périmètre). Aucun jeu de **causes de retard Intercités**, de
ponctualité par ligne TER ni de données par train n'existe sur le portail (recherche sur les 164 jeux du catalogue).

### API Opendatasoft ou data.gouv.fr ?

- Les fiches data.gouv.fr ([TGV](https://www.data.gouv.fr/datasets/regularite-mensuelle-tgv-par-liaisons),
  [Intercités](https://www.data.gouv.fr/datasets/regularite-mensuelle-intercites-sncf),
  [TER](https://www.data.gouv.fr/datasets/regularite-mensuelle-ter-sncf)) sont moissonnées depuis le portail SNCF :
  leurs ressources **pointent vers les mêmes URL d'export** `ressources.data.sncf.com/api/explore/v2.1/…/exports/…`.
  data.gouv.fr ne stocke pas de copie ; son API tabulaire n'a pas pu analyser ces CSV (« Column names cannot exceed
  63 characters »), et la fréquence y est déclarée « unknown ».
- **Recommandation : interroger directement l'API Explore v2.1 du portail SNCF.** Elle fournit, en plus des exports
  (CSV, JSON, **Parquet typé**), les métadonnées du jeu : `data_processed` (date de dernière mise à jour des données,
  utile pour détecter une nouvelle publication) et le **schéma des champs** (nom, type, libellé), utile pour échouer
  proprement si une source change de format. Passer par data.gouv.fr n'ajoute qu'un intermédiaire.
- Fiabilité réseau : depuis l'environnement d'exploration, environ deux connexions sur trois au portail ont été
  coupées à l'ouverture ; `pipeline/download.py` retente donc jusqu'à 40 fois. Cette instabilité vient
  probablement du proxy de l'environnement (data.gouv.fr a montré les mêmes coupures) : **rien ne permet d'en
  conclure que le portail SNCF est instable**. Les reprises restent utiles en production.
- **Fréquence réelle de mise à jour : non mesurable sur un seul instantané.** On observe seulement le décalage au
  5 novembre 2026 : TGV publié le 2 octobre jusqu'à septembre (≈ 1 mois de décalage), TER publié le 10 septembre
  jusqu'à août, Intercités publié le 27 juillet jusqu'à mai (≈ 2 mois, et rien depuis 3 mois). Le pipeline
  enregistrera `data_processed` à chaque passage pour mesurer la fréquence dans la durée.

---

## 2. TGV par liaisons (AQST)

### Contenu

Une ligne = **un mois × une liaison orientée (gare de départ → gare d'arrivée) × un service** (National /
International). Le jeu reprend la sélection de liaisons suivie par l'AQST (Autorité de la qualité de service dans
les transports).

| Colonne | Type | Unité / sens | Remarques |
|---|---|---|---|
| `date` | date | 1er du mois | 105 mois, janv. 2018 → sept. 2026, **aucun mois manquant** |
| `service` | texte | `National` / `International` | Reclassements, voir « Pièges » |
| `gare_depart`, `gare_arrivee` | texte | libellé en majuscules sans accent | 59 libellés, dont 8 gares étrangères ou pseudo-gares |
| `duree_moyenne` | entier | minutes, durée moyenne **prévue** | Sert à deviner le seuil « à l'heure » ; 0 quand aucun train n'a circulé |
| `nb_train_prevu` | entier | trains | **Inclut les trains annulés** (voir plus bas) |
| `nb_annulation` | entier | trains | |
| `nb_train_depart_retard`, `retard_moyen_depart`, `retard_moyen_tous_trains_depart` | entier / réel | trains, minutes | Retard au départ |
| `nb_train_retard_arrivee` | entier | trains | Trains en retard au terminus **selon le seuil composite** (5/10/15 min) |
| `retard_moyen_arrivee` | réel | minutes | Moyenne sur les trains en retard |
| `retard_moyen_tous_trains_arrivee` | réel | minutes | Moyenne sur tous les trains ; **122 valeurs négatives**, jusqu'à −472 min (→ 01) |
| `nb_train_retard_sup_15`, `_sup_30`, `_sup_60` | entier | trains | Gravité ; voir l'anomalie de début 2025 |
| `retard_moyen_trains_retard_sup15` | réel | minutes | Libellé « si liaison concurrencée par vol », mais **renseigné partout** |
| `prct_cause_externe`, `_infra`, `_gestion_trafic`, `_materiel_roulant`, `_gestion_gare`, `_prise_en_charge_voyageurs` | réel | % des **trains en retard à l'arrivée** | 6 familles de causes |
| `commentaire_annulation`, `commentaire_retards_depart` | texte | | **Toujours vides** (12 907 / 12 907) |
| `commentaires_retard_arrivee` | texte | texte libre | 698 renseignés, **uniquement en 2018 (457) et 2019 (241)** |

### Liaisons

- **130 liaisons orientées, 65 non orientées** sur toute la période ; **61 non orientées** sur les 12 derniers mois.
- Le jeu est essentiellement **en étoile autour de Paris** (Paris Lyon, Montparnasse, Est, Nord), plus des
  transversales (Lyon ↔ Marseille, Lille, Rennes, Montpellier, Marne-la-Vallée ; Lille ↔ Marseille ;
  Nantes ↔ Strasbourg ; Tourcoing ↔ Bordeaux / Marseille) et l'international SNCF (Francfort, Stuttgart, Genève,
  Lausanne, Zurich, Barcelone, Madrid, « ITALIE »).
- **A→B et B→A sont deux lignes distinctes**, et toutes les liaisons ont leur retour (→ 01, « Liaisons orientées
  sans liaison retour » : aucune).
- Apparitions, disparitions, reclassements (→ 01) :
  - `PARIS VAUGIRARD` ↔ Bordeaux, Nantes, Rennes : 2018 uniquement (Vaugirard fait partie de Paris Montparnasse :
    son code UIC 87391102 appartient à la gare « Paris Montparnasse » du référentiel, → 04) ;
  - Madrid ↔ Marseille : jusqu'en déc. 2022 ;
  - Tourcoing → Marseille : 13 mois seulement (jusqu'en août 2022) alors que Marseille → Tourcoing est présent
    104 mois : **la seule asymétrie aller/retour** ;
  - Barcelone ↔ Paris Lyon : `International` jusqu'en sept. 2025 puis `National` à partir d'oct. 2025 ;
  - de **juillet à septembre 2025**, 14 liaisons (Paris ↔ Bellegarde, Chambéry, Dijon, Mâcon, Mulhouse, Strasbourg ;
    Lyon ↔ Marseille) ont **deux lignes le même mois**, une `National` et une `International`, avec des trains
    différents : par exemple Paris Lyon → Bellegarde passe de ≈ 210 trains « nationaux » à 8–25, et 230–248 trains
    apparaissent en « international ». **Il faut sommer les deux services** pour garder une série continue.
  - `ITALIE` n'est pas une gare mais un regroupement de destinations (101 mois sur 105, absent 4 mois).
- Pas de gare orthographiée de deux façons différentes dans ce jeu (59 libellés, tous stables).

### Annulations : `nb_train_prevu` inclut les annulés

- En avril 2018 (grève), `nb_annulation` atteint 11 283 trains pour 34 317 prévus (32,9 %) : les annulés sont bien
  comptés **dans** les prévus. On calcule donc **circulés = prévus − annulés**.
- Exception : **73 lignes à 0 train prévu** (avril–décembre 2020), dont 63 avec des annulations > 0 (avril–juin 2020),
  ce qui donne un nombre de circulés négatif. Ces lignes doivent être ignorées (aucun train n'a circulé).
- Décembre 2019 : les prévus chutent de moitié (14 609 contre ≈ 30 000), alors que les annulations ne représentent
  que 16,5 %. **Une partie des trains supprimés à l'avance n'apparaît ni en prévus ni en annulés.** Le taux
  d'annulation **sous-estime donc l'effet des grèves annoncées à l'avance** (règle non documentée pour le TGV ;
  elle l'est pour Intercités et TER, voir § 4).

### Seuil « à l'heure » et cohérence des comptes de retard

Le portail décrit la **régularité composite** : à l'heure si le retard au terminus est < 5 min (trajet < 1 h 30),
< 10 min (1 h 30 – 3 h), < 15 min (> 3 h). Vérification sur les données (→ 01) : pour les liaisons de plus de 3 h,
`nb_train_retard_arrivee` est **égal** à `nb_train_retard_sup_15` dans 4 523 lignes sur 5 171 (87 %). Les écarts
restants concernent surtout des liaisons dont la durée moyenne est proche de 3 h : le seuil s'applique train par
train, alors que `duree_moyenne` n'est qu'une moyenne. Pour les trajets plus courts, `nb_train_retard_arrivee ≥
nb_train_retard_sup_15` dans 99,9 % des cas. **Le seuil composite est donc confirmé.**

### Gravité (> 15 / > 30 / > 60 min)

- Hors anomalie, sur toute la période : 10,6 % des trains circulés arrivent avec plus de 15 min de retard, 5,2 %
  avec plus de 30 min, 2,0 % avec plus de 60 min.
- **Anomalie de janvier à mars 2025** (→ 01, « Mois où la hiérarchie est rompue ») : `nb_train_retard_sup_30` vaut
  0 ou est **négatif** (jusqu'à −44, 43 valeurs négatives au total), et `nb_train_retard_sup_60` est plus grand que
  `_sup_30` sur ≈ 118 liaisons par mois. Exemple Paris Montparnasse → Bordeaux, janv. 2025 : > 15 = 124,
  > 30 = 0, > 60 = 55. La colonne > 60 semble contenir ce qui devrait être > 30, mais **ce n'est pas vérifiable** :
  il faut traiter la gravité > 30 / > 60 de ces 3 mois comme **manquante**.
- Le reste du temps, la hiérarchie est respectée : aucune ligne avec > 30 < > 60 hors janv.–mars 2025, 3 lignes avec
  > 15 < > 30, et 31 lignes (2018–2020) où les retards composites sont inférieurs aux retards > 15 min.

### Causes de retard

- Les 6 pourcentages portent sur les **trains en retard à l'arrivée** et **somment à 100 %** dans 12 625 lignes
  sur 12 907 (97,8 %). 272 lignes ont toutes les causes à 0, **dont 80 avec des trains en retard**, ce qui signifie
  « causes non renseignées » : 66 en 2018, dont 65 sur des liaisons internationales. 10 lignes somment entre 85 et
  99 % (arrondis).
- Ce sont des **parts** : le nombre de trains en retard par cause s'obtient par `prct × nb_train_retard_arrivee`.
  Pour agréger plusieurs mois ou plusieurs liaisons, il faut **pondérer par le nombre de trains en retard**.
- Répartition moyenne 2018–2025 : causes externes 17–26 %, infrastructure 18–30 %, gestion du trafic 15–25 %,
  matériel roulant 16–21 %, gestion en gare 5–10 %, prise en charge des voyageurs 3–16 % (pic en 2021).
- **Rupture en mai 2026** (→ 01, « Répartition mensuelle des causes depuis juin 2025 ») : l'infrastructure passe de
  15–28 % à ≈ 6 %, la gestion du trafic de 20–30 % à ≈ 5 %, et la gestion en gare monte de 8–12 % à 21–32 %. Le
  changement est trop brusque pour être réel : **c'est très probablement un changement de nomenclature ou
  d'attribution des causes, non documenté sur le portail**. Les causes d'avant et d'après mai 2026 ne doivent pas
  être comparées sans avertissement.

### Commentaires

Seul `commentaires_retard_arrivee` est renseigné : texte libre détaillé par jour et par numéro de train (« 01/08 :
2778 Attente ADC… »), **seulement en 2018–2019**, dont 30 commentaires mentionnent une grève (tous en 2018).
**Inutilisable pour détecter des grèves sur l'ensemble de la période.** Les champs `commentaire_annulation` et
`commentaire_retards_depart` sont toujours vides.

### Volumes (utile pour le score)

Trains circulés par liaison orientée et par mois : médiane 225, 10 % des liaisons-mois sous 67, 5 % sous 34 (→ 01).
Sur les 12 derniers mois, les plus petites liaisons (non orientées) sont Marseille – Tourcoing (≈ 22 trains par mois
et par sens), Bordeaux – Tourcoing (26–27), Nantes – Strasbourg (57), Barcelone – Paris (66) et Italie – Paris (76).

### Comparaison avec le global officiel

Recalculer une régularité « globale » en sommant les liaisons donne 1,6 à 5,6 points de moins que la régularité
TGV globale publiée (corrélation 0,81 à 1,00 selon l'année, → 01). C'est attendu, et le portail le précise : un
train compte dans plusieurs liaisons, et le global inclut des trains absents de la sélection. **Ne jamais présenter
une somme de liaisons comme la régularité TGV nationale** : utiliser `tgv_national`.

Le jeu ne dit pas si les **OUIGO** sont inclus dans les liaisons (aucune colonne ne l'indique ; le jeu par axe, lui,
isole un axe « OUIGO »). **Non vérifiable.**

---

## 3. TGV par axe et TGV global

| Jeu | Colonnes | Couverture | Remarques |
|---|---|---|---|
| `tgv_axes` | `date`, `axe`, `regularite_composite` (%), `ponctualite_origine` (%) | 2015-01 → 2026-09 ; 6 axes : Atlantique, Est, Nord, Sud-Est, Europe, OUIGO (OUIGO à partir de déc. 2015) | 1 mois sans valeur pour OUIGO. Pas de comptes de trains, seulement des taux |
| `tgv_national` | `date`, `regularite_composite` (%), `ponctualite_origine` (%) | 2015-01 → 2026-09, 141 mois sans trou | Référence officielle pour la page Statistiques |

La **ponctualité origine** est la part des trains partis avec moins d'une minute de retard. Moyennes simples des
12 derniers mois par axe : Atlantique 87,1 %, Est 84,2 %, OUIGO 83,6 %, Sud-Est 83,3 %, Nord 81,9 %, Europe 76,5 %
(→ 08). Moyennes annuelles du global : 90,4 % en 2015, 87,7 % en 2018, 90,8 % en 2020, 86,6 % en 2025, 83,3 % sur
les 9 premiers mois de 2026. Sans comptes de trains, ces jeux ne peuvent pas entrer dans un score pondéré : ils
servent de **contexte** (page Statistiques, ligne de référence sur les graphiques).

---

## 4. Intercités

### Contenu

Une ligne = **un mois × une liaison orientée** (libellé de départ → libellé d'arrivée).

| Colonne | Type | Sens |
|---|---|---|
| `date` | date | 149 mois, janv. 2014 → mai 2026, sans mois manquant |
| `depart`, `arrivee` | texte | libellés (avec tirets et accents : `PARIS-AUSTERLITZ`, `BÉZIERS`) ; parfois composites (`BRIVE/CAHORS`) |
| `nombre_de_trains_programmes` | entier | trains programmés **après** retrait des suppressions annoncées avant 16 h la veille |
| `nombre_de_trains_ayant_circule` | entier | toujours égal à programmés − annulés (0 incohérence) |
| `nombre_de_trains_annules` | entier | suppressions tardives, totales ou partielles |
| `nombre_de_trains_en_retard_a_l_arrivee` | entier | seuil composite 5/10/15 min, comme le TGV |
| `taux_de_regularite` | réel | % = (circulés − retards) / circulés ; 0 incohérence ; **vaut 0 quand 0 train a circulé** (161 lignes) |
| `nombre_de_trains_a_l_heure_pour_un_train_en_retard_a_l_arrivee` | réel | ratio dérivé ; vaut 0 quand il n'y a aucun retard (318 lignes) |

**Il n'y a ni causes, ni gravité (> 15 / 30 / 60 min), ni retard moyen, ni durée de trajet, ni commentaire.**

### Différences de définition avec le TGV

- Même seuil composite 5/10/15 min, **mais** « un train supprimé avant 16 h la veille n'est pas comptabilisé ».
  Les grèves annoncées font donc **chuter les trains programmés** au lieu de gonfler les annulations : en avril 2018,
  le taux d'annulation Intercités est de 0,8 % (contre 32,7 % pour le TGV), mais les programmés baissent de 60 % par
  rapport à avril 2017 (→ 05). **Les taux d'annulation TGV et Intercités ne sont pas comparables.**
- La sélection de liaisons est faite par l'AQST, et « des trains Intercités peuvent effectuer une partie importante
  de leur trajet sous service TER : ils sont alors comptés dans le TER » (description du portail).

### Liaisons et libellés

- **97 libellés orientés** sur toute la période ; **32 orientés sur les 12 derniers mois** (16 non orientées une fois
  les libellés normalisés). Le nombre de liaisons publiées par mois passe par paliers : 50 (2014–mi-2016), 65
  (mi-2016–2017), 46 (2018), 38 (2019), 23–24 (2020), 28 (2021), 30 (2022–2023), 32–34 (2024–2026) (→ 02).
- Trains de nuit et petites lignes : Paris ↔ Briançon, Latour-de-Carol, Cerbère, Nice, Rodez/Albi, Tarbes, Aurillac
  ont ≈ 10–30 trains par mois et par sens. Médiane depuis 2020 : 31 trains circulés par liaison-mois ; 10 % sous 14.
- **Libellés incohérents** à normaliser (→ 02) :
  - composites inversés selon le sens : `ALBI/RODEZ` ↔ `RODEZ/ALBI`, `CAHORS/BRIVE` ↔ `BRIVE/CAHORS`,
    `HENDAYE/LOURDES` ↔ `LOURDES/HENDAYE`, `CAMBRAI/MAUBEUGE` ↔ `MAUBEUGE/CAMBRAI`, `TOULOUSE-MATABIAU/CERBERE`,
    `CERBERE/TOULOUSE` ;
  - gares renommées : `ROUEN` (jusqu'en juin 2016) → `ROUEN-RIVE-DROITE` ; `LYON-PART-DIEU` (2014–2017) → `LYON`
    (depuis 2018). Rien dans les données ne dit quelle gare lyonnaise désigne `LYON` ;
  - prolongements : Toulouse – Bayonne (2018–2020) puis Toulouse – Hendaye ; `MAUBEUGE` → `MAUBEUGE/CAMBRAI` (2018).
- **Doublons** : Paris-Austerlitz ↔ Toulouse-Matabiau a **deux lignes par mois depuis janvier 2022** (53 mois),
  par exemple 81 et 28 trains programmés en janv. 2022. Aucune colonne ne les distingue. L'hypothèse « un train de
  jour et un train de nuit » est plausible (≈ 1 train par jour pour la petite ligne) mais **non vérifiable** : on
  les somme.
- Correspondance des gares avec le jeu TGV : seuls 11 libellés Intercités, une fois la ponctuation retirée, existent
  aussi dans le jeu TGV (Bordeaux, Lyon Part-Dieu, Marseille, Nancy, Nantes, Nice, Paris Est, Paris Nord,
  Paris Vaugirard, Toulouse, Tours). Le rapprochement entre types de train passe par le référentiel des gares (§ 6).

### Valeurs particulières

161 lignes ont 0 train circulé (dont 158 à 0 programmé), surtout 2016–2017, 2021 et 2023 : liaisons suspendues
(travaux, COVID). Le taux affiché est alors 0 %, ce qui est **faux** et doit être traité comme manquant.

---

## 5. TER (par région)

### Contenu

| Colonne | Sens |
|---|---|
| `date` | 164 mois, janv. 2013 → août 2026, sans mois manquant |
| `region` | **libellé de région ou de lot** (31 libellés distincts) |
| `nombre_de_trains_programmes`, `_ayant_circule`, `_annules`, `_en_retard_a_l_arrivee` | comptes de trains |
| `taux_de_regularite`, `nombre_de_trains_a_l_heure_pour_un_train_en_retard_a_l_arrivee` | taux dérivés |
| `commentaires` | texte libre, renseigné de 2013 à 2019 uniquement (926 lignes) |

- Seuil **fixe de 5 min** au terminus, quelle que soit la durée du trajet. Comme pour Intercités, les trains
  supprimés avant 16 h la veille ne sont pas comptés.
- **Aucun détail par ligne ni par gare** : agrégat de tous les TER d'une région.

### Pièges

- Libellés de région qui changent avec la réforme territoriale (→ 03) : 20 libellés par mois de 2013 à 2016,
  18 en 2017, 11 de 2018 à 2024, 14 depuis 2025. La transition n'est pas propre :
  - Grand Est dès 2017, mais Hauts-de-France, Normandie, Auvergne-Rhône-Alpes et Bourgogne-Franche-Comté en 2018 ;
  - `Midi Pyrénées` jusqu'en juin 2018, `Occitanie` à partir de juillet 2018, et `Languedoc Roussillon` s'arrête en
    déc. 2017 : **trou de 6 mois pour la partie Languedoc** ;
  - `Aquitaine` jusqu'en août 2020, `Nouvelle Aquitaine` à partir de sept. 2020, alors que `Limousin` et
    `Poitou Charentes` s'arrêtent en déc. 2017 : **Limousin et Poitou-Charentes absents de 2018 à août 2020** ;
  - `Centre` devient `Centre Val-de-Loire` en sept. 2020 (simple renommage).
- Depuis janvier 2025, trois libellés qui **ne sont pas des régions** : `Etoile Amiens`, `Loire Océan`, `Sud Azur`
  (20 mois chacun). Les données ne disent pas à quoi ils correspondent ni s'ils sont retirés des régions voisines.
  Ce sont vraisemblablement des lots de lignes ouverts à la concurrence, **non vérifié**.
- `Lorraine` 2013–2015 (35 mois) et `Nord Pas de Calais` (2 mois) : tous les comptes sont vides.
- **Programmés − annulés ≠ circulés** dans 343 lignes, et dans presque toutes depuis 2025 (165 lignes sur 168 en
  2025, 111 sur 112 en 2026). Exemple : Auvergne-Rhône-Alpes, août 2026 : 38 215 − 1 003 = 37 212, mais 37 568
  circulés (+356). Les suppressions partielles sont peut-être comptées à la fois comme annulées et comme
  circulées : **non documenté**. Le taux de régularité reste cohérent avec circulés et retards (13 écarts > 0,05 point
  sur 2 380 lignes, tous en janv. 2020 et déc. 2020).
- Les commentaires 2013–2018 mentionnent régulièrement les grèves (→ 03) : utiles pour annoter le passé, absents
  depuis 2020.

Régularité TER nationale (somme des régions) : 90,6 à 93,0 % par an ; sur les 12 derniers mois, de 84,9 %
(Occitanie) à 94,6 % (Loire Océan).

---

## 6. Référentiels de gares et rattachement aux régions

### Gares de voyageurs (SNCF Gares & Connexions)

2 792 gares, sans doublon de nom : `nom`, trigramme, segment DRG (A = gares nationales, 134 gares ; B ; C),
**position (lat, lon)**, **code INSEE de la commune** et codes UIC (plusieurs codes pour certaines gares). Aucune
valeur manquante. La région se déduit du code INSEE (département = 2 premiers caractères), via une table
département → région (COG INSEE) intégrée au script (→ 04). Toutes les gares tombent dans une région
métropolitaine.

### Taux de correspondance des noms (→ 04)

Méthode : normalisation (majuscules, sans accent ni ponctuation, `ST` → `SAINT`, suffixe `VILLE` et parenthèses
retirés), puis égalité exacte, puis « tous les mots du libellé source sont dans le nom du référentiel » (en
privilégiant les gares de segment A).

| Source | Gares (libellés composites découpés) | Exact | Mots inclus | Non rattachées |
|---|---|---|---|---|
| TGV | 59 | 41 (69 %) | 8 (14 %) | 10 (17 %) |
| Intercités | 52 | 40 (77 %) | 11 (21 %) | 1 (2 %) |

- TGV non rattachées : **8 gares étrangères ou pseudo-gares** (Barcelona, Francfort, Genève, Italie, Lausanne,
  Madrid, Stuttgart, Zurich), plus `VALENCE ALIXAN TGV` et `PARIS VAUGIRARD`. Ces deux-là se résolvent avec la
  « Liste des gares » de SNCF Réseau, qui donne la commune et le code UIC : `Valence-TGV` (commune d'Alixan,
  UIC 87763029) = « Valence TGV Rhône-Alpes Sud » ; `Paris-Vaugirard` (UIC 87391102) = un des codes UIC de
  « Paris Montparnasse ». **Toutes les gares françaises sont donc rattachables (51 sur 51 pour le TGV)**, avec une
  table de correspondance manuelle courte.
- Intercités : `PARIS-VAUGIRARD` se résout de la même façon.
- **Ambiguïtés à trancher à la main**, car la ville a plusieurs grandes gares : `LILLE` (Europe ou Flandres : les
  TGV Paris – Lille partent généralement de Lille Flandres, les TGV vers le sud de Lille Europe ; les données ne le
  disent pas), `MONTPELLIER` (Saint-Roch ou Sud de France), `NIMES` (centre ou Pont du Gard), `LYON` dans le jeu
  Intercités (le script a choisi Perrache par défaut, sans justification). **La région n'en dépend pas** ; seule la
  position sur une éventuelle carte en dépend.
- Répartition des 61 liaisons TGV actuelles (→ 04, Valence TGV ajoutée à la main) : 53 touchent l'Île-de-France ;
  **7 touchent une gare étrangère** (Barcelone, Francfort, Genève, « Italie », Lausanne, Stuttgart, Zurich) ;
  Auvergne-Rhône-Alpes 12, Provence-Alpes-Côte d'Azur 9, Hauts-de-France 8, Grand Est 6, Bretagne 6, etc.

---

## 7. Définitions « à l'heure » : ce qui est comparable

| Type | Seuil « à l'heure » au terminus | Trains supprimés la veille avant 16 h | Granularité |
|---|---|---|---|
| TGV | < 5 min (< 1 h 30), < 10 min (1 h 30–3 h), < 15 min (> 3 h) | non précisé ; les données suggèrent qu'une partie n'est pas comptée (déc. 2019) | liaison orientée |
| Intercités | idem TGV | **non comptés** | liaison orientée |
| TER | **< 5 min** fixe | **non comptés** | région |

Conséquences :

- **TGV et Intercités ont la même définition du retard** : comparer leurs régularités est défendable, avec une
  réserve pour les liaisons de durée différente (le seuil dépend de la durée).
- **Leurs taux d'annulation ne sont pas comparables** (une annonce la veille efface le train côté Intercités).
- Le **TER** est plus exigeant (5 min même pour 3 h de trajet) et agrégé par région : **il ne doit jamais être
  classé avec les liaisons**. Une section séparée « Régions TER » est possible.
- Mesure : la minute est arrondie à la minute inférieure ; capteurs à l'entrée en gare (description du portail).

---

## 8. Événements visibles dans les données

Rapport détaillé : `pipeline/explore/sorties/05_evenements.md`.

| Événement | Ce qu'on voit | Utilisable ? |
|---|---|---|
| **Grève du printemps 2018** (avril–juin) | TGV : 32,7 % puis 24,5 % et 15,1 % d'annulations ; Intercités : programmés −60 % ; TER : programmés −39 % ; commentaires TER (« mouvement social ») | Oui, par les annulations TGV et la chute des programmés |
| **Grève des retraites** (déc. 2019 – janv. 2020) | TGV : prévus divisés par 2 en déc. (15 633), 16 % d'annulations ; Intercités : −69 % de programmés ; TER : −65 % | Oui |
| **COVID-19** | Avril 2020 : 3 325 trains TGV prévus (−90 %), 61 % d'annulations, 50 liaisons à 0 prévu ; Intercités : 4 liaisons publiées ; nov. 2020 et avril 2021 : nouvelles chutes (2e et 3e confinements). La régularité **monte** (93,9 % TGV en avril 2021) parce qu'il y a peu de trains | Oui ; à exclure des tendances et de « Mon trajet » |
| **Grèves de fin 2022 et réforme des retraites 2023** | TGV : 11,3 % d'annulations en déc. 2022, 23,3 % en mars 2023 ; Intercités : programmés −49 % en mars 2023 ; TER −37 % | Oui |
| **Transfert des Intercités Normandie vers TER** (1er janv. 2020) | Les 14 liaisons Intercités normandes encore publiées s'arrêtent toutes en déc. 2019 ; TER Normandie passe d'≈ 8 200 trains programmés par mois (sept.–oct. 2019) à 10 373 en févr. 2020 (+≈ 2 100, du même ordre que les ≈ 2 700 trains Intercités normands programmés par mois en sept.–nov. 2019) | Oui : fin de série à annoter |
| Été | Régularité la plus basse en juin–juillet (TGV −2,4 et −4,1 points vs la moyenne annuelle), puis novembre | Saisonnalité nette, voir § 9 |

Aucun champ ne signale explicitement une grève depuis 2020 (les commentaires TER s'arrêtent en 2019, ceux du TGV en
2019). **La détection automatique est possible par anomalie** (annulations TGV > 5 %, ou programmés Intercités/TER
en chute de plus de 20 % sur un an), mais elle mélange grèves, COVID et travaux : **une annotation manuelle
(`data/events.yaml`) est nécessaire** pour nommer les événements.

---

## 9. Faisabilité des fonctionnalités visées

| Fonctionnalité | Verdict | Justification |
|---|---|---|
| Classement des liaisons TGV | **Faisable** | 61 liaisons non orientées actuelles, 105 mois sans trou, comptes de trains complets |
| Classement des liaisons Intercités | **Faisable** | 16 liaisons non orientées actuelles, 149 mois ; libellés à normaliser, doublons à sommer |
| Classement commun TGV + Intercités | **Partiellement faisable** | Même seuil de retard, mais annulations non comparables et pas de gravité Intercités : seulement sur la régularité, ou avec un avertissement |
| Filtre par type de train | **Faisable** | |
| Filtre par région | **Faisable** | Toutes les gares françaises rattachées (2 par table manuelle) ; une liaison appartient aux régions de ses deux extrémités ; 7 liaisons TGV ont une extrémité étrangère (filtre « International ») |
| Filtre par période (12 mois glissants, année, tout, mois précis) | **Faisable** | Données mensuelles ; décalage de publication d'1 mois (TGV) à 2 mois ou plus (Intercités) |
| Fiche liaison : score, historique | **Faisable** | Séries mensuelles par sens |
| Fiche liaison : causes de retard | **Partiellement faisable** | TGV seulement ; 80 liaisons-mois sans cause (surtout l'international en 2018) ; **rupture de nomenclature en mai 2026** |
| Fiche liaison : gravité (> 15 / 30 / 60 min) | **Partiellement faisable** | TGV seulement ; janv.–mars 2025 inexploitables pour > 30 et > 60 |
| Score avec régularité + annulations + gravité | **Faisable pour le TGV**, **partiellement pour Intercités** (pas de gravité) | Voir PLAN.md |
| Rétrécissement bayésien | **Faisable** | Comptes de trains disponibles ; forte corrélation des retards au sein d'un mois (surdispersion ≈ 9 pour le TGV, → 06) à prendre en compte |
| Causes dans le temps (agrégées) | **Partiellement faisable** | TGV seulement, pondération par les trains en retard ; série coupée en mai 2026 |
| Tendances (dégradation / amélioration) | **Faisable** | Au moins 24 mois pour toutes les liaisons actuelles ; il faut comparer aussi à l'évolution du réseau entier (→ 07) |
| Saisonnalité | **Faisable** | 8 années (TGV), 12 (Intercités) |
| Grèves | **Partiellement faisable** | Visibles par anomalies, jamais nommées depuis 2020 → `data/events.yaml` manuel |
| « Mon trajet » (départ, arrivée, mois → probabilité d'être à l'heure) | **Partiellement faisable** | Seulement pour les **paires présentes** dans les jeux (≈ 61 TGV + 16 Intercités non orientées) ; aucune donnée par train, horaire ou gare intermédiaire. Un trajet Paris → Valence passe par la liaison Paris – Valence TGV, mais Paris → Orange n'existe pas |
| Page statistiques globales | **Faisable** | `tgv_national`, `tgv_axes`, sommes Intercités et TER |
| Classement des régions TER | **Faisable (v2)** | 14 entités actuelles ; historique cassé par la réforme territoriale ; trois lots non régionaux depuis 2025 |
| Transilien | **Hors périmètre** | Comme demandé (jeu disponible mais métrique différente) |
| Petite carte sur la fiche | **Faisable** | Coordonnées des gares françaises dans le référentiel ; gares étrangères sans coordonnées (à saisir à la main si besoin) |
| Méthodologie / licence | **Faisable** | Tous les jeux sont sous ODbL ; éditeurs SNCF Voyageurs, Gares & Connexions, SNCF Réseau |

Ce que les données **ne permettent pas** : la régularité par train, par horaire ou par gare intermédiaire ; la part
OUIGO / INOUI d'une liaison ; les causes et la gravité Intercités ; les causes TER ; les annulations décidées la
veille côté Intercités et TER ; la nature exacte des lots TER 2025 ; la gare lyonnaise de l'Intercités « LYON ».
