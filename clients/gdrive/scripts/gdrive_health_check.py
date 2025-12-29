from typing import Tuple

from clients.gdrive import GDriveClient


def run_gdrive_check() -> Tuple[bool, str]:
    """
    Performs local validation for Google Drive.
    This module knows where its credentials are.
    """
    try:
        client = GDriveClient()
        client.list_files(limit=1)
        return True, "Connection successful."
    except Exception as e:
        return False, f"Connection failed: {str(e)}"
