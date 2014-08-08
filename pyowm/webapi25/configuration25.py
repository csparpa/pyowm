#!/usr/bin/env python

from pyowm.caches import nullcache
from pyowm.webapi25 import observationparser
from pyowm.webapi25 import observationlistparser
from pyowm.webapi25 import forecastparser
from pyowm.webapi25 import weatherhistoryparser
from pyowm.webapi25 import stationhistoryparser
from pyowm.webapi25 import weathercoderegistry

"""
Configuration for the PyOWM library specific to OWM web API version 2.5
"""

# OWM web API URLs
ROOT_API_URL = 'http://api.openweathermap.org/data/2.5'
ICONS_BASE_URL = 'http://openweathermap.org/img/w'
OBSERVATION_URL = ROOT_API_URL + '/weather'
FIND_OBSERVATIONS_URL = ROOT_API_URL + '/find'
THREE_HOURS_FORECAST_URL = ROOT_API_URL + '/forecast'
DAILY_FORECAST_URL = ROOT_API_URL + '/forecast/daily'
CITY_WEATHER_HISTORY_URL = ROOT_API_URL + '/history/city'
STATION_WEATHER_HISTORY_URL = ROOT_API_URL + '/history/station'

# Parser objects injection for OWM web API responses parsing
parsers = {
  'observation': observationparser.ObservationParser(),
  'observation_list': observationlistparser.ObservationListParser(),
  'forecast': forecastparser.ForecastParser(),
  'weather_history': weatherhistoryparser.WeatherHistoryParser(),
  'station_history': stationhistoryparser.StationHistoryParser()
}

# Cache provider to be used
cache = nullcache.NullCache()

# OWM web API availability test timeout in seconds
API_AVAILABILITY_TIMEOUT = 2

# Weather status keywords
RAIN_KEYWORDS = ['rain', 'drizzle'] # will be range: [300-321] + [500-531]
SUN_KEYWORDS = ['clear'] # will be range: [800-800]
CLOUDS_KEYWORDS = ['clouds'] # will be range: [801-804]
FOG_KEYWORDS = ['fog', 'haze', 'mist']  # mist=701  haze=721 fog=741
SNOW_KEYWORDS = ['snow', 'sleet'] # will be range: [600-622]

weather_code_registry = weathercoderegistry.WeatherCodeRegistry({
    "rain": [{
        "start": 500,
        "end": 531
    },
    {
        "start": 300,
        "end": 321
    }],
    "sun": [{
        "start": 800,
        "end": 800
    }],
    "clouds": [{
        "start": 801,
        "end": 804
    }],
    "fog": [{
        "start": 741,
        "end": 741
    }],
    "haze": [{
        "start": 721,
        "end": 721
    }],
    "mist": [{
        "start": 701,
        "end": 701
    }],
    "snow": [{
        "start": 600,
        "end": 622
    }]
})