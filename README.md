PyOWM
=====
PyOWM - A Python wrapper around the OpenWeatherMap API

Introduction
------------
PyOWM is a client Python wrapper library for the OpenWeatherMap (OWM) web API.

It allows quick and easy consumption of OWM weather data (either observations 
and forecast) from Python applications via a simple object model.

No additional libraries are requested: just the Python 2.7+ standard modules.

For the moment, PyOWM only supports _version 2.5_ of the OWM API.

Take off
--------
    from pyowm import OWM

    owm = OWM('your-API-key')
    
    #Search for current weather in London, UK
    obs = owm.observation_for_name('London,uk')
    w = obs.get_weather()
    w.get_detailed_status()
    'Light rain'
    w.get_wind()
    {'speed': 4.6, 'deg': 330}

Install
-------
You will need _setuptools_ installed (read [here](https://pypi.python.org/pypi/setuptools) 
how to do it). Just run:

    python setup.py install

Test
----
Unit tests can be launched by moving into the library installation folder and 
executing:

    python -m unittest discover
    
Integration tests can be launched by movin into the library installation folder
and executing:

    cd functional-tests
    python integration-tests.py  

Support
-------
Usage examples are available [here](https://github.com/csparpa/pyowm/blob/master/docs/usage-examples.md).

Library object API and technical documentation are available _here_.

License
-------
[MIT](https://github.com/csparpa/pyowm/blob/master/LICENSE) license

References
----------
[OpenWeatherMap website](http://openweathermap.org/)
