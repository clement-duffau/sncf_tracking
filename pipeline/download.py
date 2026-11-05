"""Téléchargement des jeux utilisés par l'exploration (phase 1), y compris les jeux annexes.

Usage :
    python pipeline/download.py            # tous les jeux (parquet + csv + métadonnées)
    python pipeline/download.py tgv_aqst   # un seul jeu

Le pipeline de production (`python -m pipeline build`) télécharge lui-même ce dont il a besoin.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline import config  # noqa: E402
from pipeline.fetch import telecharger  # noqa: E402

JEUX_EXPLORATION = {
    **{k: (v[0], v[1], ("parquet", "csv")) for k, v in config.JEUX.items()},
    "liste_gares": ("liste-des-gares", "SNCF Réseau", ("parquet", "csv")),
    "temps_parcours": ("meilleurs-temps-des-parcours-des-trains", "SNCF", ("parquet", "csv")),
    "frequentation_gares": ("frequentation-gares", "SNCF Gares & Connexions", ("parquet", "csv")),
}

if __name__ == "__main__":
    telecharger(sys.argv[1:] or None, jeux=JEUX_EXPLORATION)
