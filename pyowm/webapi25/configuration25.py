#!/usr/bin/env python

from observationparser import ObservationParser
from observationlistparser import ObservationListParser
from forecastparser import ForecastParser
from weatherhistoryparser import WeatherHistoryParser
from stationhistoryparser import StationHistoryParser

"""
Configuration for the PyOWM library specific to OWM web API version 2.5
"""

# OWM web API URLs
ROOT_API_URL = 'http://api.openweathermap.org/data/2.5'
ICONS_BASE_URL = 'http://openweathermap.org/img/w'
OBSERVATION_URL = ROOT_API_URL+'/weather'
FIND_OBSERVATIONS_URL = ROOT_API_URL+'/find'
THREE_HOURS_FORECAST_URL = ROOT_API_URL+'/forecast'
DAILY_FORECAST_URL = ROOT_API_URL+'/forecast/daily'
CITY_WEATHER_HISTORY_URL = ROOT_API_URL+'/history/city'
STATION_WEATHER_HISTORY_URL = ROOT_API_URL+'/history/station'

# Parser objects injection for OWM web API responses parsing
observation_parser = ObservationParser()
observation_list_parser = ObservationListParser(observation_parser)
forecast_parser = ForecastParser()
weather_history_parser = WeatherHistoryParser()
station_history_parser = StationHistoryParser()

# Weather status keywords
RAIN_KEYWORDS = ['rain','drizzle']
SUN_KEYWORDS = ['clear']
CLOUDS_KEYWORDS = ['clouds']
FOG_KEYWORDS =['fog','haze','mist']
SNOW_KEYWORDS =['snow','sleet']