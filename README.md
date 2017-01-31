#  PyOWM
A Python wrapper around the OpenWeatherMap API

[![PyPI version](https://badge.fury.io/py/pyowm.svg)](https://badge.fury.io/py/pyowm)
[![Build Status](https://travis-ci.org/csparpa/pyowm.png?branch=master)](https://travis-ci.org/csparpa/pyowm)
[![Coverage Status](https://coveralls.io/repos/csparpa/pyowm/badge.png?branch=develop)](https://coveralls.io/r/csparpa/pyowm?branch=develop)
[![Downloads](https://img.shields.io/pypi/dm/pyowm.svg)](https://img.shields.io/pypi/dm/pyowm.svg)

##  What is it?
PyOWM is a client Python wrapper library for the OpenWeatherMap (OWM) web API.

It allows quick and easy consumption of OWM weather data from Python applications via a simple object model and in a human-friendly fashion.

PyOWM runs on Python 2.7 and Python 3.2+, and integrates with [Django 1.10+ models](https://github.com/csparpa/pyowm/wiki/Django-support).


##  Installation

Install with `pip` for your ease:

```shell
$ pip install pyowm
```

There is a lot of alternatives: [setuptools](https://github.com/csparpa/pyowm/wiki/Install#install-from-source-with-setuptools), [Windows installers](https://github.com/csparpa/pyowm/wiki/Install#windows-exe) and common package managers such as [Yaourt](https://github.com/csparpa/pyowm/wiki/Install#on-archlinux-with-yaourt)

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

# Have a pro subscription? Then use:
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

PyOWM usage examples are available [here](https://github.com/csparpa/pyowm/blob/master/pyowm/docs/usage-examples.md).

## Documentation
Each release has its own [changelog](https://github.com/csparpa/pyowm/wiki/Changelog).

The library API documentation is available on [Read the Docs](https://pyowm.readthedocs.org).


## Contributing

_Contributors (coding, testing, packaging, reporting issues) are welcome!_.

See the [notes on development](https://github.com/csparpa/pyowm/wiki/Notes-on-development) wiki page to get started.

See the [notes on testing](https://github.com/csparpa/pyowm/wiki/Notes-on-testing) wiki page to get started


## Community
Join the **[PyOWM public Slack team](https://pyowm.slack.com)** by signing up [here](http://pyowm-slackin.herokuapp.com/)

Here are [some cool projects](https://github.com/csparpa/pyowm/wiki/Community-Projects-using-PyOWM) that use PyOWM

## References
* If you liked PyOWM, [consider giving me a tip](https://gratipay.com/csparpa)!
* [OpenWeatherMap website](http://openweathermap.org/)
* [OpenWeatherMap web API docs](http://openweathermap.org/api)


## License
[MIT license](https://github.com/csparpa/pyowm/blob/master/LICENSE)
