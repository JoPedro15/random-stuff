# 🧩 Automation Hub Monorepo

[![Main CI](https://github.com/JoPedro15/automation-hub/actions/workflows/main.ci.yml/badge.svg)](https://github.com/JoPedro15/automation-hub/actions)
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![Security: Bandit](https://img.shields.io/badge/security-bandit-yellow)
![Security: pip--audit](https://img.shields.io/badge/security-pip--audit-green)
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

## 🔌 Standardized Client Architecture

Every client under the clients/ directory follows a predictable, industrial-grade pattern to ensure maintainability:

```text
clients/
└── <service>/
    ├── data/               # Persistent tokens and local credentials (git-ignored)
    ├── <service>_client/   # Core logic package
    │   ├── __init__.py     # Package exposure and class promotion
    │   ├── client.py       # Main Service Client (Refactored architecture)
    │   └── auth.py         # Authentication & OAuth2 Handlers
    ├── tests/              # Pytest integration suites
    ├── Makefile            # Local task runner (test, lint, fmt)
    └── pyproject.toml      # Build system and tool configuration
```

## 🔌 Available Clients

### Spotify Client

* **Purpose**: Integration with Spotify Web API.
* **Status**: Fully operational with OAuth2 support and CI testing.

### Google Drive Client

* **Purpose**: Automated cloud storage management for AI datasets and outputs.
* **Technical Highlights**:
    * **Automated Pagination**: Seamlessly handles folders with thousands of items using internal _fetch_files.
    * **Security-First Deletion**: Supports strict prefix-based cleanup (test_*) and full folder purging.
    * **Resilient IO**: Implements Google's resumable media upload protocol for large file stability.
    * **Full Lifecycle Testing**: Integrated suite covering the entire CRUD flow.

---

## 🛠️ Tooling & Quality Gates

We enforce high-quality standards through a centralized **GNU Make** automation system.

### 1️⃣ Environment & Security Orchestration

The **make setup** command is the "Single Source of Truth" for environment health:

```bash
make setup      # Creates VENV, installs dependencies, and runs Security Audits
source .venv/bin/activate
```

### 2️⃣ Integrated Security Scanning

We don't just write code; we secure it. Our setup includes:

* **Static Analysis (SAST)**: Using Bandit to detect insecure patterns (e.g., eval, shell=True).
* **Dependency Auditing**: Using pip-audit to scan for known vulnerabilities (CVEs) in third-party libraries.

### 3️⃣ Quality Commands

### 🛠️ Automation Commands

The project uses `make` to orchestrate quality gates and testing. Below are the primary commands available from the root
directory:

| Command         | Description                                                                        |
|:----------------|:-----------------------------------------------------------------------------------|
| `make test-all` | Runs integration tests across all clients (GDrive, Spotify).                       |
| `make security` | Triggers a full security scan (Bandit & pip-audit) excluding virtual environments. |
| `make lint-all` | Runs static code analysis via **Ruff** to ensure code quality.                     |
| `make fmt-all`  | Standardizes code style using **Black** and **Isort**.                             |
| `make clean`    | Purges all caches (`__pycache__`, `.pytest_cache`) and local test artifacts.       |