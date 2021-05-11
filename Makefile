PYTHON_VERSION ?= 3
PYTHON := python$(PYTHON_VERSION)

.PHONY: help clean clean-pyc clean-build list test test-all coverage docs release sdist

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "develop - create a virtualenv and set pre-commit hooks"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

develop: clean
	$(PYTHON) -m venv env
	env/bin/pip install -Ue .[develop]
	env/bin/pre-commit install

lint:
	pylama gray test

test:
	pytest

test-all:
	tox

coverage:
	coverage run --source gray setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/gray.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ gray
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

build: clean
	env/bin/python -m pip install -U build
	env/bin/python -m build


upload: build
	env/bin/python -m pip install -U twine
	env/bin/python -m twine upload --repository pypi dist/*
