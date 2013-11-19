PyOWM
=====
PyOWM - A Python wrapper around the OpenWeatherMap API

Introduction
------------
PyOWM is a client Python wrapper library for the OpenWeatherMap (OWM) web API.

It allows quick and easy consumption of OWM weather data (either observations 
and forecast) from Python applications via a simple object model.

No additional libraries are requested: only the Python 2.6/2.7 standard library modules.

For the moment only _version 2.5_ of the OWM API is supported.

Install
-------
You will need _setuptools_ installed - read [here](https://pypi.python.org/pypi/setuptools) 
how to do it. Just run (superuser privileges might be needed):

    python setup.py install

Install
-------
As simple as:

    python setup.py test

Take off
--------
    from pyowm import OWM, timeutils

    owm = OWM('your-API-key')
    
    # Will it be sunny tomorrow at this time in Milan (Italy) ?
    f = owm.daily_forecast("Milan,it")
    tomorrow = timeutils.tomorrow()
    f.will_be_sunny_at(tomorrow)      # True
    
    # Search for current weather in London (UK)
    obs = owm.weather_at('London,uk')
    w = obs.get_weather()
    w.get_detailed_status()           # 'Light rain'
    w.get_wind()                      # {'speed': 4.6, 'deg': 330}

Support
-------
The library API documentation is available on [Read the Docs](https://pyowm.readthedocs.org).

Usage examples are available [here](https://github.com/csparpa/pyowm/wiki/Usage-examples).

Continuous integration builds are available on [Travis](https://travis-ci.org/csparpa/pyowm).

Technical and development documents are available in the [docs section](https://github.com/csparpa/pyowm/tree/master/docs/internals).

License
-------
[MIT](https://github.com/csparpa/pyowm/blob/master/LICENSE) license

References
----------
[OpenWeatherMap website](http://openweathermap.org/)
