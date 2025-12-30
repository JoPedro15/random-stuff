import io
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from googleapiclient.discovery import Resource, build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from clients.gdrive.gdrive_client.auth import get_google_service_credentials


class GDriveClient:
    """
    Client to interact with Google Drive API v3 for automation tasks.

    This client handles authentication, file management (upload/existence checks),
    and advanced deletion logic including pagination and prefix filtering.
    """

    def __init__(
            self, credentials_path: Optional[str] = None, token_path: Optional[str] = None
    ) -> None:
        """
        Initializes the GDriveClient with robust path resolution for both
        credentials and token files.
        """
        # 1. Define the base directory of this client
        # Path of this file: .../automation-hub/clients/gdrive/gdrive_client/client.py
        base_dir: Path = Path(__file__).parent

        # 2. Resolve Credentials Path (Argument > Env Var > Default Hub Path)
        # Using parent.parent to go from 'gdrive_client' to 'gdrive' folder
        default_creds: str = str(base_dir.parent / "data" / "credentials.json")
        self.credentials_path: str = (
                credentials_path or os.getenv("GDRIVE_CREDENTIALS_PATH") or default_creds
        )

        # 3. Resolve Token Path (Argument > Env Var > Default Hub Path)
        default_token: str = str(base_dir.parent / "data" / "token.json")
        self.token_path: str = (
                token_path or os.getenv("GDRIVE_TOKEN_PATH") or default_token
        )

        # 4. Critical Path Validation
        if not os.path.exists(self.credentials_path):
            raise FileNotFoundError(
                f"❌ Credentials file missing! \nChecked: {self.credentials_path}"
            )

        # 5. Remaining configuration
        self.scopes: List[str] = ["https://www.googleapis.com/auth/drive"]
        self.output_folder_id: Optional[str] = os.getenv("OUTPUT_FOLDER_ID")

        # Initialize the actual Google service
        self.service: Resource = self._init_service()

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

    def upload_file(self, file_path: str, folder_id: Optional[str] = None) -> str:
        """
        Uploads a local file to a specific Google Drive folder.

        Args:
            file_path (str): Local path of the file to upload.
            folder_id (Optional[str]): Target folder ID.
            Defaults to OUTPUT_FOLDER_ID env var.

        Returns:
            str: The unique ID of the uploaded file in Google Drive.
        """
        file_name: str = os.path.basename(file_path)
        target_folder: str = folder_id or self.output_folder_id or ""

        file_metadata: Dict[str, Any] = {
            "name": file_name,
            "parents": [target_folder] if target_folder else [],
        }

        # Resumable=True is critical for reliability in large file uploads
        media: MediaFileUpload = MediaFileUpload(file_path, resumable=True)

        file: Dict[str, Any] = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        print(f"✅ File '{file_name}' uploaded. ID: {file.get('id')}")
        return str(file.get("id"))

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
    ) -> List[Dict[str, str]]:
        """
        Internal helper to fetch all files matching a query, handling pagination.

        Args:
            query (str): The Google Drive search query.
            fields (str): Fields to return for each file. Defaults to "id, name".

        Returns:
            List[Dict[str, str]]: Full list of all matching files across all pages.
        """
        all_files: List[Dict[str, str]] = []
        page_token: Optional[str] = None

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
        print(f">>> 🔎 Detected MIME type: {mime_type}")

        request = None
        # 2. Decide between Download or Export
        if "vnd.google-apps" in mime_type:
            # It's a Google Doc/Sheet/Slide - Need to export
            # For Google Sheets, we export to XLSX (suitable for pandas)
            export_mime: str = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            print(f">>> 🔄 Exporting Google Editor file to {export_mime}...")
            request = self.service.files().export_media(
                fileId=file_id, mimeType=export_mime
            )
        else:
            # It's a binary file - Standard download
            print(f">>> 📥 Downloading binary file...")
            request = self.service.files().get_media(fileId=file_id)

        # 3. Perform the actual data transfer
        fh = io.FileIO(local_path, "wb")
        downloader: MediaIoBaseDownload = MediaIoBaseDownload(fh, request)
        done: bool = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f">>> ⏳ Progress: {int(status.progress() * 100)}%")

        print(f"✅ File successfully saved to: {local_path}")

    def list_files(
            self, folder_id: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, str]]:
        """
        Lists files. If folder_id is None, it lists files from the root
        or generic drive access (useful for health checks).

        Args:
            folder_id (str): The ID of the folder to inspect.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing 'id' and 'name'.
        """
        query: str = "trashed = false"
        if folder_id or self.output_folder_id:
            target: str = folder_id or self.output_folder_id or ""
            query += f" and '{target}' in parents"

        results = (
            self.service.files()
            .list(q=query, spaces="drive", fields="files(id, name)", pageSize=limit)
            .execute()
        )
        return results.get("files", [])

    def _list_and_delete(self, query: str) -> List[str]:
        """
        Internal helper to fetch files based on a query and delete them.

        Args:
            query (str): Google Drive API search query.

        Returns:
            List[str]: List of deleted file IDs.
        """
        # We use our new helper to get ALL files first
        files_to_delete: List[Dict[str, str]] = self._fetch_files(query)
        deleted_ids: List[str] = []

        for f in files_to_delete:
            self.service.files().delete(fileId=f["id"]).execute()
            deleted_ids.append(f["id"])
            print(f"✅ Deleted: {f['name']} ({f['id']})")

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

    def clear_folder_content(self, folder_id: str) -> List[str]:
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

    def delete_files_by_prefix(self, folder_id: str, file_prefix: str) -> List[str]:
        """
        Deletes files that start with a specific string.

        Args:
            folder_id (str): The ID of the folder.
            file_prefix (str): Prefix to match (e.g., 'temp_').

        Returns:
            List[str]: IDs of deleted files.
        """
        if not folder_id or not file_prefix:
            print("⚠️ Skipping deletion: folder_id or prefix missing.")
            return []

        query: str = (
            f"'{folder_id}' in parents and trashed = false "
            f"and name startswith '{file_prefix}'"
        )
        return self._list_and_delete(query)
