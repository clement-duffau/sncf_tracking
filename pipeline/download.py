"""Téléchargement des jeux open data SNCF utilisés par le projet.

Usage :
    python pipeline/download.py            # tous les jeux
    python pipeline/download.py tgv_aqst   # un seul jeu (clé du dictionnaire DATASETS)

Pour chaque jeu, on récupère depuis l'API Opendatasoft (Explore v2.1) du portail
SNCF (https://ressources.data.sncf.com) :
  - <cle>.parquet   : export complet typé (lu directement par DuckDB) ;
  - <cle>.csv       : même export en CSV « ; » (pour inspection humaine) ;
  - <cle>.meta.json : métadonnées du jeu (licence, date de modification,
                      schéma des champs avec libellés et descriptions).

Les fichiers sont écrits dans data/raw/ (non versionné).
Le portail coupe parfois la connexion à l'ouverture : chaque requête est
retentée plusieurs fois avant d'échouer.
"""

from __future__ import annotations

import signal
import sys
import time
from pathlib import Path

import requests

BASE = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets"
RAW = Path(__file__).resolve().parent.parent / "data" / "raw"

# clé locale -> identifiant du jeu sur le portail SNCF
DATASETS = {
    "tgv_aqst": "regularite-mensuelle-tgv-aqst",          # TGV par liaison
    "tgv_axes": "regularite-mensuelle-tgv-axes",          # TGV par axe
    "tgv_national": "reglarite-mensuelle-tgv-nationale",  # TGV global (sic : « reglarite »)
    "intercites": "regularite-mensuelle-intercites",      # Intercités par liaison
    "ter": "regularite-mensuelle-ter",                    # TER par région
    "gares_voyageurs": "gares-de-voyageurs",              # référentiel gares de voyageurs
    "liste_gares": "liste-des-gares",                     # référentiel SNCF Réseau (départements)
    "temps_parcours": "meilleurs-temps-des-parcours-des-trains",
    "frequentation_gares": "frequentation-gares",
}

ESSAIS = 40
PAUSE_S = 2
DUREE_MAX_ESSAI_S = 180  # au-delà, l'essai est abandonné (connexion bloquée)


class EssaiTropLong(Exception):
    pass


def _alarme(signum, frame):
    raise EssaiTropLong()


def telecharger(url: str, dest: Path) -> None:
    """Télécharge url vers dest, avec reprises ; écrit d'abord un .part."""
    derniere_erreur: Exception | None = None
    for essai in range(1, ESSAIS + 1):
        signal.signal(signal.SIGALRM, _alarme)
        signal.alarm(DUREE_MAX_ESSAI_S)
        try:
            with requests.get(url, stream=True, timeout=(20, 60)) as r:
                r.raise_for_status()
                tmp = dest.with_suffix(dest.suffix + ".part")
                with open(tmp, "wb") as f:
                    for bloc in r.iter_content(1 << 16):
                        f.write(bloc)
                tmp.replace(dest)
                print(f"  OK  {dest.name} ({dest.stat().st_size:,} o, essai {essai})")
                return
        except requests.HTTPError as e:
            # Une erreur HTTP (404, 400…) n'est pas transitoire : on échoue tout de suite.
            if e.response is not None and e.response.status_code < 500:
                raise
            derniere_erreur = e
        except (requests.RequestException, EssaiTropLong) as e:
            derniere_erreur = e
        finally:
            signal.alarm(0)
        time.sleep(PAUSE_S)
    raise RuntimeError(f"Échec du téléchargement de {url} : {derniere_erreur}")


def main(cles: list[str]) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    for cle in cles or list(DATASETS):
        ident = DATASETS[cle]
        print(f"[{cle}] {ident}")
        telecharger(f"{BASE}/{ident}", RAW / f"{cle}.meta.json")
        telecharger(f"{BASE}/{ident}/exports/parquet", RAW / f"{cle}.parquet")
        telecharger(f"{BASE}/{ident}/exports/csv?delimiter=%3B", RAW / f"{cle}.csv")
    # Trace de la date de téléchargement (utile pour DATA.md)
    (RAW / "TELECHARGE_LE.txt").write_text(time.strftime("%Y-%m-%dT%H:%M:%S%z") + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
