#!/usr/bin/env bash

set -o errexit

cd ..
rm -fv dist/*
echo 'Generating source and binary PyPi distributions...'
python2.7 setup.py sdist
python2.7 setup.py bdist_egg
python3.2 setup.py bdist_egg
python3.3 setup.py bdist_egg
python3.4 setup.py bdist_egg
python3.5 setup.py bdist_egg
python3.6 setup.py bdist_egg
echo 'Done'