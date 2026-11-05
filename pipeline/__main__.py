"""Point d'entrée du pipeline.

    python -m pipeline build                 télécharge les jeux SNCF et produit site/public/data/
    python -m pipeline build --hors-ligne    réutilise data/raw/ sans réseau
    python -m pipeline verifier              y a-t-il de nouvelles données depuis le dernier build ?
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

from . import checks, clean, config, events, export, fetch, gares, load, score, trends
from .events import ErreurEvenements
from .gares import ErreurGare
from .schemas import ErreurSource


def _avertir(msg: str) -> None:
    prefixe = "::warning::" if os.environ.get("GITHUB_ACTIONS") else "AVERTISSEMENT : "
    print(prefixe + msg)


def build(args) -> None:
    t0 = time.time()
    metas = fetch.metas_locales() if args.hors_ligne else fetch.telecharger()
    lock = checks.lire_lock()
    for msg in checks.verifier_metas(metas, lock):
        _avertir(msg)

    con = load.connexion()
    checks.verifier_donnees(con, lock)
    evts = events.charger()
    for msg in events.candidats_non_annotes(con, evts):
        _avertir(f"mois anormal non annoté dans data/events.yaml — {msg}")

    gares.construire(con)
    clean.construire(con, evts)
    clean.verifier_doublons(con)
    pers = score.construire(con)
    trends.construire(con, evts)
    tailles = export.exporter(con, evts, metas, pers, Path(args.sortie))
    if not args.sans_lock:
        checks.ecrire_lock(metas, con)

    n_liaisons = len([f for f in tailles if f.startswith("liaison/")])
    print(f"\n{len(tailles)} fichiers écrits dans {args.sortie} ({n_liaisons} fiches liaison) :")
    for f, t in tailles.items():
        if not f.startswith("liaison/"):
            print(f"  {f:32} {t / 1024:8.1f} Ko")
    print(f"  liaison/*.json                   {sum(t for f, t in tailles.items() if f.startswith('liaison/')) / 1024:8.1f} Ko au total")
    print(f"Terminé en {time.time() - t0:.1f} s.")


def verifier(args) -> None:
    """Compare la date de mise à jour de chaque jeu à data/sources.lock.json."""
    lock = checks.lire_lock()
    nouveaux = []
    for cle, (ident, _e, _f) in config.JEUX.items():
        d = fetch.metadonnees(ident)["metas"]["default"].get("data_processed")
        avant = lock.get(cle, {}).get("data_processed")
        etat = "inchangé" if d == avant else "NOUVEAU"
        print(f"{cle:16} {d}  ({etat})")
        if d != avant:
            nouveaux.append(cle)
    sortie = os.environ.get("GITHUB_OUTPUT")
    if sortie:
        with open(sortie, "a") as f:
            f.write(f"nouveau={'true' if nouveaux else 'false'}\n")
    print("Nouvelles données : " + (", ".join(nouveaux) if nouveaux else "aucune"))


def main() -> None:
    p = argparse.ArgumentParser(prog="python -m pipeline")
    sp = p.add_subparsers(dest="commande", required=True)
    b = sp.add_parser("build", help="télécharger les données et produire les fichiers du site")
    b.add_argument("--hors-ligne", action="store_true", help="réutiliser data/raw/ sans réseau")
    b.add_argument("--sortie", default=str(config.SORTIE), help="dossier de sortie (défaut : site/public/data)")
    b.add_argument("--sans-lock", action="store_true", help="ne pas mettre à jour data/sources.lock.json")
    b.set_defaults(func=build)
    v = sp.add_parser("verifier", help="détecter de nouvelles publications sans rien télécharger d'autre")
    v.set_defaults(func=verifier)
    args = p.parse_args()
    try:
        args.func(args)
    except (ErreurSource, ErreurGare, ErreurEvenements) as e:
        print(f"\nÉCHEC : {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
