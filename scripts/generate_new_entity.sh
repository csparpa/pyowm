#!/usr/bin/env bash

set -o errexit

echo "Generating boilerplate for new entity..."

python3 fill_entity_template.py "$@"

echo 'Done'