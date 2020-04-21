#!/usr/bin/env bash

echo "Running pre-commit hook"
./scripts/run-django-tests.sh

# $? son komut sonlanma degerini saklar
if [ $? -ne 0 ]; then
 echo "Unit Tests or Flake8 must pass before commit!"
 exit 1
fi
