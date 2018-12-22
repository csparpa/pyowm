#!/usr/bin/env bash

# Rules:
#  - deploy to Test PyPI upon every push on the develop branch
#  - only deploy to the real PyPI upon merged pull requests on the master branch
#  - gracefully fail if integrated branch is neither develop nor master
#  - under any circumstance, only deply if the corresponding release does not yet exist (otherwise, gracefully fail)

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

    REL_VERSION="$(cd .. && python3.5 -c "from pyowm.constants import PYOWM_VERSION; from pyowm.utils.stringutils import version_tuple_to_str; print(version_tuple_to_str(PYOWM_VERSION))")"

    echo "*** Checking if target release already exists on the repository..."
    wget "https://pypi.org/pypi/pyowm/${REL_VERSION}/json"
    OUTCOME="$(echo $?)"
    if [ $OUTCOME = "0" ]; then
        echo "*** OK: release is brand new"
    else
        echo "*** WARNING: release is already on the repository!"
        echo "*** SKIPPING deployment"
        exit 0
    fi

else
    echo "*** Will not build branch $TRAVIS_BRANCH as this is neither DEVELOP nor MASTER"
    echo "*** SKIPPING deployment"
    exit 0
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