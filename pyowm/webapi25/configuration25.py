#!/usr/bin/env python

from pyowm.caches import nullcache
import observationparser
import observationlistparser
import forecastparser
import weatherhistoryparser
import stationhistoryparser

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

# XML Schemas URLs for PyOWM model entities
ROOT_XMLNS_URL = 'http://github.com/csparpa/pyowm/tree/master/pyowm/webapi25/xsd'
LOCATION_XMLNS_URL = ROOT_XMLNS_URL + '/location.xsd'
WEATHER_XMLNS_URL = ROOT_XMLNS_URL + '/weather.xsd'
OBSERVATION_XMLNS_URL = ROOT_XMLNS_URL + '/observation.xsd'
FORECAST_XMLNS_URL = ROOT_XMLNS_URL + '/forecast.xsd'
STATION_HISTORY_XMLNS_URL = ROOT_XMLNS_URL + '/station_history.xsd'

# XML Schema prefixes for PyOWM model entities
LOCATION_XMLNS_PREFIX = 'l'
WEATHER_XMLNS_PREFIX = 'w'
OBSERVATION_XMLNS_PREFIX = 'o'
FORECAST_XMLNS_PREFIX = 'f'
STATION_HISTORY_XMLNS_PREFIX = 'sh'

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
