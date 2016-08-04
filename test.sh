#!/usr/bin/env bash

# Exit on any error
set -e

echo "Creating virtualenv..."
VENV_NAME=".venv"
if ! [ -e "${VENV_NAME}/bin/activate" ]; then
  virtualenv ${VENV_NAME}
fi
source "${VENV_NAME}/bin/activate"

echo "Installing requirements..."
pip install -q -r requirements.txt -r requirements-tests.txt

echo "Cleaning .pyc files..."
find . -iname "*.pyc" -delete

echo "Running tests..."
nosetests --with-coverage --cover-erase --cover-package=aws_assume_role

echo "Running flake8..."
flake8 aws_assume_role/ tests/
echo "OK"

echo "Deactivating virtualenv..."
deactivate
