# 🧩 Automation Hub Monorepo

![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![CI Quality Pipeline](https://github.com/JoPedro15/automation-hub/actions/workflows/ci-pipeline.yml/badge.svg?branch=main)
![Infrastructure Health](https://github.com/JoPedro15/automation-hub/actions/workflows/infrastructure-health.yml/badge.svg)
<br />
![Ruff](https://img.shields.io/badge/linter-Ruff-000000?style=flat-square&logo=python&logoColor=white)
![Security](https://img.shields.io/badge/security-Bandit%20%7C%20Audit-44cc11?style=flat-square&logo=shield&logoColor=white)

## 🚀 Overview

A professional Infrastructure Monorepo designed for modular Python services and automated foundation layers.

This repository acts as the Single Source of Truth (SSoT) for our automation ecosystem, providing production-ready
connectors and utilities to be consumed by external research and application projects.

## 🏗️ Architecture & Structure

The repository is organized into distinct functional layers to ensure absolute separation of concerns and
infrastructure stability:

| Layer                        | Path         | Description                                                        |
| :--------------------------- | :----------- | :----------------------------------------------------------------- |
| **Infrastructure (Clients)** | `clients/`   | Standalone, independent connectors (Core, GDrive, AI Utils).       |
| **Governance (Docs)**        | `docs/`      | Engineering standards, architecture diagrams, and Git conventions. |
| **Orchestration (Scripts)**  | `scripts/`   | Global maintenance tools and environment health checks.            |
| **Tooling**                  | `Root Files` | Centralized quality gates (`Makefile`, `.pre-commit-config.yaml`). |

## 🔌 Standardized Client Architecture

Every client in `clients/` is treated as an independent, industrial-grade module to ensure maintainability and
scalability.

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

### Key Principles:

- **Promotion Pattern**: Promotion Pattern: Interfaces are exposed at the package root level (`__init__.py`),
  allowing clean imports like \`from clients.gdrive import GDriveClient.
- **Independent Lifecycles**: Each client can be validated in isolation or as part of the global pipeline via
  the root \`Makefile.
- **Security Isolation**: Credentials and local caches are stored in an isolated \`data/ folder within each client
- context.
- **Silent Testing**: Pytest is pre-configured to suppress third-party **DeprecationWarnings**
  (e.g., Google API/httplib2), ensuring focus on actionable logs.

## 🔌 Core Infrastructure Modules

Each module in the clients/ directory is an independent, installable Python package leveraging the Promotion Pattern
for clean API exposure.

### 🛠️ [Core Library](./clients/core_lib/README.md)

The ecosystem's foundation. Provides the standardized ANSI-colored Logger used across all modules to enforce our
**Zero-Print Policy**.

### 📂 [Google Drive Client](./clients/gdrive/README.md)

A high-level orchestration layer for the Google Drive API, featuring resilient IO and automated pagination.

### 🧠 [AI Utilities](./clients/ai_utils/README.md)

Specialized tools for data acquisition and feature engineering, providing type-safe processors and managed ingestors.

## 🛠️ Global Quality Gate (GNU Make)

We use a unified orchestration system to ensure parity between local development and CI/CD pipelines.

### Environment Setup (`make setup`)

Our **4-Step Orchestrator** ensures a healthy environment:

- **VENV**: Initializes a Python 3.12 virtual environment.
- **Requirements**: Installs all global and development dependencies.
- **Editable Mapping**: Installs all clients in **Editable Mode** for real-time cross-module development.
- **Integrity Check**: Executes a smoke test to verify module discovery and package health.

### Quality Assurance (`make quality`)

The mandatory gate before any push. It executes:

- **Ruff**: Unified engine for Linting, Formatting, and **Security SAST (Bandit rules)**.
- **Pre-commit**: Local validation of AST, YAML syntax, and strict No-Print policies.
- **Security Audit**: Scans dependencies for known vulnerabilities (CVEs) via `pip-audit`.
- **Tests**: Executes the full \`pytest suite with automated warning suppression.

## 📖 Governance & Standards

- **Type Safety**: Mandatory type annotations for all infrastructure methods.
- **No-Print Policy**: Raw `print` statements are strictly forbidden; use the `core-lib` Logger.
- **Clean Workspace**: Use `make clean` to purge caches and build artifacts.

______________________________________________________________________

**João Pedro** | Automation Engineer
<br />
[GitHub](https://github.com/JoPedro15) • [Automation Hub](https://github.com/JoPedro15/automation-hub) • [AI Lab](https://github.com/JoPedro15/ai-lab)
<br />
