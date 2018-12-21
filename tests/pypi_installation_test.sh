#!/usr/bin/env bash
echo "*** Start of Pypi installation test ..."
venv="$(readlink -f $(date +%s)_pyowm_installation_test)"
virtualenv "$venv" && cd "$venv" && source bin/activate
echo "*** Created virtualenv: $venv ..."

# Test
pip install pyowm
if [ $? -ne 0 ]; then
    echo "*** Pip installation failed!"
    exit 1
fi
echo "*** Pip installation was OK ..."
python -c "import pyowm"
if [ $? -ne 0 ]; then
    echo "*** Test import of library failed!"
    exit 2
fi
echo "*** Test import of library was OK"

# Cleanup
deactivate
rm -rf "$venv"
exit 0