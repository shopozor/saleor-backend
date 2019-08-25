#! /bin/bash

rm -f Pipfile Pipfile.lock

pipenv install -r saleor/requirements.txt
pipenv install -r requirements.txt

pipenv install --dev -r saleor/requirements_dev.txt
pipenv install --dev -r requirements-dev.txt