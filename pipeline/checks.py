"""Contrôles de cohérence : le build échoue proprement (message explicite) si une source change.

- schéma déclaré par le portail (schemas.verifier_metadonnees) ;
- nombre d'enregistrements qui ne baisse pas de plus de 5 % par rapport au dernier build (data/sources.lock.json) ;
- dernier mois publié qui ne recule pas ;
- causes TGV qui somment à 100 % ± 2 dans au moins 95 % des lignes où elles sont renseignées.
"""

from __future__ import annotations

import json
from pathlib import Path

import duckdb

from . import config, schemas
from .schemas import ErreurSource

REQ_DERNIER_MOIS = {
    "tgv_aqst": "select max(date)::date from tgv_aqst",
    "tgv_axes": "select max(date)::date from tgv_axes",
    "tgv_national": "select max(date)::date from tgv_national",
    "intercites": "select max(date)::date from intercites",
    "ter": "select max(date)::date from ter",
}


def lire_lock(chemin: Path = config.LOCK) -> dict:
    return json.loads(chemin.read_text()) if chemin.exists() else {}


def verifier_metas(metas: dict[str, dict], lock: dict) -> list[str]:
    avertissements = []
    for cle, meta in metas.items():
        avertissements += schemas.verifier_metadonnees(cle, meta)
        m = meta["metas"]["default"]
        avant = lock.get(cle, {})
        n, n_avant = m.get("records_count"), avant.get("records_count")
        if n is not None and n_avant and n < (1 - config.BAISSE_LIGNES_MAX) * n_avant:
            raise ErreurSource(f"Jeu {cle} : {n} enregistrements contre {n_avant} au dernier build (baisse > 5 %)")
    return avertissements


def dernier_mois(con: duckdb.DuckDBPyConnection) -> dict[str, str]:
    return {cle: con.execute(req).fetchall()[0][0].isoformat()[:7] for cle, req in REQ_DERNIER_MOIS.items()}


def verifier_donnees(con: duckdb.DuckDBPyConnection, lock: dict) -> None:
    for cle, mois in dernier_mois(con).items():
        avant = lock.get(cle, {}).get("dernier_mois")
        if avant and mois < avant:
            raise ErreurSource(f"Jeu {cle} : dernier mois {mois} antérieur à celui du dernier build ({avant})")
    somme = " + ".join(f"prct_cause_{c}" for c in
                       ("externe", "infra", "gestion_trafic", "materiel_roulant", "gestion_gare", "prise_en_charge_voyageurs"))
    ok, total = con.execute(f"""
      select count(*) filter (where abs(({somme}) - 100) <= {config.CAUSES_TOLERANCE}), count(*)
      from tgv_aqst where ({somme}) > 0""").fetchall()[0]
    if total and ok / total < config.CAUSES_PART_MIN:
        raise ErreurSource(f"Jeu tgv_aqst : les causes somment à 100 % dans {ok}/{total} lignes seulement "
                           f"(minimum {config.CAUSES_PART_MIN:.0%}) — format des pourcentages changé ?")


def ecrire_lock(metas: dict[str, dict], con: duckdb.DuckDBPyConnection, chemin: Path = config.LOCK) -> dict:
    mois = dernier_mois(con)
    lock = {cle: {"data_processed": meta["metas"]["default"].get("data_processed"),
                  "records_count": meta["metas"]["default"].get("records_count"),
                  **({"dernier_mois": mois[cle]} if cle in mois else {})}
            for cle, meta in sorted(metas.items())}
    chemin.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n")
    return lock
