#!/usr/bin/env bash

set -o errexit

if [ -z "$OWM_API_KEY" ]; then
    echo "*** OWM_API_KEY env variable is not set: aborting"
    exit 1
fi

export OWM_API_KEY
cd integration
tox

echo "*** End of integration tests"
