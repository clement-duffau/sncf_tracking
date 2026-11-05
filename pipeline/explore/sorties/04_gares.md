# Exploration — rattachement des gares au référentiel et aux régions

_Généré par `pipeline/explore/04_gares.py`._

## Référentiel « Gares de voyageurs » (Gares & Connexions)

### Volumes

| gares | noms_distincts | noms_normalises_distincts | sans_coordonnees | sans_insee | segment_A |
|---|---|---|---|---|---|
| 2792 | 2792 | 2792 | 0 | 0 | 134 |

### Gares dont le département n'est pas rattaché à une région métropolitaine

| dep | gares | exemple |
|---|---|---|

## Taux de correspondance

### Par source et méthode (unités = gares, libellés composites découpés)

| source | methode | gares | pct |
|---|---|---|---|
| Intercités | exact | 40 | 76.9 |
| Intercités | manuel (UIC) | 1 | 1.9 |
| Intercités | mots inclus | 11 | 21.2 |
| TGV | exact | 41 | 69.5 |
| TGV | manuel (UIC) | 2 | 3.4 |
| TGV | mots inclus | 8 | 13.6 |
| TGV | non rattaché | 8 | 13.6 |

### Correspondances obtenues par « mots inclus » (à valider à la main)

| source | libelle_source | gare_referentiel | jaro_winkler |
|---|---|---|---|
| Intercités | BOULOGNE-VILLE | Boulogne-sur-Mer | 0.9 |
| Intercités | BRIVE | Brive-la-Gaillarde | 0.86 |
| Intercités | CHERBOURG | Cherbourg-en-Cotentin | 0.89 |
| Intercités | LATOUR-DE-CAROL | Latour-de-Carol - Enveitg | 0.93 |
| Intercités | LIMOGES | Limoges Bénédictins | 0.87 |
| Intercités | LYON | Lyon Perrache | 0.86 |
| Intercités | PARIS-BERCY | Paris Bercy Bourgogne - Pays d'Auvergne | 0.86 |
| Intercités | PARIS-NORD | Paris Gare du Nord | 0.87 |
| Intercités | ROUEN | Rouen Rive Droite | 0.86 |
| Intercités | ST-GERVAIS | Saint-Gervais-les-Bains Le Fayet | 0.88 |
| Intercités | TOULOUSE | Toulouse Matabiau | 0.89 |
| TGV | BELLEGARDE (AIN) | Bellegarde-sur-Valserine | 0.88 |
| TGV | LE CREUSOT MONTCEAU MONTCHANIN | Le Creusot - Montceau-les-Mines - Montchanin TGV | 0.92 |
| TGV | LILLE | Lille Europe | 0.88 |
| TGV | MACON LOCHE | Mâcon Loché TGV | 0.95 |
| TGV | MARNE LA VALLEE | Marne-la-Vallée Chessy | 0.94 |
| TGV | MONTPELLIER | Montpellier Saint-Roch | 0.9 |
| TGV | PARIS LYON | Paris Gare de Lyon | 0.91 |
| TGV | PARIS NORD | Paris Gare du Nord | 0.87 |

### Gares non rattachées

| source | morceau |
|---|---|
| TGV | BARCELONA |
| TGV | FRANCFORT |
| TGV | GENEVE |
| TGV | ITALIE |
| TGV | LAUSANNE |
| TGV | MADRID |
| TGV | STUTTGART |
| TGV | ZURICH |

### Villes ayant plusieurs gares de segment A dans le référentiel (ambiguïté possible du libellé source)

| ville | gares |
|---|---|
| AVIGNON | Avignon Centre ; Avignon TGV |
| BESANCON | Besançon Franche-Comté TGV ; Besançon Viotte |
| LILLE | Lille Europe ; Lille Flandres |
| LYON | Lyon Part Dieu ; Lyon Perrache ; Lyon Saint-Exupéry TGV |
| MONTPELLIER | Montpellier Saint-Roch ; Montpellier Sud de France |
| NIMES | Nîmes ; Nîmes Pont du Gard |
| PARIS | Paris Austerlitz ; Paris Bercy Bourgogne - Pays d'Auvergne ; Paris Est ; Paris Gare de Lyon ; Paris Gare du Nord ; Paris Montparnasse ; Paris Saint-Lazare |
| VALENCE | Valence ; Valence TGV Rhône-Alpes Sud |

### Correspondances exactes (contrôle)

| source | libelle_source | gare_referentiel |
|---|---|---|
| Intercités | ALBI | Albi |
| Intercités | AMIENS | Amiens |
| Intercités | AURILLAC | Aurillac |
| Intercités | BAYONNE | Bayonne |
| Intercités | BELFORT | Belfort |
| Intercités | BORDEAUX-ST-JEAN | Bordeaux Saint-Jean |
| Intercités | BOURG-ST-MAURICE | Bourg-Saint-Maurice |
| Intercités | BOURGES | Bourges |
| Intercités | BRIANÇON | Briançon |
| Intercités | BÉZIERS | Béziers |
| Intercités | CAEN | Caen |
| Intercités | CAHORS | Cahors |
| Intercités | CAMBRAI | Cambrai |
| Intercités | CERBERE | Cerbère |
| Intercités | CLERMONT-FERRAND | Clermont-Ferrand |
| Intercités | GRANVILLE | Granville |
| Intercités | HENDAYE | Hendaye |
| Intercités | LE HAVRE | Le Havre |
| Intercités | LOURDES | Lourdes |
| Intercités | LYON-PART-DIEU | Lyon Part Dieu |
| Intercités | MARSEILLE-ST-CHARLES | Marseille Saint-Charles |
| Intercités | MAUBEUGE | Maubeuge |
| Intercités | MODANE | Modane |
| Intercités | NANCY | Nancy |
| Intercités | NANTES | Nantes |
| Intercités | NEVERS | Nevers |
| Intercités | NICE-VILLE | Nice |
| Intercités | NÎMES | Nîmes |
| Intercités | ORLÉANS | Orléans |
| Intercités | PARIS-AUSTERLITZ | Paris Austerlitz |
| Intercités | PARIS-EST | Paris Est |
| Intercités | PARIS-ST-LAZARE | Paris Saint-Lazare |
| Intercités | RODEZ | Rodez |
| Intercités | ROUEN-RIVE-DROITE | Rouen Rive Droite |
| Intercités | ST-QUENTIN | Saint-Quentin |
| Intercités | TARBES | Tarbes |
| Intercités | TOULOUSE-MATABIAU | Toulouse Matabiau |
| Intercités | TOURS | Tours |
| Intercités | TROUVILLE-DEAUVILLE | Trouville - Deauville |
| Intercités | TROYES | Troyes |
| TGV | AIX EN PROVENCE TGV | Aix-en-Provence TGV |
| TGV | ANGERS SAINT LAUD | Angers Saint-Laud |
| TGV | ANGOULEME | Angoulême |
| TGV | ANNECY | Annecy |
| TGV | ARRAS | Arras |
| TGV | AVIGNON TGV | Avignon TGV |
| TGV | BESANCON FRANCHE COMTE TGV | Besançon Franche-Comté TGV |
| TGV | BORDEAUX ST JEAN | Bordeaux Saint-Jean |
| TGV | BREST | Brest |
| TGV | CHAMBERY CHALLES LES EAUX | Chambéry - Challes-les-Eaux |
| TGV | DIJON VILLE | Dijon |
| TGV | DOUAI | Douai |
| TGV | DUNKERQUE | Dunkerque |
| TGV | GRENOBLE | Grenoble |
| TGV | LA ROCHELLE VILLE | La Rochelle |
| TGV | LAVAL | Laval |
| TGV | LE MANS | Le Mans |
| TGV | LYON PART DIEU | Lyon Part Dieu |
| TGV | MARSEILLE ST CHARLES | Marseille Saint-Charles |
| TGV | METZ | Metz |
| TGV | MULHOUSE VILLE | Mulhouse |
| TGV | NANCY | Nancy |
| TGV | NANTES | Nantes |
| TGV | NICE VILLE | Nice |
| TGV | NIMES | Nîmes |
| TGV | PARIS EST | Paris Est |
| TGV | PARIS MONTPARNASSE | Paris Montparnasse |
| TGV | PERPIGNAN | Perpignan |
| TGV | POITIERS | Poitiers |
| TGV | QUIMPER | Quimper |
| TGV | REIMS | Reims |
| TGV | RENNES | Rennes |
| TGV | SAINT ETIENNE CHATEAUCREUX | Saint-Étienne Châteaucreux |
| TGV | ST MALO | Saint-Malo |
| TGV | ST PIERRE DES CORPS | Saint-Pierre-des-Corps |
| TGV | STRASBOURG | Strasbourg |
| TGV | TOULON | Toulon |
| TGV | TOULOUSE MATABIAU | Toulouse Matabiau |
| TGV | TOURCOING | Tourcoing |
| TGV | TOURS | Tours |
| TGV | VANNES | Vannes |

## Résolution des 2 gares françaises non rattachées via « Liste des gares » (SNCF Réseau, codes UIC)

### Valence TGV (commune d'Alixan) et Paris-Vaugirard : code UIC puis gare de voyageurs correspondante

| libelle_reseau | commune | departemen | code_uic | gare_voyageurs | codes_uic |
|---|---|---|---|---|---|
| Paris-Vaugirard | PARIS | PARIS | 87391102 | Paris Montparnasse | 87391003;87391011;87391102 |
| Valence-TGV | ALIXAN | DROME | 87763029 | Valence TGV Rhône-Alpes Sud | 87763029 |

## Régions des liaisons (12 derniers mois)

### Régions des gares TGV rattachées

| region | gares | liste |
|---|---|---|
| Auvergne-Rhône-Alpes | 7 | ANNECY, BELLEGARDE (AIN), CHAMBERY CHALLES LES EAUX, GRENOBLE, LYON PART DIEU, SAINT ETIENNE CHATEAUCREUX, VALENCE ALIXAN TGV |
| Bourgogne-Franche-Comté | 4 | BESANCON FRANCHE COMTE TGV, DIJON VILLE, LE CREUSOT MONTCEAU MONTCHANIN, MACON LOCHE |
| Bretagne | 5 | BREST, QUIMPER, RENNES, ST MALO, VANNES |
| Centre-Val de Loire | 2 | ST PIERRE DES CORPS, TOURS |
| Grand Est | 5 | METZ, MULHOUSE VILLE, NANCY, REIMS, STRASBOURG |
| Hauts-de-France | 5 | ARRAS, DOUAI, DUNKERQUE, LILLE, TOURCOING |
| Nouvelle-Aquitaine | 4 | ANGOULEME, BORDEAUX ST JEAN, LA ROCHELLE VILLE, POITIERS |
| Occitanie | 4 | MONTPELLIER, NIMES, PERPIGNAN, TOULOUSE MATABIAU |
| Pays de la Loire | 4 | ANGERS SAINT LAUD, LAVAL, LE MANS, NANTES |
| Provence-Alpes-Côte d'Azur | 5 | AIX EN PROVENCE TGV, AVIGNON TGV, MARSEILLE ST CHARLES, NICE VILLE, TOULON |
| Île-de-France | 6 | MARNE LA VALLEE, PARIS EST, PARIS LYON, PARIS MONTPARNASSE, PARIS NORD, PARIS VAUGIRARD |
|  | 8 | BARCELONA, FRANCFORT, GENEVE, ITALIE, LAUSANNE, MADRID, STUTTGART, ZURICH |

### Régions des gares Intercités rattachées

| region | gares | liste |
|---|---|---|
| Auvergne-Rhône-Alpes | 7 | AURILLAC, BOURG-ST-MAURICE, CLERMONT-FERRAND, LYON, LYON-PART-DIEU, MODANE, ST-GERVAIS |
| Bourgogne-Franche-Comté | 2 | BELFORT, NEVERS |
| Centre-Val de Loire | 3 | BOURGES, ORLÉANS, TOURS |
| Grand Est | 2 | NANCY, TROYES |
| Hauts-de-France | 5 | AMIENS, BOULOGNE-VILLE, CAMBRAI, MAUBEUGE, ST-QUENTIN |
| Normandie | 7 | CAEN, CHERBOURG, GRANVILLE, LE HAVRE, ROUEN, ROUEN-RIVE-DROITE, TROUVILLE-DEAUVILLE |
| Nouvelle-Aquitaine | 5 | BAYONNE, BORDEAUX-ST-JEAN, BRIVE, HENDAYE, LIMOGES |
| Occitanie | 11 | ALBI, BÉZIERS, CAHORS, CERBERE, LATOUR-DE-CAROL, LOURDES, NÎMES, RODEZ, TARBES, TOULOUSE, TOULOUSE-MATABIAU |
| Pays de la Loire | 1 | NANTES |
| Provence-Alpes-Côte d'Azur | 3 | BRIANÇON, MARSEILLE-ST-CHARLES, NICE-VILLE |
| Île-de-France | 6 | PARIS-AUSTERLITZ, PARIS-BERCY, PARIS-EST, PARIS-NORD, PARIS-ST-LAZARE, PARIS-VAUGIRARD |

### Nombre de liaisons TGV (non orientées, 12 derniers mois) touchant chaque région

| region | liaisons |
|---|---|
| Île-de-France | 53 |
| Auvergne-Rhône-Alpes | 12 |
| Provence-Alpes-Côte d'Azur | 9 |
| Hauts-de-France | 8 |
|  | 7 |
| Bretagne | 6 |
| Grand Est | 6 |
| Nouvelle-Aquitaine | 5 |
| Occitanie | 5 |
| Pays de la Loire | 5 |
| Bourgogne-Franche-Comté | 4 |
| Centre-Val de Loire | 2 |

