"""Schémas attendus des jeux sources : le build échoue avec un message clair si une source change.

On ne vérifie que les colonnes utilisées par le pipeline (une colonne en plus est signalée, pas bloquante).
"""

from __future__ import annotations

import duckdb

# type Opendatasoft -> types DuckDB acceptés à la lecture du Parquet
TYPES_ACCEPTES = {
    "date": {"DATE", "TIMESTAMP", "TIMESTAMP WITH TIME ZONE"},
    "text": {"VARCHAR"},
    "int": {"BIGINT", "INTEGER", "HUGEINT", "SMALLINT"},
    "double": {"DOUBLE", "FLOAT", "DECIMAL", "BIGINT", "INTEGER"},
}

CAUSES = [
    "prct_cause_externe", "prct_cause_infra", "prct_cause_gestion_trafic",
    "prct_cause_materiel_roulant", "prct_cause_gestion_gare", "prct_cause_prise_en_charge_voyageurs",
]

SCHEMAS: dict[str, dict[str, str]] = {
    "tgv_aqst": {
        "date": "date", "service": "text", "gare_depart": "text", "gare_arrivee": "text",
        "duree_moyenne": "int", "nb_train_prevu": "int", "nb_annulation": "int",
        "nb_train_retard_arrivee": "int", "retard_moyen_arrivee": "double",
        "nb_train_retard_sup_15": "int", "nb_train_retard_sup_30": "int", "nb_train_retard_sup_60": "int",
        **{c: "double" for c in CAUSES},
    },
    "tgv_axes": {"date": "date", "axe": "text", "regularite_composite": "double", "ponctualite_origine": "double"},
    "tgv_national": {"date": "date", "regularite_composite": "double", "ponctualite_origine": "double"},
    "intercites": {
        "date": "date", "depart": "text", "arrivee": "text",
        "nombre_de_trains_programmes": "int", "nombre_de_trains_ayant_circule": "int",
        "nombre_de_trains_annules": "int", "nombre_de_trains_en_retard_a_l_arrivee": "int",
    },
    "ter": {
        "date": "date", "region": "text",
        "nombre_de_trains_programmes": "int", "nombre_de_trains_ayant_circule": "int",
        "nombre_de_trains_annules": "int", "nombre_de_trains_en_retard_a_l_arrivee": "int",
    },
    "gares_voyageurs": {"nom": "text", "codeinsee": "text", "codes_uic": "text", "position_geographique": "geo_point_2d"},
}


# Colonnes publiées mais volontairement non utilisées (pas d'avertissement)
IGNOREES: dict[str, set[str]] = {
    "tgv_aqst": {"commentaire_annulation", "nb_train_depart_retard", "retard_moyen_depart",
                 "retard_moyen_tous_trains_depart", "commentaire_retards_depart", "retard_moyen_tous_trains_arrivee",
                 "commentaires_retard_arrivee", "retard_moyen_trains_retard_sup15"},
    "intercites": {"taux_de_regularite", "nombre_de_trains_a_l_heure_pour_un_train_en_retard_a_l_arrivee"},
    "ter": {"taux_de_regularite", "nombre_de_trains_a_l_heure_pour_un_train_en_retard_a_l_arrivee", "commentaires"},
    "gares_voyageurs": {"libellecourt", "segment_drg", "id"},
}


class ErreurSource(Exception):
    """Une source a changé de format ou de contenu de façon incompatible."""


def verifier_metadonnees(cle: str, meta: dict) -> list[str]:
    """Compare le schéma déclaré par le portail au schéma attendu. Renvoie les avertissements."""
    attendus = SCHEMAS[cle]
    declares = {f["name"]: f["type"] for f in meta.get("fields", [])}
    erreurs = [f"colonne « {c} » absente" for c in attendus if c not in declares]
    erreurs += [f"colonne « {c} » de type {declares[c]} au lieu de {t}"
                for c, t in attendus.items() if c in declares and declares[c] != t]
    if erreurs:
        raise ErreurSource(f"Jeu {cle} : " + " ; ".join(erreurs))
    connues = set(attendus) | IGNOREES.get(cle, set())
    return [f"Jeu {cle} : nouvelle colonne « {c} » (ignorée)" for c in declares if c not in connues]


def verifier_table(con: duckdb.DuckDBPyConnection, cle: str) -> None:
    """Vérifie les colonnes et types réellement lus par DuckDB (Parquet ou CSV)."""
    colonnes = {r[0]: r[1] for r in con.sql(f"describe {cle}").fetchall()}
    for c, t in SCHEMAS[cle].items():
        if c not in colonnes:
            raise ErreurSource(f"Jeu {cle} : colonne « {c} » absente du fichier téléchargé")
        if t in TYPES_ACCEPTES and colonnes[c].split("(")[0] not in TYPES_ACCEPTES[t]:
            raise ErreurSource(f"Jeu {cle} : colonne « {c} » lue en {colonnes[c]}, attendu {t}")
