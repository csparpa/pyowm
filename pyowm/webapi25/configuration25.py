from pyowm.caches import nullcache
from pyowm.webapi25 import observationparser, observationlistparser, \
    forecastparser, weatherhistoryparser, stationparser, stationlistparser, \
    stationhistoryparser, uvindexparser, uvindexlistparser, coindexparser, \
    weathercoderegistry, cityidregistry, ozone_parser, no2indexparser, \
    so2indexparser

"""
Configuration for the PyOWM library specific to OWM web API version 2.5
"""

# Subdomains mapping
API_SUBSCRIPTION_SUBDOMAINS = {
    'free': 'api',
    'pro': 'pro'
}

# Default usage of SSL on OWM API calls
USE_SSL = False
VERIFY_SSL_CERTS = True

# OWM web API URLs
ROOT_API_URL = 'http://%s.openweathermap.org/data/2.5'
ROOT_HISTORY_URL = 'http://history.openweathermap.org/data/2.5'
ICONS_BASE_URL = 'http://openweathermap.org/img/w'
OBSERVATION_URL = ROOT_API_URL + '/weather'
GROUP_OBSERVATIONS_URL = ROOT_API_URL + '/group'
STATION_URL = ROOT_API_URL + '/station'
FIND_OBSERVATIONS_URL = ROOT_API_URL + '/find'
FIND_STATION_URL = ROOT_API_URL + '/station/find'
BBOX_STATION_URL = ROOT_API_URL + '/box/station'
THREE_HOURS_FORECAST_URL = ROOT_API_URL + '/forecast'
DAILY_FORECAST_URL = ROOT_API_URL + '/forecast/daily'
CITY_WEATHER_HISTORY_URL = ROOT_HISTORY_URL + '/history/city'
STATION_WEATHER_HISTORY_URL = ROOT_API_URL + '/history/station'

# OWM UV web API URLs
ROOT_UV_API_URL = 'http://api.openweathermap.org/data/2.5'
UV_INDEX_URL = ROOT_UV_API_URL + '/uvi'
UV_INDEX_FORECAST_URL = ROOT_UV_API_URL + '/uvi/forecast'
UV_INDEX_HISTORY_URL = ROOT_UV_API_URL + '/uvi/history'

# OWM Air Pollution API URLs
ROOT_POLLUTION_API_URL = 'http://api.openweathermap.org/pollution/v1'
CO_INDEX_URL = ROOT_POLLUTION_API_URL + '/co'
OZONE_URL = ROOT_POLLUTION_API_URL + '/o3'
NO2_INDEX_URL = ROOT_POLLUTION_API_URL + '/no2'
SO2_INDEX_URL = ROOT_POLLUTION_API_URL + '/so2'


# Parser objects injection for OWM web API responses parsing
parsers = {
  'observation': observationparser.ObservationParser(),
  'observation_list': observationlistparser.ObservationListParser(),
  'forecast': forecastparser.ForecastParser(),
  'weather_history': weatherhistoryparser.WeatherHistoryParser(),
  'station_history': stationhistoryparser.StationHistoryParser(),
  'station': stationparser.StationParser(),
  'station_list': stationlistparser.StationListParser(),
  'uvindex': uvindexparser.UVIndexParser(),
  'uvindex_list': uvindexlistparser.UVIndexListParser(),
  'coindex': coindexparser.COIndexParser(),
  'ozone': ozone_parser.OzoneParser(),
  'no2index': no2indexparser.NO2IndexParser(),
  'so2index': so2indexparser.SO2IndexParser()
}

# City ID registry
city_id_registry = cityidregistry.CityIDRegistry('cityids/%03d-%03d.txt.gz')

# Cache provider to be used
cache = nullcache.NullCache()

# Default language for OWM web API queries text results
language = 'en'

# Default API subscription type ('free' or 'pro')
API_SUBSCRIPTION_TYPE = 'free'

# OWM web API availability timeout in seconds
API_AVAILABILITY_TIMEOUT = 2

# Weather status code registry
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
    }],
    "tornado": [{
        "start": 781,
        "end": 781
    },
    {
        "start": 900,
        "end": 900
    }],
    "storm": [{
        "start": 901,
        "end": 901
    },
    {
        "start": 960,
        "end": 961
    }],
    "hurricane": [{
        "start": 902,
        "end": 902
    },
    {
        "start": 962,
        "end": 962
    }]
})
