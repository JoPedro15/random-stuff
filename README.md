# 🧩 Automation Hub Monorepo

<div style="text-align: center;">
    <img src="https://img.shields.io/badge/python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://github.com/JoPedro15/automation-hub/actions/workflows/ci-pipeline.yml/badge.svg?branch=main" alt="CI Quality Pipeline" />
  <img src="https://github.com/JoPedro15/automation-hub/actions/workflows/infrastructure-health.yml/badge.svg" alt="Infrastructure Health" />
  <br />

  <img src="https://img.shields.io/badge/linter-Ruff-000000?style=flat-square&logo=python&logoColor=white" alt="Ruff" />
  <img src="https://img.shields.io/badge/security-Bandit%20%7C%20Audit-44cc11?style=flat-square&logo=shield&logoColor=white" alt="Security" />
  <img src="https://img.shields.io/badge/stack-Monorepo-orange?style=flat-square&logo=git" alt="Monorepo" />
</div>

## 🚀 Overview

A professional monorepo for modular Python services and automated workflows.

This repository acts as the **Single Source of Truth (SSoT)** for our automation ecosystem, strictly separating
infrastructure (clients) from business logic (projects).

## 🏗️ Architecture & Structure

The repository is organized into distinct layers to ensure scalability and code reusability:

| Layer        | Path        | Description                                                                 |
|:-------------|:------------|:----------------------------------------------------------------------------|
| **Clients**  | `clients/`  | Standalone infrastructure connectors (Spotify, GDrive).                     |
| **Projects** | `projects/` | Application-level logic, AI experiments, and specific automation use cases. |
| **Common**   | `common/`   | Shared utilities (Auth helpers, Logging) reused across the repo.            |
| **Tooling**  | `tooling/`  | Centralized automation rules and CI/CD configurations.                      |

## 🔌 Standardized Client Architecture

Every client in `clients/` in this ecosystem is treated as an independent module:

1. Internal logic is hidden in submodules.
2. Main interface is exposed via `__init__.py`.
3. Independent testing suite and `pyproject.toml`.

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

For detailed implementation, usage examples, and API methods, refer to the specific documentation:

- **[Google Drive Client Documentation](./clients/gdrive/README.md)**

## 🛠️ Tooling & Quality Gates

We enforce high-quality standards through a centralized **GNU Make** automation system, ensuring parity between local
development and CI/CD pipelines.

### 1️⃣ Environment & Security Orchestration

The `make setup` command is our "Single Source of Truth" for environment health:

- **Automation**: Creates a Python 3.12 virtual environment and installs dependencies.
- **Safety**: Automatically triggers a security audit and configures **pre-commit hooks** to enforce standards locally.

### 2️⃣ Integrated Security & Quality Scanning

We integrate professional-grade tools to secure our research and code:

* **Static Analysis (SAST)**: `Bandit` scans for insecure patterns.
* **Vulnerability Audit**: `pip-audit` checks the dependency tree for known CVEs.
* **Unified Linting**: `Ruff` handles formatting, imports sorting, and logic linting in a single pass.

### 🛠️ Automation Commands

We use **GNU Make** to orchestrate quality gates across the monorepo:

| Command         | Description                                                           |
|:----------------|:----------------------------------------------------------------------|
| `make setup`    | Initializes environment, installs deps, and sets up pre-commit hooks. |
| `make quality`  | The full gate: Runs Ruff (Lint/Fmt), Security scans, and Tests.       |
| `make security` | Specifically triggers Bandit and pip-audit scans.                     |
| `make test`     | Executes pytest across all active clients and projects.               |
| `make clean`    | Purges all caches (`__pycache__`, `.pytest_cache`) and artifacts.     |

## 📖 Governance & Standards

This repository serves as the core governance center for all related automation projects.

- 🏛️ [Layered System](./docs/architecture/layered-system.md): Deep dive into our modular architecture.
- 🌿 [Git Conventions](./docs/standards/git-conventions.md): Branch naming and commit standards.

### Google Drive Client

* **Purpose**: Automated cloud storage management for AI datasets and outputs.
* **Technical Highlights**:
    * **Automated Pagination**: Seamlessly handles folders with thousands of items using internal _fetch_files.
    * **Security-First Deletion**: Supports strict prefix-based cleanup (test_*) and full folder purging.
    * **Resilient IO**: Implements Google's resumable media upload protocol for large file stability.
    * **Full Lifecycle Testing**: Integrated suite covering the entire CRUD flow.

______________________________________________________________________

<div align="center">
  <p>
    <strong>João Pedro Silva</strong> | Automation Engineer <br />
    <a href="https://github.com/JoPedro15">GitHub</a> •
    <a href="https://github.com/JoPedro15/automation-hub">Automation Hub</a> •
    <a href="https://github.com/JoPedro15/ai-lab">AI Lab</a>
  </p>
</div>
