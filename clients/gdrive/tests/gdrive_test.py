from pathlib import Path

from clients.gdrive import GDriveClient


def test_upload() -> None:
    """
    Test the upload functionality by dynamically locating credentials.
    """
    # 1. Get the directory where this test file is located (automation-hub/clients/gdrive/tests)
    current_dir: Path = Path(__file__).parent

    # 2. Navigate up to 'clients/gdrive' and then into 'data'
    # This works regardless of where you run the test from
    gdrive_root: Path = current_dir.parent
    creds_path: str = str(gdrive_root / "data" / "credentials.json")
    token_path: str = str(gdrive_root / "data" / "token.json")

    # Initialize the client
    client: GDriveClient = GDriveClient(
        credentials_path=creds_path,
        token_path=token_path,
    )

    TARGET_FOLDER_ID = "1-R5QTpmZzh2LKs8zO5UKk80NLZ85p8u9"

    # 3. Create a dummy file for testing
    test_file: str = "test_upload.txt"
    with open(test_file, "w") as f:
        f.write("Hello from Automation Hub! This is a dynamic path test upload.")

    # 4. Perform upload and assert
    file_id = client.upload_file(file_path=test_file, folder_id=TARGET_FOLDER_ID)

    assert file_id is not None
    print(f"\nUpload successful to folder {TARGET_FOLDER_ID}! File ID: {file_id}")


if __name__ == "__main__":
    test_upload()
