Build the image
===============
```
cd <pyowm-root-dir>
build -t pyowm:latest .
```


Start container
===============
```
docker run -d --name pyowm pyowm
```

Run tests on Tox
================
```
docker exec -ti pyowm tox
```