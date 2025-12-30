from typing import List

import pandas as pd


class DataProcessorClient:
    """
    Client specialized in data processing and feature engineering tasks.

    This client provides standardized methods to transform DataFrames,
    ensuring consistency across different AI and Data Science projects.
    """

    def __init__(self) -> None:
        """
        Initializes the DataProcessorClient.
        Currently stateless, but prepared for future global configurations.
        """
        pass

    def encode_categorical_features(
            self, df: pd.DataFrame, columns: List[str], drop_first: bool = True
    ) -> pd.DataFrame:
        """
        Encodes categorical features using One-Hot Encoding (Dummy Encoding).

        Args:
            df (pd.DataFrame): The input pandas DataFrame.
            columns (List[str]): A list of column names to be encoded.
            drop_first (bool): Whether to get k-1 dummies out of k categorical levels
                             to prevent multicollinearity. Defaults to True.

        Returns:
            pd.DataFrame: A new DataFrame with transformed categorical features.
        """
        # Filter columns that actually exist in the DataFrame to prevent errors
        existing_cols: List[str] = [col for col in columns if col in df.columns]

        if not existing_cols:
            print("⚠️ No matching columns found for encoding.")
            return df

        return pd.get_dummies(df, columns=existing_cols, drop_first=drop_first)

    def handle_missing_values(
            self, df: pd.DataFrame, strategy: str = "drop"
    ) -> pd.DataFrame:
        """
        Example of a future method to maintain consistency with the GDrive template.

        Args:
            df (pd.DataFrame): Input DataFrame.
            strategy (str): Method to handle NaNs ('drop' or 'fill').
        """
        if strategy == "drop":
            return df.dropna()
        return df
