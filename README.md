# 🧩 Random Stuff Monorepo

[![Spotify CI](https://github.com/JoPedro15/random-stuff/actions/workflows/spotify.ci.yml/badge.svg)](https://github.com/JoPedro15/random-stuff/actions)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A collection of modular Python services, clients, and automated experiments.
This repository follows **Monorepo Best Practices**, with a clear separation between infrastructure (clients) and
business logic (projects).

---

## 🏗️ Architecture & Structure

The repository is organized into distinct layers to ensure scalability and code reusability:

| Layer        | Path        | Description                                                                     |
|:-------------|:------------|:--------------------------------------------------------------------------------|
| **Clients**  | `clients/`  | Infrastructure connectors (e.g., Spotify API). Designed as standalone packages. |
| **Projects** | `projects/` | Application-level logic and specific use cases.                                 |
| **Common**   | `common/`   | Shared utilities (Logging, Env Management, etc.) reused across the repo.        |
| **Tooling**  | `tooling/`  | Centralized Makefile rules and CI/CD configurations.                            |

---

## 🛠️ Global Tooling & Quality Gates

This project uses a centralized automation system via **GNU Make**.

### 1️⃣ Environment Setup

We use a single, shared virtual environment at the root level to minimize overhead:

```bash
make setup
source .venv/bin/activate
``