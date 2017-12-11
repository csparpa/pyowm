#!/usr/bin/env bash

baseimagename="csparpa/pyowm"

cd ..
for imagetype in $(find -maxdepth 1 -name 'Dockerfile.*' -printf '%P\n' | cut -d'.' -f2); do
	echo "Building from Dockerfile.$imagetype to image $baseimagename.$imagetype..."
	docker build . -f Dockerfile.$imagetype -t $baseimagename.$imagetype
done

