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
	flake8 --exit-zero ./$(PACKAGE_NAME)
	yamllint . || exit 0

dist:
	$(PYTHON_INTERPRETER) setup.py bdist_egg
	cp ./$(PACKAGE_NAME)/pyspark_entrypoint.py ./dist/pyspark_entrypoint.py
	cp -r ./emr ./dist/emr

s3dist: dist
	@bash -c "aws s3 sync --delete ./dist s3://{{cookiecutter.s3_bucket}}/dist"
