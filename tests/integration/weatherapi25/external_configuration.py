"""
Configuration for the PyOWM library specific to OWM Weather API version 2.5
"""

# OWM Weather API URLs
ROOT_API_URL = 'apibase'
ICONS_BASE_URL = 'iconbase'
OBSERVATION_URL = ROOT_API_URL + '/a'
FIND_OBSERVATIONS_URL = ROOT_API_URL + '/b'
THREE_HOURS_FORECAST_URL = ROOT_API_URL + '/c'
DAILY_FORECAST_URL = ROOT_API_URL + '/d/daily'
CITY_WEATHER_HISTORY_URL = ROOT_API_URL + '/e'
STATION_WEATHER_HISTORY_URL = ROOT_API_URL + '/f'

USE_SSL = False
VERIFY_SSL_CERTS = True

# Parser objects injection for OWM Weather API responses parsing
parsers = {
  'observation': None,
  'observation_list': None,
  'forecast': None,
  'weather_history': None,
  'station_history': None
}

# Cache provider to be used
cache = None

# Default language for OWM Weather API queries text results
language = 'ru'

# Default API subscription type ('free' or 'pro')
API_SUBSCRIPTION_TYPE = 'free'

# OWM Weather API availability test timeout in seconds
API_AVAILABILITY_TIMEOUT = 2

# Weather status keywords
RAIN_KEYWORDS = ['rain', 'drizzle']
SUN_KEYWORDS = ['clear']
CLOUDS_KEYWORDS = ['clouds']
FOG_KEYWORDS = ['fog', 'haze', 'mist']
SNOW_KEYWORDS = ['snow', 'sleet']
