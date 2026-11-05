"""Score de fiabilité (V2, « note moyenne d'un train prévu ») avec rétrécissement bayésien.

Voir docs/PLAN.md § 3. Pour chaque type de train, période et liaison non orientée :

    taux lissé = (x + M·μ) / (n + M)

μ = taux moyen du type sur la période, M = config.POIDS_PRIOR[type] (en trains).
Composantes : R (retard au seuil composite), A (annulation), G30 / G60 (retards > 30 / > 60 min).
Intercités : G30 = R·q30 et G60 = R·q60, où q30, q60 = parts des > 30 / > 60 min parmi les trains TGV en
retard sur les mêmes mois (gravité non publiée pour les Intercités).

score = 100 − 100/3 · [ (1−A)·((R−G30)·1 + (G30−G60)·2 + G60·3) + A·3 ]

L'intervalle à 80 % est obtenu par simulation : chaque composante est tirée dans sa loi bêta a posteriori
exprimée en trains « effectifs » (n / D, pour tenir compte de la corrélation des retards d'un même mois).
"""

from __future__ import annotations

from datetime import date

import duckdb
import numpy as np

from . import config


def _mois_moins(d: date, n: int) -> date:
    m = d.year * 12 + d.month - 1 - n
    return date(m // 12, m % 12 + 1, 1)


def periodes(con: duckdb.DuckDBPyConnection) -> list[dict]:
    """Périodes standard par type : 12 derniers mois, chaque année civile, tout l'historique."""
    out = []
    for type_train, debut, fin in con.sql("select type, min(mois), max(mois) from mesure group by 1 order by 1").fetchall():
        out.append({"type": type_train, "cle": "12m", "libelle": "12 derniers mois",
                    "debut": _mois_moins(fin, config.FENETRE_MOIS - 1), "fin": fin, "partielle": False})
        for annee in range(debut.year, fin.year + 1):
            d, f = max(date(annee, 1, 1), debut), min(date(annee, 12, 1), fin)
            out.append({"type": type_train, "cle": str(annee), "libelle": str(annee), "debut": d, "fin": f,
                        "partielle": (f.month - d.month + 1) < 12})
        out.append({"type": type_train, "cle": "tout", "libelle": "Tout l'historique", "debut": debut, "fin": fin,
                    "partielle": False})
    return out


def note(R, A, G30, G60):
    """Score V2 (0–100) à partir des taux (scalaires ou tableaux numpy)."""
    b = config.BAREME
    pts_retard = ((R - G30) * b["retard_30"] + (G30 - G60) * b["retard_30_60"] + G60 * b["retard_60"])
    return (1 - A) * ((1 - R) * b["a_l_heure"] + pts_retard) + A * b["annule"]


def construire(con: duckdb.DuckDBPyConnection) -> list[dict]:
    pers = periodes(con)
    con.sql("create or replace table periode (type varchar, cle varchar, libelle varchar, debut date, fin date, partielle boolean)")
    con.executemany("insert into periode values (?, ?, ?, ?, ?, ?)",
                    [(p["type"], p["cle"], p["libelle"], p["debut"], p["fin"], p["partielle"]) for p in pers])

    con.sql("""
    create or replace table agregat as
    select p.type, p.cle periode, m.liaison,
      sum(prevus)::double prevus, sum(annules)::double annules, sum(circules)::double circules,
      sum(retards)::double retards,
      coalesce(sum(circules) filter (where sup30 is not null), 0)::double circules_g,
      coalesce(sum(sup30), 0)::double sup30, coalesce(sum(sup60), 0)::double sup60,
      count(distinct mois) mois
    from mesure m join periode p on p.type = m.type and m.mois between p.debut and p.fin
    group by all
    """)
    # Prior μ par type × période ; parts de gravité TGV parmi les retards sur les mêmes mois (pour Intercités)
    con.sql("""
    create or replace table prior as
    with mu as (
      select type, periode, sum(retards) / sum(circules) mu_r, sum(annules) / sum(prevus) mu_a,
        sum(sup30) / nullif(sum(circules_g), 0) mu_g30, sum(sup60) / nullif(sum(circules_g), 0) mu_g60
      from agregat group by all),
    tgv_mois as (
      select mois, sum(retards) filter (where sup30 is not null) ret_g, sum(sup30) s30, sum(sup60) s60
      from mesure where type = 'TGV' group by 1),
    q as (
      select p.type, p.cle periode, sum(s30) / nullif(sum(ret_g), 0) q30, sum(s60) / nullif(sum(ret_g), 0) q60
      from periode p left join tgv_mois t on t.mois between p.debut and p.fin group by all),
    q_tout as (select sum(s30) / sum(ret_g) q30, sum(s60) / sum(ret_g) q60 from tgv_mois)
    select mu.*, coalesce(q.q30, (select q30 from q_tout)) q30, coalesce(q.q60, (select q60 from q_tout)) q60
    from mu join q using (type, periode)
    """)

    rows = con.sql("""
    select a.*, p.mu_r, p.mu_a, p.mu_g30, p.mu_g60, p.q30, p.q60
    from agregat a join prior p using (type, periode) order by a.type, a.periode, a.liaison
    """).fetchall()
    cols = [c for c in con.sql("""select a.*, p.mu_r, p.mu_a, p.mu_g30, p.mu_g60, p.q30, p.q60
                                  from agregat a join prior p using (type, periode) limit 0""").columns]
    rng = np.random.default_rng(config.GRAINE)
    resultats = []
    for row in rows:
        r = dict(zip(cols, row))
        t = r["type"]
        M, D = config.POIDS_PRIOR[t], config.SURDISPERSION[t]
        lisse = lambda x, n, mu: (x + M * mu) / (n + M)  # noqa: E731
        R = lisse(r["retards"], r["circules"], r["mu_r"])
        A = lisse(r["annules"], r["prevus"], r["mu_a"])
        tgv = t == "TGV" and r["mu_g30"] is not None
        if tgv:
            G30 = lisse(r["sup30"], r["circules_g"], r["mu_g30"])
            G60 = lisse(r["sup60"], r["circules_g"], r["mu_g60"])
        else:
            G30, G60 = R * r["q30"], R * r["q60"]
        score = note(R, A, G30, G60)

        # Intervalle à 80 % par simulation (trains effectifs = n / D)
        k = config.TIRAGES_INTERVALLE
        m_eff = M / D

        def tirage(x, n, mu):
            return rng.beta(x / D + m_eff * mu, (n - x) / D + m_eff * (1 - mu), k)

        Rs, As = tirage(r["retards"], r["circules"], r["mu_r"]), tirage(r["annules"], r["prevus"], r["mu_a"])
        if tgv:
            G30s = np.minimum(tirage(r["sup30"], r["circules_g"], r["mu_g30"]), Rs)
            G60s = np.minimum(tirage(r["sup60"], r["circules_g"], r["mu_g60"]), G30s)
        else:
            G30s, G60s = Rs * r["q30"], Rs * r["q60"]
        bas, haut = np.quantile(note(Rs, As, G30s, G60s), [0.1, 0.9])

        resultats.append({
            "type": t, "periode": r["periode"], "liaison": r["liaison"], "mois": r["mois"],
            "prevus": r["prevus"], "circules": r["circules"],
            "regularite": 1 - r["retards"] / r["circules"] if r["circules"] else None,
            "annulation": r["annules"] / r["prevus"],
            "sup30": r["sup30"] / r["circules_g"] if tgv and r["circules_g"] else None,
            "sup60": r["sup60"] / r["circules_g"] if tgv and r["circules_g"] else None,
            "R": R, "A": A, "G30": G30, "G60": G60, "gravite_estimee": not tgv,
            "score": float(score), "bas": float(bas), "haut": float(haut),
        })

    con.sql("""create or replace table score (type varchar, periode varchar, liaison varchar, mois integer,
      prevus double, circules double, regularite double, annulation double, sup30 double, sup60 double,
      R double, A double, G30 double, G60 double, gravite_estimee boolean, score double, bas double, haut double)""")
    cles = ["type", "periode", "liaison", "mois", "prevus", "circules", "regularite", "annulation", "sup30", "sup60",
            "R", "A", "G30", "G60", "gravite_estimee", "score", "bas", "haut"]
    con.executemany(f"insert into score values ({', '.join('?' * len(cles))})",
                    [tuple(x[c] for c in cles) for x in resultats])
    con.sql("""
    create or replace table score as
    select s.*, row_number() over (partition by s.type, s.periode order by s.score desc, s.liaison) rang,
      count(*) over (partition by s.type, s.periode) nb_classees,
      s.mois < least(""" + str(config.COUVERTURE_PARTIELLE) + """, datediff('month', p.debut, p.fin) + 1) couverture_partielle
    from score s join periode p on p.type = s.type and p.cle = s.periode
    """)
    return pers
