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

- **Promotion Pattern**: The main interface is always exposed at the package root level (`__init__.py`), allowing clean
  imports like `from clients.gdrive import GDriveClient`.
- **Independent Lifecycles**: Each client has its own `Makefile` and `tests/`, allowing them to be validated in
  isolation or as part of the global pipeline.
- **Security Isolation**: Credentials and local caches are stored in an isolated `data/` folder within each client,
  ensuring secrets never leave their specific context.

## 🔌 Core Infrastructure Modules

Each module in the clients/ directory is an independent, installable Python package leveraging the Promotion Pattern
for clean API exposure.

### 🛠️ [Core Library](./clients/core_lib/README.md)

The foundation of the ecosystem. It provides the standardized ANSI-colored Logger used across all modules to enforce our
**Zero-Print Policy**.

- **Feature**: Thread-safe logging with precise timestamps and status-coded colors.

### 📂 [Google Drive Client](./clients/gdrive/README.md)

A high-level orchestration layer for the Google Drive API.

- **Feature**: Resilient IO, automated pagination, and secure file lifecycle management.

### 🧠 [AI Utilities](./clients/ai_utils/README.md)

Specialized tools for data acquisition and feature engineering.

- **Data Ingestor**: Managed acquisition with local cache validation and integrity checks.
- **Data Processor**: Type-safe feature engineering and categorical encoding.

## 🛠️ Global Quality Gate (GNU Make)

We use a unified orchestration system to ensure parity between local development and CI/CD pipelines.

### Environment Setup (`make setup`)

Our **5-Step Orchestrator** ensures a healthy environment:

- **VENV**: Creates a Python 3.12 virtual environment.
- **Dependencies**: Installs global requirements.
- **Client Linking**: Installs all clients in editable mode for cross-module development.
- **Integrity**: Runs a verification script to ensure all modules are correctly mapped.
- **Security**: Initializes pre-commit hooks and triggers a Bandit SAST scan.

### Quality Assurance (`make quality`)

The mandatory gate before any push. It executes:

- **Ruff**: Atomic linting and formatting (Scripts & Notebooks).
- **Pre-commit**: Validates AST, YAML syntax, and large file blocks.
- **Security**: Runs `Bandit` and `pip-audit` for vulnerability detection.
- **Tests**: Executes the full `pytest` suite across all clients.

## 📖 Governance & Standards

- **Type Safety**: Mandatory type annotations for all infrastructure methods.
- **No-Print Policy**: Raw `print` statements are strictly forbidden; use the `core-lib` Logger.
- **Clean Workspace**: Use `make clean` to purge caches and build artifacts.

______________________________________________________________________

**João Pedro** | Automation Engineer
<br />
[GitHub](https://github.com/JoPedro15) • [Automation Hub](https://github.com/JoPedro15/automation-hub) • [AI Lab](https://github.com/JoPedro15/ai-lab)
<br />
