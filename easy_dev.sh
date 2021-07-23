#!/bin/bash

set -o errexit

test -d plugins

if [ $? -eq 1 ]
then
  echo "change directory to git clone directory"
  echo "unable to find plugins/ directory in $PWD"
  exit 1
fi

echo "Running Pycodestyle"
pycodestyle --config=.pycodestyle plugins/module_utils/ plugins/modules --show-source

echo "Running Yamllint"
yamllint tests/integration

echo "Running Static Analysis Tools ( bandit )"
bandit -r plugins/

echo "Running Add Docs / Generate Readmes"
collection_prep_add_docs -p . -b master

echo "Show git status"
git status