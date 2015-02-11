"""
XMLNS configuration
"""

# XML Schemas URLs for PyOWM model entities
ROOT_XMLNS_URL = 'http://github.com/csparpa/pyowm/tree/master/pyowm/webapi25/xsd'
LOCATION_XMLNS_URL = ROOT_XMLNS_URL + '/location.xsd'
WEATHER_XMLNS_URL = ROOT_XMLNS_URL + '/weather.xsd'
OBSERVATION_XMLNS_URL = ROOT_XMLNS_URL + '/observation.xsd'
FORECAST_XMLNS_URL = ROOT_XMLNS_URL + '/forecast.xsd'
STATION_HISTORY_XMLNS_URL = ROOT_XMLNS_URL + '/station_history.xsd'
LIST_STATION_XMLNS_URL = ROOT_XMLNS_URL + '/station.xsd'

# XML Schema prefixes for PyOWM model entities
LOCATION_XMLNS_PREFIX = 'l'
WEATHER_XMLNS_PREFIX = 'w'
OBSERVATION_XMLNS_PREFIX = 'o'
FORECAST_XMLNS_PREFIX = 'f'
STATION_HISTORY_XMLNS_PREFIX = 'sh'
LIST_STATION_XMLNS_PREFIX = 's'
