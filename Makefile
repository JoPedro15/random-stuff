# random-stuff/Makefile
include tooling/python.mk

.PHONY: setup all test lint fmt
setup:
	@echo "Tip: each project has its own setup. Example:"
	@echo "  make -C projects/spotify setup"

all: ## Run lint+tests across all python projects
	$(MAKE) -C projects/spotify ci

test:
	$(MAKE) -C projects/spotify test

lint:
	$(MAKE) -C projects/spotify lint

fmt:
	$(MAKE) -C projects/spotify fmt