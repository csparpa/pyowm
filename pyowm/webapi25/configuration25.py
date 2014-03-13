#!/usr/bin/env python

from pyowm.caches import nullcache
from pyowm.webapi25 import observationparser
from pyowm.webapi25 import observationlistparser
from pyowm.webapi25 import forecastparser
from pyowm.webapi25 import weatherhistoryparser
from pyowm.webapi25 import stationhistoryparser

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
RAIN_KEYWORDS = ['rain', 'drizzle']
SUN_KEYWORDS = ['clear']
CLOUDS_KEYWORDS = ['clouds']
FOG_KEYWORDS = ['fog', 'haze', 'mist']
SNOW_KEYWORDS = ['snow', 'sleet']
