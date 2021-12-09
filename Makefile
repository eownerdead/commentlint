POETRY = poetry

PYMODULE = commentlint

FLAKE8FLAGS = --show-source

MYPYFLAGS = --show-column-numbers --pretty

lint: flake8 mypy

flake8:
	$(POETRY) run flake8 $(FLAKE8FLAGS)

mypy:
	$(POETRY) run mypy $(MYPYFLAGS) $(PYMODULE)

fmt: yapf isort

yapf:
	$(POETRY) run yapf -ir $(PYMODULE)

isort:
	$(POETRY) run isort $(PYMODULE)
