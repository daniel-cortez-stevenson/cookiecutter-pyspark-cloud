.PHONY: update-install install install-dev test lint dist s3dist

# GLOBALS
PROJECT_NAME = {{cookiecutter.repo_name}}
PACKAGE_NAME = {{cookiecutter.package_name}}
PYTHON_INTERPRETER = python

# COMMANDS
update-install:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel

install: update-install
	$(PYTHON_INTERPRETER) -m pip install -U .[client]

install-dev: update-install
	$(PYTHON_INTERPRETER) -m pip install -U -e .[client,dev,spark,spark-node]

test: clean-test
	$(PYTHON_INTERPRETER) setup.py pytest

lint:
	flake8 --exit-zero ./$(PYPACKAGE)
	yamllint . || exit 0

dist: clean-build
	$(PYTHON_INTERPRETER) setup.py bdist_egg
	cp ./$(PYPACKAGE)/pyspark_entrypoint.py ./dist/pyspark_entrypoint.py

s3dist: dist
	@bash -c "aws s3 sync --delete ./dist s3://$(bucket)/dist"
