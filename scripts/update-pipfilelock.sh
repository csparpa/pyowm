#!/usr/bin/env bash

THIS_FOLDER="$(pwd)"
PYOWM_FOLDER="$(dirname $(pwd))"

echo '*** Creating temporary virtualenv...'
virtualenv pipfilelocker
source pipfilelocker/bin/activate
pip install pipenv

echo '*** Updating Pipfile.lock...'
cd "$PYOWM_FOLDER"
pipenv lock

echo '*** Removing temporary virtualenv...'
deactivate
cd "$THIS_FOLDER"
rm -rf pipfilelocker

echo '*** Done'