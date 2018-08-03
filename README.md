[![logo](logos/180x180.png)](https://github.com/csparpa)

#  PyOWM - LongTerm Support for Python2.7
A Python wrapper around the OpenWeatherMap API

**This is a LongTerm Support branch that will be dropped on January 1st, 2020 as part of the EOL for Python 2.x**

[![PyPI version](https://badge.fury.io/py/pyowm.svg)](https://badge.fury.io/py/pyowm)
[![Latest Release Documentation](https://readthedocs.org/projects/pyowm/badge/?version=latest)](https://pyowm.readthedocs.io)
[![Build Status](https://travis-ci.org/csparpa/pyowm.png?branch=master)](https://travis-ci.org/csparpa/pyowm)
[![Coverage Status](https://coveralls.io/repos/github/csparpa/pyowm/badge.svg?branch=master)](https://coveralls.io/github/csparpa/pyowm?branch=master)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/csparpa)

##  What is it?
PyOWM is a client Python wrapper library for OpenWeatherMap (OWM) web APIs.

It allows quick and easy consumption of OWM data from Python applications via a simple object model and in a human-friendly fashion.

PyOWM runs on Python 2.7 and Python 3.4+ (but watch out! Python 2.x will eventually be dropped - [check details out](https://github.com/csparpa/pyowm/wiki/Timeline-for-dropping-Python-2.x-support))

PyOWM also integrates with [Django 1.10+ models](https://github.com/csparpa/pyowm/wiki/Django-support).


##  Installation

Install with `pip` for your ease:

```shell
$ pip install git+https://github.com/csparpa/pyowm.git@v2.9-LTS
```



##  Usage

### API key

As OpenWeatherMap APIs need a valid API key to allow responses,
*PyOWM won't work if you don't provide one*. This stands for both free and paid (pro) subscription plans.

You can signup for a free API key [on the OWM website](https://home.openweathermap.org/users/sign_up)

Please notice that the free API subscription plan is subject to requests throttling.

### Examples

That's a simple example of what you can do with PyOWM and a free OWM API Key:

```python
import pyowm

owm = pyowm.OWM('your-API-key')  # You MUST provide a valid API key

# Have a pro subscription? Then use:
# owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')

# Search for current weather in London (Great Britain)
observation = owm.weather_at_place('London,GB')
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

And this is a usage example with a paid OWM API key:

```python
import pyowm

paid_owm = pyowm.OWM(API_key='your-pro-API-key', subscription_type='pro')

# Will it be clear tomorrow at this time in Milan (Italy) ?
forecast = paid_owm.daily_forecast("Milan,IT")
tomorrow = pyowm.timeutils.tomorrow()
forecast.will_be_clear_at(tomorrow)  # The sun always shines on Italy, right? ;-)
```

More PyOWM usage examples are available [here](https://github.com/csparpa/pyowm/blob/master/pyowm/docs/usage-examples.md).


## Documentation
The library software API documentation is available on [Read the Docs](https://pyowm.readthedocs.io/).

Each release has its own [changelog](https://github.com/csparpa/pyowm/wiki/Changelog).


## Contributing

_Contributors (coding, testing, packaging, reporting issues) are welcome!_.

See the [the official documentation website](https://pyowm.readthedocs.io/) for details or the [CONTRIBUTING.md](https://github.com/csparpa/pyowm/blob/master/CONTRIBUTING.md) file for a quick primer.


## Community
Join the **[PyOWM public Slack team](https://pyowm.slack.com)** by signing up [here](http://pyowm-slackin.herokuapp.com/)

Here are [some cool projects](https://github.com/csparpa/pyowm/wiki/Community-Projects-using-PyOWM) that use PyOWM

## References
* [OpenWeatherMap website](http://openweathermap.org/)
* [OpenWeatherMap web API docs](http://openweathermap.org/api)


## License
[MIT license](https://github.com/csparpa/pyowm/blob/master/LICENSE)
