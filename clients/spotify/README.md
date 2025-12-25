# 🎧 Spotify Client

A lightweight **Python client for the Spotify Web API**, built using the **Client Credentials Flow**.  
This module lets you authenticate, search for tracks or albums, and fetch album details — all through a simple CLI
interface.

---

## 🧩 Features

- 🔐 **Client Credentials authentication** (no user login required)
- 🎵 **Search tracks** by name, artist, and album
- 💿 **Fetch album details** by ID
- 🧱 Modular structure with reusable helpers
- 🧪 Fully testable with `pytest`, `ruff`, `black`, and `isort` integrations

## ⚙️ Setup

```
# 1️⃣ Activate repo venv (recommended)
source ../.venv/bin/activate

# 2️⃣ Install dependencies
make setup
```

## 🧠 Usage

▶️ Run the CLI

```
make run

```

## 🧪 Testing

This project includes automated tests powered by pytest.

### 🧰 Run all tests

```
make test
```

## 👩‍💻 Developer Commands

| Command         | Description                                          |
|-----------------|------------------------------------------------------|
| `make setup`    | Install dependencies into the repo’s `.venv`         |
| `make fmt`      | Format code using `isort` + `black`                  |
| `make lint`     | Run `ruff` linting                                   |
| `make lint-fix` | Auto-fix simple lint issues                          |
| `make test`     | Execute all tests with `pytest`                      |
| `make run`      | Launch CLI via `main.py`                             |
| `make clean`    | Remove caches (`__pycache__`, `.pytest_cache`, etc.) |

## 🧱 Project Structure

```
spotify/
├─ src/
│  ├─ client.py              # SpotifyClient class
│  ├─ main.py                # CLI entrypoint
│  └─ utils.py               # Helpers for formatting & parsing
├─ tests/
│  └─ client_test.py         # Unit/integration tests
├─ Makefile                  # Build & dev automation
├─ pyproject.toml            # Tooling setup (pytest, ruff, black, etc.)
└─ README.md                 # This file
```