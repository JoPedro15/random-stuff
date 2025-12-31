# Detect if running in GitHub Actions
CI ?= false

# Variables
VENV           := .venv
CORE_LIB_DIR   := clients/core_lib
AI_UTILS_DIR   := clients/ai_utils
GDRIVE_DIR     := clients/gdrive

ifeq ($(CI), true)
    PY      := python3
    PIP     := pip
else
    PY      := $(VENV)/bin/python
    PIP     := $(VENV)/bin/pip
endif

REQ_DEV     := requirements.txt

.PHONY: setup update-deps security health test-all clean lint-all fmt-all

# --- Main Orchestration ---

# Full environment orchestration: Creates VENV, installs dependencies and audits security
setup:
	@echo ">>> 🛠️ Starting Full Environment Setup..."
	@if [ ! -d "$(VENV)" ]; then \
       echo ">>> Creating Virtual Environment..."; \
       python3 -m venv $(VENV); \
    fi
	@$(PIP) install --upgrade pip
	@$(MAKE) update-deps
	@$(MAKE) verify-env
	@$(MAKE) security
	@echo ">>> ✅ System ready, orchestrated and secured!"

# Installs root requirements and all clients in editable mode
update-deps:
	@echo ">>> 📦 Updating development requirements from $(REQ_DEV)..."
	$(PIP) install -U -r $(REQ_DEV)
	@echo ">>> 🏗️ Installing Core Foundation (core-lib)..."
	$(PIP) install -e $(CORE_LIB_DIR)
	@echo ">>> 🚀 Installing Domain Clients..."
	$(PIP) install -e $(GDRIVE_DIR)
	$(PIP) install -e $(AI_UTILS_DIR)

# Sanity check to ensure TOML dependencies (like openpyxl) were actually installed
verify-env:
	@echo ">>> 🔍 Verifying environment integrity..."
	@$(PY) -c "import openpyxl; import pandas; import core_lib_client; import ai_utils_client; print('>>> ✨ Integrity Check Passed: All packages found.')" || \
    (echo ">>> ❌ Integrity Check Failed: Missing dependencies. Check your pyproject.toml files." && exit 1)

# --- Security (The Shield) ---

security:
	@echo ">>> 🛡️ Running Security Analysis (Bandit)..."
	# Scanning all clients for common security issues
	$(PY) -m bandit -r clients/ -ll --exclude .venv,*/.venv/*
	@echo ">>> Running Dependency Audit (pip-audit)..."
	$(PY) -m pip_audit --skip-editable --ignore-vuln CVE-2025-53000

# --- Health & Monitoring ---

health:
	@echo ">>> Running Global Health Checks..."
    	@export PYTHONPATH=.:$(PYTHONPATH) && \
    	 $(PY) scripts/global_health_check.py

# --- Linting & Formatting (Universal & Fast) ---

lint-all:
	@echo ">>> 🔍 Global Linting with Ruff..."
	# We run from root to catch cross-package issues and import sorting
	$(PY) -m ruff check . --select E,F,I
	$(PY) -m ruff format --check .

fmt-all:
	@echo ">>> 🖋️ Global Formatting and Import Sorting..."
	$(PY) -m ruff check . --select I --fix
	$(PY) -m ruff format .

# --- Testing ---

test-all:
	@echo ">>> Running all automation tests..."
	$(MAKE) -C $(GDRIVE_DIR) test
	@echo ">>> ✨ All tests completed!"

# --- Cleanup ---

clean:
	@echo ">>> 🧹 Cleaning up project artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	@echo ">>> Workspace is clean."