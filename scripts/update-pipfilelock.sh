#!/usr/bin/env bash

echo '*** Updating Pipfile.lock ...'
cd ..
pipenv lock
echo '*** Done'
