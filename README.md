PyOWM
=====
A Python wrapper around the OpenWeatherMap API

What is it?
------------
PyOWM is a client Python wrapper library for the OpenWeatherMap (OWM) web API.

It allows quick and easy consumption of OWM weather data from Python applications via a simple object model and in a human-friendly fashion.

No additional libraries are requested: only the Python 2.6/2.7 standard library modules.

For the moment only _version 2.5_ of the OWM API is supported.

License
-------
[MIT](https://github.com/csparpa/pyowm/blob/master/LICENSE) license

Install
-------
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

Take off
--------
```python
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
```

Documentation
-------------
Usage examples are available in [the wiki page](https://github.com/csparpa/pyowm/wiki/Usage-examples).

The library API documentation is available on [Read the Docs](https://pyowm.readthedocs.org).

Test
----
As simple as:

`python setup.py test -s tests.unit`

Development
-----------
PyOWM is continuously built with [Travis-CI](https://travis-ci.org/csparpa/pyowm).

_Contributors (code enhancement, issue/bug reporting) are welcome!_


References
----------
* [OpenWeatherMap website](http://openweathermap.org/)
* [OpenWeatherMap web API wiki](http://bugs.openweathermap.org/projects/api/wiki)
