from typing import List

import pandas as pd


def encode_categorical_features(
        df: pd.DataFrame, columns: List[str], drop_first: bool = True
) -> pd.DataFrame:
    """
    Encodes categorical features using One-Hot Encoding.

    Args:
        df: The input pandas DataFrame.
        columns: A list of column names to be encoded.
        drop_first: Whether to get k-1 dummies out of k categorical levels.
    """
    # Filter columns that actually exist in the DataFrame
    existing_cols: List[str] = [col for col in columns if col in df.columns]

    if not existing_cols:
        return df

    return pd.get_dummies(df, columns=existing_cols, drop_first=drop_first)
