# 🧠 Random Stuff

A collection of small, focused Python projects — each exploring a different API, automation, or learning experiment.  
This repository serves as a playground for building and testing ideas with clean structure and reusable tooling.

---

## 📂 Structure

Each subfolder is an **independent, testable project** that can be run with its own Makefile and dependencies.

---

## 🧰 Tooling

All projects share a consistent developer setup powered by:

- **Python ≥ 3.9**
- **Black**, **isort**, and **Ruff** for formatting and linting
- **Makefiles** for automation (`setup`, `lint`, `test`, `run`)
- A common logging utility (`common/python/logging_utils.py`)

---

## ⚙️ Developer Workflow

```bash
# Install or update dependencies
make setup

# Format and lint all code
make fmt
make lint

# Run tests (if available)
make test

# Run a project (inside its folder)
cd spotify
make run
