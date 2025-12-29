# Layered System Architecture

This project follows a modular, layered architecture designed to separate core infrastructure from specific business
logic. This ensures high reusability and simplifies maintenance across the automation ecosystem.

## 🏗️ Architecture Overview

The system is divided into four main layers:

### 1. Clients Layer (`/clients`)

The **Infrastructure Layer**. It contains standalone connectors for external APIs (e.g., Spotify, Google Drive).

- **Goal**: Handle authentication, rate limiting, and low-level API calls.
- **Rules**: Clients should not contain business logic; they only provide the "pipes" to communicate with external
  services.
- **Standard**: Every client must have its own `Makefile`, `tests/`, and `pyproject.toml`.

### 2. Common Layer (`/common`)

The **Shared Utilities Layer**.

- **Goal**: Provide cross-cutting concerns used by both Clients and Projects.
- **Content**: Logging configurations, custom decorators, data validation schemas, and global exception handlers.
- **Rules**: Must be platform-agnostic and side-effect free.

### 3. Projects Layer (`/projects`)

The **Application/Orchestration Layer**.

- **Goal**: Where the actual automation happens. It consumes one or more Clients to perform specific tasks.
- **Examples**: AI-lab experiments, automated data syncing, or notification engines.
- **Rules**: This is where business logic resides. Projects should never talk directly to external APIs without using a
  Client.

### 4. Tooling Layer (`/tooling`)

The **Governance & CI/CD Layer**.

- **Goal**: Host centralized scripts, GitHub Actions, and quality gate configurations.
- **Standard**: The SSoT (Single Source of Truth) for linters, security scanners, and environment setup rules.

---

## 🛠️ Code Standards within Layers

- **Type Annotations**: Mandatory for all function signatures.
- **Modular Imports**: Packages must expose their main classes via `__init__.py` (Promotion Pattern).
- **Error Handling**: Clients must raise custom exceptions that Projects can catch and handle.DoD).