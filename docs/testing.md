Testing
=======

The PyOWM library focuses on unit and integration testing.

Unit tests
----------
Unit tests aim to test the SW API of each class.

We make use of _monkey patching_ (which is more convenient than mocking because
Python is a dynamically typed) whenever there is the need to test the behavior
of a SW component which is bound to an external SW entity/system (ie: the parts
of the PyOWM library that call the real PyOWM web API via HTTP).

The default unit testing enviroment is Python's _unittest_: simple and clean
enough, so no additional dependencies are needed.

Unit tests can be easily run using _tox_. Running:

    tox

triggers unit tests execution on all Python platfoms that are supported by
PyOQM.

Unit tests can also be launched by moving into the library installation folder
and executing:

    python -m unittest discover


Functional tests
----------------
Insert your API key into this module:

    tests.functional.api_key

and then you can run the integration tests from the library installation 
folder with:

    cd tests/functional
    pythonXY test_integration_webapi25.py

for Python interpreter version XY.
Please note that depending on your subscription type some of the tests
may fail, eg: if you have a free subscription tier, the test cases that
invoke the OWM API to get historical weather data will fail as these
data can only be retrieved using a paid account.


Continuous integration
----------------------
A Travis CI account has been established in order to continously run tests and
build the SW.


Integration tests
-----------------
Also integration tests will be provided: their aim is to test PyOWM behaviour
against the real OWM web API.
    
Integration tests can be launched by moving into the library installation folder
and executing:

    cd tests/functional
    pythonXY integration-tests.py

of course replace XY with your target Python version.