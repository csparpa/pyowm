#!/usr/bin/env python

"""
Constants for the PyOWM library:
"""

# Version numbers
PYOWM_VERSION = '0.1.1'
OWM_API_VERSION = '2.5'

# OpenWeatherMap API URLs
ROOT_API_URL = 'http://api.openweathermap.org/data/2.5'
ICONS_BASE_URL = 'http://openweathermap.org/img/w'
OBSERVATION_URL = ROOT_API_URL+'/weather'
FIND_OBSERVATIONS_URL = ROOT_API_URL+'/find'
THREE_HOURS_FORECAST_URL = ROOT_API_URL+'/forecast'
DAILY_FORECAST_URL = ROOT_API_URL+'/forecast/daily'
CITY_WEATHER_HISTORY_URL = ROOT_API_URL+'/history/city'
STATION_WEATHER_HISTORY_URL = ROOT_API_URL+'/history/station'

# Weather status keywords
RAIN_KEYWORDS = ['rain','drizzle']
SUN_KEYWORDS = ['clear']
CLOUDS_KEYWORDS = ['clouds']
FOG_KEYWORDS =['fog','haze','mist']
SNOW_KEYWORDS =['snow','sleet']