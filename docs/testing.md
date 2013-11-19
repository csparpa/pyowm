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

Unit tests can be launched by moving into the library installation folder and 
executing:

    python -m unittest discover

or by executing the 

    ./run-all-tests.[bat|bash]
    
scripts in the library root folder.


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

    cd functional-tests
    python integration-tests.py  