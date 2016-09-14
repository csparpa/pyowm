#  PyOWM
A Python wrapper around the OpenWeatherMap API

[![PyPI version](https://badge.fury.io/py/pyowm.svg)](https://badge.fury.io/py/pyowm)
[![Build Status](https://travis-ci.org/csparpa/pyowm.png?branch=master)](https://travis-ci.org/csparpa/pyowm)
[![Coverage Status](https://coveralls.io/repos/csparpa/pyowm/badge.png?branch=develop)](https://coveralls.io/r/csparpa/pyowm?branch=develop)
[![Downloads](https://img.shields.io/pypi/dm/pyowm.svg)](https://img.shields.io/pypi/dm/pyowm.svg)

##  What is it?
PyOWM is a client Python wrapper library for the OpenWeatherMap (OWM) web API.

It allows quick and easy consumption of OWM weather data from Python applications via a simple object model and in a human-friendly fashion.

No additional libraries are requested: only the Python standard library modules.

##  Support

PyOWM currently supports _version 2.5_ of the OWM API (which is the latest one)

PyOWM runs on Python 2.7, 3.2, 3.3, 3.4 and 3.5

##  Usage

### API key

As the OpenWeatherMap API needs a valid API key to allow responses, 
*PyOWM won't work if you don't provide one*. This stands for both the free and paid (pro) subscription plans.

You can signup for a free API key [on the OWM website](https://home.openweathermap.org/users/sign_up)

Please notice that the free API subscription plan is subject to requests throttling.

### Examples

```python
import pyowm

owm = pyowm.OWM('your-API-key')  # You MUST provide a valid API key

# You have a pro subscription? Use:
# owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')
    
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

##  Installation

### Using pip

`pip install pyowm`

### From source with setuptools

1. Download the source archive either from GitHub ([select a release](https://github.com/csparpa/pyowm/releases)
   or just take the [main branch](https://github.com/csparpa/pyowm/archive/master.zip))
   or from the [Python Package Index](https://pypi.python.org/pypi/pyowm) 
2. Uncompress:

       `unzip pywom-x.y.z`

3. Launch setuptools:

       `cd pywom-x.y.z`
       
       `python setup.py install`

### exe installer (Windows users)

The installer is available on the [Python Package Index](https://pypi.python.org/pypi/pyowm) 

### Docker
You can run a Docker container mounting the latest PyOWM release code with:
```
docker run -d --name pyowm csparpa/pyowm
```

The source code is under `/pyowm` inside the container.
You can globally install PyOWM on the container with:
```
docker exec -ti pyowm bash -c 'pip install pyowm'
```

## License

[MIT](https://github.com/csparpa/pyowm/blob/master/LICENSE) license

## Changelog
Please read the [changelog](https://github.com/csparpa/pyowm/wiki/Changelog) page of the wiki


## Documentation
Usage examples are available in [the wiki page](https://github.com/csparpa/pyowm/wiki/Usage-examples).

The library API documentation is available on [Read the Docs](https://pyowm.readthedocs.org).

## Testing
Unit testing is as simple as `python setup.py test -s tests.unit`. This shall
be done for each different Python interpreter supported by PyOWM.

A more straighforward way to run tests is using [Tox](http://tox.readthedocs.org).
From the project root folder, just launch:

`tox`

PyOWM is continuously built with [Travis-CI](https://travis-ci.org/csparpa/pyowm) and code coverage is checked
with [Coveralls.io](https://coveralls.io/r/csparpa/pyowm)

## Discussion
Join the [PyOWM public Slack team](https://pyowm.slack.com) by signing up [here](http://pyowm-slackin.herokuapp.com/)

## Development
Contributors (code enhancement, issue/bug reporting) are __welcome!__. See the
[notes on development](https://github.com/csparpa/pyowm/wiki/Notes-on-development) to get started.

Since version 2.2 PyOWM adopts [Semantic Versioning](http://semver.org/).

If you liked PyOWM, [consider giving me a tip](https://gratipay.com/csparpa)!

## References
* [OpenWeatherMap website](http://openweathermap.org/)
* [OpenWeatherMap web API wiki](http://bugs.openweathermap.org/projects/api/wiki)
