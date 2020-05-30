#!/usr/bin/env bash
echo "*** Start of local installation test ..."
venv="$(readlink -f $(date +%s)_pyowm_installation_test)"
virtualenv "$venv" && cd "$venv" && source bin/activate
echo "*** Created virtualenv: $venv ..."

# Understand if running on localhost or on Travis CI
if [ -z "$TRAVIS_BUILD_DIR" ]; then
   TRAVIS_BUILD_DIR="$(readlink -f ../..)"
fi
echo "*** PyOWM source package is in: $TRAVIS_BUILD_DIR"

# Test PyOWM installation from local folder
cd "$TRAVIS_BUILD_DIR"
pip install -r requirements.txt
pip install -e .
if [ $? -ne 0 ]; then
    echo "*** Pip installation failed!"
    exit 1
fi
echo "*** Pip installation from local folder was OK ..."
python -c "import pyowm"
if [ $? -ne 0 ]; then
    echo "*** Test import of library failed!"
    deactivate
    rm -rf "$venv"
    exit 2
fi
echo "*** Test import of library was OK"

# Test dependencies installation
python -c "import requests" && python -c "import geojson"
if [ $? -ne 0 ]; then
    echo "*** Test import of dependencies failed!"
    deactivate
    rm -rf "$venv"
    exit 3
fi
echo "*** Test import of dependencies was OK"

# Cleanup
deactivate
rm -rf "$venv"
exit 0