"""Chargement des fichiers bruts dans DuckDB (une vue par jeu)."""

from __future__ import annotations

from pathlib import Path

import duckdb

from . import config, schemas


def connexion(raw: Path = config.RAW) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    for cle, (_ident, _editeur, formats) in config.JEUX.items():
        if "parquet" in formats:
            f = raw / f"{cle}.parquet"
            source = f"read_parquet('{f.as_posix()}')"
        else:
            f = raw / f"{cle}.csv"
            source = f"read_csv('{f.as_posix()}', delim = ';', header = true, all_varchar = true)"
        if not f.exists():
            raise schemas.ErreurSource(f"Fichier {f} manquant")
        con.sql(f"create or replace view {cle} as select * from {source}")
        schemas.verifier_table(con, cle)
    return con
