#!/usr/bin/env bash

echo "Running pre-commit hook"
./scripts/run-django-tests.sh

# $? son komut cikis degerini saklar
if [ $? -ne 0 ]; then
 echo "Unit Tests or Flake 8 must pass before commit!"
 exit 1
fi
