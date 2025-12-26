VENV        := .venv
PY          := $(VENV)/bin/python
PIP         := $(PY) -m pip
REQ_DEV     := requirements.txt

.PHONY: setup update-deps security test-all test-spotify test-gdrive lint fmt clean


setup:
	@echo ">>> Creating Virtual Environment..."
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	@$(MAKE) update-deps
	@echo ">>> System ready!"

update-deps:
	@echo ">>> Installing/Updating all development requirements..."
	# -U upgrades all specified packages to the newest available version
	$(PIP) install -U -r $(REQ_DEV)

security:
	@echo ">>> Running Security Analysis (Bandit)..."
	$(PY) -m bandit -r clients/ -ll
	@echo ">>> Running Dependency Audit (pip-audit)..."
	$(PY) -m pip_audit clients/spotify/
	$(PY) -m pip_audit clients/gdrive/

test-all:
	@echo ">>> Running all automation tests..."
	@$(MAKE) test-spotify
	@$(MAKE) test-gdrive
	@echo ">>> All tests completed!"

test-spotify:
	$(MAKE) -C clients/spotify test

test-gdrive:
	$(MAKE) -C clients/gdrive test

lint:
	$(MAKE) -C clients/spotify lint

fmt:
	$(MAKE) -C clients/spotify fmt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	$(MAKE) -C clients/spotify clean