#!/usr/bin/env bash

set -o errexit

VERSION="$1"

cd ..
echo "Building Docker image: csparpa/pyowm:$VERSION..."
docker build -t csparpa/pyowm:${VERSION} .
docker tag csparpa/pyowm:${VERSION} csparpa/pyowm:latest
echo "done"
