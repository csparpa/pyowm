#!/usr/bin/env python

"""
Module containing the PyOWM library main entry point
"""

from time import time
from pyowm import constants
from pyowm.webapi25.configuration25 import (
    OBSERVATION_URL, FIND_OBSERVATIONS_URL, THREE_HOURS_FORECAST_URL,
    DAILY_FORECAST_URL, CITY_WEATHER_HISTORY_URL, STATION_WEATHER_HISTORY_URL,
    FIND_STATION_URL, API_AVAILABILITY_TIMEOUT)
from pyowm.webapi25.configuration25 import city_id_registry as zzz
from pyowm.abstractions import owm
from pyowm.caches import nullcache
from pyowm.commons import owmhttpclient
from pyowm.utils import timeformatutils
from pyowm.webapi25 import forecaster
from pyowm.webapi25 import historian


class OWM25(owm.OWM):
    """
    OWM subclass providing methods for each OWM web API 2.5 endpoint. The class
    is instantiated with *jsonparser* subclasses, each one parsing the response
    payload of a specific API endpoint

    :param parsers: the dictionary containing *jsonparser* concrete instances
        to be used as parsers for OWM web API 2.5 responses
    :type parsers: dict
    :param API_key: the OWM web API key (defaults to ``None``)
    :type API_key: str
    :param cache: a concrete implementation of class *OWMCache* serving as the
        cache provider (defaults to a *NullCache* instance)
    :type cache: an *OWMCache* concrete instance
    :param language: the language in which you want text results to be returned.
          It's a two-characters string, eg: "en", "ru", "it". Defaults to: "en"
    :type language: str
    :returns: an *OWM25* instance

    """
    def __init__(self, parsers, API_key=None, cache=nullcache.NullCache(),
                 language="en"):
        self._parsers = parsers
        if API_key is not None:
            assert type(API_key) is str, "If provided, 'API_key' must be a str"
        self._API_key = API_key
        self._httpclient = owmhttpclient.OWMHTTPClient(API_key, cache)
        self._language = language

    def get_API_key(self):
        """
        Returns the str OWM API key

        :returns: a str

        """
        return self._API_key

    def set_API_key(self, API_key):
        """
        Updates the str OWM API key

        :param API_key: the new str API key
        :type API_key: str

        """
        self._API_key = API_key

    def get_API_version(self):
        """
        Returns the currently supported OWM web API version

        :returns: the OWM web API version string

        """
        return "2.5"

    def get_version(self):
        """
        Returns the current version of the PyOWM library

        :returns: the current PyOWM library version string

        """
        return constants.PYOWM_VERSION

    def get_language(self):
        """
        Returns the language in which the OWM web API shall return text results

        :returns: the language

        """
        return self._language

    def set_language(self, language):
        """
        Sets the language in which the OWM web API shall return text results

        :param language: the new two-characters language (eg: "ru")
        :type API_key: str

        """
        self._language = language

    def city_id_registry(self):
        """
        Gives the *CityIDRegistry* singleton instance that can be used to lookup
        for city IDs.

        :returns: a *CityIDRegistry* instance
        """
        return zzz

    def is_API_online(self):
        """
        Returns True if the OWM web API is currently online. A short timeout
        is used to determine API service availability.

        :returns: bool

        """
        data = self._httpclient.call_API(OBSERVATION_URL, {},
                                         API_AVAILABILITY_TIMEOUT)
        if data is not None:
            return True
        return False

    def weather_at_place(self, name):
        """
        Queries the OWM web API for the currently observed weather at the
        specified toponym (eg: "London,uk")

        :param name: the location's toponym
        :type name: str
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed or *APICallException* when OWM web API can not be
            reached
        """
        assert type(name) is str, "'name' must be a str"
        json_data = self._httpclient.call_API(OBSERVATION_URL,
                                          {'q': name,'lang': self._language})
        return self._parsers['observation'].parse_JSON(json_data)

    def weather_at_coords(self, lat, lon):
        """
        Queries the OWM web API for the currently observed weather at the
        specified geographic (eg: 51.503614, -0.107331).

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed or *APICallException* when OWM web API can not be
            reached
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        json_data = self._httpclient.call_API(OBSERVATION_URL,
                                              {'lon': lon, 'lat': lat, 
                                               'lang': self._language})
        return self._parsers['observation'].parse_JSON(json_data)

    def weather_at_id(self, id):
        """
        Queries the OWM web API for the currently observed weather at the
        specified city ID (eg: 5128581)

        :param id: the location's city ID
        :type id: int
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed or *APICallException* when OWM web API can not be
            reached
        """
        assert type(id) is int, "'id' must be an int"
        if id < 0:
            raise ValueError("'id' value must be greater than 0")
        json_data = self._httpclient.call_API(OBSERVATION_URL,
                                              {'id': id,
                                               'lang': self._language})
        return self._parsers['observation'].parse_JSON(json_data)

    def weather_at_places(self, pattern, searchtype, limit=None):
        """
        Queries the OWM web API for the currently observed weather in all the
        locations whose name is matching the specified text search parameters.
        A twofold search can be issued: *'accurate'* (exact matching) and
        *'like'* (matches names that are similar to the supplied pattern).

        :param pattern: the string pattern (not a regex) to be searched for the
            toponym
        :type pattern: str
        :param searchtype: the search mode to be used, must be *'accurate'* for
          an exact matching or *'like'* for a likelihood matching
        :type: searchtype: str
        :param limit: the maximum number of *Observation* items in the returned
            list (default is ``None``, which stands for any number of items)
        :param limit: int or ``None``
        :returns: a list of *Observation* objects or ``None`` if no weather
            data is available
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* when bad value is supplied for the search
            type or the maximum number of items retrieved
        """
        assert isinstance(pattern, str), "'pattern' must be a str"
        assert isinstance(searchtype, str), "'searchtype' must be a str"
        if searchtype != "accurate" and searchtype != "like":
            raise ValueError("'searchtype' value must be 'accurate' or 'like'")
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        params = {'q': pattern, 'type': searchtype, 'lang': self._language}
        if limit is not None:
            # fix for OWM 2.5 API bug!
            params['cnt'] = limit - 1
        json_data = self._httpclient.call_API(FIND_OBSERVATIONS_URL, params)
        return self._parsers['observation_list'].parse_JSON(json_data)

    def weather_around_coords(self, lat, lon, limit=None):
        """
        Queries the OWM web API for the currently observed weather in all the
        locations in the proximity of the specified coordinates.

        :param lat: location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param limit: the maximum number of *Observation* items in the returned
            list (default is ``None``, which stands for any number of items)
        :param limit: int or ``None``
        :returns: a list of *Observation* objects or ``None`` if no weather
            data is available
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* when coordinates values are out of bounds or
            negative values are provided for limit
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        params = {'lon': lon, 'lat': lat, 'lang': self._language}
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
            params['cnt'] = limit
        json_data = self._httpclient.call_API(FIND_OBSERVATIONS_URL, params)
        return self._parsers['observation_list'].parse_JSON(json_data)

    def three_hours_forecast(self, name):
        """
        Queries the OWM web API for three hours weather forecast for the
        specified location (eg: "London,uk"). A *Forecaster* object is
        returned, containing a *Forecast* instance covering a global streak of
        five days: this instance encapsulates *Weather* objects, with a time
        interval of three hours one from each other

        :param name: the location's toponym
        :type name: str
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached
        """
        assert type(name) is str, "'name' must be a str"
        json_data = self._httpclient.call_API(THREE_HOURS_FORECAST_URL,
                                          {'q': name, 'lang': self._language})
        forecast = self._parsers['forecast'].parse_JSON(json_data)
        if forecast is not None:
            forecast.set_interval("3h")
            return forecaster.Forecaster(forecast)
        else:
            return None

    def three_hours_forecast_at_coords(self, lat, lon):
        """
        Queries the OWM web API for three hours weather forecast for the
        specified geographic coordinate (eg: latitude: 51.5073509,
        longitude: -0.1277583). A *Forecaster* object is returned,
        containing a *Forecast* instance covering a global streak of
        five days: this instance encapsulates *Weather* objects, with a time
        interval of three hours one from each other

        :param lat: location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        params = {'lon': lon, 'lat': lat, 'lang': self._language}
        json_data = self._httpclient.call_API(THREE_HOURS_FORECAST_URL, params)
        forecast = self._parsers['forecast'].parse_JSON(json_data)
        if forecast is not None:
            forecast.set_interval("3h")
            return forecaster.Forecaster(forecast)
        else:
            return None

    def three_hours_forecast_at_id(self, id):
        """
        Queries the OWM web API for three hours weather forecast for the
        specified city ID (eg: 5128581). A *Forecaster* object is returned,
        containing a *Forecast* instance covering a global streak of
        five days: this instance encapsulates *Weather* objects, with a time
        interval of three hours one from each other

        :param id: the location's city ID
        :type id: int
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached
        """
        assert type(id) is int, "'id' must be an int"
        if id < 0:
            raise ValueError("'id' value must be greater than 0")
        json_data = self._httpclient.call_API(THREE_HOURS_FORECAST_URL,
                                              {'id': id,
                                               'lang': self._language})
        forecast = self._parsers['forecast'].parse_JSON(json_data)
        if forecast is not None:
            forecast.set_interval("3h")
            return forecaster.Forecaster(forecast)
        else:
            return None


    def daily_forecast(self, name, limit=None):
        """
        Queries the OWM web API for daily weather forecast for the specified
        location (eg: "London,uk"). A *Forecaster* object is returned,
        containing a *Forecast* instance covering a global streak of fourteen
        days by default: this instance encapsulates *Weather* objects, with a
        time interval of one day one from each other

        :param name: the location's toponym
        :type name: str
        :param limit: the maximum number of daily *Weather* items to be
            retrieved (default is ``None``, which stands for any number of
            items)
        :type limit: int or ``None``
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if negative values are supplied for limit
        """
        assert type(name) is str, "'name' must be a str"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        params = {'q': name, 'lang': self._language}
        if limit is not None:
            params['cnt'] = limit
        json_data = self._httpclient.call_API(DAILY_FORECAST_URL, params)
        forecast = self._parsers['forecast'].parse_JSON(json_data)
        if forecast is not None:
            forecast.set_interval("daily")
            return forecaster.Forecaster(forecast)
        else:
            return None

    def daily_forecast_at_coords(self, lat, lon, limit=None):
        """
        Queries the OWM web API for daily weather forecast for the specified
        geographic coordinate (eg: latitude: 51.5073509, longitude: -0.1277583).
        A *Forecaster* object is returned, containing a *Forecast* instance
        covering a global streak of fourteen days by default: this instance
        encapsulates *Weather* objects, with a time interval of one day one
        from each other

        :param lat: location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param limit: the maximum number of daily *Weather* items to be
            retrieved (default is ``None``, which stands for any number of
            items)
        :type limit: int or ``None``
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if negative values are supplied for limit
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        params = {'lon': lon, 'lat': lat, 'lang': self._language}
        if limit is not None:
            params['cnt'] = limit
        json_data = self._httpclient.call_API(DAILY_FORECAST_URL, params)
        forecast = self._parsers['forecast'].parse_JSON(json_data)
        if forecast is not None:
            forecast.set_interval("daily")
            return forecaster.Forecaster(forecast)
        else:
            return None

    def daily_forecast_at_id(self, id, limit=None):
        """
        Queries the OWM web API for daily weather forecast for the specified
        city ID (eg: 5128581). A *Forecaster* object is returned, containing
        a *Forecast* instance covering a global streak of fourteen days by
        default: this instance encapsulates *Weather* objects, with a time
        interval of one day one from each other

        :param id: the location's city ID
        :type id: int
        :param limit: the maximum number of daily *Weather* items to be
            retrieved (default is ``None``, which stands for any number of
            items)
        :type limit: int or ``None``
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if negative values are supplied for limit
        """
        assert type(id) is int, "'id' must be an int"
        if id < 0:
            raise ValueError("'id' value must be greater than 0")
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")

        params = {'id': id, 'lang': self._language}
        if limit is not None:
            params['cnt'] = limit
        json_data = self._httpclient.call_API(DAILY_FORECAST_URL, params)
        forecast = self._parsers['forecast'].parse_JSON(json_data)
        if forecast is not None:
            forecast.set_interval("daily")
            return forecaster.Forecaster(forecast)
        else:
            return None


    def weather_history_at_place(self, name, start=None, end=None):
        """
        Queries the OWM web API for weather history for the specified location
        (eg: "London,uk"). A list of *Weather* objects is returned. It is
        possible to query for weather history in a closed time period, whose
        boundaries can be passed as optional parameters.

        :param name: the location's toponym
        :type name: str
        :param start: the object conveying the time value for the start query
            boundary (defaults to ``None``)
        :type start: int, ``datetime.datetime`` or ISO8601-formatted
            string
        :param end: the object conveying the time value for the end query
            boundary (defaults to ``None``)
        :type end: int, ``datetime.datetime`` or ISO8601-formatted string
        :returns: a list of *Weather* instances or ``None`` if history data is
            not available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if the time boundaries are not in the correct
            chronological order, if one of the time boundaries is not ``None``
            and the other is or if one or both of the time boundaries are after
            the current time

        """
        assert type(name) is str, "'name' must be a str"
        params = {'q': name, 'lang': self._language}
        if start is None and end is None:
            pass
        elif start is not None and end is not None:
            unix_start = timeformatutils.to_UNIXtime(start)
            unix_end = timeformatutils.to_UNIXtime(end)
            if unix_start >= unix_end:
                raise ValueError("Error: the start time boundary must " \
                                 "precede the end time!")
            current_time = time()
            if unix_start > current_time:
                raise ValueError("Error: the start time boundary must " \
                                 "precede the current time!")
            params['start'] = str(unix_start)
            params['end'] = str(unix_end)
        else:
            raise ValueError("Error: one of the time boundaries is None, " \
                             "while the other is not!")
        json_data = self._httpclient.call_API(CITY_WEATHER_HISTORY_URL,
                                              params)
        return self._parsers['weather_history'].parse_JSON(json_data)

    def weather_history_at_id(self, id, start=None, end=None):
        """
        Queries the OWM web API for weather history for the specified city ID.
        A list of *Weather* objects is returned. It is possible to query for
        weather history in a closed time period, whose boundaries can be passed
        as optional parameters.

        :param id: the city ID
        :type id: int
        :param start: the object conveying the time value for the start query
            boundary (defaults to ``None``)
        :type start: int, ``datetime.datetime`` or ISO8601-formatted
            string
        :param end: the object conveying the time value for the end query
            boundary (defaults to ``None``)
        :type end: int, ``datetime.datetime`` or ISO8601-formatted string
        :returns: a list of *Weather* instances or ``None`` if history data is
            not available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if the time boundaries are not in the correct
            chronological order, if one of the time boundaries is not ``None``
            and the other is or if one or both of the time boundaries are after
            the current time

        """
        assert type(id) is int, "'id' must be an int"
        if id < 0:
            raise ValueError("'id' value must be greater than 0")
        params = {'id': id, 'lang': self._language}
        if start is None and end is None:
            pass
        elif start is not None and end is not None:
            unix_start = timeformatutils.to_UNIXtime(start)
            unix_end = timeformatutils.to_UNIXtime(end)
            if unix_start >= unix_end:
                raise ValueError("Error: the start time boundary must " \
                                 "precede the end time!")
            current_time = time()
            if unix_start > current_time:
                raise ValueError("Error: the start time boundary must " \
                                 "precede the current time!")
            params['start'] = str(unix_start)
            params['end'] = str(unix_end)
        else:
            raise ValueError("Error: one of the time boundaries is None, " \
                             "while the other is not!")
        json_data = self._httpclient.call_API(CITY_WEATHER_HISTORY_URL,
                                              params)
        return self._parsers['weather_history'].parse_JSON(json_data)

    def station_at_coords(self, lat, lon, limit=None):
        """
        Queries the OWM web API for weather stations nearest to the
        specified geographic coordinate (eg: latitude: 51.5073509,
        longitude: -0.1277583). A list of *Station* objects is returned,
        this instance encapsulates a last reported *Weather* object.

        :param lat: location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param cnt: the maximum number of *Station* items to be retrieved
            (default is ``None``, which stands for any number of items)
        :type cnt: int or ``None``

        :returns: a list of *Station* objects or ``None`` if station data is
            not available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        params = {'lat': lat, 'lon': lon}
        if limit is not None:
            params['cnt'] = limit
        json_data = self._httpclient.call_API(FIND_STATION_URL, params)
        return self._parsers['station_list'].parse_JSON(json_data)

    def station_tick_history(self, station_ID, limit=None):
        """
        Queries the OWM web API for historic weather data measurements for the
        specified meteostation (eg: 2865), sampled once a minute (tick).
        A *StationHistory* object instance is returned, encapsulating the
        measurements: the total number of data points can be limited using the
        appropriate parameter

        :param station_ID: the numeric ID of the meteostation
        :type station_ID: int
        :param limit: the maximum number of data points the result shall
            contain (default is ``None``, which stands for any number of data
            points)
        :type limit: int or ``None``
        :returns: a *StationHistory* instance or ``None`` if data is not
            available for the specified meteostation
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if the limit value is negative

        """
        assert isinstance(station_ID, int), "'station_ID' must be int"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        station_history = self._retrieve_station_history(station_ID, limit,
                                                         "tick")
        if station_history is not None:
            return historian.Historian(station_history)
        else:
            return None

    def station_hour_history(self, station_ID, limit=None):
        """
        Queries the OWM web API for historic weather data measurements for the
        specified meteostation (eg: 2865), sampled once a hour.
        A *Historian* object instance is returned, encapsulating a
        *StationHistory* objects which contains the measurements. The total
        number of retrieved data points can be limited using the appropriate
        parameter

        :param station_ID: the numeric ID of the meteostation
        :type station_ID: int
        :param limit: the maximum number of data points the result shall
            contain (default is ``None``, which stands for any number of data
            points)
        :type limit: int or ``None``
        :returns: a *Historian* instance or ``None`` if data is not
            available for the specified meteostation
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if the limit value is negative

        """
        assert isinstance(station_ID, int), "'station_ID' must be int"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        station_history = self._retrieve_station_history(station_ID, limit,
                                                         "hour")
        if station_history is not None:
            return historian.Historian(station_history)
        else:
            return None

    def station_day_history(self, station_ID, limit=None):
        """
        Queries the OWM web API for historic weather data measurements for the
        specified meteostation (eg: 2865), sampled once a day.
        A *Historian* object instance is returned, encapsulating a
        *StationHistory* objects which contains the measurements. The total
        number of retrieved data points can be limited using the appropriate
        parameter

        :param station_ID: the numeric ID of the meteostation
        :type station_ID: int
        :param limit: the maximum number of data points the result shall
            contain (default is ``None``, which stands for any number of data
            points)
        :type limit: int or ``None``
        :returns: a *Historian* instance or ``None`` if data is not
            available for the specified meteostation
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if the limit value is negative

        """
        assert isinstance(station_ID, int), "'station_ID' must be int"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        station_history = self._retrieve_station_history(station_ID, limit,
                                                         "day")
        if station_history is not None:
            return historian.Historian(station_history)
        else:
            return None

    def _retrieve_station_history(self, station_ID, limit, interval):
        """
        Helper method for station_X_history functions.
        """
        params = {'id': station_ID, 'type': interval, 'lang': self._language}
        if limit is not None:
            params['cnt'] = limit
        json_data = self._httpclient.call_API(STATION_WEATHER_HISTORY_URL,
                                              params)
        station_history = \
            self._parsers['station_history'].parse_JSON(json_data)
        if station_history is not None:
            station_history.set_station_ID(station_ID)
            station_history.set_interval(interval)
        return station_history

    def __repr__(self):
        return "<%s.%s - API key=%s, OWM web API version=%s, " \
               "PyOWM version=%s, language=%s>" % (__name__,
                                      self.__class__.__name__,
                                      self._API_key, self.get_API_version(),
                                      self.get_version(),
                                      self._language)
