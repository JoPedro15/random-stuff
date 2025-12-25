# random-stuff/Makefile

-include tooling/python.mk

.PHONY: setup all test lint fmt

setup:
	@echo ">>> Setting up development environment..."
	@echo "Tip: Install individual clients/projects if needed."
	@echo "Example: make -C clients/spotify setup"
	@if [ ! -d ".venv" ]; then python3 -m venv .venv; fi

all: ## Run lint+tests across all python projects
	$(MAKE) -C clients/spotify ci

test:
	$(MAKE) -C clients/spotify test

lint:
	$(MAKE) -C clients/spotify lint

fmt:
	$(MAKE) -C clients/spotify fmt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	$(MAKE) -C clients/spotify clean