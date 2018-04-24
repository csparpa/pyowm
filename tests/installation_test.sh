#!/usr/bin/env bash
echo " --- Start of installation test ..."
venv="$(readlink -f $(date +%s)_pyowm_installation_test)"
virtualenv "$venv" && cd "$venv" && source bin/activate
echo " --- Created virtualenv: $venv ..."

# Test PyOWM installation
pip install pyowm
if [ $? -ne 0 ]; then
    echo " --- Pip installation failed!"
    exit 1
fi
echo " --- Pip installation was OK ..."
python -c "import pyowm"
if [ $? -ne 0 ]; then
    echo " --- Test import of library failed!"
    deactivate
    rm -rf "$venv"
    exit 2
fi
echo " --- Test import of library was OK"

# Test dependencies installation
python -c "import requests" && python - c "import geojson"
if [ $? -ne 0 ]; then
    echo " --- Test import of dependencies failed!"
    deactivate
    rm -rf "$venv"
    exit 3
fi
echo " --- Test import of dependencies was OK"

# Cleanup
deactivate
rm -rf "$venv"
exit 0