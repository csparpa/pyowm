Playing with Docker image locally
=================================

Build the image
---------------
```
cd <pyowm-root-dir>
docker build -t pyowm:latest .
```


Start container
---------------
```
docker run -d --name pyowm pyowm
```

Run tests on Tox
---------------
```
docker exec -ti pyowm tox
```


Releasing on DockerHub
======================

Eg: for tagged version 2.3.1

```
VERSION="2.3.1"

# Build and tag
docker build -t csparpa/pyowm:${VERSION} .
docker tag csparpa/pyowm:${VERSION} csparpa/pyowm:latest

# Push to DockerHub
docker push csparpa/pyowm:${VERSION}
docker push csparpa/pyowm:latest
```