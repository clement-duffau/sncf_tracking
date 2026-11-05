"""Paramètres du pipeline : chemins, jeux de données, constantes de la méthode (voir docs/PLAN.md)."""

from __future__ import annotations

from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
RAW = RACINE / "data" / "raw"
REFS = Path(__file__).resolve().parent / "refs"
EVENEMENTS = RACINE / "data" / "events.yaml"
LOCK = RACINE / "data" / "sources.lock.json"
SORTIE = RACINE / "site" / "public" / "data"

API = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets"
PORTAIL = "https://ressources.data.sncf.com/explore/dataset"

# clé locale -> (identifiant du jeu sur le portail, éditeur, formats téléchargés)
JEUX: dict[str, tuple[str, str, tuple[str, ...]]] = {
    "tgv_aqst": ("regularite-mensuelle-tgv-aqst", "SNCF Voyageurs", ("parquet",)),
    "tgv_axes": ("regularite-mensuelle-tgv-axes", "SNCF Voyageurs", ("parquet",)),
    "tgv_national": ("reglarite-mensuelle-tgv-nationale", "SNCF Voyageurs", ("parquet",)),  # sic
    "intercites": ("regularite-mensuelle-intercites", "SNCF Voyageurs", ("parquet",)),
    "ter": ("regularite-mensuelle-ter", "SNCF Voyageurs", ("parquet",)),
    # CSV : la position y est en clair (« lat, lon »), alors que le Parquet l'encode en WKB
    "gares_voyageurs": ("gares-de-voyageurs", "SNCF Gares & Connexions", ("csv",)),
}

TYPES = ("TGV", "Intercités")
PREFIXE_TYPE = {"TGV": "tgv", "Intercités": "ic"}

# ------------------------------------------------------------------ méthode (docs/PLAN.md § 3, 5, 6)
# Surdispersion D : variance mensuelle observée / variance binomiale (médiane par liaison).
# Poids du prior M (en trains) : Bayes empirique, méthode des moments, M = m · D.
# Estimés par pipeline/explore/06_score_variantes.py sur oct. 2025 – sept. 2026 ; à recalibrer une fois par an.
SURDISPERSION = {"TGV": 9.4, "Intercités": 2.3}
POIDS_PRIOR = {"TGV": 560.0, "Intercités": 60.0}

# Barème du score V2 : points d'un train prévu selon son issue
BAREME = {"a_l_heure": 100, "retard_30": 67, "retard_30_60": 33, "retard_60": 0, "annule": 0}

FENETRE_MOIS = 12              # « 12 derniers mois »
COUVERTURE_PARTIELLE = 6       # moins de 6 mois de données sur 12 → couverture partielle
TIRAGES_INTERVALLE = 4000      # simulations pour l'intervalle à 80 % du score
GRAINE = 20261105

# Tendances
SEUIL_Z = 2.0
SEUIL_DELTA = 0.02             # 2 points de régularité
PENTE_MOIS = 36

# Saisonnalité et « Mon trajet »
SAISON_K0 = 3.0                # poids (en années) du profil du type dans le profil d'une liaison
TRAJET_ANNEES = 5              # années du même mois calendaire utilisées
TRAJET_M_EFF = 60.0            # force du prior en trains « effectifs »
TRAJET_PEU_ANNEES = 3
TRAJET_PEU_TRAINS = 100

# Contrôles de cohérence (pipeline/checks.py)
BAISSE_LIGNES_MAX = 0.05
CAUSES_TOLERANCE = 2.0         # la somme des 6 pourcentages doit valoir 100 ± 2…
CAUSES_PART_MIN = 0.95         # … dans au moins 95 % des lignes où les causes sont renseignées

VERSION_METHODE = "1.0"
