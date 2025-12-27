# 🧩 Automation Hub Monorepo

[![Main CI](https://github.com/JoPedro15/automation-hub/actions/workflows/main.ci.yml/badge.svg)](https://github.com/JoPedro15/automation-hub/actions)
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A professional monorepo for modular Python services and automated workflows.

This repository follows **Monorepo Best Practices**, strictly separating
infrastructure (clients) from business logic (projects).

---

## 🏗️ Architecture & Structure

The repository is organized into distinct layers to ensure scalability and code reusability:

| Layer        | Path        | Description                                                                 |
|:-------------|:------------|:----------------------------------------------------------------------------|
| **Clients**  | `clients/`  | Standalone infrastructure connectors (Spotify, GDrive).                     |
| **Projects** | `projects/` | Application-level logic, AI experiments, and specific automation use cases. |
| **Common**   | `common/`   | Shared utilities (Auth helpers, Logging) reused across the repo.            |
| **Tooling**  | `tooling/`  | Centralized automation rules and CI/CD configurations.                      |

---

## 🔌 Available Clients

### Spotify Client

* **Purpose**: Integration with Spotify Web API.
* **Status**: Fully operational with OAuth2 support and CI testing.

### Google Drive Client

* **Purpose**: Automated file management (Upload/Download/List).
* **Technical Highlights**:
    * Dynamic path resolution for credentials.
    * Integrated with local `pytest` suite.
    * Supports specific folder uploads via `folder_id`.

---

## 🛠️ Tooling & Quality Gates

This project uses a centralized automation system via **GNU Make**.

### 1️⃣ Environment Setup

We use a single, shared virtual environment at the root level to minimize overhead:

```bash
make setup
source .venv/bin/activate
```