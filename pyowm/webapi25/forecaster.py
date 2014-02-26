#!/usr/bin/env python

"""
Module containing weather forecast abstraction classes and data structures.
"""

from pyowm.utils import timeformatutils
from pyowm.webapi25 import weatherutils
from pyowm.webapi25.configuration25 import (
    CLOUDS_KEYWORDS, FOG_KEYWORDS, RAIN_KEYWORDS, SNOW_KEYWORDS, SUN_KEYWORDS)


class Forecaster(object):

    """
    A class providing convenience methods for manipulating weather forecast
    data. The class encapsulates a *Forecast* instance and provides
    abstractions on the top of it in order to let programmers exploit weather
    forecast data in a human-friendly fashion

    :param forecast: a *Forecast* instance
    :type forecast: *Forecast*
    :returns: a *Forecaster* instance

    """

    def __init__(self, forecast):
        self._forecast = forecast

    def get_forecast(self):
        """
        Returns the *Forecast* instance

        :returns: the *Forecast* instance
        """
        return self._forecast

    def when_starts(self, timeformat='unix'):
        """
        Returns the GMT time of the start of the forecast coverage, which is
        the time of the most ancient *Weather* item in the forecast

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: a long or a str
        :raises: *ValueError* when invalid time format values are provided

        """
        start_coverage = min([item.get_reference_time() \
                              for item in self._forecast])
        if timeformat == 'unix':
            return start_coverage
        elif timeformat == 'iso':
            return timeformatutils.to_ISO8601(start_coverage)
        else:
            raise ValueError("Invalid value for parameter 'format'")

    def when_ends(self, timeformat='unix'):
        """
        Returns the GMT time of the end of the forecast coverage, which is the
        time of the most recent *Weather* item in the forecast

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: a long or a str
        :raises: *ValueError* when invalid time format values are provided

        """
        end_coverage = max([item.get_reference_time() \
                            for item in self._forecast])
        if timeformat == 'unix':
            return end_coverage
        elif timeformat == 'iso':
            return timeformatutils.to_ISO8601(end_coverage)
        else:
            raise ValueError("Invalid value for parameter 'format'")

    def will_have_rain(self):
        """
        Tells if into the forecast coverage exist one or more *Weather* items
        related to rain conditions

        :returns: boolean

        """
        return weatherutils.statuses_match_any(RAIN_KEYWORDS,
                                               self._forecast.get_weathers())

    def will_have_sun(self):
        """
        Tells if into the forecast coverage exist one or more *Weather* items
        related to sun conditions

        :returns: boolean

        """
        return weatherutils.statuses_match_any(SUN_KEYWORDS,
                                               self._forecast.get_weathers())

    def will_have_fog(self):
        """
        Tells if into the forecast coverage exist one or more *Weather* items
        related to fog conditions

        :returns: boolean

        """
        return weatherutils.statuses_match_any(FOG_KEYWORDS,
                                   self._forecast.get_weathers())

    def will_have_clouds(self):
        """
        Tells if into the forecast coverage exist one or more *Weather* items
        related to cloud conditions

        :returns: boolean

        """
        return weatherutils.statuses_match_any(CLOUDS_KEYWORDS,
                                   self._forecast.get_weathers())

    def will_have_snow(self):
        """
        Tells if into the forecast coverage exist one or more *Weather* items
        related to snow conditions

        :returns: boolean

        """
        return weatherutils.statuses_match_any(SNOW_KEYWORDS,
                                   self._forecast.get_weathers())

    def when_rain(self):
        """
        Returns a sublist of the *Weather* list in the forecast, containing
        only items having rain as weather condition.

        :returns: a list of *Weather* objects
        """
        return weatherutils.filter_by_matching_statuses(RAIN_KEYWORDS,
                                           self._forecast.get_weathers())

    def when_sun(self):
        """
        Returns a sublist of the *Weather* list in the forecast, containing
        only items having sun as weather condition.

        :returns: a list of *Weather* objects
        """
        return weatherutils.filter_by_matching_statuses(SUN_KEYWORDS,
                                           self._forecast.get_weathers())

    def when_fog(self):
        """
        Returns a sublist of the *Weather* list in the forecast, containing
        only items having fog as weather condition.

        :returns: a list of *Weather* objects
        """
        return weatherutils.filter_by_matching_statuses(FOG_KEYWORDS,
                                           self._forecast.get_weathers())

    def when_clouds(self):
        """
        Returns a sublist of the *Weather* list in the forecast, containing
        only items having clouds as weather condition.

        :returns: a list of *Weather* objects
        """
        return weatherutils.filter_by_matching_statuses(CLOUDS_KEYWORDS,
                                           self._forecast.get_weathers())

    def when_snow(self):
        """
        Returns a sublist of the *Weather* list in the forecast, containing
        only items having snow as weather condition.

        :returns: a list of *Weather* objects
        """
        return weatherutils.filter_by_matching_statuses(SNOW_KEYWORDS,
                                           self._forecast.get_weathers())

    def will_be_rainy_at(self, timeobject):
        """
        Tells if at the specified time the condition is rain. The check is
        performed on the *Weather* item of the forecast which is closest to the
        time value conveyed by the parameter

        :param timeobject: may be a UNIX time, a ``datetime.datetime`` object
            or an ISO8601-formatted string in the format
            ``YYYY-MM-DD HH:MM:SS+00``
        :type timeobject: long/int, ``datetime.datetime`` or str)
        :returns: boolean

        """
        time = timeformatutils.to_UNIXtime(timeobject)
        weather = weatherutils.find_closest_weather(
                                        self._forecast.get_weathers(), time)
        return weatherutils.status_matches_any(RAIN_KEYWORDS, weather)

    def will_be_sunny_at(self, timeobject):
        """
        Tells if at the specified time the condition is sun. The check is
        performed on the *Weather* item of the forecast which is closest to the
        time value conveyed by the parameter

        :param timeobject: may be a UNIX time, a ``datetime.datetime`` object
            or an ISO8601-formatted string in the format
            ``YYYY-MM-DD HH:MM:SS+00``
        :type timeobject: long/int, ``datetime.datetime`` or str)
        :returns: boolean

        """
        time = timeformatutils.to_UNIXtime(timeobject)
        closest_weather = weatherutils.find_closest_weather(
                                        self._forecast.get_weathers(), time)
        return weatherutils.status_matches_any(SUN_KEYWORDS, closest_weather)

    def will_be_snowy_at(self, timeobject):
        """
        Tells if at the specified time the condition is snow. The check is
        performed on the *Weather* item of the forecast which is closest to the
        time value conveyed by the parameter

        :param timeobject: may be a UNIX time, a ``datetime.datetime`` object
            or an ISO8601-formatted string in the format
            ``YYYY-MM-DD HH:MM:SS+00``
        :type timeobject: long/int, ``datetime.datetime`` or str)
        :returns: boolean

        """
        time = timeformatutils.to_UNIXtime(timeobject)
        weather = weatherutils.find_closest_weather(
                                        self._forecast.get_weathers(), time)
        return weatherutils.status_matches_any(SNOW_KEYWORDS, weather)

    def will_be_cloudy_at(self, timeobject):
        """
        Tells if at the specified time the condition is clouds. The check is
        performed on the *Weather* item of the forecast which is closest to the
        time value conveyed by the parameter

        :param timeobject: may be a UNIX time, a ``datetime.datetime`` object
            or an ISO8601-formatted string in the format
            ``YYYY-MM-DD HH:MM:SS+00``
        :type timeobject: long/int, ``datetime.datetime`` or str)
        :returns: boolean

        """
        time = timeformatutils.to_UNIXtime(timeobject)
        weather = weatherutils.find_closest_weather(
                                        self._forecast.get_weathers(), time)
        return weatherutils.status_matches_any(CLOUDS_KEYWORDS, weather)

    def will_be_foggy_at(self, timeobject):
        """
        Tells if at the specified time the condition is fog. The check is
        performed on the *Weather* item of the forecast which is closest to the
        time value conveyed by the parameter

        :param timeobject: may be a UNIX time, a ``datetime.datetime`` object
            or an ISO8601-formatted string in the format
            ``YYYY-MM-DD HH:MM:SS+00``
        :type timeobject: long/int, ``datetime.datetime`` or str)
        :returns: boolean

        """
        time = timeformatutils.to_UNIXtime(timeobject)
        weather = weatherutils.find_closest_weather(
                                        self._forecast.get_weathers(), time)
        return weatherutils.status_matches_any(FOG_KEYWORDS, weather)

    def get_weather_at(self, timeobject):
        """
        Gives the *Weather* item in the forecast that is closest in time to
        the time value conveyed by the parameter

        :param timeobject: may be a UNIX time, a ``datetime.datetime`` object
            or an ISO8601-formatted string in the format
            ``YYYY-MM-DD HH:MM:SS+00``
        :type timeobject: long/int, ``datetime.datetime`` or str)
        :returns: a *Weather* object

        """
        return weatherutils. \
            find_closest_weather(self._forecast.get_weathers(),
                                 timeformatutils.to_UNIXtime(timeobject))

    def most_hot(self):
        """
        Returns the *Weather* object in the forecast having the highest max
        temperature. The temperature is retrieved using the
        ``get_temperature['temp_max']`` call; was 'temp_max' key missing for
        every *Weather* instance in the forecast, ``None`` would be returned.

        :returns: a *Weather* object or ``None`` if no item in the forecast is
            eligible
        """
        maxtemp = -270.0  # No one would survive that...
        hottest = None
        for weather in self._forecast.get_weathers():
            d = weather.get_temperature()
            if 'temp_max' in d:
                if d['temp_max'] > maxtemp:
                    maxtemp = d['temp_max']
                    hottest = weather
        return hottest

    def most_cold(self):
        """
        Returns the *Weather* object in the forecast having the lowest min
        temperature. The temperature is retrieved using the
        ``get_temperature['temp_min']`` call; was 'temp_min' key missing for
        every *Weather* instance in the forecast, ``None`` would be returned.

        :returns: a *Weather* object or ``None`` if no item in the forecast is
            eligible
        """
        mintemp = 1000.0  # No one would survive that...
        coldest = None
        for weather in self._forecast.get_weathers():
            d = weather.get_temperature()
            if 'temp_min' in d:
                if d['temp_min'] < mintemp:
                    mintemp = d['temp_min']
                    coldest = weather
        return coldest

    def most_humid(self):
        """
        Returns the *Weather* object in the forecast having the highest
        humidty.

        :returns: a *Weather* object or ``None`` if no item in the forecast is
            eligible
        """
        max_humidity = 0
        most_humid = None
        for weather in self._forecast.get_weathers():
            h = weather.get_humidity()
            if h > max_humidity:
                max_humidity = h
                most_humid = weather
        return most_humid

    def most_rainy(self):
        """
        Returns the *Weather* object in the forecast having the highest
        precipitation volume. The rain amount is retrieved via the
        ``get_rain['all']`` call; was the 'all' key missing for every *Weather*
        instance in the forecast,``None`` would be returned.

        :returns: a *Weather* object or ``None`` if no item in the forecast is
            eligible
        """
        max_rain = 0
        most_rainy = None
        for weather in self._forecast.get_weathers():
            d = weather.get_rain()
            if 'all' in d:
                if d['all'] > max_rain:
                    max_rain = d['all']
                    most_rainy = weather
        return most_rainy

    def most_snowy(self):
        """
        Returns the *Weather* object in the forecast having the highest
        snow volume. The snow amount is retrieved via the ``get_snow['all']``
        call; was the 'all' key missing for every *Weather* instance in the
        forecast, ``None`` would be returned.

        :returns: a *Weather* object or ``None`` if no item in the forecast is
            eligible
        """
        max_snow = 0
        most_snowy = None
        for weather in self._forecast.get_weathers():
            d = weather.get_snow()
            if 'all' in d:
                if d['all'] > max_snow:
                    max_snow = d['all']
                    most_snowy = weather
        return most_snowy

    def most_windy(self):
        """
        Returns the *Weather* object in the forecast having the highest
        wind speed. The snow amount is retrieved via the ``get_wind['speed']``
        call; was the 'speed' key missing for every *Weather* instance in the
        forecast, ``None`` would be returned.

        :returns: a *Weather* object or ``None`` if no item in the forecast is
            eligible
        """
        max_wind_speed = 0
        most_windy = None
        for weather in self._forecast.get_weathers():
            d = weather.get_wind()
            if 'speed' in d:
                if d['speed'] > max_wind_speed:
                    max_wind_speed = d['speed']
                    most_windy = weather
        return most_windy

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)
