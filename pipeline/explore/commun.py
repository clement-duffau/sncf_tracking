"""Outils communs aux scripts d'exploration (phase 1).

Chaque script d'exploration ouvre une connexion DuckDB en mémoire où chaque
fichier `data/raw/<cle>.parquet` est exposé comme une vue `<cle>`, puis écrit
un rapport Markdown dans `pipeline/explore/sorties/<script>.md`.

Les rapports sont versionnés : ce sont les « preuves » chiffrées citées dans
docs/DATA.md et docs/PLAN.md.
"""

from __future__ import annotations

import math
from datetime import date, datetime
from pathlib import Path

import duckdb

RACINE = Path(__file__).resolve().parents[2]
RAW = RACINE / "data" / "raw"
SORTIES = Path(__file__).resolve().parent / "sorties"


def connexion() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    for f in sorted(RAW.glob("*.parquet")):
        con.sql(f"create view {f.stem} as select * from read_parquet('{f.as_posix()}')")
    return con


def _cellule(v) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return ""
    if isinstance(v, float):
        return f"{v:.2f}".rstrip("0").rstrip(".") if abs(v) < 1e6 else f"{v:.0f}"
    if isinstance(v, (date, datetime)):
        return v.isoformat()[:10]
    return str(v).replace("|", "\\|").replace("\n", " ")


class Rapport:
    """Accumule des sections Markdown et les écrit (et les affiche)."""

    def __init__(self, nom: str, titre: str, con: duckdb.DuckDBPyConnection):
        self.nom, self.con = nom, con
        self.lignes: list[str] = [f"# {titre}", "", "_Généré par `pipeline/explore/" + nom + ".py`._", ""]

    def section(self, titre: str) -> None:
        self.lignes += [f"## {titre}", ""]

    def texte(self, t: str) -> None:
        self.lignes += [t, ""]

    def table(self, titre: str, sql: str, max_lignes: int = 200):
        """Exécute sql, ajoute le résultat en tableau Markdown et le renvoie."""
        rel = self.con.sql(sql)
        cols = rel.columns
        rows = rel.fetchall()
        self.lignes += [f"### {titre}", ""]
        self.lignes.append("| " + " | ".join(cols) + " |")
        self.lignes.append("|" + "---|" * len(cols))
        for r in rows[:max_lignes]:
            self.lignes.append("| " + " | ".join(_cellule(v) for v in r) + " |")
        if len(rows) > max_lignes:
            self.lignes.append(f"\n… {len(rows) - max_lignes} lignes supplémentaires non affichées.")
        self.lignes.append("")
        return rows

    def ecrire(self) -> Path:
        SORTIES.mkdir(exist_ok=True)
        p = SORTIES / f"{self.nom}.md"
        p.write_text("\n".join(self.lignes) + "\n", encoding="utf-8")
        print("\n".join(self.lignes))
        print(f"\n→ écrit dans {p.relative_to(RACINE)}")
        return p
