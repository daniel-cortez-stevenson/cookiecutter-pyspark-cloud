# Copyright 2020 Daniel Cortez Stevenson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
.PHONY: update-install install install-dev test dist s3dist clean clean-all clean-build clean-test lint lint-all pylint yamllint

# GLOBALS
PROJECT_NAME = {{ cookiecutter.repo_name }}
PACKAGE_NAME = {{ cookiecutter.package_name }}
PYTHON_INTERPRETER = python

# COMMANDS
update-install:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel

install: update-install
	$(PYTHON_INTERPRETER) -m pip install -U .[client]

install-dev: clean-build update-install
	$(PYTHON_INTERPRETER) -m pip install -U -e .[client,dev,spark,spark-node]

test: clean-test
	$(PYTHON_INTERPRETER) setup.py pytest

lint: lint-all
lint-all: pylint yamllint
pylint:
	flake8 ./$(PACKAGE_NAME)
yamllint:
	yamllint .

clean: clean-all
clean-all: clean-test clean-build
clean-test:
	find . -name '.coverage' -exec rm -f {} +
	find . -name 'coverage.xml' -exec rm -f {} +
	find . -name '.pytest_cache' -exec rm -fr {} +
clean-build:
	find . -name 'build' -exec rm -fr {} +
	find . -name '_build' -exec rm -fr {} +
	find . -name 'dist' -exec rm -fr {} +
	find . -name 'libs' -exec rm -fr {} +
	find . -name '.eggs' -exec rm -fr {} +
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

dist: clean-build
	$(PYTHON_INTERPRETER) setup.py bdist_egg
	cp ./$(PACKAGE_NAME)/pyspark_entrypoint.py ./dist/pyspark_entrypoint.py
	cp -r ./emr ./dist/emr

s3dist: dist
	@bash -c "aws s3 sync --delete ./dist s3://{{ cookiecutter.s3_bucket }}/dist"
