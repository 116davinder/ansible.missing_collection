#!/bin/bash

test -d plugins

if [ $? -eq 1 ]
then
  echo "change directory to git clone directory"
  echo "unable to find plugins/ directory in $PWD"
  exit 1
fi

echo "Running Pycodestyle"
pycodestyle --config=.pycodestyle plugins/module_utils/ plugins/modules

echo "Running Yamllint"
yamllint tests/

echo "Running Static Analysis Tools ( bandit )"
bandit -r -v plugins/

echo "Running Add Docs / Generate Readmes"
collection_prep_add_docs -p . -b master

echo "Show git Diff"
git status && git status