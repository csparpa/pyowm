#!/usr/bin/env bash

set -o errexit

cd ..
rm -fv build/*
rm -fv dist/*
echo 'Generating source distribution...'
python2.7 setup.py sdist

echo 'Generating .egg distributions...'
python3.4 setup.py bdist_egg
python3.5 setup.py bdist_egg
python3.6 setup.py bdist_egg
python3.7 setup.py bdist_egg

echo 'Generating Wheel distributions...'
python2 setup.py sdist bdist_wheel
python3 setup.py sdist bdist_wheel

echo 'Generating Windows self-extracting .exe ...'
python2 setup.py bdist_wininst
python3 setup.py bdist_wininst


echo 'Done'