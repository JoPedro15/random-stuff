# random-stuff/Makefile

.PHONY: setup all test lint fmt clean

setup:
	@echo ">>> Initializing Monorepo Environment with Python 3.13..."
	@if [ ! -d ".venv" ]; then python3 -m venv .venv; fi
	# Install each client in editable mode so they are available globally in the venv
	$(MAKE) -C clients/spotify setup
	$(MAKE) -C clients/gdrive setup

all: lint test

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