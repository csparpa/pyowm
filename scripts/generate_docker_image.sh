#!/usr/bin/env bash

set -o errexit

VERSION="$1"
BASEIMAGENAME="csparpa/pyowm"

cd ..
for imagetype in $(find -maxdepth 2 -name 'Dockerfile.*' -printf '%P\n' | cut -d'.' -f2); do
	echo "Building from Dockerfile.$imagetype to image $BASEIMAGENAME:${VERSION}.$imagetype ..."
	docker build -f dockerfiles/Dockerfile.$imagetype -t $BASEIMAGENAME:${VERSION}.$imagetype .
done
echo "done"
