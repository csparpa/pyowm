#!/usr/bin/env python

"""
Module containing the PyOWM library main entry point
"""

from time import time
from pyowm.constants import PYOWM_VERSION
from pyowm.webapi25.configuration25 import OBSERVATION_URL, \
    FIND_OBSERVATIONS_URL, THREE_HOURS_FORECAST_URL, DAILY_FORECAST_URL, \
    CITY_WEATHER_HISTORY_URL, STATION_WEATHER_HISTORY_URL
from pyowm.abstractions.owm import OWM
from pyowm.caches.nullcache import NullCache
from pyowm.commons.owmhttpclient import OWMHTTPClient 
from pyowm.utils import converter
from pyowm.webapi25.forecaster import Forecaster
from pyowm.webapi25.historian import Historian


class OWM25(OWM):
    """
    OWM subclass providing methods for each OWM web API 2.5 endpoint. The class
    is instantiated with *jsonparser* subclasses, each one parsing the response
    payload of a specific API endpoint
    
    :param parsers: the dictionary containing *jsonparser* concrete instances
        to be used as parsers for OWM web API 2.5 reponses
    :type parsers: dict 
    :param API_key: the OWM web API key (can be ``None``)
    :type API_key: str
    :returns:  an *OWM25* instance 
    
    """
    def __init__(self, parsers, API_key=None, cache=NullCache()):
        self.__parsers = parsers
        if API_key is not None:
            assert type(API_key) is str, "If provided, 'API_key' must be a str"
        self.__API_key = API_key
        self.__httpclient = OWMHTTPClient(API_key, cache)

    def get_API_key(self):
        """
        Returns the OWM API key
        
        :returns: the OWM API key string
        
        """
        return self.__API_key

    def set_API_key(self, API_key):
        """
        Updates the OWM API key
        
        :param API_key: the new value for the OWM API key
        :type API_key: str
        
        """
        self.__API_key = API_key    
    
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
        return PYOWM_VERSION

    # Main OWM web API querying methods

    def weather_at(self, name):
        """
        Queries the OWM web API for the currently observed weather at the 
        specified toponym (eg: "London,uk")
        
        :param name: the location's toponym
        :type name: str
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM web API responses' data cannot
            be parsed or *APICallException* when OWM web API can not be reached
        """
        assert type(name) is str, "'name' must be a str"
        json_data = self.__httpclient.call_API(OBSERVATION_URL, {'q': name})
        return self.__parsers['observation'].parse_JSON(json_data)

    
    def weather_at_coords(self, lon, lat):
        """
        Queries the OWM web API for the currently observed weather at the 
        specified geographic (eg: -0.107331,51.503614).
        
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM web API responses' data cannot
            be parsed or *APICallException* when OWM web API can not be reached
        """
        assert type(lon) is float or type(lon) is int,"'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int,"'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        json_data = self.__httpclient.call_API(OBSERVATION_URL, 
                                               {'lon': lon, 'lat': lat})
        return self.__parsers['observation'].parse_JSON(json_data)
    
    def find_weather_by_name(self, pattern, searchtype, limit=None):
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
        :returns: a list of *Observation* objects or ``None`` if no weather data
            is available
        :raises: *ParseResponseException* when OWM web API responses' data cannot
            be parsed, *APICallException* when OWM web API can not be reached,
            *ValueError* when bad value is supplied for the search type or the
            maximum number of items retrieved
        """
        assert isinstance(pattern, str), "'pattern' must be a str"
        assert isinstance(searchtype, str), "'searchtype' must be a str"
        if searchtype is not "accurate" and searchtype is not "like":
            raise ValueError("'searchtype' value must be 'accurate' or 'like'")
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        params = {'q': pattern, 'type': searchtype}        
        if limit is not None:
            params['cnt'] = limit-1 # -1 is needed to fix a bug of the OWM 2.5 API!
        json_data = self.__httpclient.call_API(FIND_OBSERVATIONS_URL, params)
        return self.__parsers['observation_list'].parse_JSON(json_data)

    def find_weather_by_coords(self, lon, lat, limit=None):
        """
        Queries the OWM web API for the currently observed weather in all the 
        locations in the proximity of the specified coordinates.
        
        :param lon: location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param lat: location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param limit: the maximum number of *Observation* items in the returned
            list (default is ``None``, which stands for any number of items)
        :param limit: int or ``None``
        :returns: a list of *Observation* objects or ``None`` if no weather data
            is available
        :raises: *ParseResponseException* when OWM web API responses' data cannot
            be parsed, *APICallException* when OWM web API can not be reached,
            *ValueError* when coordinates values are out of bounds or negative
            values are provided for limit
        """
        assert type(lon) is float or type(lon) is int,"'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int,"'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        params = {'lon': lon, 'lat': lat}        
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
            params['cnt'] = limit
        json_data = self.__httpclient.call_API(FIND_OBSERVATIONS_URL, params)
        return self.__parsers['observation_list'].parse_JSON(json_data)
    
    def three_hours_forecast(self, name):
        """
        Queries the OWM web API for three hours weather forecast for the specified 
        location (eg: "London,uk"). A *Forecaster* object is returned, containing
        a *Forecast* instance covering a global streak of five days: this instance
        encapsulates *Weather* objects, with a time interval of three hours one
        from each other
        
        :param name: the location's toponym
        :type name: str
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data cannot
            be parsed, *APICallException* when OWM web API can not be reached
        """
        assert type(name) is str, "'name' must be a str"
        json_data = self.__httpclient.call_API(THREE_HOURS_FORECAST_URL, {'q': name})
        forecast = self.__parsers['forecast'].parse_JSON(json_data)
        if forecast:
            forecast.set_interval("3h")
            return Forecaster(forecast)
        else:
            return None
    
    def daily_forecast(self, name, limit=None):
        """
        Queries the OWM web API for daily weather forecast for the specified 
        location (eg: "London,uk"). A *Forecaster* object is returned, containing
        a *Forecast* instance covering a global streak of fourteen days by default:
        this instance encapsulates *Weather* objects, with a time interval of one
        day one from each other
        
        :param name: the location's toponym
        :type name: str
        :param limit: the maximum number of daily *Weather* items to be retrieved
            (default is ``None``, which stands for any number of items)
        :type limit: int or ``None``
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data cannot
            be parsed, *APICallException* when OWM web API can not be reached,
            *ValueError* if negative values are supplied for limit
        """
        assert type(name) is str, "'name' must be a str"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        params = {'q': name}
        if limit is not None:
            params['cnt'] = limit
        json_data = self.__httpclient.call_API(DAILY_FORECAST_URL, params)
        forecast = self.__parsers['forecast'].parse_JSON(json_data)
        if forecast:
            forecast.set_interval("daily")
            return Forecaster(forecast)
        else:
            return None
        
    def weather_history(self, name, start=None, end=None):
        """
        Queries the OWM web API for weather history for the specified location 
        (eg: "London,uk"). A list of *Weather* objects is returned. It is possible
        to query for weather history in a closed time period, whose boundaries
        can be passed as optional parameters.        
        
        :param name: the location's toponym
        :type name: str
        :param start: the object conveying the time value for the start query boundary
            (defaults to ``None``)
        :type start: int/long, ``datetime.datetime`` or ISO8601-formatted string
        :param end: the object conveying the time value for the end query boundary
            (defaults to ``None``)
        :type end: int/long, ``datetime.datetime`` or ISO8601-formatted string
        :returns: a list of *Weather* instances or ``None`` if history data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data cannot
            be parsed, *APICallException* when OWM web API can not be reached,
            *ValueError* if the time boundaries are not in the correct chronological
            order, if one of the time boundaries is not ``None`` and the other is
            or if one or both of the time boundaries are after the current time
            
        """
        assert type(name) is str, "'name' must be a str"
        params = {'q': name}
        if start is None and end is None:
            pass
        elif start is not None and end is not None:
            unix_start = converter.to_UNIXtime(start)
            unix_end = converter.to_UNIXtime(end)
            if unix_start >= unix_end:
                raise ValueError("Error: the start time boundary must precede" \
                                 "the end time!")
            current_time = long(time())
            if unix_start > current_time: 
                raise ValueError("Error: the start time boundary must precede" \
                                 "the current time!")            
            params['start'] = str(unix_start)
            params['end'] = str(unix_end)
        else:
            raise ValueError("Error: one of the time boundaries is None, " \
                             "while the other is not!")
        json_data = self.__httpclient.call_API(CITY_WEATHER_HISTORY_URL, params)
        return self.__parsers['weather_history'].parse_JSON(json_data)
    
    def station_tick_history(self, station_ID, limit=None):
        """
        Queries the OWM web API for historic weather data measurements for the
        specified meteostation (eg: 2865), sampled once a minute (tick). 
        A *StationHistory* object instance is returned, encapsulating the 
        measurements: the total number of data points can be limited using the
        appropriate parameter        
        
        :param station_ID: the numeric ID of the meteostation
        :type station_ID: int
        :param limit: the maximum number of data points the result shall contain
            (default is ``None``, which stands for any number of data points)
        :type limit: int or ``None``
        :returns: a *StationHistory* instance or ``None`` if data is not
            available for the specified meteostation
        :raises: *ParseResponseException* when OWM web API responses' data cannot
            be parsed, *APICallException* when OWM web API can not be reached,
            *ValueError* if the limit value is negative
            
        """
        assert isinstance(station_ID, int), "'station_ID' must be int"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        station_history = self.__retrieve_station_history(station_ID, limit, "tick")
        if station_history:
            return Historian(station_history)
        else:
            return None
    
    
    def station_hour_history(self, station_ID, limit=None):
        """
        Queries the OWM web API for historic weather data measurements for the
        specified meteostation (eg: 2865), sampled once a hour. 
        A *StationHistory* object instance is returned, encapsulating the 
        measurements: the total number of data points can be limited using the
        appropriate parameter        
        
        :param station_ID: the numeric ID of the meteostation
        :type station_ID: int
        :param limit: the maximum number of data points the result shall contain
            (default is ``None``, which stands for any number of data points)
        :type limit: int or ``None``
        :returns: a *StationHistory* instance or ``None`` if data is not
            available for the specified meteostation
        :raises: *ParseResponseException* when OWM web API responses' data cannot
            be parsed, *APICallException* when OWM web API can not be reached,
            *ValueError* if the limit value is negative
            
        """
        assert isinstance(station_ID, int), "'station_ID' must be int"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        station_history = self.__retrieve_station_history(station_ID, limit, "hour")
        if station_history:
            return Historian(station_history)
        else:
            return None
    
    def station_day_history(self, station_ID, limit=None):
        """
        Queries the OWM web API for historic weather data measurements for the
        specified meteostation (eg: 2865), sampled once a day. 
        A *StationHistory* object instance is returned, encapsulating the 
        measurements: the total number of data points can be limited using the
        appropriate parameter        
        
        :param station_ID: the numeric ID of the meteostation
        :type station_ID: int
        :param limit: the maximum number of data points the result shall contain
            (default is ``None``, which stands for any number of data points)
        :type limit: int or ``None``
        :returns: a *StationHistory* instance or ``None`` if data is not
            available for the specified meteostation
        :raises: *ParseResponseException* when OWM web API responses' data cannot
            be parsed, *APICallException* when OWM web API can not be reached,
            *ValueError* if the limit value is negative
            
        """
        assert isinstance(station_ID, int), "'station_ID' must be int"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        station_history = self.__retrieve_station_history(station_ID, limit, "day")
        if station_history:
            return Historian(station_history)
        else:
            return None
    
    def __retrieve_station_history(self, station_ID, limit, interval):
        """
        Helper method for station_X_history functions.
        """
        params = {'id': station_ID, 'type': interval}
        if limit is not None:
            params['cnt'] = limit
        json_data = self.__httpclient.call_API(STATION_WEATHER_HISTORY_URL, params)
        station_history = \
            self.__parsers['station_history'].parse_JSON(json_data)
        if station_history:
            station_history.set_station_ID(station_ID)
            station_history.set_interval(interval)
        return station_history
    
    def __str__(self):
        """Redefine __str__ hook for pretty-printing of OWM instances"""
        return '[OWM25: API_key=%s]' % self.__API_key