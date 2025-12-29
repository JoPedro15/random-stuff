# Variables
VENV        := .venv
PY          := $(VENV)/bin/python
PIP         := $(PY) -m pip
REQ_DEV     := requirements.txt

# Client directories
SPOTIFY_DIR := clients/spotify
GDRIVE_DIR  := clients/gdrive

.PHONY: setup update-deps security health test-all test-spotify test-gdrive clean lint-all fmt-all

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
	@$(MAKE) security
	@echo ">>> ✅ System ready and secured!"

# Installs or upgrades all development requirements from the root file
update-deps:
	@echo ">>> 📦 Updating development requirements..."
	$(PIP) install -U -r $(REQ_DEV)

# Performs static code analysis and checks for vulnerable dependencies
security:
	@echo ">>> 🛡️ Running Security Analysis (Bandit)..."
	# Bandit: scans for common security issues (filtered by Medium/High severity)
	$(PY) -m bandit -r clients/ -ll --exclude .venv,*/.venv/*
	@echo ">>> Running Dependency Audit (pip-audit)..."
	# pip-audit: scans the entire environment for known vulnerabilities
	$(PY) -m pip_audit

# --- Health & Monitoring ---

# Run all health checks from root
health:
	@echo ">>> Running Global Health Checks..."
	@export PYTHONPATH=.:$(PYTHONPATH) && \
	 export GDRIVE_CREDENTIALS_PATH="clients/gdrive/data/credentials.json" && \
	 export GDRIVE_TOKEN_PATH="clients/gdrive/data/token.json" && \
	 $(PY) scripts/global_health_check.py

# --- Testing ---

# Runs all test suites across the entire hub
test-all:
	@echo ">>> 🧪 Running all automation tests..."
	@$(MAKE) test-spotify
	@$(MAKE) test-gdrive
	@echo ">>> ✨ All tests completed!"

# Triggers Spotify-specific integration tests via its local Makefile
test-spotify:
	$(MAKE) -C $(SPOTIFY_DIR) test

# Triggers Google Drive-specific integration tests via its local Makefile
test-gdrive:
	$(MAKE) -C $(GDRIVE_DIR) test

# --- Linting & Formatting ---

# Executes static code analysis (linting) for all clients
lint-all:
	@echo ">>> 🔍 Linting all clients..."
	$(MAKE) -C $(SPOTIFY_DIR) lint
	$(MAKE) -C $(GDRIVE_DIR) lint

# Standardizes code style across all clients
fmt-all:
	@echo ">>> 🖋️ Formatting all clients..."
	$(MAKE) -C $(SPOTIFY_DIR) fmt
	$(MAKE) -C $(GDRIVE_DIR) fmt

# --- Cleanup ---

# Recursively purges Python caches, build artifacts, and test leftovers
clean:
	@echo ">>> 🧹 Cleaning up project artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	$(MAKE) -C $(SPOTIFY_DIR) clean
	$(MAKE) -C $(GDRIVE_DIR) clean
	@echo ">>> Workspace is clean."