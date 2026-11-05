"""Téléchargement depuis l'API Explore v2.1 du portail SNCF, avec reprises.

Pour chaque jeu : métadonnées (`<cle>.meta.json` : date de mise à jour, schéma) puis exports
(`<cle>.parquet`, `<cle>.csv`) dans data/raw/. Le portail (ou le réseau) coupe parfois la connexion
à l'ouverture : chaque requête est retentée, avec une durée maximale par essai.
"""

from __future__ import annotations

import json
import signal
import sys
import time
from pathlib import Path

import requests

from . import config

ESSAIS = 40
PAUSE_S = 2
DUREE_MAX_ESSAI_S = 180


class EssaiTropLong(Exception):
    pass


def _alarme(signum, frame):  # pragma: no cover - dépend du réseau
    raise EssaiTropLong()


def _get(url: str, dest: Path | None = None) -> bytes | None:
    """GET avec reprises. Écrit dans dest (via un .part) ou renvoie le contenu."""
    erreur: Exception | None = None
    alarme = hasattr(signal, "SIGALRM")
    for essai in range(1, ESSAIS + 1):
        if alarme:
            signal.signal(signal.SIGALRM, _alarme)
            signal.alarm(DUREE_MAX_ESSAI_S)
        try:
            with requests.get(url, stream=True, timeout=(20, 60)) as r:
                r.raise_for_status()
                if dest is None:
                    return r.content
                tmp = dest.with_suffix(dest.suffix + ".part")
                with open(tmp, "wb") as f:
                    for bloc in r.iter_content(1 << 16):
                        f.write(bloc)
                tmp.replace(dest)
                print(f"  OK  {dest.name} ({dest.stat().st_size:,} o, essai {essai})".replace(",", " "))
                return None
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code < 500:
                raise
            erreur = e
        except (requests.RequestException, EssaiTropLong) as e:
            erreur = e
        finally:
            if alarme:
                signal.alarm(0)
        time.sleep(PAUSE_S)
    raise RuntimeError(f"Échec du téléchargement de {url} après {ESSAIS} essais : {erreur}")


def metadonnees(ident: str) -> dict:
    """Métadonnées d'un jeu (quelques Ko) : metas.default.data_processed, records_count, fields…"""
    return json.loads(_get(f"{config.API}/{ident}"))


def telecharger(cles: list[str] | None = None, raw: Path = config.RAW,
                jeux: dict | None = None, formats: tuple[str, ...] | None = None) -> dict[str, dict]:
    """Télécharge métadonnées et exports ; renvoie {cle: métadonnées}."""
    jeux = jeux or config.JEUX
    raw.mkdir(parents=True, exist_ok=True)
    metas = {}
    for cle in cles or list(jeux):
        ident, _editeur, fmts = jeux[cle]
        print(f"[{cle}] {ident}")
        meta = metadonnees(ident)
        (raw / f"{cle}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
        metas[cle] = meta
        for fmt in formats or fmts:
            suffixe = "csv?delimiter=%3B" if fmt == "csv" else fmt
            _get(f"{config.API}/{ident}/exports/{suffixe}", raw / f"{cle}.{fmt}")
    return metas


def metas_locales(raw: Path = config.RAW) -> dict[str, dict]:
    """Métadonnées déjà téléchargées (mode hors ligne)."""
    metas = {}
    for cle in config.JEUX:
        p = raw / f"{cle}.meta.json"
        if not p.exists():
            sys.exit(f"Mode hors ligne : {p} manquant. Lancez d'abord `python -m pipeline build`.")
        metas[cle] = json.loads(p.read_text())
    return metas
