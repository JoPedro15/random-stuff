# automation-hub/scripts/health_check_gdrive.py
import os
import sys
from pathlib import Path

# --- 1. Infrastructure Setup ---
PROJECT_ROOT: Path = Path(__file__).parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT))

# Import the client - using the promoted path from automation-hub
try:
    from clients.gdrive import GDriveClient
except ImportError as err:
    sys.stderr.write(f"❌ Critical Import Error in GDrive Health Check: {err}\n")
    sys.exit(1)


def run_check() -> tuple[bool, str]:
    """
    Performs a deep diagnostic for Google Drive integration.
    Validates credentials existence, token validity, and API reachability.

    Returns:
        tuple[bool, str]: (Success status, Diagnostic message)
    """
    # 1. Path & Environment Pre-check
    creds_path: str = os.getenv(
        "GDRIVE_CREDENTIALS_PATH", "clients/gdrive/data/credentials.json"
    )

    if not os.path.exists(creds_path):
        return False, f"Missing credentials file at: {creds_path}"

    try:
        # 2. Client Instantiation
        # The GDriveClient.__init__ already handles token directory creation
        client: GDriveClient = GDriveClient()

        # 3. API Communication Test
        # We perform a minimal 'list' operation to verify the token/auth flow
        files: list = client.list_files(limit=1)

        count: int = len(files)
        return True, f"Connection verified. Accessible files: {count}"

    except Exception as e:
        error_msg: str = str(e)

        # 4. Intelligent Error Categorization
        if "refresh_token" in error_msg.lower():
            return False, "Token expired or invalid. Please re-authenticate."
        if "unreachable" in error_msg.lower() or "connection" in error_msg.lower():
            return False, "Network unreachable. Check your internet connection."

        return False, f"Unexpected API failure: {error_msg}"


if __name__ == "__main__":
    # Allows standalone execution for manual debugging
    success, message = run_check()
    status: str = "✅" if success else "❌"
    sys.stderr.write(f"{status} GDrive Health: {message}")
    sys.exit(0 if success else 1)
