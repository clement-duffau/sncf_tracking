"""Écriture des fichiers du site (site/public/data/) et des exports ouverts (donnees/*.csv, ODbL).

Formats décrits dans docs/PLAN.md § 2. Les taux sont arrondis à 4 décimales (0,01 point), les scores à 0,1.
"""

from __future__ import annotations

import csv
import json
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

import duckdb

from . import config
from .clean import CAUSES
from .events import Evenement

TITRES = {
    "tgv_aqst": "Régularité mensuelle TGV par liaisons",
    "tgv_axes": "Régularité mensuelle TGV par axe",
    "tgv_national": "Régularité mensuelle TGV globale",
    "intercites": "Régularité mensuelle Intercités",
    "ter": "Régularité mensuelle TER",
    "gares_voyageurs": "Gares de voyageurs",
}


def _r(x, n=4):
    return None if x is None else round(float(x), n)


def _mois(d: date | None) -> str | None:
    return None if d is None else d.isoformat()[:7]


def _ecrire(chemin: Path, obj) -> None:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def _dicts(con, sql: str, params=None) -> list[dict]:
    rel = con.execute(sql, params or [])
    cols = [d[0] for d in rel.description]
    return [dict(zip(cols, r)) for r in rel.fetchall()]


def exporter(con: duckdb.DuckDBPyConnection, evts: list[Evenement], metas: dict, pers: list[dict],
             sortie: Path = config.SORTIE) -> dict[str, int]:
    if sortie.exists():
        shutil.rmtree(sortie)
    sortie.mkdir(parents=True)

    fenetres = {p["type"]: {"debut": _mois(p["debut"]), "fin": _mois(p["fin"])} for p in pers if p["cle"] == "12m"}
    prior12 = {r["type"]: r for r in _dicts(con, "select * from prior where periode = '12m'")}

    # ------------------------------------------------------------------ meta.json
    meta = {
        "genere_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version_methode": config.VERSION_METHODE,
        "sources": {cle: {"titre": TITRES[cle], "url": f"{config.PORTAIL}/{config.JEUX[cle][0]}/",
                          "editeur": config.JEUX[cle][1], "licence": "ODbL",
                          "donnees_mises_a_jour": m["metas"]["default"].get("data_processed")}
                    for cle, m in metas.items()},
        "fenetres": fenetres,
        "periodes": {t: [{"cle": p["cle"], "libelle": p["libelle"], "debut": _mois(p["debut"]), "fin": _mois(p["fin"]),
                          "partielle": p["partielle"]} for p in pers if p["type"] == t] for t in config.TYPES},
        "parametres": {
            "bareme": config.BAREME, "poids_prior": config.POIDS_PRIOR, "surdispersion": config.SURDISPERSION,
            "moyennes_12m": {t: {"retard": _r(p["mu_r"]), "annulation": _r(p["mu_a"]), "sup30": _r(p["mu_g30"]),
                                 "sup60": _r(p["mu_g60"]), "q30": _r(p["q30"]), "q60": _r(p["q60"])}
                             for t, p in prior12.items()},
            "seuils_tendance": {"z": config.SEUIL_Z, "delta": config.SEUIL_DELTA},
        },
    }
    _ecrire(sortie / "meta.json", meta)

    # ------------------------------------------------------------------ liaisons (communes à plusieurs fichiers)
    liaisons = _dicts(con, """
      select l.*, t.etiquette, t.etiquette_relative, t.delta, t.delta_relatif, t.reg_12m, t.reg_avant, t.z, t.z_relatif,
        p.pente, p.r2 pente_r2
      from liaison l left join tendance t on t.liaison = l.id left join pente p on p.liaison = l.id
      order by l.type desc, l.nom""")
    index = {l["id"]: i for i, l in enumerate(liaisons)}
    ext = {e["id"]: e for e in _dicts(con, "select * from extremite")}
    spark = {}
    for t, f in fenetres.items():
        for lid, mo, reg in con.execute("""
            select liaison, mois, 1 - sum(retards) / nullif(sum(circules), 0) from mesure
            where type = ? and mois >= ?::date group by all""", [t, f["debut"] + "-01"]).fetchall():
            debut = date.fromisoformat(f["debut"] + "-01")
            i = (mo.year - debut.year) * 12 + mo.month - debut.month
            spark.setdefault(lid, [None] * config.FENETRE_MOIS)[i] = _r(reg)
    trains_mois = dict(con.execute("select liaison, prevus / mois from score where periode = '12m'").fetchall())

    def ident(l):
        return {
            "id": l["id"], "type": l["type"], "nom": l["nom"],
            "a": {"id": l["a"], "nom": l["nom_a"], "gares": ext[l["a"]]["gares"]},
            "b": {"id": l["b"], "nom": l["nom_b"], "gares": ext[l["b"]]["gares"]},
            "regions": l["regions"], "pays": l["pays"], "international": l["international"], "duree": l["duree"],
            "premier_mois": _mois(l["premier_mois"]), "dernier_mois": _mois(l["dernier_mois"]), "active": l["active"],
        }

    def tendance(l):
        if not l["etiquette"]:
            return None
        return {"etiquette": l["etiquette"], "etiquette_relative": l["etiquette_relative"],
                "reg_12m": _r(l["reg_12m"]), "reg_avant": _r(l["reg_avant"]), "delta": _r(l["delta"]),
                "delta_relatif": _r(l["delta_relatif"]), "z": _r(l["z"], 2), "z_relatif": _r(l["z_relatif"], 2),
                "pente_an": _r(l["pente"]), "pente_r2": _r(l["pente_r2"], 2)}

    # ------------------------------------------------------------------ classement.json
    colonnes = ["liaison", "rang", "score", "bas", "haut", "regularite", "annulation", "sup30", "circules",
                "trains_mois", "mois", "partielle"]
    scores: dict[str, dict[str, list]] = {t: {} for t in config.TYPES}
    for s in _dicts(con, "select * from score order by type, periode, rang"):
        scores[s["type"]].setdefault(s["periode"], []).append([
            index[s["liaison"]], s["rang"], _r(s["score"], 1), _r(s["bas"], 1), _r(s["haut"], 1),
            _r(s["regularite"]), _r(s["annulation"]), _r(s["sup30"]), int(s["circules"]),
            round(s["prevus"] / s["mois"]), s["mois"], s["couverture_partielle"]])
    _ecrire(sortie / "classement.json", {
        "liaisons": [{**ident(l), "tendance": tendance(l), "spark": spark.get(l["id"]),
                      "trains_mois_12m": round(trains_mois[l["id"]]) if l["id"] in trains_mois else None}
                     for l in liaisons],
        "colonnes": colonnes, "scores": scores,
    })

    # ------------------------------------------------------------------ mensuel-<type>.json (colonnes)
    for t, nom in (("TGV", "tgv"), ("Intercités", "intercites")):
        cols = ["prevus", "annules", "retards"] + (["sup15", "sup30", "sup60", "retards_avec_causes"]
                                                    + [f"cause_{c}" for c in CAUSES] if t == "TGV" else [])
        rows = con.execute(f"""select liaison, sens, year(mois) * 100 + month(mois), {', '.join(cols)}
                               from mesure where type = ? order by liaison, sens, mois""", [t]).fetchall()
        donnees = {"liaison": [index[r[0]] for r in rows], "sens": [0 if r[1] == "ab" else 1 for r in rows],
                   "mois": [r[2] for r in rows]}
        for j, c in enumerate(cols):
            donnees[c] = [None if r[3 + j] is None else round(r[3 + j]) for r in rows]
        _ecrire(sortie / f"mensuel-{nom}.json", {"liaisons": [l["id"] for l in liaisons], "colonnes": donnees,
                                                  "rupture_causes": _mois(next((e.debut for e in evts if e.effet == "rupture_causes"), None))})

    # ------------------------------------------------------------------ liaison/<id>.json
    saison_type = {}
    for t, mo, e in con.execute("select type, mois, effet from saison_type").fetchall():
        saison_type.setdefault(t, [None] * 12)[mo - 1] = _r(e)
    for l in liaisons:
        lid = l["id"]
        series = {}
        for sens in ("ab", "ba"):
            rows = _dicts(con, "select * from mesure where liaison = ? and sens = ? order by mois", [lid, sens])
            if not rows:
                continue
            serie = {"mois": [_mois(r["mois"]) for r in rows]}
            for c in ["prevus", "annules", "circules", "retards"] + (
                    ["sup15", "sup30", "sup60", "retards_avec_causes"] + [f"cause_{x}" for x in CAUSES] if l["type"] == "TGV" else []):
                serie[c] = [None if r[c] is None else round(r[c]) for r in rows]
            series[sens] = serie
        saison = [None] * 12
        for mo, e, eb, n in con.execute(
                "select mois, effet, effet_brut, annees from saison_liaison where liaison = ?", [lid]).fetchall():
            saison[mo - 1] = {"effet": _r(e), "brut": _r(eb), "annees": n}
        trajets = {}
        for tr in _dicts(con, "select * from trajet where liaison = ? order by sens, mois", [lid]):
            trajets.setdefault(tr["sens"], []).append({
                "mois": tr["mois"], "proba": _r(tr["proba"]), "ic": [_r(tr["ic_bas"]), _r(tr["ic_haut"])],
                "prediction": [_r(tr["pred_bas"]), _r(tr["pred_haut"])], "prior": _r(tr["prior"]),
                "trains": tr["trains"], "annees": json.loads(tr["par_annee"]), "p_annulation": _r(tr["p_annulation"]),
                "p_sup30": _r(tr["p_sup30"]), "peu_de_donnees": tr["peu_de_donnees"]})
        sc = {s["periode"]: {"rang": s["rang"], "classees": s["nb_classees"], "score": _r(s["score"], 1),
                             "intervalle": [_r(s["bas"], 1), _r(s["haut"], 1)], "regularite": _r(s["regularite"]),
                             "annulation": _r(s["annulation"]), "sup30": _r(s["sup30"]), "sup60": _r(s["sup60"]),
                             "gravite_estimee": s["gravite_estimee"], "circules": int(s["circules"]), "mois": s["mois"],
                             "partielle": s["couverture_partielle"]}
              for s in _dicts(con, "select * from score where liaison = ?", [lid])}
        evts_l = [e.id for e in evts if l["type"] in e.types
                  and e.fin >= l["premier_mois"] and e.debut <= l["dernier_mois"]]
        _ecrire(sortie / "liaison" / f"{lid}.json", {
            **ident(l), "tendance": tendance(l), "scores": sc, "series": series,
            "saisonnalite": {"liaison": saison, "type": saison_type.get(l["type"])},
            "mon_trajet": trajets, "evenements": evts_l,
            "rupture_causes": _mois(next((e.debut for e in evts if e.effet == "rupture_causes"), None)),
        })

    # ------------------------------------------------------------------ gares.json
    gares = _dicts(con, "select * from gare order by nom")
    desserte: dict[str, set] = {}
    for l in liaisons:
        for cote in ("a", "b"):
            for g in ext[l[cote]]["gares"]:
                desserte.setdefault(g, set()).add(index[l["id"]])
    _ecrire(sortie / "gares.json", [{"id": g["id"], "nom": g["nom"], "region": g["region"], "pays": g["pays"],
                                     "lat": _r(g["lat"], 5), "lon": _r(g["lon"], 5), "precision": g["precision"],
                                     "liaisons": sorted(desserte.get(g["id"], []))} for g in gares])

    # ------------------------------------------------------------------ evenements.json
    _ecrire(sortie / "evenements.json", [{
        "id": e.id, "titre": e.titre, "type": e.type, "debut": _mois(e.debut), "fin": _mois(e.fin), "types": e.types,
        "exclure": e.exclure, "effet": e.effet, "observe": e.observe, "sources": e.sources} for e in evts])

    # ------------------------------------------------------------------ stats.json
    causes_mens = _dicts(con, f"""
      select year(mois) * 100 + month(mois) mois, any_value(nomenclature_causes) nomenclature,
        sum(retards_avec_causes) retards, {', '.join(f'round(sum(cause_{c})) {c}' for c in CAUSES)}
      from mesure where type = 'TGV' group by mois order by mois""")
    stats = {
        "tgv_national": [[int(f"{d:%Y%m}"), _r(r, 2), _r(p, 2)] for d, r, p in con.execute(
            "select date::date, regularite_composite, ponctualite_origine from tgv_national order by 1").fetchall()],
        "tgv_axes": {axe: [[int(f"{d:%Y%m}"), _r(r, 2), _r(p, 2)] for _, d, r, p in rows]
                     for axe, rows in _grouper(con.execute(
                         "select axe, date::date, regularite_composite, ponctualite_origine from tgv_axes order by 1, 2").fetchall())},
        "types": {t: [[int(f"{d:%Y%m}"), int(p), int(a), int(c), int(rt)] for _, d, p, a, c, rt in rows]
                  for t, rows in _grouper(con.execute("""
                    select type, mois, sum(prevus), sum(annules), sum(circules), sum(retards) from mesure
                    group by all order by 1, 2""").fetchall())},
        "types_colonnes": ["mois", "prevus", "annules", "circules", "retards"],
        "ter": [[int(f"{d:%Y%m}"), int(p or 0), int(a or 0), int(c or 0), int(r or 0)] for d, p, a, c, r in con.execute("""
            select date::date, sum(nombre_de_trains_programmes), sum(nombre_de_trains_annules),
              sum(nombre_de_trains_ayant_circule), sum(nombre_de_trains_en_retard_a_l_arrivee)
            from ter group by 1 order by 1""").fetchall()],
        "causes_tgv": {"colonnes": ["mois", "nomenclature", "retards"] + CAUSES,
                       "lignes": [[c["mois"], c["nomenclature"], int(c["retards"] or 0)] + [int(c[x] or 0) for x in CAUSES]
                                  for c in causes_mens]},
        "saisonnalite": saison_type,
        "tendance_reseau": {t: _r(d) for t, d in con.execute(
            "select type, any_value(delta_type) from tendance group by 1").fetchall()},
    }
    _ecrire(sortie / "stats.json", stats)

    # ------------------------------------------------------------------ donnees/ (CSV ouverts, ODbL)
    dossier = sortie / "donnees"
    dossier.mkdir()
    con.sql(f"copy (select * exclude (a, b) from mesure order by type, liaison, sens, mois) to '{(dossier / 'mesures_mensuelles.csv').as_posix()}' (header, delimiter ';')")
    con.sql(f"copy (select * from score order by type, periode, rang) to '{(dossier / 'scores.csv').as_posix()}' (header, delimiter ';')")
    con.sql(f"copy (select * from liaison order by type, id) to '{(dossier / 'liaisons.csv').as_posix()}' (header, delimiter ';')")
    con.sql(f"copy (select * from gare order by id) to '{(dossier / 'gares.csv').as_posix()}' (header, delimiter ';')")
    con.sql(f"copy (select * exclude (par_annee) from trajet order by type, liaison, sens, mois) to '{(dossier / 'mon_trajet.csv').as_posix()}' (header, delimiter ';')")
    (dossier / "LICENCE.md").write_text(LICENCE, encoding="utf-8")

    return {str(p.relative_to(sortie)): p.stat().st_size for p in sorted(sortie.rglob("*")) if p.is_file()}


def _grouper(rows):
    out: dict = {}
    for r in rows:
        out.setdefault(r[0], []).append(r)
    return out.items()


LICENCE = """# Licence des données

Ces fichiers forment une base de données dérivée des jeux open data SNCF suivants, publiés sur
https://ressources.data.sncf.com sous licence Open Database License (ODbL) :

- SNCF Voyageurs : Régularité mensuelle TGV par liaisons, TGV par axe, TGV globale, Intercités, TER ;
- SNCF Gares & Connexions : Gares de voyageurs.

Ils sont mis à disposition sous la même licence, l'Open Database License (ODbL) 1.0 :
https://opendatacommons.org/licenses/odbl/1-0/

Les traitements appliqués (fusion des sens et des services, normalisation des libellés, rétrécissement
bayésien, tendances, « Mon trajet ») sont décrits dans docs/DATA.md et docs/PLAN.md du dépôt du projet,
et sur la page Méthodologie du site.

Fichiers (séparateur « ; ») :
- mesures_mensuelles.csv : comptes de trains par liaison × sens × mois ;
- scores.csv : scores de fiabilité par liaison et période ;
- liaisons.csv, gares.csv : référentiels ;
- mon_trajet.csv : probabilités d'arriver à l'heure par liaison × sens × mois calendaire.
"""
