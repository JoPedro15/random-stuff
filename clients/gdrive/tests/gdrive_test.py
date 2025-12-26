from pathlib import Path
from typing import Optional

from clients.gdrive import GDriveClient


def test_upload() -> None:
    """
    Test the upload functionality using the project's output folder structure.
    """
    # 1. Setup paths using pathlib for cross-platform compatibility
    # current_dir is clients/gdrive/tests
    current_dir: Path = Path(__file__).parent
    gdrive_root: Path = current_dir.parent

    # Define paths for credentials and token
    creds_path: str = str(gdrive_root / "data" / "credentials.json")
    token_path: str = str(gdrive_root / "data" / "token.json")

    # 2. Define and create the output directory
    output_dir: Path = gdrive_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 3. Create the dummy file inside the output folder
    test_file_path: Path = output_dir / "test_upload.txt"
    test_file_path.write_text(
        "Hello from Automation Hub! This is a test upload using the output folder."
    )

    # 4. Initialize the client
    client: GDriveClient = GDriveClient(
        credentials_path=creds_path,
        token_path=token_path,
    )

    # Consider moving this to an environment variable in the future
    target_folder_id: str = "1-R5QTpmZzh2LKs8zO5UKk80NLZ85p8u9"

    # 5. Perform upload using the absolute path of the file
    # Converting to string as most API clients expect str, not Path objects
    file_id: Optional[str] = client.upload_file(
        file_path=str(test_file_path), folder_id=target_folder_id
    )

    # 6. Assertions and Logging
    assert file_id is not None, "Failed to upload file to Google Drive"

    print(f"\nUpload successful! File stored in: {test_file_path}")
    print(f"File ID: {file_id}")


if __name__ == "__main__":
    test_upload()
