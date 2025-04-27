[![logo](logos/180x180.png)](https://github.com/csparpa)

#  PyOWM  
**A Python wrapper around OpenWeatherMap web APIs**

[![PyPI version](https://badge.fury.io/py/pyowm.svg)](https://badge.fury.io/py/pyowm)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyowm.svg)](https://img.shields.io/pypi/dm/pyowm.svg)
<br>
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyowm.svg)](https://img.shields.io/pypi/pyversions/pyowm.svg)
<br>
[![Latest Release Documentation](https://readthedocs.org/projects/pyowm/badge/?version=latest)](https://pyowm.readthedocs.io/en/latest/)
[![Build Status](https://travis-ci.org/csparpa/pyowm.png?branch=develop)](https://travis-ci.org/csparpa/pyowm)
[![Coverage Status](https://coveralls.io/repos/github/csparpa/pyowm/badge.svg?branch=develop)](https://coveralls.io/github/csparpa/pyowm?branch=master)
<br>
<a href="https://www.buymeacoffee.com/LmAl1n9" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/black_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/csparpa%40gmail.com)

## Maintainer wanted !!!
*I am not able to maintain this project anymore :-( *
Anyone who is able to replace me in this effort, please get in touch

##  What is it?
PyOWM is a client Python wrapper library for OpenWeatherMap (OWM) web APIs. It allows quick and easy consumption of OWM data from Python applications via a simple object model and in a human-friendly fashion.

PyOWM runs on Python 3.7+

**Former Dark Sky API users**: you can can use PyOWM to get [OpenWeatherMap's OneCall API](https://openweathermap.org/api/one-call-api) data as an easy replacement to Dark Sky

### What kind of data can I get with PyOWM ?
With PyOWM you can integrate into your code any of the following OpenWeatherMap web APIs:

 - **Weather API v3.0** + **OneCall API**, providing current weather data, weather forecasts, weather history
 - **Agro API v1.0**, providing soil data and satellite imagery search and download
 - **Air Pollution API v3.0**, providing data about CO, O3, NO2 and SO2
 - **UV Index API v3.0**, providing data about Ultraviolet exposition
 - **Stations API v3.0**, allowing to create and manage meteostation and publish local weather measurements
 - **Weather Alerts API v3.0**, allowing to set triggers on weather conditions and areas and poll for spawned alerts
 - **Image tiles** for several map layers provided by OWM
 - **Geocoding API v1.0** allowing to perform direct/reverse geocoding 


## In case of trouble...
Please **read the [FAQ](https://pyowm.readthedocs.io/en/latest/v3/faq.html)** before filing a new issue on GitHub! There are many common issues, therefore a fix for your issue might come easier than you think

 ##  Get started

### API key

As OpenWeatherMap APIs need a valid API key to allow responses, *PyOWM won't work if you don't provide one*. This stands for both free and paid (pro) subscription plans.
You can signup for a free API key [on the OWM website](https://home.openweathermap.org/users/sign_up)
Please notice that the free API subscription plan is subject to requests throttling.

### Example

With a free OWM API Key:

```python
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

# ---------- FREE API KEY examples ---------------------

owm = OWM('your free OWM API key')
mgr = owm.weather_manager()


# Search for current weather in London (Great Britain) and get details
observation = mgr.weather_at_place('London,GB')
w = observation.weather

w.detailed_status         # 'clouds'
w.wind()                  # {'speed': 4.6, 'deg': 330}
w.humidity                # 87
w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
w.rain                    # {}
w.heat_index              # None
w.clouds                  # 75

# Will it be clear tomorrow at this time in Milan (Italy) ?
forecast = mgr.forecast_at_place('Milan,IT', 'daily')
answer = forecast.will_be_clear_at(timestamps.tomorrow())

# ---------- PAID API KEY example ---------------------

config_dict = config.get_default_config_for_subscription_type('professional')
owm = OWM('your paid OWM API key', config_dict)

# What's the current humidity in Berlin (Germany) ?
one_call_object = mgr.one_call(lat=52.5244, lon=13.4105)
one_call_object.current.humidity
```


##  Installation
Install with `pip` for your ease:

```shell
$ pip install pyowm
```

There are alternatives: _setuptools_, _Windows installers_ and common Linux package managers such as _Yaourt (Arch Linux)_
_YaST/Zypper (OpenSuse)_ (please refer to the documentation for more detail)

Eager to fetch the very latest updates to PyOWM? Install the development trunk (which might be unstable). Eg on Linux:

```shell
$ git clone https://github.com/csparpa/pyowm.git
$ cd pyowm && git checkout develop
$ pip install -r requirements.txt && python setup.py install
```

## Documentation
The library software API documentation is available on [Read the Docs](https://pyowm.readthedocs.io/en/latest/).

The [Code recipes](https://pyowm.readthedocs.io/en/latest/v3/code-recipes.html) section comes in handy!


## Community & Contributing

Here are [some cool projects](https://github.com/csparpa/pyowm/wiki/Community-Projects-using-PyOWM) that use PyOWM

Join the **[PyOWM public Slack team](https://pyowm.slack.com)** by signing up [here](http://pyowm-slackin.herokuapp.com/)

_Contributors (coding, testing, packaging, reporting issues) are welcome!_ See the [the official documentation website](https://pyowm.readthedocs.io/) for details or the [CONTRIBUTING.md](https://github.com/csparpa/pyowm/blob/master/CONTRIBUTING.md) file for a quick primer.


## License
[MIT license](https://github.com/csparpa/pyowm/blob/master/LICENSE)
