"""Tendances, saisonnalité et « Mon trajet » (docs/PLAN.md § 5 et 6).

Les mois exclus par data/events.yaml (`exclure: tendances | saisonnalite | mon_trajet`) sont retirés
des calculs correspondants.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import date

import duckdb
import numpy as np

from . import config
from .events import Evenement, mois_exclus
from .score import _mois_moins

Z80 = 1.2816


def _table_mois(con, nom: str, mois: set[date]) -> None:
    con.sql(f"create or replace table {nom} (mois date)")
    if mois:
        con.executemany(f"insert into {nom} values (?)", [(m,) for m in sorted(mois)])


def tendances(con: duckdb.DuckDBPyConnection, evts: list[Evenement]) -> None:
    """12 derniers mois vs 12 précédents, test z gonflé par la surdispersion, absolu et relatif au type."""
    lignes = []
    for t in config.TYPES:
        _table_mois(con, "exclus", mois_exclus(evts, t, "tendances"))
        fin = con.execute("select max(mois) from mesure where type = ?", [t]).fetchall()[0][0]
        d1, d0 = _mois_moins(fin, 11), _mois_moins(fin, 23)
        res = con.execute("""
          select liaison,
            sum(circules) filter (where mois >= ?) n1, sum(retards) filter (where mois >= ?) k1,
            sum(circules) filter (where mois < ?) n0, sum(retards) filter (where mois < ?) k0
          from mesure where type = ? and mois >= ? and mois not in (select mois from exclus)
          group by 1""", [d1, d1, d1, d1, t, d0]).fetchall()
        D = config.SURDISPERSION[t]
        valides = [r for r in res if r[1] and r[3]]
        n1, k1 = sum(r[1] for r in valides), sum(r[2] for r in valides)
        n0, k0 = sum(r[3] for r in valides), sum(r[4] for r in valides)
        delta_type = (1 - k1 / n1) - (1 - k0 / n0) if valides else None
        for liaison, n1, k1, n0, k0 in res:
            if not n1:
                continue
            p1 = 1 - k1 / n1
            if not n0:
                lignes.append((t, liaison, p1, None, None, None, None, None, "nouvelle", None, delta_type))
                continue
            p0 = 1 - k0 / n0
            se = math.sqrt(D * (p1 * (1 - p1) / n1 + p0 * (1 - p0) / n0)) or 1e-9
            delta, rel = p1 - p0, (p1 - p0) - delta_type
            z, zr = delta / se, rel / se

            def etiquette(zz, dd):
                if zz >= config.SEUIL_Z and dd >= config.SEUIL_DELTA:
                    return "amelioration"
                if zz <= -config.SEUIL_Z and dd <= -config.SEUIL_DELTA:
                    return "degradation"
                return "stable"
            lignes.append((t, liaison, p1, p0, delta, z, rel, zr, etiquette(z, delta), etiquette(zr, rel), delta_type))
    con.sql("""create or replace table tendance (type varchar, liaison varchar, reg_12m double, reg_avant double,
               delta double, z double, delta_relatif double, z_relatif double, etiquette varchar,
               etiquette_relative varchar, delta_type double)""")
    con.executemany("insert into tendance values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", lignes)


def saisonnalite(con: duckdb.DuckDBPyConnection, evts: list[Evenement]) -> None:
    """Profil saisonnier du type et de chaque liaison (rétréci vers celui du type)."""
    lignes_type, lignes_liaison = [], []
    for t in config.TYPES:
        _table_mois(con, "exclus", mois_exclus(evts, t, "saisonnalite"))
        # écart de chaque mois à la moyenne de son année (années d'au moins 10 mois valides)
        effets_type = con.execute("""
          with m as (select mois, 1 - sum(retards) / sum(circules) reg from mesure
                     where type = ? and mois not in (select mois from exclus) group by 1),
          a as (select year(mois) y, avg(reg) moy from m group by 1 having count(*) >= 10)
          select month(mois), avg(reg - moy), count(*) from m join a on a.y = year(m.mois) group by 1 order by 1
        """, [t]).fetchall()
        profil = {mo: e for mo, e, _ in effets_type}
        lignes_type += [(t, mo, e, n) for mo, e, n in effets_type]
        rows = con.execute("""
          with m as (select liaison, mois, 1 - sum(retards) / sum(circules) reg from mesure
                     where type = ? and circules > 0 and mois not in (select mois from exclus) group by all),
          a as (select liaison, year(mois) y, avg(reg) moy from m group by all having count(*) >= 10)
          select m.liaison, month(mois), avg(reg - moy), count(*) from m
          join a on a.liaison = m.liaison and a.y = year(m.mois) group by all
        """, [t]).fetchall()
        for liaison, mo, e, n in rows:
            k0 = config.SAISON_K0
            lignes_liaison.append((t, liaison, mo, (n * e + k0 * profil.get(mo, 0)) / (n + k0), e, n))
    con.sql("create or replace table saison_type (type varchar, mois integer, effet double, annees integer)")
    con.executemany("insert into saison_type values (?, ?, ?, ?)", lignes_type)
    con.sql("""create or replace table saison_liaison (type varchar, liaison varchar, mois integer, effet double,
               effet_brut double, annees integer)""")
    con.executemany("insert into saison_liaison values (?, ?, ?, ?, ?, ?)", lignes_liaison)


def pentes(con: duckdb.DuckDBPyConnection, evts: list[Evenement]) -> None:
    """Pente (points de régularité par an) sur 36 mois, désaisonnalisée avec le profil du type."""
    lignes = []
    for t in config.TYPES:
        _table_mois(con, "exclus", mois_exclus(evts, t, "tendances"))
        fin = con.execute("select max(mois) from mesure where type = ?", [t]).fetchall()[0][0]
        debut = _mois_moins(fin, config.PENTE_MOIS - 1)
        lignes += con.execute("""
          with m as (select liaison, mois, 1 - sum(retards) / sum(circules) reg from mesure
                     where type = ? and mois >= ? and circules > 0 and mois not in (select mois from exclus) group by all),
          d as (select m.liaison, datediff('month', ?::date, m.mois) / 12.0 t, reg - coalesce(s.effet, 0) reg_ds
                from m left join saison_type s on s.type = ? and s.mois = month(m.mois))
          select ?, liaison, regr_slope(reg_ds, t), regr_r2(reg_ds, t), count(*) from d group by liaison
          having count(*) >= 18
        """, [t, debut, debut, t, t]).fetchall()
    con.sql("create or replace table pente (type varchar, liaison varchar, pente double, r2 double, mois integer)")
    con.executemany("insert into pente values (?, ?, ?, ?, ?)", lignes)


def mon_trajet(con: duckdb.DuckDBPyConnection, evts: list[Evenement]) -> None:
    """Probabilité qu'un train prévu arrive à l'heure, par liaison active × sens × mois calendaire."""
    rng = np.random.default_rng(config.GRAINE + 1)
    lignes = []
    for t in config.TYPES:
        D, m_eff = config.SURDISPERSION[t], config.TRAJET_M_EFF
        _table_mois(con, "exclus", mois_exclus(evts, t, "mon_trajet"))
        fin = con.execute("select max(mois) from mesure where type = ?", [t]).fetchall()[0][0]
        saison = dict(con.execute("select mois, effet from saison_type where type = ?", [t]).fetchall())
        niveaux = {(l, s): p for l, s, p in con.execute("""
          select liaison, sens, 1 - (sum(retards) + sum(annules)) / sum(prevus) from mesure
          where type = ? and mois > ? and mois not in (select mois from exclus) group by all
        """, [t, _mois_moins(fin, 24)]).fetchall()}
        obs = defaultdict(list)
        for l, s, mo, prevus, annules, retards, sup30, circ in con.execute("""
          select liaison, sens, mois, prevus, annules, retards, sup30, circules from mesure
          where type = ? and mois not in (select mois from exclus) order by mois desc
        """, [t]).fetchall():
            if (l, s) in niveaux:
                obs[(l, s, mo.month)].append((mo.year, prevus, annules, retards, sup30, circ))

        # variance d'une année sur l'autre, hors aléa binomial (médiane sur les cellules d'au moins 4 années)
        excedents = []
        for cle, ans in obs.items():
            ans = ans[: config.TRAJET_ANNEES]
            if len(ans) >= 4:
                ps = [(p - a - r) / p for _, p, a, r, _, _ in ans]
                binom = np.mean([q * (1 - q) / p for q, (_, p, *_rest) in zip(ps, ans)])
                excedents.append(max(np.var(ps, ddof=1) - binom, 0.0))
        tau2 = float(np.median(excedents)) if excedents else 0.0

        for (l, s), niveau in niveaux.items():
            for mo in range(1, 13):
                ans = obs.get((l, s, mo), [])[: config.TRAJET_ANNEES]
                prior = min(max(niveau + saison.get(mo, 0.0), 0.01), 0.99)
                n = sum(a[1] for a in ans)
                k = sum(a[1] - a[2] - a[3] for a in ans)
                alpha, beta = k / D + m_eff * prior, (n - k) / D + m_eff * (1 - prior)
                moy = alpha / (alpha + beta)
                var_post = alpha * beta / ((alpha + beta) ** 2 * (alpha + beta + 1))
                ic_bas, ic_haut = np.quantile(rng.beta(alpha, beta, 4000), [0.1, 0.9])
                ps = [(p - a - r) / p for _, p, a, r, _, _ in ans]
                if len(ps) >= 2:
                    y = len(ps) - 1
                    s2 = (y * np.var(ps, ddof=1) + config.SAISON_K0 * tau2) / (y + config.SAISON_K0)
                else:
                    s2 = tau2
                et = math.sqrt(var_post + s2)
                p_annul = sum(a[2] for a in ans) / n if n else None
                circ_g = sum(a[5] for a in ans if a[4] is not None)
                p_sup30 = (sum(a[4] for a in ans if a[4] is not None) / circ_g) if (t == "TGV" and circ_g) else None
                lignes.append((t, l, s, mo, moy, float(ic_bas), float(ic_haut), max(moy - Z80 * et, 0.0),
                               min(moy + Z80 * et, 1.0), prior, int(n), len(ans),
                               [{"annee": a[0], "p": round(q, 4), "trains": int(a[1])} for a, q in zip(ans, ps)],
                               p_annul, p_sup30,
                               len(ans) < config.TRAJET_PEU_ANNEES or n < config.TRAJET_PEU_TRAINS))
    con.sql("""create or replace table trajet (type varchar, liaison varchar, sens varchar, mois integer,
      proba double, ic_bas double, ic_haut double, pred_bas double, pred_haut double, prior double,
      trains integer, annees integer, par_annee json, p_annulation double, p_sup30 double, peu_de_donnees boolean)""")
    con.executemany("insert into trajet values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [(*x[:12], json.dumps(x[12]), *x[13:]) for x in lignes])


def construire(con: duckdb.DuckDBPyConnection, evts: list[Evenement]) -> None:
    tendances(con, evts)
    saisonnalite(con, evts)
    pentes(con, evts)
    mon_trajet(con, evts)
