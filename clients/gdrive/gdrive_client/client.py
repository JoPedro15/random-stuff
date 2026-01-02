import io
import os
from pathlib import Path
from typing import Any

from googleapiclient.discovery import Resource, build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from clients.core_lib.core_lib_client.logger_client import logger
from clients.gdrive.gdrive_client.auth import get_google_service_credentials


class GDriveClient:
    """
    Client to interact with Google Drive API v3 for automation tasks.

    This client handles authentication, file management (upload/existence checks),
    and advanced deletion logic including pagination and prefix filtering.
    """

    def __init__(self, credentials_path: str, token_path: str = "") -> None:
        """
        Initializes the GDriveClient with robust path resolution for both
        credentials and token files.
        """
        # 1. Define the base directory of this client

        self.creds = None
        # Logic to handle missing token
        if token_path and os.path.exists(token_path):
            # Load existing token logic
            pass

        if not self.creds:
            # Fallback to Service Account or flow without token
            pass

        base_dir: Path = Path(__file__).parent

        # 2. Resolve Credentials Path
        default_creds: str = str(base_dir.parent / "data" / "credentials.json")
        self.credentials_path: str = (
            credentials_path or os.getenv("GDRIVE_CREDENTIALS_PATH") or default_creds
        )

        # 3. Resolve Token Path
        default_token: str = str(base_dir.parent / "data" / "token.json")
        self.token_path: str = (
            token_path or os.getenv("GDRIVE_TOKEN_PATH") or default_token
        )

        # 4. Critical Path Validation
        if not os.path.exists(self.credentials_path):
            raise FileNotFoundError(
                f"❌ Credentials file missing! \nChecked: {self.credentials_path}"
            )

        # 5. Configuration
        self.scopes: list[str] = ["https://www.googleapis.com/auth/drive"]
        self.output_folder_id: str | None = os.getenv("OUTPUT_FOLDER_ID")

        # 6. Initialize the service
        # Casting to Any here stops the "Unresolved attribute reference" in the IDE
        # while allowing you to use .files(), .list(), etc.
        self.service: Any = self._init_service()

    def _init_service(self) -> Resource:
        """
        Builds the Google Drive API service resource.

        Returns:
            Resource: An authorized Google Drive API service object.
        """
        if not os.path.exists(self.credentials_path):
            raise FileNotFoundError(
                f"Credentials file missing at: {self.credentials_path}"
            )
        creds = get_google_service_credentials(
            self.credentials_path, self.token_path, self.scopes
        )
        return build("drive", "v3", credentials=creds)

    def upload_file(
        self, file_path: str, folder_id: str, overwrite: bool = True
    ) -> str:
        """
        Uploads a file to Google Drive.
        If overwrite is True, it updates the existing file
        with the same name in the target folder.

        Args:
            file_path (str): Local path to the file.
            folder_id (str): GDrive ID of the destination folder.
            overwrite (bool): Default is True.
            If True, replaces existing file; else, creates a duplicate.

        Returns:
            str: The GDrive ID of the uploaded or updated file.
        """
        # Extract file name from the local path
        file_name: str = os.path.basename(file_path)

        # Initialize the media upload object for GDrive API
        media: MediaFileUpload = MediaFileUpload(file_path, resumable=True)

        # 1. Check for existing file if overwrite is enabled
        if overwrite:
            # Query to find files with the same name in the specific parent folder
            query: str = (
                f"name = '{file_name}' and '{folder_id}' in parents and trashed = false"
            )

            # Execute the search request
            response: dict[str, Any] = (
                self.service.files().list(q=query, fields="files(id)").execute()
            )

            existing_files: list[dict[str, str]] = response.get("files", [])

            if existing_files:
                # File exists: Perform an UPDATE operation instead of CREATE
                file_id: str = existing_files[0]["id"]
                logger.info(f"Overwriting existing file: {file_name} (ID: {file_id})")

                # Using service.files().update to replace the content of the existing ID
                updated_file = (
                    self.service.files()
                    .update(fileId=file_id, media_body=media)
                    .execute()
                )

                return updated_file.get("id")

        # 2. File does not exist or overwrite is False: Perform a CREATE operation
        file_metadata: dict[str, Any] = {"name": file_name, "parents": [folder_id]}

        logger.info(f"Uploading as a new file: {file_name}")

        # Using service.files().create to generate a new entry in GDrive
        new_file = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        return new_file.get("id")

    def file_exists(self, file_name: str, folder_id: str) -> bool:
        """
        Verifies if a file exists within a specific folder.

        Args:
            file_name (str): Exact name of the file.
            folder_id (str): ID of the parent folder.

        Returns:
            bool: True if the file exists and is not trashed.
        """
        query: str = (
            f"name = '{file_name}' and '{folder_id}' in parents and trashed = false"
        )
        results = (
            self.service.files()
            .list(q=query, spaces="drive", fields="files(id)")
            .execute()
        )

        return len(results.get("files", [])) > 0

    def _fetch_files(
        self, query: str, fields: str = "id, name"
    ) -> list[dict[str, str]]:
        """
        Internal helper to fetch all files matching a query, handling pagination.

        Args:
            query (str): The Google Drive search query.
            fields (str): Fields to return for each file. Defaults to "id, name".

        Returns:
            List[Dict[str, str]]: Full list of all matching files across all pages.
        """
        all_files: list[dict[str, str]] = []
        page_token: str | None = None

        while True:
            results = (
                self.service.files()
                .list(
                    q=query,
                    fields=f"nextPageToken, files({fields})",
                    pageToken=page_token,
                    spaces="drive",
                )
                .execute()
            )

            all_files.extend(results.get("files", []))

            page_token = results.get("nextPageToken")
            if not page_token:
                break

        return all_files

    def download_file(self, file_id: str, local_path: str) -> None:
        """
        Downloads a file from Google Drive.
        Handles both binary files and Google Docs Editor files (via export).
        """
        # 1. First, fetch metadata to check the MIME type
        file_metadata: dict = (
            self.service.files().get(fileId=file_id, fields="mimeType, name").execute()
        )

        mime_type: str = file_metadata.get("mimeType", "")
        logger.info(f">>> Detected MIME type: {mime_type}")

        request = None
        # 2. Decide between Download or Export
        if "vnd.google-apps" in mime_type:
            # It's a Google Doc/Sheet/Slide - Need to export
            # For Google Sheets, we export to XLSX (suitable for pandas)
            export_mime: str = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            logger.info(f">>> Exporting Google Editor file to {export_mime}...")
            request = self.service.files().export_media(
                fileId=file_id, mimeType=export_mime
            )
        else:
            # It's a binary file - Standard download
            logger.info(">>> Downloading binary file...")
            request = self.service.files().get_media(fileId=file_id)

        # 3. Perform the actual data transfer
        fh = io.FileIO(local_path, "wb")
        downloader: MediaIoBaseDownload = MediaIoBaseDownload(fh, request)
        done: bool = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                logger.info(f">>> Progress: {int(status.progress() * 100)}%")

        logger.success(f"File successfully saved to: {local_path}")

    def list_files(
        self, folder_id: str | None = None, limit: int = 10
    ) -> list[dict[str, str]]:
        """
        Lists files in a specific folder or across the drive.

        Args:
            folder_id (Optional[str]): The ID of the folder to inspect.
                If None, uses root or generic access.
            limit (int): Maximum number of files to return. Defaults to 10.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing 'id' and 'name'.
        """
        query: str = "trashed = false"
        if folder_id or self.output_folder_id:
            target: str = folder_id or self.output_folder_id or ""
            query += f" and '{target}' in parents"

        # Break the chain into multiple lines to avoid E501 and improve readability
        results = (
            self.service.files()
            .list(q=query, spaces="drive", fields="files(id, name)", pageSize=limit)
            .execute()
        )
        return results.get("files", [])

    def _list_and_delete(self, query: str) -> list[str]:
        """
        Internal helper to fetch files based on a query and delete them.

        Args:
            query (str): Google Drive API search query.

        Returns:
            List[str]: List of deleted file IDs.
        """
        # We use our new helper to get ALL files first
        files_to_delete: list[dict[str, str]] = self._fetch_files(query)
        deleted_ids: list[str] = []

        for f in files_to_delete:
            self.service.files().delete(fileId=f["id"]).execute()
            deleted_ids.append(f["id"])
            logger.success(f"Deleted: {f['name']} ({f['id']})")

        return deleted_ids

    def delete_specific_file(self, file_name: str, folder_id: str) -> bool:
        """
        Deletes a specific file by name in a folder.

        Args:
            file_name (str): The name of the file to remove.
            folder_id (str): The ID of the folder.

        Returns:
            bool: True if files were deleted, False if none were found.
        """
        query: str = (
            f"name = '{file_name}' and '{folder_id}' in parents and trashed = false"
        )
        deleted = self._list_and_delete(query)
        return len(deleted) > 0

    def clear_folder_content(self, folder_id: str) -> list[str]:
        """
        Permanently removes all files and subfolders from a folder.

        Args:
            folder_id (str): The ID of the folder to empty.

        Returns:
            List[str]: IDs of all deleted items.
        """
        if not folder_id:
            return []

        query: str = f"'{folder_id}' in parents and trashed = false"
        return self._list_and_delete(query)

    def delete_files_by_prefix(self, folder_id: str, file_prefix: str) -> list[str]:
        """
        Deletes files in a specific folder that start with a given prefix.
        Uses 'contains' for GDrive API search and refines with Python's startswith.

        Args:
            folder_id (str): The ID of the GDrive folder.
            file_prefix (str): The prefix to match (e.g., 'test_').

        Returns:
            List[str]: A list of IDs of the deleted files.
        """
        if not folder_id or not file_prefix:
            logger.warning("Skipping deletion: folder_id or prefix missing.")
            return []

        # 1. Search for files containing the prefix
        # (startswith is not supported by GDrive API)
        # This query is valid for GDrive API v3
        query: str = (
            f"'{folder_id}' in parents and "
            f"name contains '{file_prefix}' and "
            f"trashed = false"
        )

        # 2. Fetch files from GDrive
        # We fetch name and id to perform client-side filtering
        files_found: list[dict[str, str]] = self._fetch_files(query)

        if not files_found:
            logger.info(f"No files found containing prefix: '{file_prefix}'")
            return []

        # 3. Refine the list using Python's startswith (Precise Filtering)
        # This prevents deleting files like 'backup_test_file.csv'
        # when prefix is 'test_'
        file_ids_to_delete: list[str] = [
            f["id"] for f in files_found if f["name"].startswith(file_prefix)
        ]

        if not file_ids_to_delete:
            logger.info(f"No files strictly starting with: '{file_prefix}'")
            return []

        # 4. Perform the deletion using your existing internal method
        logger.info(
            f"Deleting {len(file_ids_to_delete)} files with prefix '{file_prefix}'..."
        )

        # Assuming _list_and_delete accepts a list of IDs or we call a delete method
        # Since your original code passed a query to _list_and_delete,
        # you might need to adjust that method to accept IDs directly or
        # iterate through them:

        deleted_ids: list[str] = []
        for fid in file_ids_to_delete:
            try:
                self.service.files().delete(fileId=fid).execute()
                deleted_ids.append(fid)
            except Exception as e:
                logger.error(f"Failed to delete file {fid}: {str(e)}")

        return deleted_ids
