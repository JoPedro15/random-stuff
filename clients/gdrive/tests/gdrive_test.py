# ruff: noqa: S101
import os
import time
from pathlib import Path

import pytest
from dotenv import load_dotenv

from clients.gdrive import GDriveClient

OUTPUT_DIR: Path = Path(__file__).parent.parent / "output"


@pytest.fixture(scope="module")
def gdrive_setup() -> tuple[GDriveClient, str]:
    """
    Setup client and target folder for integration tests.
    Ensures environment variables are present before starting.
    """
    load_dotenv()

    # Ensure the output directory exists locally
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    root: Path = Path(__file__).parent.parent
    creds_path: Path = root / "data" / "credentials.json"
    token_path: Path = root / "data" / "token.json"

    # Check if files actually exist before passing them
    creds: str = str(creds_path) if creds_path.exists() else ""
    # In CI, token.json will likely not exist
    token: str = str(token_path) if token_path.exists() else ""

    folder_id: str = os.getenv("OUTPUT_FOLDER_ID", "")

    if not folder_id:
        pytest.skip("OUTPUT_FOLDER_ID not set, skipping integration tests.")

    # Ensure at least credentials exist
    if not creds:
        pytest.fail(f"Credentials not found at {creds_path}. Check CI setup.")

    client: GDriveClient = GDriveClient(creds, token)
    return client, folder_id


@pytest.mark.integration
def test_gdrive_full_lifecycle(gdrive_setup: tuple[GDriveClient, str]) -> None:
    """
    Tests the full CRUD lifecycle of files in Google Drive.

    Steps:
    1. Upload test_1.txt
    2. Check existence
    3. Upload multiple files (test_2, test_3)
    4. Delete specific file
    5. Clear entire folder
    6. Verify empty state
    """

    client, folder_id = gdrive_setup

    # Mapping filenames to their absolute local paths
    file_names: list[str] = ["test_1.txt", "test_2.txt", "test_3.txt"]
    local_paths: list[Path] = [OUTPUT_DIR / name for name in file_names]

    try:
        # Pre-test cleanup in the cloud
        client.clear_folder_content(folder_id)

        # --- TEST 1: Create/Upload test_1.txt ---
        target_path: Path = local_paths[0]
        with open(target_path, "w") as f:
            f.write("Automation test content")

        # Pass the string path to the client
        file_id_1: str = client.upload_file(str(target_path), folder_id)
        assert file_id_1 is not None

        # --- TEST 2: Validate existence ---
        assert client.file_exists(file_names[0], folder_id) is True

        # --- TEST 3: Add multiple files ---
        for path in local_paths[1:]:
            with open(path, "w") as f:
                f.write(f"Content for {path.name}")
            client.upload_file(str(path), folder_id)

        time.sleep(1)  # API propagation

        files_list: list = client.list_files(folder_id)
        assert len(files_list) == 3

        # --- TEST 4: Delete specific file ---
        client.delete_specific_file(file_names[2], folder_id)
        time.sleep(1)
        assert client.file_exists(file_names[2], folder_id) is False
        assert len(client.list_files(folder_id)) == 2

        # --- TEST 5 & 6: Clear all and validate ---
        client.clear_folder_content(folder_id)
        time.sleep(1)
        assert len(client.list_files(folder_id)) == 0

    finally:
        # Cleanup local artifacts in the output folder
        for path in local_paths:
            if path.exists():
                path.unlink()
