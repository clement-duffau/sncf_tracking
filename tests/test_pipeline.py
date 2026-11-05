"""Tests du pipeline sur un mini-jeu synthétique (aucun accès réseau).

Lancer : python -m pytest -q tests
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import duckdb
import pytest

from pipeline import checks, clean, config, events, export, gares, load, score, trends
from pipeline.events import ErreurEvenements
from pipeline.gares import ErreurGare, normaliser
from pipeline.schemas import ErreurSource

CAUSES = ["externe", "infra", "gestion_trafic", "materiel_roulant", "gestion_gare", "prise_en_charge_voyageurs"]


def _mois(debut: date, n: int) -> list[date]:
    out = []
    for i in range(n):
        m = debut.year * 12 + debut.month - 1 + i
        out.append(date(m // 12, m % 12 + 1, 1))
    return out


def _tgv(mo, service, dep, arr, prevus, annul, retards, s15, s30, s60, causes=(30, 20, 20, 10, 10, 10), duree=50):
    return (mo, service, dep, arr, duree, prevus, annul, retards, 12.5, s15, s30, s60, *causes)


def fabriquer(raw: Path, lignes_tgv: list | None = None, lignes_ic: list | None = None) -> None:
    """Écrit un mini-jeu de fichiers bruts au format du portail SNCF."""
    raw.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    mois = _mois(date(2023, 10, 1), 36)
    if lignes_tgv is None:
        lignes_tgv = []
        for i, mo in enumerate(mois):
            for dep, arr in (("PARIS EST", "REIMS"), ("REIMS", "PARIS EST")):
                lignes_tgv.append(_tgv(mo, "National", dep, arr, 400, 4, 40 + i % 5, 20, 10, 4))
            for dep, arr in (("PARIS EST", "NANCY"), ("NANCY", "PARIS EST")):
                lignes_tgv.append(_tgv(mo, "National", dep, arr, 500, 5, 100 + i % 7, 60, 30, 12, duree=95))
            # petite liaison très ponctuelle (20 trains par mois)
            for dep, arr in (("PARIS EST", "METZ"), ("METZ", "PARIS EST")):
                lignes_tgv.append(_tgv(mo, "National", dep, arr, 20, 0, 0, 0, 0, 0, causes=(0,) * 6, duree=85))
    cols_tgv = ("date date, service varchar, gare_depart varchar, gare_arrivee varchar, duree_moyenne bigint, "
                "nb_train_prevu bigint, nb_annulation bigint, nb_train_retard_arrivee bigint, retard_moyen_arrivee double, "
                "nb_train_retard_sup_15 bigint, nb_train_retard_sup_30 bigint, nb_train_retard_sup_60 bigint, "
                + ", ".join(f"prct_cause_{c} double" for c in CAUSES))
    con.sql(f"create table tgv_aqst ({cols_tgv})")
    con.executemany(f"insert into tgv_aqst values ({', '.join('?' * 18)})", lignes_tgv)

    if lignes_ic is None:
        lignes_ic = []
        for mo in mois:
            lignes_ic += [(mo, "PARIS-EST", "METZ/NANCY", 60, 58, 2, 10), (mo, "NANCY/METZ", "PARIS-EST", 60, 59, 1, 12),
                          (mo, "PARIS-EST", "METZ/NANCY", 30, 30, 0, 3)]  # doublon du même mois
    con.sql("""create table intercites (date date, depart varchar, arrivee varchar, nombre_de_trains_programmes bigint,
               nombre_de_trains_ayant_circule bigint, nombre_de_trains_annules bigint,
               nombre_de_trains_en_retard_a_l_arrivee bigint)""")
    con.executemany("insert into intercites values (?, ?, ?, ?, ?, ?, ?)", lignes_ic)

    con.sql("create table tgv_national (date date, regularite_composite double, ponctualite_origine double)")
    con.executemany("insert into tgv_national values (?, 88.0, 80.0)", [(m,) for m in mois])
    con.sql("create table tgv_axes (date date, axe varchar, regularite_composite double, ponctualite_origine double)")
    con.executemany("insert into tgv_axes values (?, 'Est', 90.0, 85.0)", [(m,) for m in mois])
    con.sql("""create table ter (date date, region varchar, nombre_de_trains_programmes bigint,
               nombre_de_trains_ayant_circule bigint, nombre_de_trains_annules bigint, nombre_de_trains_en_retard_a_l_arrivee bigint)""")
    con.executemany("insert into ter values (?, 'Grand Est', 1000, 980, 20, 60)", [(m,) for m in mois])
    for t in ("tgv_aqst", "intercites", "tgv_national", "tgv_axes", "ter"):
        con.sql(f"copy {t} to '{(raw / f'{t}.parquet').as_posix()}' (format parquet)")
    (raw / "gares_voyageurs.csv").write_text(
        "nom;libellecourt;segment_drg;position_geographique;codeinsee;codes_uic;id\n"
        "Paris Est;PES;A;48.8768, 2.3592;75110;87113001;1\n"
        "Reims;RMS;A;49.2594, 4.0244;51454;87171009;2\n"
        "Nancy;NCY;A;48.6895, 6.1744;54395;87141002;3\n"
        "Metz;MZ;A;49.1097, 6.1772;57463;87192039;4\n", encoding="utf-8")


def preparer(tmp_path: Path, **kw):
    raw = tmp_path / "raw"
    fabriquer(raw, **kw)
    con = load.connexion(raw)
    evts = events.charger()
    gares.construire(con)
    clean.construire(con, evts)
    return con, evts


# ------------------------------------------------------------------ gares
def test_normaliser():
    assert normaliser("ST PIERRE DES CORPS") == "SAINT PIERRE DES CORPS"
    assert normaliser("NICE-VILLE") == "NICE"
    assert normaliser("BELLEGARDE (AIN)") == "BELLEGARDE"
    assert normaliser("Béziers") == "BEZIERS"


def test_gare_inconnue_fait_echouer(tmp_path):
    raw = tmp_path / "raw"
    mo = date(2026, 1, 1)
    fabriquer(raw, lignes_tgv=[_tgv(mo, "National", "PARIS EST", "GARE IMAGINAIRE", 10, 0, 1, 0, 0, 0)])
    con = load.connexion(raw)
    with pytest.raises(ErreurGare, match="GARE IMAGINAIRE"):
        gares.construire(con)


# ------------------------------------------------------------------ nettoyage
def test_fusion_sens_et_services(tmp_path):
    mo = date(2026, 1, 1)
    lignes = [
        _tgv(mo, "National", "PARIS EST", "REIMS", 100, 2, 10, 5, 2, 1),
        _tgv(mo, "International", "PARIS EST", "REIMS", 50, 0, 5, 2, 1, 0),   # même mois, autre service
        _tgv(mo, "National", "REIMS", "PARIS EST", 120, 0, 12, 6, 3, 1),
        _tgv(date(2026, 2, 1), "National", "REIMS", "PARIS EST", 0, 3, 0, 0, 0, 0),  # 0 prévu : ignoré
    ]
    con, _ = preparer(tmp_path, lignes_tgv=lignes)
    rows = con.sql("select liaison, sens, prevus, annules, circules, retards from mesure where type = 'TGV' order by sens").fetchall()
    assert rows == [("tgv-paris-est--reims", "ab", 150, 2, 148, 15),
                    ("tgv-paris-est--reims", "ba", 120, 0, 120, 12)]
    assert con.sql("select count(*) from liaison where type = 'TGV'").fetchall()[0][0] == 1


def test_gravite_invalide_et_causes(tmp_path):
    lignes = [
        _tgv(date(2026, 1, 1), "National", "PARIS EST", "REIMS", 100, 0, 20, 10, 2, 5),        # > 30 < > 60 : invalide
        _tgv(date(2025, 2, 1), "National", "PARIS EST", "REIMS", 100, 0, 20, 10, 5, 2),        # mois déclaré invalide
        _tgv(date(2025, 6, 1), "National", "PARIS EST", "REIMS", 100, 0, 20, 10, 5, 2),        # valide
        _tgv(date(2025, 7, 1), "National", "PARIS EST", "REIMS", 100, 0, 20, 10, 5, 2, causes=(0,) * 6),
    ]
    con, _ = preparer(tmp_path, lignes_tgv=lignes)
    r = dict(con.sql("select mois, sup30 from mesure where type = 'TGV'").fetchall())
    assert r[date(2026, 1, 1)] is None and r[date(2025, 2, 1)] is None and r[date(2025, 6, 1)] == 5
    c = con.sql("select cause_externe, retards_avec_causes, nomenclature_causes from mesure where mois = '2025-06-01'").fetchall()[0]
    assert c == (pytest.approx(6.0), 20, 1)   # 30 % de 20 trains en retard
    c = con.sql("select cause_externe, retards_avec_causes from mesure where mois = '2025-07-01'").fetchall()[0]
    assert c == (None, 0)                      # causes non renseignées
    assert con.sql("select nomenclature_causes from mesure where mois = '2026-01-01'").fetchall()[0][0] == 1


def test_intercites_libelles_composites_et_doublons(tmp_path):
    con, _ = preparer(tmp_path)
    rows = con.sql("""select liaison, sens, prevus, retards from mesure
                      where type = 'Intercités' and mois = '2026-01-01' order by sens""").fetchall()
    assert rows == [("ic-metz+nancy--paris-est", "ab", 60, 12), ("ic-metz+nancy--paris-est", "ba", 90, 13)]
    nom = con.sql("select nom from liaison where type = 'Intercités'").fetchall()[0][0]
    assert nom == "Metz / Nancy – Paris Est"


# ------------------------------------------------------------------ score
def test_bareme():
    assert score.note(0, 0, 0, 0) == 100
    assert score.note(0, 1, 0, 0) == 0
    assert score.note(1, 0, 1, 1) == 0
    assert score.note(1, 0, 0, 0) == 67
    assert score.note(1, 0, 1, 0) == 33


def test_scores_et_retrecissement(tmp_path):
    con, _ = preparer(tmp_path)
    score.construire(con)
    s = {l: (sc, rg) for l, sc, rg in con.sql(
        "select liaison, score, regularite from score where type = 'TGV' and periode = '12m'").fetchall()}
    # Metz : 100 % à l'heure mais 480 trains seulement en 12 mois → ramené vers la moyenne
    metz, reims = s["tgv-metz--paris-est"], s["tgv-paris-est--reims"]
    assert metz[1] == 1.0
    assert metz[0] < 100
    assert reims[0] < metz[0]
    rangs = con.sql("select liaison, rang from score where type = 'TGV' and periode = '12m' order by rang").fetchall()
    assert [r for _, r in rangs] == [1, 2, 3]
    bas, sc, haut = con.sql("select bas, score, haut from score where liaison = 'tgv-paris-est--reims' and periode = '12m'").fetchall()[0]
    assert bas < sc < haut
    # Intercités : gravité estimée à partir des parts TGV
    assert con.sql("select bool_and(gravite_estimee) from score where type = 'Intercités'").fetchall()[0][0]


# ------------------------------------------------------------------ événements
def test_evenements_valides():
    evts = events.charger()
    assert len({e.id for e in evts}) == len(evts)
    assert date(2025, 2, 1) in events.mois_effet(evts, "TGV", "gravite_invalide")
    assert date(2020, 4, 1) in events.mois_exclus(evts, "TGV", "tendances")


def test_evenements_invalides(tmp_path):
    p = tmp_path / "e.yaml"
    p.write_text("- {id: x, titre: X, type: greve, debut: 2020-13, types: [TGV], sources: [u]}\n")
    with pytest.raises(ErreurEvenements, match="invalide"):
        events.charger(p)
    p.write_text("- {id: x, titre: X, type: inconnu, debut: 2020-01, types: [TGV], sources: [u]}\n")
    with pytest.raises(ErreurEvenements, match="inconnu"):
        events.charger(p)


# ------------------------------------------------------------------ contrôles
def test_baisse_des_lignes_fait_echouer():
    meta = {"fields": [{"name": c, "type": t} for c, t in
                       {"date": "date", "axe": "text", "regularite_composite": "double", "ponctualite_origine": "double"}.items()],
            "metas": {"default": {"records_count": 800, "data_processed": "x"}}}
    with pytest.raises(ErreurSource, match="baisse"):
        checks.verifier_metas({"tgv_axes": meta}, {"tgv_axes": {"records_count": 900}})
    meta["fields"] = meta["fields"][:2]
    with pytest.raises(ErreurSource, match="absente"):
        checks.verifier_metas({"tgv_axes": meta}, {})


# ------------------------------------------------------------------ bout en bout
def test_build_complet(tmp_path):
    con, evts = preparer(tmp_path)
    pers = score.construire(con)
    trends.construire(con, evts)
    metas = {cle: {"metas": {"default": {"data_processed": "2026-10-01T00:00:00+00:00"}}} for cle in config.JEUX}
    tailles = export.exporter(con, evts, metas, pers, tmp_path / "sortie")
    for f in ("meta.json", "classement.json", "mensuel-tgv.json", "mensuel-intercites.json", "stats.json",
              "gares.json", "evenements.json", "donnees/LICENCE.md", "donnees/mesures_mensuelles.csv"):
        assert f in tailles, f
    c = json.loads((tmp_path / "sortie" / "classement.json").read_text())
    assert len(c["liaisons"]) == 4
    assert len(c["scores"]["TGV"]["12m"][0]) == len(c["colonnes"])
    fiche = json.loads((tmp_path / "sortie" / "liaison" / "tgv-paris-est--reims.json").read_text())
    assert set(fiche["mon_trajet"]) == {"ab", "ba"} and len(fiche["mon_trajet"]["ab"]) == 12
    assert 0 < fiche["mon_trajet"]["ab"][0]["proba"] < 1
    assert fiche["tendance"]["etiquette"] in {"stable", "amelioration", "degradation"}
