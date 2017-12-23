#!/usr/bin/env bash

set -o errexit

BASEIMAGENAME="csparpa/pyowm"


docker images csparpa/pyowm | grep '^csparpa/pyowm' | while IFS= read -r line ; do
    version=$(echo $line | awk '{print $2}')
    echo "Publishing image: csparpa/pyowm:$version to DockerHub..."
    docker push csparpa/pyowm:${version}
    echo "done"
    echo ""
done

echo "All images successfully pushed"