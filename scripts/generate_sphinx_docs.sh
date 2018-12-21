#!/usr/bin/env bash

echo '*** Generating Sphinx HTML documentations...'
cd ../sphinx
make clean
make html

if [ "$?" -ne 0 ]; then
    echo "*** Errors occurred"
    exit 1
fi

echo '*** Done'
