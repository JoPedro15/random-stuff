# automation-hub/scripts/health_check_data_processor.py
import sys
from pathlib import Path

# --- 1. Infrastructure Setup ---
PROJECT_ROOT: Path = Path(__file__).parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT))

try:
    import numpy as np
    import pandas as pd

    from clients.ai_utils.ai_utils_client.data_processor_client import (
        DataProcessorClient,
    )
except ImportError as err:
    sys.stderr.write(
        f"❌ Critical Import Error in Data Processor Health Check: {err}\n"
    )
    sys.exit(1)


def run_check() -> tuple[bool, str]:
    """
    Validates the Data Processor infrastructure and core transformation logic.
    Checks: Dependencies, Client Instantiation, and Encoding Engine integrity.
    """
    try:
        # 1. Instantiate Client
        processor: DataProcessorClient = DataProcessorClient()

        # 2. Logic Smoke Test: Categorical Encoding
        # We create a dummy dataframe to verify if the encoding engine is functional
        test_df: pd.DataFrame = pd.DataFrame(
            {"category": ["A", "B", "A"], "value": [1, 2, 3]}
        )

        encoded_df: pd.DataFrame = processor.encode_categorical_features(
            test_df, columns=["category"], drop_first=True
        )

        # Validation: If drop_first=True, 'category' column is removed
        # and replaced by n-1 dummy columns
        if "category" in encoded_df.columns or encoded_df.empty:
            return (
                False,
                "Encoding logic failed: Columns were not transformed correctly.",
            )

        # 3. Logic Smoke Test: Missing Values
        # Verify if the pandas dropna integration is working
        df_nan: pd.DataFrame = pd.DataFrame({"val": [1, np.nan, 3]})
        df_cleaned: pd.DataFrame = processor.handle_missing_values(
            df_nan, strategy="drop"
        )

        if len(df_cleaned) != 2:
            return False, "Missing values handler failed: Rows were not dropped."

        return True, "Processor logic and dependencies (Pandas/Numpy) verified."

    except Exception as e:
        return False, f"Data Processor Health Failure: {str(e)}"


if __name__ == "__main__":
    # Standalone execution for manual debugging
    success, message = run_check()
    status: str = "✅" if success else "❌"
    sys.stdout.write(f"{status} Data Processor Health: {message}\n")
    sys.exit(0 if success else 1)
