# automation-hub/scripts/health_check_data_ingestor.py
import os
import sys
from pathlib import Path

# --- 1. Infrastructure Setup ---
PROJECT_ROOT: Path = Path(__file__).parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT))

try:
    import openpyxl  # Added to satisfy Ruff's awareness of engine requirements
    import pandas as pd

    from clients.ai_utils.ai_utils_client.data_ingestor_client import DataIngestorClient
except ImportError as err:
    sys.stderr.write(f"❌ Critical Import Error in Data Ingestor Health Check: {err}\n")
    sys.exit(1)


def run_check() -> tuple[bool, str]:
    """
    Validates the Data Ingestor infrastructure.
    Checks: Dependencies, Path Integrity, and Cache Directory Permissions.
    """
    try:
        # 1. Dependency Check
        # Verify openpyxl version to ensure the engine is functional
        # and satisfy Ruff F401
        _engine_version: str = openpyxl.__version__
        pd.DataFrame()  # Smoke test for pandas

        # 2. Environment & Path Validation (Fix for Ruff F841)
        # We now use creds_path to verify if the file actually exists
        creds_path: str = os.getenv("GOOGLE_CREDENTIALS_PATH", "data/credentials.json")
        if not os.path.exists(creds_path):
            return False, f"Credentials file missing at: {creds_path}"

        # 3. Cache Write Permission Test
        test_cache_dir: Path = PROJECT_ROOT / "data" / "cache"
        try:
            test_cache_dir.mkdir(parents=True, exist_ok=True)
            test_file: Path = test_cache_dir / ".ingestor_write_test"
            test_file.write_text(f"connectivity_test_via_{_engine_version}")
            test_file.unlink()
        except Exception as e:
            return False, f"Cache directory (data/cache) is not writable: {str(e)}"

        # 4. Client Instantiation Smoke Test
        ingestor: DataIngestorClient = DataIngestorClient()

        if ingestor.gdrive is None:
            return False, "DataIngestor initialized with a null GDriveClient."

        return True, "Ingestor initialized and Cache IO verified."

    except Exception as e:
        return False, f"Ingestor Health Failure: {str(e)}"


if __name__ == "__main__":
    # Standalone execution for manual debugging
    success, message = run_check()
    status: str = "✅" if success else "❌"
    sys.stdout.write(f"{status} Data Ingestor Health: {message}\n")
    sys.exit(0 if success else 1)
