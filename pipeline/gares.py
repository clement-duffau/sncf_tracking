"""Rattachement des libellés de gares des jeux de régularité au référentiel « Gares de voyageurs ».

Règles, dans l'ordre (voir docs/DATA.md § 6) :
  1. gare étrangère ou pseudo-gare : refs/gares_etrangeres.csv ;
  2. alias manuel : refs/gares_alias.csv (cas relus à la main : ambiguïtés, noms très différents) ;
  3. égalité des noms normalisés (majuscules, sans accent ni ponctuation, ST → SAINT,
     parenthèses et suffixe « VILLE » retirés).
Un libellé qui ne passe aucune règle fait échouer le build, avec une suggestion à valider.

Les libellés Intercités composites (« BRIVE/CAHORS ») désignent une extrémité à plusieurs gares.
"""

from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

import duckdb

from . import config


class ErreurGare(Exception):
    pass


def normaliser(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().upper()
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[^A-Z0-9]+", " ", s).strip()
    s = re.sub(r"(^| )STE( |$)", r"\1SAINTE\2", s)
    s = re.sub(r"(^| )ST( |$)", r"\1SAINT\2", s)
    s = re.sub(r" VILLE$", "", s)
    return re.sub(r" +", " ", s)


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def _lire_csv(p: Path) -> list[dict]:
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _region_dep(code_insee: str, deps: dict[str, str]) -> str | None:
    dep = code_insee[:3] if code_insee.startswith("97") else code_insee[:2]
    return deps.get(dep)


def construire(con: duckdb.DuckDBPyConnection, refs: Path = config.REFS) -> None:
    """Crée les tables `gare` (une ligne par gare) et `libelle_gare` (libellé source → gare)."""
    deps = {r["dep"]: r["region"] for r in _lire_csv(refs / "departements.csv")}
    alias = {r["libelle"]: r for r in _lire_csv(refs / "gares_alias.csv")}
    etrangeres = {r["libelle"]: r for r in _lire_csv(refs / "gares_etrangeres.csv")}

    ref = {}
    for nom, insee, uic, pos in con.sql(
            "select nom, codeinsee, codes_uic, position_geographique from gares_voyageurs").fetchall():
        lat, lon = (float(x) for x in pos.split(",")) if pos else (None, None)
        ref[nom] = {"nom": nom, "insee": insee, "uic": uic, "lat": lat, "lon": lon,
                    "region": _region_dep(insee or "", deps)}
    par_norm: dict[str, list[str]] = {}
    for nom in ref:
        par_norm.setdefault(normaliser(nom), []).append(nom)

    libelles = sorted({m for (m,) in con.sql("""
        select distinct g from (select gare_depart g from tgv_aqst union select gare_arrivee from tgv_aqst)
        union
        select distinct unnest(string_split(g, '/')) from (select depart g from intercites union select arrivee from intercites)
    """).fetchall()})

    gares: dict[str, dict] = {}
    lignes, inconnus = [], []
    for lib in libelles:
        if lib in etrangeres:
            e = etrangeres[lib]
            g = {"id": slug(e["nom_affiche"]), "nom": e["nom_affiche"], "nom_referentiel": None, "uic": None,
                 "lat": float(e["lat"]) if e["lat"] else None, "lon": float(e["lon"]) if e["lon"] else None,
                 "region": None, "pays": e["pays"], "precision": "approximative", "methode": "etrangere"}
        else:
            if lib in alias:
                a = alias[lib]
                if a["gare_referentiel"] not in ref:
                    raise ErreurGare(f"refs/gares_alias.csv : « {a['gare_referentiel']} » absent du référentiel")
                r, nom, precision, methode = ref[a["gare_referentiel"]], a["nom_affiche"] or a["gare_referentiel"], a["precision"], "alias"
            else:
                cands = par_norm.get(normaliser(lib), [])
                if len(cands) != 1:
                    inconnus.append(lib)
                    continue
                r, nom, precision, methode = ref[cands[0]], cands[0], "gare", "exact"
            g = {"id": slug(nom), "nom": nom, "nom_referentiel": r["nom"], "uic": r["uic"], "lat": r["lat"],
                 "lon": r["lon"], "region": r["region"], "pays": "France", "precision": precision, "methode": methode}
        if g["id"] in gares and gares[g["id"]]["nom_referentiel"] != g["nom_referentiel"]:
            raise ErreurGare(f"Deux gares différentes ont le même identifiant « {g['id']} »")
        gares[g["id"]] = g
        lignes.append((lib, g["id"]))

    if inconnus:
        suggestions = []
        for lib in inconnus:
            mots = set(normaliser(lib).split())
            cands = sorted(n for n in ref if mots <= set(normaliser(n).split()))[:3]
            suggestions.append(f"  - « {lib} » : candidats {cands or 'aucun'}")
        raise ErreurGare("Gares non rattachées au référentiel ; ajoutez-les à pipeline/refs/gares_alias.csv "
                         "(ou gares_etrangeres.csv) :\n" + "\n".join(suggestions))

    con.sql("""create or replace table gare (id varchar primary key, nom varchar, nom_referentiel varchar,
               uic varchar, lat double, lon double, region varchar, pays varchar, precision varchar, methode varchar)""")
    con.executemany("insert into gare values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [tuple(g[k] for k in ("id", "nom", "nom_referentiel", "uic", "lat", "lon", "region", "pays",
                                           "precision", "methode")) for g in gares.values()])
    con.sql("create or replace table libelle_gare (libelle varchar primary key, gare varchar)")
    con.executemany("insert into libelle_gare values (?, ?)", lignes)
    sans_region = con.sql("select id from gare where pays = 'France' and region is null").fetchall()
    if sans_region:
        raise ErreurGare(f"Gares françaises sans région : {sans_region}")
