Testing
=======

The PyOWM library is developed using Test-Driven Development techniques and
testing is therefore a focus point in its development and maintenance.

Unit tests
----------
Unit tests aim to test the SW API of each class.

We make use of _monkey patching_ (which is more convenient than mocking because
Python is a dynamically typed) whenever there is the need to test the behavior
of a SW component which is bound to an external SW entity/system (ie: the parts
of the PyOWM library that call the real PyOWM web API via HTTP).

Unit tests are run before each and every commit. 
Because of the simplicity of this library, I didn't set any continuous 
integration system up yet, but in the future this should be accomplished.
The default unit testing enviroment is Python's _unittest_: simple and clean
enough, so no additional dependencies are needed.

Unit tests can be launched by moving into the library installation folder and 
executing:

    python -m unittest discover

or by executing the 

    tests\run-all-tests.[bat|bash]
    
scripts

Integration tests
-----------------

Also integration tests will be provided: their aim is to test PyOWM behaviour
against the real OWM web API.
    
Integration tests can be launched by moving into the library installation folder
and executing:

    cd functional-tests
    python integration-tests.py  