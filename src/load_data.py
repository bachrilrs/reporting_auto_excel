#!/usr/bin/env python3

import pandas as pd


def load_data(file_path,separator=','):
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded data.
    """
    try:
        data = pd.read_csv(file_path, sep=separator)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except pd.errors.EmptyDataError:
        print(f"No data: {file_path} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Parsing error: Could not parse {file_path}.")
        return None