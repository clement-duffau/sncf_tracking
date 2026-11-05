"""Lecture et validation de data/events.yaml ; détection des mois anormaux non annotés."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import duckdb
import yaml

from . import config

TYPES_EVENEMENT = {"greve", "covid", "incident", "meteo", "donnees", "perimetre"}
TYPES_TRAIN = {"TGV", "Intercités", "TER"}
EXCLUSIONS = {"tendances", "saisonnalite", "mon_trajet"}
EFFETS = {"gravite_invalide", "rupture_causes"}
MOIS = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


class ErreurEvenements(Exception):
    pass


@dataclass
class Evenement:
    id: str
    titre: str
    type: str
    debut: date
    fin: date
    types: list[str]
    exclure: list[str] = field(default_factory=list)
    effet: str | None = None
    observe: str = ""
    sources: list[str] = field(default_factory=list)

    def mois(self) -> list[date]:
        out, d = [], self.debut
        while d <= self.fin:
            out.append(d)
            d = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
        return out


def _mois(v, ctx: str) -> date:
    s = str(v)
    if not MOIS.match(s):
        raise ErreurEvenements(f"{ctx} : mois « {s} » invalide (format AAAA-MM attendu)")
    return date(int(s[:4]), int(s[5:]), 1)


def charger(chemin: Path = config.EVENEMENTS) -> list[Evenement]:
    brut = yaml.safe_load(chemin.read_text(encoding="utf-8")) or []
    if not isinstance(brut, list):
        raise ErreurEvenements("events.yaml doit contenir une liste")
    evts, ids = [], set()
    for i, e in enumerate(brut):
        ctx = f"events.yaml, entrée {i + 1} ({e.get('id', '?')})"
        for cle in ("id", "titre", "type", "debut", "types", "sources"):
            if not e.get(cle):
                raise ErreurEvenements(f"{ctx} : champ « {cle} » manquant")
        if e["id"] in ids:
            raise ErreurEvenements(f"{ctx} : identifiant en double")
        ids.add(e["id"])
        if e["type"] not in TYPES_EVENEMENT:
            raise ErreurEvenements(f"{ctx} : type « {e['type']} » inconnu")
        if set(e["types"]) - TYPES_TRAIN:
            raise ErreurEvenements(f"{ctx} : type de train inconnu {set(e['types']) - TYPES_TRAIN}")
        exclure = e.get("exclure") or []
        if set(exclure) - EXCLUSIONS:
            raise ErreurEvenements(f"{ctx} : exclusion inconnue {set(exclure) - EXCLUSIONS}")
        if e.get("effet") and e["effet"] not in EFFETS:
            raise ErreurEvenements(f"{ctx} : effet « {e['effet']} » inconnu")
        debut = _mois(e["debut"], ctx)
        fin = _mois(e.get("fin", e["debut"]), ctx)
        if fin < debut:
            raise ErreurEvenements(f"{ctx} : fin avant le début")
        evts.append(Evenement(e["id"], e["titre"], e["type"], debut, fin, list(e["types"]), list(exclure),
                              e.get("effet"), (e.get("observe") or "").strip(), list(e["sources"])))
    return evts


def mois_exclus(evts: list[Evenement], type_train: str, calcul: str) -> set[date]:
    return {m for e in evts if type_train in e.types and calcul in e.exclure for m in e.mois()}


def mois_effet(evts: list[Evenement], type_train: str, effet: str) -> set[date]:
    return {m for e in evts if type_train in e.types and e.effet == effet for m in e.mois()}


def debut_rupture_causes(evts: list[Evenement]) -> date | None:
    ruptures = [e.debut for e in evts if e.effet == "rupture_causes"]
    return max(ruptures) if ruptures else None


def candidats_non_annotes(con: duckdb.DuckDBPyConnection, evts: list[Evenement]) -> list[str]:
    """Mois anormaux (annulations TGV > 5 %, programmés Intercités / TER en baisse de plus de 20 % sur
    un an) qu'aucun événement ne couvre pour ce type de train. Le pipeline les signale sans les écrire."""
    requete = """
    with tgv as (select 'TGV' type, date, sum(nb_annulation) / nullif(sum(nb_train_prevu), 0) taux
                 from tgv_aqst group by all),
    -- périmètre constant : seules les liaisons (ou régions) publiées les deux mois comptent
    prog as (select 'Intercités' type, date, depart || '>' || arrivee k, sum(nombre_de_trains_programmes) p
             from intercites group by all
             union all select 'TER', date, region, sum(nombre_de_trains_programmes) from ter group by all),
    baisse as (select a.type, a.date, sum(a.p) / nullif(sum(b.p), 0) - 1 v from prog a
               join prog b on b.type = a.type and b.k = a.k and b.date = a.date - interval 12 month
               group by all)
    select type, date::date, 'annulations ' || round(100 * taux, 1) || ' %' from tgv where taux > 0.05
    union all
    select type, date::date, 'programmés ' || round(100 * v, 1) || ' % sur un an' from baisse where v < -0.20
    order by 2, 1
    """
    couverts = {(t, m) for e in evts for t in e.types for m in e.mois()}
    return [f"{t} {d:%Y-%m} : {motif}" for t, d, motif in con.sql(requete).fetchall() if (t, d) not in couverts]
