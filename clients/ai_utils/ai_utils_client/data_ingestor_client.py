# automation-hub/ai_utils_client/data_ingestor_client.py
import os

import pandas as pd

from clients.core_lib.core_lib_client.logger_client import logger
from clients.gdrive import GDriveClient


class DataIngestorClient:
    """
    Service class to handle data acquisition and local caching logic.
    Ensures data integrity before loading into the pipeline.
    """

    def __init__(self, gdrive_client: GDriveClient | None = None) -> None:
        """
        Initializes the ingestor.
        Injects a GDriveClient to reuse authentication sessions.

        Args:
            gdrive_client: An instance of GDriveClient.
            If None, a new one will be created.
        """

        if gdrive_client:
            self.gdrive = gdrive_client
        else:
            # SSoT: Getting credentials path from environment or default location
            creds_path: str = os.getenv(
                "GOOGLE_CREDENTIALS_PATH", "data/credentials.json"
            )
            # The client now requires at least the credentials_path
            self.gdrive = GDriveClient(credentials_path=creds_path)

    def get_spreadsheet_data(
        self,
        local_file_path: str,
        file_id: str,
        min_file_size: int = 500,
        force_download: bool = False,
    ) -> pd.DataFrame:
        """
        Retrieves spreadsheet data from a local cache or downloads it from GDrive.
        Automatically handles Google Sheets to Excel export conversion.

        Args:
            local_file_path: Target path on the local filesystem.
            file_id: Unique Google Drive file identifier.
            min_file_size: Minimum threshold in bytes to consider a file valid.
            force_download: If True, invalidates cache and triggers a new download.

        Returns:
            pd.DataFrame: The loaded dataset ready for processing.
        """

        file_exists: bool = os.path.exists(local_file_path)
        is_corrupted: bool = False

        # 1. Evaluate existing file health
        if file_exists:
            file_size: int = os.path.getsize(local_file_path)
            is_corrupted = file_size < min_file_size

        # 2. Handle Cache Invalidation
        # Deletes the file if it fails integrity check or if a fresh sync is requested
        if is_corrupted or force_download:
            reason: str = "File corrupted" if is_corrupted else "Force download"
            logger.info(
                f">>> Cache Invalidation ({reason}): removing {local_file_path}"
            )

            # Use safe removal to avoid race conditions
            if os.path.exists(local_file_path):
                os.remove(local_file_path)
            file_exists = False

        # 3. Data Acquisition Phase
        # Downloads from GDrive only if the local cache is empty or invalidated
        if not file_exists:
            logger.info(
                f">>> Resource missing or invalidated. Ingesting (ID: {file_id})..."
            )
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            self.gdrive.download_file(file_id=file_id, local_path=local_file_path)
        else:
            logger.info(f">>> File found: using existing file at {local_file_path}")

        # 4. Data Loading
        # We use 'openpyxl' as it is the standard for modern .xlsx files
        # exported by GDrive
        return pd.read_excel(local_file_path, engine="openpyxl")
