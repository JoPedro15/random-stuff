# Ensure local sources are importable: spotify/src and repo root (so 'common' works)
export PYTHONPATH := $(CURDIR)/src:$(CURDIR)/..:$(PYTHONPATH)

# Virtualenv & python inside the repo root
VENV ?= $(abspath $(CURDIR)/../.venv)
PY   ?= $(VENV)/bin/python

.PHONY: help setup ci test lint fmt run coverage clean

help:
	@echo "Targets:"
	@echo "  make setup     - install deps into the repo venv"
	@echo "  make fmt       - format (isort + black)"
	@echo "  make lint      - lint with ruff"
	@echo "  make test      - run pytest (verbose)"
	@echo "  make coverage  - run tests with coverage"
	@echo "  make run       - run main.py"
	@echo "  make clean     - remove caches"

setup:
	$(PY) -m pip install -U pip
	$(PY) -m pip install -e .
	@if [ -f requirements.txt ]; then $(PY) -m pip install -r requirements.txt; fi

ci: lint test

lint:
	$(PY) -m ruff check .

lint-fix:
	$(PY) -m ruff check --fix .

fmt:
	$(PY) -m isort .
	$(PY) -m black .

test:
	$(PY) -m pytest -v

coverage:
	$(PY) -m pip install -q coverage pytest-cov
	$(PY) -m pytest -v --cov=src --cov-report=term-missing

run:
	$(PY) src/main.py

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache __pycache__ */__pycache__
