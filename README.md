[![logo](logos/180x180.png)](https://github.com/csparpa)

#  PyOWM  
**A Python wrapper around OpenWeatherMap web APIs**

[![PyPI version](https://badge.fury.io/py/pyowm.svg)](https://badge.fury.io/py/pyowm)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyowm.svg)](https://img.shields.io/pypi/dm/pyowm.svg)
<br>
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyowm.svg)](https://img.shields.io/pypi/pyversions/pyowm.svg)
<br>
[![Latest Release Documentation](https://readthedocs.org/projects/pyowm/badge/?version=latest)](https://pyowm.readthedocs.io/en/latest/)
[![Build Status](https://travis-ci.org/csparpa/pyowm.png?branch=master)](https://travis-ci.org/csparpa/pyowm)
[![Coverage Status](https://coveralls.io/repos/github/csparpa/pyowm/badge.svg?branch=master)](https://coveralls.io/github/csparpa/pyowm?branch=master)
<br>
<a href="https://www.buymeacoffee.com/LmAl1n9" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/black_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/csparpa)

##  What is it?
PyOWM is a client Python wrapper library for OpenWeatherMap (OWM) web APIs.

It allows quick and easy consumption of OWM data from Python applications via a simple object model and in a human-friendly fashion.

With PyOWM you can integrate into your code any of the following OpenWeatherMap web APIs:

 - **[Weather API v2.5](https://pyowm.readthedocs.io/en/latest/usage-examples-v2/weather-api-usage-examples.html)**, providing
    - current weather data
    - weather forecasts
    - weather history
 - **[Agro API v1.0](https://pyowm.readthedocs.io/en/latest/usage-examples-v2/agro-api-usage-examples.html)**, providing soil data and satellite imagery search and download
 - **[Air Pollution API v3.0](https://pyowm.readthedocs.io/en/latest/usage-examples-v2/air-pollution-api-usage-examples.html)**, providing data about CO, O3, NO2 and SO2
 - **[UV Index API v3.0](https://pyowm.readthedocs.io/en/latest/usage-examples-v2/uv-api-usage-examples.html)**, providing data about Ultraviolet exposition
 - **[Stations API v3.0](https://pyowm.readthedocs.io/en/latest/usage-examples-v2/stations-api-usage-examples.html)**, allowing to create and manage meteostation and publish local weather measurements
 - **[Weather Alerts API v3.0](https://pyowm.readthedocs.io/en/latest/usage-examples-v2/alerts-api-usage-examples.html)**, allowing to set triggers on weather conditions and areas and poll for spawned alerts
 - **[Image tiles](https://pyowm.readthedocs.io/en/latest/usage-examples-v2/map-tiles-client-examples.html)** for several map layers provided by OWM

PyOWM runs on Python 3.5+

PyOWM also integrates with [Django 1.10+ models](https://github.com/csparpa/pyowm/wiki/Django-support).


##  Installation

Install with `pip` for your ease:

```shell
$ pip install pyowm
```

There is a lot of alternatives: [setuptools](https://github.com/csparpa/pyowm/wiki/Install#install-from-source-with-setuptools), 
[Windows installers](https://github.com/csparpa/pyowm/wiki/Install#windows-exe) and common package managers such as
[Yaourt (Arch Linux)](https://github.com/csparpa/pyowm/wiki/Install#on-archlinux-with-yaourt) and [YaST/Zypper (OpenSuse)](https://github.com/csparpa/pyowm/wiki/Install#on-opensuse-with-yastzypper)

Eager to fetch the very latest updates to PyOWM? Install the development trunk:

```shell
$ pip install git+https://github.com/csparpa/pyowm.git@develop
```



##  Usage

### API key

As OpenWeatherMap APIs need a valid API key to allow responses,
*PyOWM won't work if you don't provide one*. This stands for both free and paid (pro) subscription plans.

You can signup for a free API key [on the OWM website](https://home.openweathermap.org/users/sign_up)

Please notice that the free API subscription plan is subject to requests throttling.

### Examples

That's a simple example of what you can do with PyOWM Weather API and a free OWM API Key:

```python
import pyowm

owm = pyowm.OWM('your-API-key')  # You MUST provide a valid API key

# Have a pro subscription? Then use:
# owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')

# Search for current weather in London (Great Britain)
observation = owm.weather_at_place('London,GB')
w = observation.weather
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

And this is an example using a paid OWM API key:

```python
import pyowm

paid_owm = pyowm.OWM(API_key='your-pro-API-key', subscription_type='pro')

# Will it be clear tomorrow at this time in Milan (Italy) ?
forecast = paid_owm.daily_forecast("Milan,IT")
tomorrow = pyowm.timeutils.tomorrow()
forecast.will_be_clear_at(tomorrow)  # The sun always shines on Italy, right? ;)
```

## Documentation
The library software API documentation is available on [Read the Docs](https://pyowm.readthedocs.io/en/latest/).

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
