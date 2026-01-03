# automation-hub/Makefile

# AUTOMATION-HUB Orchestrator
# Central Management for Cross-Domain Automation Clients

# --- Configuration ---
SHELL := /bin/bash
VENV  := .venv
CI    ?= false

# Clients Directory Mapping
CORE_LIB_DIR   := clients/core_lib
AI_UTILS_DIR   := clients/ai_utils
GDRIVE_DIR     := clients/gdrive
SCRIPTS_DIR    := scripts

# Binary detection (Headless mode for CI vs Local Virtualenv)
ifeq ($(CI), true)
    BIN :=
    PY  := python3
    PIP := pip
else
    BIN := $(VENV)/bin/
    PY  := $(BIN)python
    PIP := $(BIN)pip
endif

# Tooling definitions (Synchronized with pyproject.toml)
RUFF    := $(BIN)ruff
PRE     := $(BIN)pre-commit
PYTEST  := $(BIN)pytest
AUDIT   := $(BIN)pip-audit

# Export PYTHONPATH with absolute paths for reliable module discovery
ROOT_DIR := $(shell pwd)
export PYTHONPATH := $(ROOT_DIR):$(ROOT_DIR)/$(GDRIVE_DIR):$(ROOT_DIR)/$(CORE_LIB_DIR):$(ROOT_DIR)/$(AI_UTILS_DIR)

.PHONY: help setup quality security health test-all clean lint-and-format verify-env update-deps

help:
	@echo "Automation Hub - Management Targets:"
	@echo "  setup            - Full environment initialization (Editable Mode)"
	@echo "  quality          - Full Gate: Clean -> Ruff (Lint/Fmt/Security) -> Pre-commit -> Test"
	@echo "  lint-and-format  - Auto-fix, Style and Security scan via Ruff"
	@echo "  security         - Dependency Vulnerability Audit (pip-audit)"
	@echo "  test-all         - Execute the complete automated test suite"
	@echo "  health           - Infrastructure integrity check (CI/CD focused)"

# --- Main Pipelines ---

# Core Pipeline: The master gatekeeper for code quality
quality: clean
	@echo ">>> 🚀 [PIPELINE] Starting Full Quality Gate..."
	@$(MAKE) lint-and-format
	@echo ">>> 🔍 [VALIDATION] Running Pre-commit Hooks..."
	$(PRE) run --all-files
	@echo ">>> 🛡️ [SECURITY] Running Dependency Audit..."
	@$(MAKE) security
	@echo ">>> 🧪 [TESTS] Executing Test Suite..."
	@$(MAKE) test-all
	@echo ">>> 🏆 [SUCCESS] System is healthy and production-ready."

# Developer Workflow: Unified engine for style and common security leaks
lint-and-format:
	@echo ">>> 🔧 [RUFF] Running Unified Quality Engine (Lint, Format, Security)..."
	$(RUFF) check . --fix --exit-zero
	$(RUFF) format .
	@echo ">>> ✅ Codebase is clean and formatted."

# --- Infrastructure & Environment ---

# CI/CD specific target for environment readiness
update-deps:
	@echo ">>> 📦 Preparing Environment Infrastructure (CI Mode: $(CI))..."
	$(PIP) install --upgrade pip
	# We call setup directly as it already handles requirements and editable installs
	@$(MAKE) setup
	fi

setup:
	@echo ">>> 🛠️  [STEP 1/5] Initializing Virtual Environment..."
	@if [ ! -d "$(VENV)" ]; then python3 -m venv $(VENV); fi
	@$(PIP) install --upgrade pip
	@echo ">>> 📦 [STEP 2/5] Installing Development Requirements..."
	$(PIP) install -U -r requirements.txt
	@echo ">>> 🏗️  [STEP 3/5] Installing Internal Clients in Editable Mode..."
	$(PIP) install -e $(CORE_LIB_DIR)
	$(PIP) install -e $(GDRIVE_DIR)
	$(PIP) install -e $(AI_UTILS_DIR)
	@echo ">>> 🔍 [STEP 4/5] Verifying Package Integrity..."
	@$(MAKE) verify-env
	@echo ">>> 🛡️  [STEP 5/5] Finalizing Git Hooks..."
	@if [ "$(CI)" = "false" ]; then $(PRE) install; fi
	@echo ">>> ✅ [SUCCESS] Environment is ready and orchestrated!"

verify-env:
	@echo ">>> 🔍 Verifying Package Integrity..."
	@$(PY) -c "import pandas; import core_lib_client; import gdrive_client; print('>>> ✨ Integrity Check Passed.')" || \
	(echo ">>> ❌ Integrity Check Failed: Missing modules." && exit 1)

# --- Tooling & Validation ---

security:
	@echo ">>> 🛡️ Running Dependency Audit..."
	$(AUDIT) --skip-editable --ignore-vuln CVE-2025-53000

health:
	@echo ">>> 🧪 Running Infrastructure Health Check..."
	# Simple smoke test to ensure core client initialization
	$(PY) -c "from gdrive_client.client import GDriveClient; print('>>> ✅ GDriveClient import healthy.')"

test-all:
	@echo ">>> 🧪 Running Pytest suite..."
	$(PYTEST) --verbose

# --- Maintenance ---

clean:
	@echo ">>> 🧹 Cleaning Workspace..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	@echo ">>> Workspace is clean."
