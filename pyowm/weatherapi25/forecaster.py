#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.utils import formatting, weather
from pyowm.weatherapi25 import weathercoderegistry


class Forecaster:

    """
    A class providing convenience methods for manipulating weather forecast
    data. The class encapsulates a *Forecast* instance and provides
    abstractions on the top of it in order to let programmers exploit weather
    forecast data in a human-friendly fashion.

    :param forecast: a *Forecast* instance
    :type forecast: *Forecast*
    :returns: a *Forecaster* instance

    """

    def __init__(self, forecast):
        self.forecast = forecast
        self._wc_registry = weathercoderegistry.WeatherCodeRegistry.get_instance()

    def when_starts(self, timeformat='unix'):
        """
        Returns the GMT time of the start of the forecast coverage, which is
        the time of the most ancient *Weather* item in the forecast

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: a long or a str
        :raises: *ValueError* when invalid time format values are provided

        """
        start_coverage = min(item.reference_time() for item in self.forecast)
        return formatting.timeformat(start_coverage, timeformat)

    def when_ends(self, timeformat='unix'):
        """
        Returns the GMT time of the end of the forecast coverage, which is the
        time of the most recent *Weather* item in the forecast

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: a long or a str
        :raises: *ValueError* when invalid time format values are provided

        """
        end_coverage = max(item.reference_time() for item in self.forecast)
        return formatting.timeformat(end_coverage, timeformat)

    def will_have_rain(self):
        """
        Tells if into the forecast coverage exist one or more *Weather* items
        related to rain conditions

        :returns: boolean

        """        
        return weather.any_status_is(self.forecast.weathers, "rain", self._wc_registry)

    def will_have_clear(self):
        """
        Tells if into the forecast coverage exist one or more *Weather* items
        related to clear sky conditions

        :returns: boolean

        """
        return weather.any_status_is(self.forecast.weathers, "sun", self._wc_registry)

    def will_have_fog(self):
        """
        Tells if into the forecast coverage exist one or more *Weather* items
        related to fog conditions

        :returns: boolean

        """
        return weather.any_status_is(self.forecast.weathers, "fog", self._wc_registry)

    def will_have_clouds(self):
        """
        Tells if into the forecast coverage exist one or more *Weather* items
        related to cloud conditions

        :returns: boolean

        """
        return weather.any_status_is(self.forecast.weathers, "clouds", self._wc_registry)

    def will_have_snow(self):
        """
        Tells if into the forecast coverage exist one or more *Weather* items
        related to snow conditions

        :returns: boolean

        """
        return weather.any_status_is(self.forecast.weathers, "snow", self._wc_registry)

    def will_have_storm(self):
        """
        Tells if into the forecast coverage exist one or more *Weather* items
        related to storms

        :returns: boolean

        """
        return weather.any_status_is(self.forecast.weathers, "storm", self._wc_registry)

    def will_have_tornado(self):
        """
        Tells if into the forecast coverage exist one or more *Weather* items
        related to tornadoes

        :returns: boolean

        """
        return weather.any_status_is(self.forecast.weathers, "tornado", self._wc_registry)

    def will_have_hurricane(self):
        """
        Tells if into the forecast coverage exist one or more *Weather* items
        related to hurricanes

        :returns: boolean

        """
        return weather.any_status_is(self.forecast.weathers, "hurricane", self._wc_registry)

    def when_rain(self):
        """
        Returns a sublist of the *Weather* list in the forecast, containing
        only items having rain as weather condition.

        :returns: a list of *Weather* objects
        """
        return weather.filter_by_status(self.forecast.weathers, "rain", self._wc_registry)

    def when_clear(self):
        """
        Returns a sublist of the *Weather* list in the forecast, containing
        only items having clear sky as weather condition.

        :returns: a list of *Weather* objects
        """
        return weather.filter_by_status(self.forecast.weathers, "sun", self._wc_registry)


    def when_fog(self):
        """
        Returns a sublist of the *Weather* list in the forecast, containing
        only items having fog as weather condition.

        :returns: a list of *Weather* objects
        """
        return weather.filter_by_status(self.forecast.weathers, "fog", self._wc_registry)

    def when_clouds(self):
        """
        Returns a sublist of the *Weather* list in the forecast, containing
        only items having clouds as weather condition.

        :returns: a list of *Weather* objects
        """
        return weather.filter_by_status(self.forecast.weathers, "clouds", self._wc_registry)

    def when_snow(self):
        """
        Returns a sublist of the *Weather* list in the forecast, containing
        only items having snow as weather condition.

        :returns: a list of *Weather* objects
        """
        return weather.filter_by_status(self.forecast.weathers, "snow", self._wc_registry)

    def when_storm(self):
        """
        Returns a sublist of the *Weather* list in the forecast, containing
        only items having storm as weather condition.

        :returns: a list of *Weather* objects
        """
        return weather.filter_by_status(self.forecast.weathers, "storm", self._wc_registry)

    def when_tornado(self):
        """
        Returns a sublist of the *Weather* list in the forecast, containing
        only items having tornado as weather condition.

        :returns: a list of *Weather* objects
        """
        return weather.filter_by_status(self.forecast.weathers, "tornado", self._wc_registry)

    def when_hurricane(self):
        """
        Returns a sublist of the *Weather* list in the forecast, containing
        only items having hurricane as weather condition.

        :returns: a list of *Weather* objects
        """
        return weather.filter_by_status(self.forecast.weathers, "hurricane", self._wc_registry)

    def _will_be(self, timeobject, weather_condition):
        """
        Tells if at the specified weather condition will occur at the specified
        time. The check is performed on the *Weather* item of the forecast
        which is closest to the time value conveyed by the parameter

        :param timeobject: may be a UNIX time, a ``datetime.datetime`` object
            or an ISO8601-formatted string in the format
            ``YYYY-MM-DD HH:MM:SS+00``
        :type timeobject: long/int, ``datetime.datetime`` or str)
        :param weather_condition: the weather condition to be looked up
        :type weather_condition: str
        :returns: boolean

        """
        time_value = formatting.to_UNIXtime(timeobject)
        closest_weather = weather.find_closest_weather(
                                        self.forecast.weathers,
                                        time_value)
        return weather.status_is(closest_weather, weather_condition, self._wc_registry)

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
        return self._will_be(timeobject, "rain")

    def will_be_clear_at(self, timeobject):
        """
        Tells if at the specified time the condition is clear sky. The check is
        performed on the *Weather* item of the forecast which is closest to the
        time value conveyed by the parameter

        :param timeobject: may be a UNIX time, a ``datetime.datetime`` object
            or an ISO8601-formatted string in the format
            ``YYYY-MM-DD HH:MM:SS+00``
        :type timeobject: long/int, ``datetime.datetime`` or str)
        :returns: boolean

        """
        return self._will_be(timeobject, "sun")

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
        return self._will_be(timeobject, "snow")

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
        return self._will_be(timeobject, "clouds")

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
        return self._will_be(timeobject, "fog")

    def will_be_stormy_at(self, timeobject):
        """
        Tells if at the specified time the condition is storm. The check is
        performed on the *Weather* item of the forecast which is closest to the
        time value conveyed by the parameter

        :param timeobject: may be a UNIX time, a ``datetime.datetime`` object
            or an ISO8601-formatted string in the format
            ``YYYY-MM-DD HH:MM:SS+00``
        :type timeobject: long/int, ``datetime.datetime`` or str)
        :returns: boolean

        """
        return self._will_be(timeobject, "storm")

    def will_be_tornado_at(self, timeobject):
        """
        Tells if at the specified time the condition is tornado. The check is
        performed on the *Weather* item of the forecast which is closest to the
        time value conveyed by the parameter

        :param timeobject: may be a UNIX time, a ``datetime.datetime`` object
            or an ISO8601-formatted string in the format
            ``YYYY-MM-DD HH:MM:SS+00``
        :type timeobject: long/int, ``datetime.datetime`` or str)
        :returns: boolean

        """
        return self._will_be(timeobject, "tornado")

    def will_be_hurricane_at(self, timeobject):
        """
        Tells if at the specified time the condition is hurricane. The check is
        performed on the *Weather* item of the forecast which is closest to the
        time value conveyed by the parameter

        :param timeobject: may be a UNIX time, a ``datetime.datetime`` object
            or an ISO8601-formatted string in the format
            ``YYYY-MM-DD HH:MM:SS+00``
        :type timeobject: long/int, ``datetime.datetime`` or str)
        :returns: boolean

        """
        return self._will_be(timeobject, "hurricane")

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
        return weather. \
            find_closest_weather(self.forecast.weathers,
                                 formatting.to_UNIXtime(timeobject))

    def most_hot(self):
        """
        Returns the *Weather* object in the forecast having the highest max
        temperature. Was 'temp_max' key missing for
        every *Weather* instance in the forecast, ``None`` would be returned.

        :returns: a *Weather* object or ``None`` if no item in the forecast is
            eligible
        """
        maxtemp = -270.0  # No one would survive that...
        hottest = None
        for weather in self.forecast.weathers:
            d = weather.temperature()
            if 'temp_max' in d and d['temp_max'] > maxtemp:
                maxtemp = d['temp_max']
                hottest = weather
        return hottest

    def most_cold(self):
        """
        Returns the *Weather* object in the forecast having the lowest min
        temperature. Was 'temp_min' key missing for
        every *Weather* instance in the forecast, ``None`` would be returned.

        :returns: a *Weather* object or ``None`` if no item in the forecast is
            eligible
        """
        mintemp = 1000.0  # No one would survive that...
        coldest = None
        for weather in self.forecast.weathers:
            d = weather.temperature()
            if 'temp_min' in d and d['temp_min'] < mintemp:
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
        for weather in self.forecast.weathers:
            h = weather.humidity
            if h > max_humidity:
                max_humidity = h
                most_humid = weather
        return most_humid

    def most_rainy(self):
        """
        Returns the *Weather* object in the forecast having the highest
        precipitation volume. Was the 'all' key missing for every *Weather*
        instance in the forecast,``None`` would be returned.

        :returns: a *Weather* object or ``None`` if no item in the forecast is
            eligible
        """
        max_rain = 0
        most_rainy = None
        for weather in self.forecast.weathers:
            d = weather.rain
            if 'all' in d and d['all'] > max_rain:
                max_rain = d['all']
                most_rainy = weather
        return most_rainy

    def most_snowy(self):
        """
        Returns the *Weather* object in the forecast having the highest
        snow volume. Was the 'all' key missing for every *Weather* instance in the
        forecast, ``None`` would be returned.

        :returns: a *Weather* object or ``None`` if no item in the forecast is
            eligible
        """
        max_snow = 0
        most_snowy = None
        for weather in self.forecast.weathers:
            d = weather.snow
            if 'all' in d and d['all'] > max_snow:
                max_snow = d['all']
                most_snowy = weather
        return most_snowy

    def most_windy(self):
        """
        Returns the *Weather* object in the forecast having the highest
        wind speed. Was the 'speed' key missing for every *Weather* instance in the
        forecast, ``None`` would be returned.

        :returns: a *Weather* object or ``None`` if no item in the forecast is
            eligible
        """
        max_wind_speed = 0
        most_windy = None
        for weather in self.forecast.weathers:
            d = weather.wind()
            if 'speed' in d and d['speed'] > max_wind_speed:
                max_wind_speed = d['speed']
                most_windy = weather
        return most_windy

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)
