# clients/gdrive/Makefile

ROOT_DIR := $(shell git rev-parse --show-toplevel)
VENV     := $(ROOT_DIR)/.venv
PY       := $(VENV)/bin/python

# Export PYTHONPATH so the interpreter finds the root packages
export PYTHONPATH := $(ROOT_DIR):$(PYTHONPATH)

.PHONY: setup test lint fmt clean

setup:
	@echo ">>> Installing GDrive Client and its dependencies..."
	$(PY) -m pip install -U pip
	# This installs everything listed in [project.dependencies] of pyproject.toml
	$(PY) -m pip install -e .
	# Install development tools
	$(PY) -m pip install pytest ruff black isort

test:
	@echo ">>> Running GDrive tests..."
	$(PY) -m pytest tests/gdrive_test.py -vv

lint:
	$(PY) -m ruff check .

fmt:
	$(PY) -m isort .
	$(PY) -m black .

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache __pycache__ *.egg-info