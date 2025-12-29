# Layered System Architecture

This project follows a modular, layered architecture designed to separate core infrastructure from specific business
logic. This ensures high reusability and simplifies maintenance across the automation ecosystem.

## 🏗️ Architecture Overview

The system is divided into four main layers:

### 1. Clients Layer (`/clients`)

**The Infrastructure Layer.** Standalone connectors for external APIs (e.g., Google Drive).

- **Goal**: Handle authentication, rate limiting, and low-level API calls.
- **Rules**: No business logic; only "pipes" to communicate with external services.
- **Standard**: Every client must have its own `Makefile`, `tests/`, and `pyproject.toml`.

### 2. Common Layer (`/common`)

**The Shared Utilities Layer.**

- **Goal**: Provide cross-cutting concerns used by both Clients and Projects.
- **Content**: Logging configurations, custom decorators, and global exception handlers.
- **Rules**: Must be platform-agnostic and side-effect free.

### 3. Projects Layer (`/projects`)

**The Application/Orchestration Layer.**

- **Goal**: Where the actual automation happens. It consumes Clients to perform tasks.
- **Example**: `ai-lab` consuming `gdrive-client` to fetch datasets.
- **Rules**: Business logic resides here. Never talk directly to external APIs without a Client.

### 4. Tooling Layer (`/tooling`)

**The Governance & CI/CD Layer.**

- **Goal**: Host centralized scripts and GitHub Actions.
- **Standard**: The SSoT (Single Source of Truth) for linters and environment rules.

---

## 🛠️ Code Standards & Implementation

To maintain consistency across the ecosystem, the following standards are mandatory:

### Type Annotations (PEP 484)

All function signatures must use type hints to improve maintainability and IDE support.

### Promotion Pattern

A component is considered complete only if:

- [ ] Passes make quality (Linting, Security, Tests).
- [ ] Has 100% type annotation coverage.
- [ ] Documentation in docs/ is updated.