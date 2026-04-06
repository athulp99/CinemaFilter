PYTHON := python3
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_DIR)/bin/pip

.PHONY: venv install run

venv:
	$(PYTHON) -m venv $(VENV_DIR)

install:
	$(VENV_PIP) install -r requirements.txt

run:
	$(VENV_PYTHON) run.py
