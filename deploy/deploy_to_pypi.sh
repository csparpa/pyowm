#!/usr/bin/env bash

# Rules:
#  - deploy to Test PyPI upon every push on the develop branch
#  - only deploy to the real PyPI upon merged pull requests on the master branch

if [ $TRAVIS_BRANCH = "develop" ] && [[ $TRAVIS_EVENT_TYPE == "push" ]]; then
    echo "*** Will build the DEVELOP branch and publish to Test PyPI at $TEST_PYPI_URL"

    # Get env variables
    export INDEX_URL="$TEST_PYPI_URL"
    export PYPI_USERNAME="$TEST_PYPI_USERNAME"
    export PYPI_PASSWORD="$TEST_PYPI_PASSWORD"

    # Get commit SHA and patch development release number
    TS="$(date "+%Y%m%d%H0000")"
    echo "*** Development release number is: post$TS"
    sed -i -e "s/constants.PYOWM_VERSION/constants.PYOWM_VERSION+\".post${TS}\"/g" setup.py

elif [ $TRAVIS_BRANCH = "master" ] && [[ $TRAVIS_EVENT_TYPE == "pull_request" ]]; then
    echo "*** Will build the MASTER branch and publish to PyPI at $PYPI_URL"

    # Get env variables
    export INDEX_URL="$PYPI_URL"
    export PYPI_USERNAME="$PYPI_USERNAME"
    export PYPI_PASSWORD="$PYPI_PASSWORD"

else
    echo "*** Wrong deployment conditions: branch=$TRAVIS_BRANCH event=$TRAVIS_EVENT_TYPE"
    exit 5
fi

echo '*** Generating source distribution...'
python setup.py sdist

echo '*** Generating egg distribution...'
python setup.py bdist_egg

echo '*** Generating wheel distribution...'
python setup.py bdist_wheel

echo '*** Uploading all artifacts to PyPi...'
twine upload --repository-url "$INDEX_URL" \
             --username "$PYPI_USERNAME" \
             --password "$PYPI_PASSWORD" \
             --skip-existing \
             dist/*
if [ "$?" -ne 0 ]; then
    exit 7
fi

echo '*** Done'