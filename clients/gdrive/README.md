# 📂 Google Drive Client

A standalone infrastructure connector for Google Drive API, providing standardized methods for file orchestration.

## ⚙️ Features

- **OAuth2 Authentication**: Automatic token refresh and credential management.
- **Promotion Pattern**: Simplified interface via `gdrive_client` package root.
- **Resilient Operations**: Custom exception handling for API timeouts and 404s.

## 🛠 Setup & Local Development

Each client is independent. To work specifically on this module:

```bash
  cd clients/gdrive
  make setup      # Configure local venv for GDrive only
  make test       # Run integration tests for GDrive
```

## 🏗 Implementation Details

### Promotion Pattern

To simplify usage in the Projects Layer, we expose the main client at the package level:

```python
# Instead of: from clients.gdrive.gdrive_client.client import GDriveClient
# Use:
from clients.gdrive import GDriveClient

client = GDriveClient(credentials_path="data/credentials.json")
```

### Key Methods

| Method                         | Description                                                |
|:-------------------------------|:-----------------------------------------------------------|
| `upload_file(src, folder_id)`  | Uploads a local file to a specific Google Drive folder.    |
| `download_file(file_id, dest)` | Downloads a file from Drive to the specified local path.   |
| `list_files(query)`            | Searches and lists files based on GDrive metadata queries. |

## Testing

This module uses `pytest with mocks to simulate API responses. Run tests using the local Makefile:

```bash
    make test
```

## Security

- **Credentials**: Stored in `data/credentials.json` (git-ignored).
- **Tokens**: Managed automatically in `data/token.json` (git-ignored).