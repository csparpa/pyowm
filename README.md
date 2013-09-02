PyOWM
=====
PyOWM - A Python wrapper around the OpenWeatherMap API

Introduction
------------
PyOWM is a client Python wrapper library for the OpenWeatherMap (OWM) web API.

It allows quick and easy consumption of OWM weather and forecast data from Python applications.

For the moment, PyOWM only supports version 2.5 of the OWM API.


Code snippet
------------
    from pyowm import OWM, Location
    
    location = Location('London')
    APIkey = 'your-API-key'
    
    owm = OWM(location, APIkey)
    
    # Query for current weather in London
    w = owm.currentWeather()
    w.getDetailedStatus()
    'Clear'
    w.getTemperature(unit='celsius')
    23

Install
-------
TBD

Support
-------
Usage examples are available [here](https://github.com/csparpa/pyowm/blob/master/docs/usage-examples.md).
Technical documentation is available here.

License
-------
[MIT](https://github.com/csparpa/pyowm/blob/master/LICENSE) license

References
----------
[OpenWeatherMap website](http://openweathermap.org/)
