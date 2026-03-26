PYTHON := .venv/bin/python

.PHONY: run debug ports test lint

run:
	$(PYTHON) -m nami run

debug:
	$(PYTHON) -m nami run --debug

ports:
	$(PYTHON) -m nami list-ports

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	$(PYTHON) -m ruff check src/
