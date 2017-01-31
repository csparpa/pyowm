#!/usr/bin/env bash

set -o errexit

VERSION="$1"

echo "Publishing image: csparpa/pyowm:$VERSION to DockerHub..."
docker push csparpa/pyowm:${VERSION}
docker push csparpa/pyowm:latest
echo "done"