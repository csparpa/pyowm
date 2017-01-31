#!/usr/bin/env bash

echo 'Generating Sphinx HTML documentations...'
cd ../sphinx
make clean
make html
echo 'Done'
