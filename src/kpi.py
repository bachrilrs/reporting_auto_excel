"""
API de reporting.

Ce module contient les fonctions qui transforment les données nettoyées
en tableaux exploitables pour le reporting Excel.
"""

from __future__ import annotations

import pandas as pd

from data_cleaning import clean_data


def build_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crée le tableau de résumé global.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame nettoyé.

    Returns
    -------
    pd.DataFrame
        Tableau de synthèse avec les principaux indicateurs.
    """
    total_ca = df.loc[df["statut"] == "gagné", "montant"].sum()
    nb_clients = df["client"].nunique()
    nb_opportunites = len(df)
    nb_gagnees = (df["statut"] == "gagné").sum()

    taux_conversion = (
        nb_gagnees / nb_opportunites
        if nb_opportunites > 0
        else 0
    )

    return pd.DataFrame(
        {
            "Indicateur": [
                "Chiffre d'affaires gagné",
                "Nombre de clients uniques",
                "Nombre d'opportunités",
                "Opportunités gagnées",
                "Taux de conversion",
            ],
            "Valeur": [
                total_ca,
                nb_clients,
                nb_opportunites,
                nb_gagnees,
                taux_conversion,
            ],
        }
    )


def build_top_clients(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crée le tableau des meilleurs clients par chiffre d'affaires.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame nettoyé.

    Returns
    -------
    pd.DataFrame
        Clients classés par chiffre d'affaires décroissant.
    """
    return (
        df[df["statut"] == "gagné"]
        .groupby("client", as_index=False)
        .agg(
            chiffre_affaires=("montant", "sum"),
            nombre_ventes=("montant", "count"),
        )
        .sort_values("chiffre_affaires", ascending=False)
    )


def build_source_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crée le tableau de performance par source d'acquisition.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame nettoyé.

    Returns
    -------
    pd.DataFrame
        Performance par source : opportunités, ventes gagnées,
        chiffre d'affaires et taux de conversion.
    """
    performance = (
        df.groupby("source", as_index=False)
        .agg(
            opportunites=("source", "count"),
            opportunites_gagnees=(
                "statut",
                lambda values: (values == "gagné").sum(),
            ),
            chiffre_affaires=(
                "montant",
                lambda values: values[
                    df.loc[values.index, "statut"] == "gagné"
                ].sum(),
            ),
        )
    )

    performance["taux_conversion"] = (
        performance["opportunites_gagnees"] / performance["opportunites"]
    )

    return performance.sort_values("chiffre_affaires", ascending=False)


def build_monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crée un tableau de chiffre d'affaires gagné par mois.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame nettoyé.

    Returns
    -------
    pd.DataFrame
        Chiffre d'affaires mensuel.
    """
    return (
        df[df["statut"] == "gagné"]
        .groupby("mois", as_index=False)
        .agg(chiffre_affaires=("montant", "sum"))
        .sort_values("mois")
    )


def generate_report_tables(raw_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Génère tous les tableaux nécessaires au reporting.

    Cette fonction sert de point d'entrée principal :
    elle prend les données brutes, les nettoie, puis retourne
    les différents tableaux prêts à exporter.

    Parameters
    ----------
    raw_df : pd.DataFrame
        Données brutes.

    Returns
    -------
    dict[str, pd.DataFrame]
        Dictionnaire contenant les différents onglets du reporting.
    """
    clean_df = clean_data(raw_df)

    return {
        "Données nettoyées": clean_df,
        "Résumé": build_summary(clean_df),
        "Top clients": build_top_clients(clean_df),
        "Performance sources": build_source_performance(clean_df),
        "CA mensuel": build_monthly_revenue(clean_df),
    }