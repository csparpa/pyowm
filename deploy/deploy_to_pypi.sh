#!/usr/bin/env bash

# Rules:
#  - deploy to Test PyPI upon every push

if [ $TRAVIS_BRANCH = "develop" ] && [[ $TRAVIS_EVENT_TYPE == "push" ]]; then
    export INDEX_URL="$TEST_PYPI_URL"
    export PYPI_USERNAME="$TEST_PYPI_USERNAME"
    export PYPI_PASSWORD="$TEST_PYPI_PASSWORD"
else
    echo 'Wrong deployment conditions: branch=$TRAVIS_BRANCH event=$TRAVIS_EVENT_TYPE'
    exit 5
fi

echo 'Generating source distribution...'
python setup.py sdist

echo 'Generating egg distribution...'
python setup.py bdist_egg

echo 'Generating wheel distribution...'
python setup.py bdist_wheel

echo 'Uploading all artifacts to PyPi...'
twine upload --repository-url "$INDEX_URL" \
             --username "$PYPI_USERNAME" \
             --password "$PYPI_PASSWORD" \
             --skip-existing \
             dist/*
echo 'Done'