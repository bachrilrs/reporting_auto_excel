"""
Fonctions de nettoyage et de validation des données.

Ce module contient les fonctions responsables de :
- vérifier la présence des colonnes attendues ;
- contrôler les formats de données ;
- nettoyer les données brutes ;
- préparer le DataFrame pour l'analyse.
"""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {
    "date",
    "client",
    "statut",
    "commercial",
    "source",
    "montant",
}


def validate_required_columns(df: pd.DataFrame) -> None:
    """
    Vérifie que toutes les colonnes nécessaires sont présentes.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame à valider.

    Raises
    ------
    ValueError
        Si une ou plusieurs colonnes sont absentes.
    """
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Colonnes manquantes dans le fichier : {sorted(missing_columns)}"
        )


def is_datetime_convertible(df: pd.DataFrame, column_name: str) -> bool:
    """
    Vérifie si une colonne peut être convertie en datetime.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame à vérifier.
    column_name : str
        Nom de la colonne à vérifier.

    Returns
    -------
    bool
        True si la colonne peut être convertie, False sinon.
    """
    if column_name not in df.columns:
        return False

    converted = pd.to_datetime(df[column_name], errors="coerce")

    return converted.notna().all()


def contains_na(df: pd.DataFrame, column_name: str) -> bool:
    """
    Vérifie si une colonne contient des valeurs manquantes.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame à vérifier.
    column_name : str
        Nom de la colonne à vérifier.

    Returns
    -------
    bool
        True si la colonne contient au moins une valeur manquante.
    """
    if column_name not in df.columns:
        raise ValueError(f"La colonne '{column_name}' n'existe pas.")

    return df[column_name].isna().any()


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie les données brutes pour préparer l'analyse.

    Opérations réalisées :
    - validation des colonnes nécessaires ;
    - conversion de la date ;
    - nettoyage des champs texte ;
    - conversion du montant en numérique ;
    - création d'une colonne mois.

    Parameters
    ----------
    df : pd.DataFrame
        Données brutes.

    Returns
    -------
    pd.DataFrame
        Données nettoyées.
    """
    validate_required_columns(df)

    clean_df = df.copy()

    clean_df["date"] = pd.to_datetime(clean_df["date"], errors="coerce")
    clean_df["client"] = clean_df["client"].astype(str).str.strip()
    clean_df["statut"] = clean_df["statut"].astype(str).str.lower().str.strip()
    clean_df["commercial"] = clean_df["commercial"].astype(str).str.strip()
    clean_df["source"] = clean_df["source"].astype(str).str.strip()
    clean_df["montant"] = pd.to_numeric(
        clean_df["montant"],
        errors="coerce",
    ).fillna(0)

    clean_df["mois"] = clean_df["date"].dt.to_period("M").astype(str)

    return clean_df