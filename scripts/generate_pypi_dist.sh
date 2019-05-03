#!/usr/bin/env bash

set -o errexit

cd ..
rm -fv build/*
rm -fv dist/*
echo 'Generating source distribution...'
python3.7 setup.py sdist

echo 'Generating .egg distributions...'
python3.7 setup.py bdist_egg
python3.8 setup.py bdist_egg

echo 'Generating Wheel distributions...'
python3 setup.py sdist bdist_wheel

echo 'Generating Windows self-extracting .exe ...'
python3 setup.py bdist_wininst


echo 'Done'