PyOWM
=====
PyOWM - A Python wrapper around the OpenWeatherMap API

Introduction
------------
PyOWM is a client Python wrapper library for the OpenWeatherMap (OWM) web API.

It allows quick and easy consumption of OWM weather data (either observations 
and forecast) from Python applications via a simple object model.

For the moment, PyOWM only supports _version 2.5_ of the OWM API.


Code snippet
------------
    from pyowm import OWM

    owm = OWM('your-API-key')
    
    #Search for current weather in London, UK
    obs = owm.observation('London,uk')
    w = obs.getWeather()
    w.getDetailedStatus()
    'Light rain'
    w.getWind()['speed']
    3.08

Install
-------
TBD

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
