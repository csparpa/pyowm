PyOWM
=====
A Python wrapper around the OpenWeatherMap API

[![Build Status](https://travis-ci.org/csparpa/pyowm.png?branch=master)](https://travis-ci.org/csparpa/pyowm)
[![Coverage Status](https://coveralls.io/repos/csparpa/pyowm/badge.png?branch=develop)](https://coveralls.io/r/csparpa/pyowm?branch=develop)
[![Latest Version](https://pypip.in/version/pyowm/badge.svg)](https://pypi.python.org/pypi/pyowm/)
[![Downloads](https://pypip.in/download/pyowm/badge.svg?period=week)](https://pypi.python.org/pypi/pyowm/)

What is it?
------------
PyOWM is a client Python wrapper library for the OpenWeatherMap (OWM) web API.

It allows quick and easy consumption of OWM weather data from Python applications via a simple object model and in a human-friendly fashion.

No additional libraries are requested: only the Python standard library modules.

Support
-------
PyOWM currently supports _version 2.5_ of the OWM API (which is the latest one)

PyOWM runs on Python 2.7, 3.2 and 3.3

Usage examples
--------------
```python
import pyowm

owm = pyowm.OWM('your-API-key')
    
# Will it be sunny tomorrow at this time in Milan (Italy) ?
forecast = owm.daily_forecast("Milan,it")
tomorrow = pyowm.timeutils.tomorrow()
forecast.will_be_sunny_at(tomorrow)  # Always True in Italy, right? ;-)

# Search for current weather in London (UK)
observation = owm.weather_at_place('London,uk')
w = observation.get_weather()
print(w)                      # <Weather - reference time=2013-12-18 09:20, 
                              # status=Clouds>

# Weather details
w.get_wind()                  # {'speed': 4.6, 'deg': 330}
w.get_humidity()              # 87
w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

# Search current weather observations in the surroundings of 
# lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
observation_list = owm.weather_around_coords(-22.57, -43.12)
```

Installation
------------
**With [pip](https://pypi.python.org/pypi/pip)**

`pip install pyowm`

**From source with [setuptools](https://pypi.python.org/pypi/setuptools)**

1. Download the source archive either from GitHub ([select a release](https://github.com/csparpa/pyowm/releases)
   or just take the [main branch](https://github.com/csparpa/pyowm/archive/master.zip))
   or from the [Python Package Index](https://pypi.python.org/pypi/pyowm) 
2. Uncompress:

       `unzip pywom-x.y.z`

3. Launch setuptools:

       `cd pywom-x.y.z`
       
       `python setup.py install`

**.exe installer (Windows users)**

The installer is available on the [Python Package Index](https://pypi.python.org/pypi/pyowm) 

License
-------
[MIT](https://github.com/csparpa/pyowm/blob/master/LICENSE) license

What's new
----------
Please read the [changelog](https://github.com/csparpa/pyowm/wiki/Changelog) page of the wiki


Documentation
-------------
Usage examples are available in [the wiki page](https://github.com/csparpa/pyowm/wiki/Usage-examples).

The library API documentation is available on [Read the Docs](https://pyowm.readthedocs.org).

Test
----
Unit testing is as simple as `python setup.py test -s tests.unit`

PyOWM is continuously built with [Travis-CI](https://travis-ci.org/csparpa/pyowm) and code coverage is checked
with [Coveralls.io](https://coveralls.io/r/csparpa/pyowm)

Development
-----------
Contributors (code enhancement, issue/bug reporting) are __welcome!__. See the
[notes on development](https://github.com/csparpa/pyowm/wiki/Notes-on-development) to get started.

If you liked PyOWM, [consider giving me a tip](https://gratipay.com/csparpa)!

References
----------
* [OpenWeatherMap website](http://openweathermap.org/)
* [OpenWeatherMap web API wiki](http://bugs.openweathermap.org/projects/api/wiki)
