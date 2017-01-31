#!/usr/bin/env bash
set -o errexit

cd ..
echo 'Uploading all artifacts to PyPi'
twine upload dist/*
echo 'done'