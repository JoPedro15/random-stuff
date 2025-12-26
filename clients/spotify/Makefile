# clients/spotify/Makefile

ROOT_DIR := $(shell git rev-parse --show-toplevel)

VENV := $(ROOT_DIR)/.venv
PY   := $(VENV)/bin/python

export PYTHONPATH := $(ROOT_DIR):$(PYTHONPATH)

.PHONY: help setup ci test lint fmt run clean

help:
	@echo "Spotify Client Commands:"
	@echo "  make setup     - Install dependencies into root venv"
	@echo "  make fmt       - Format code (black + isort)"
	@echo "  make lint      - Check style (ruff)"
	@echo "  make test      - Run pytest"
	@echo "  make run       - Run main.py"

setup:
	$(PY) -m pip install -U pip
	$(PY) -m pip install -e .
	$(PY) -m pip install ruff black isort pytest
	@if [ -f requirements.txt ]; then $(PY) -m pip install -r requirements.txt; fi

ci: lint test

lint:
	$(PY) -m ruff check .

fmt:
	$(PY) -m isort .
	$(PY) -m black .

test:
	$(PY) -m pytest -v

run:
	$(PY) spotify_client/main.py

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache __pycache__ */__pycache__ *.egg-info