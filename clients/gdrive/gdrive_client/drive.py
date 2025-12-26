import os
from typing import Any, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class GDriveClient:
    """
    Service client for Google Drive API v3 operations.
    Handles automated OAuth2 authentication and file management.
    """

    # Full drive access scope
    SCOPES: List[str] = ["https://www.googleapis.com/auth/drive"]

    def __init__(
        self,
        credentials_path: str = "data/credentials.json",
        token_path: str = "data/token.json",
    ) -> None:
        """
        Initialize the client with paths to security credentials.
        """
        self.credentials_path: str = credentials_path
        self.token_path: str = token_path
        # Use Any here because the Google Resource object is dynamically built
        self.service: Any = self._authenticate()

    def _authenticate(self) -> Any:
        """
        Authenticates the user using OAuth2 flow.

        Returns:
            Any: The authorized Google Drive service object (Resource).
        """
        creds: Optional[Credentials] = None

        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        # Returning as Any bypasses the IDE's static analysis for dynamic methods
        return build("drive", "v3", credentials=creds)

    def list_files(self, limit: int = 10) -> List[dict[str, str]]:
        """
        Retrieve a list of files from the drive.
        """
        # The IDE will no longer flag .files() as unresolved
        results = (
            self.service.files()
            .list(pageSize=limit, fields="nextPageToken, files(id, name)")
            .execute()
        )
        return results.get("files", [])

    def download_file(self, file_id: str, local_path: str) -> None:
        """
        Download a file from GDrive to a local destination.
        """
        request = self.service.files().get_media(fileId=file_id)
        with open(local_path, "wb") as f:
            f.write(request.execute())

    def upload_file(self, file_path: str, folder_id: Optional[str] = None) -> str:
        """
        Uploads a local file to Google Drive.
        """
        file_metadata: dict[str, Any] = {"name": os.path.basename(file_path)}
        if folder_id:
            file_metadata["parents"] = [folder_id]

        media = MediaFileUpload(file_path, resumable=True)

        file = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        return file.get("id")
