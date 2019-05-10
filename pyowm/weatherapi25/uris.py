#!/usr/bin/env python
# -*- coding: utf-8 -*-


ROOT_WEATHER_API = 'http://%s.openweathermap.org/data/2.5'
ROOT_HISTORY_URI = 'http://history.openweathermap.org/data/2.5'
OBSERVATION_URI = ROOT_WEATHER_API + '/weather'
GROUP_OBSERVATIONS_URI = ROOT_WEATHER_API + '/group'
STATION_URI = ROOT_WEATHER_API + '/station'
FIND_OBSERVATIONS_URI = ROOT_WEATHER_API + '/find'
FIND_STATION_URI = ROOT_WEATHER_API + '/station/find'
BBOX_STATION_URI = ROOT_WEATHER_API + '/box/station'
BBOX_CITY_URI = ROOT_WEATHER_API + '/box/city'
THREE_HOURS_FORECAST_URI = ROOT_WEATHER_API + '/forecast'
DAILY_FORECAST_URI = ROOT_WEATHER_API + '/forecast/daily'
CITY_WEATHER_HISTORY_URI = ROOT_HISTORY_URI + '/history/city'
STATION_WEATHER_HISTORY_URI = ROOT_WEATHER_API + '/history/station'

ICONS_BASE_URI = 'http://openweathermap.org/img/w/%s.png'