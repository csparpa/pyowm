#!/usr/bin/env python

"""
Module containing the PyOWM library main entry point
"""

from constants import OWM_API_VERSION, PYOWM_VERSION, OBSERVATION_URL, \
    FIND_OBSERVATIONS_URL, THREE_HOURS_FORECAST_URL, DAILY_FORECAST_URL
from utils import httputils, jsonparser
from forecaster import Forecaster

class OWM(object):
    """
    A global facade class representing the OWM web API. Every query to the API
    is done programmatically via an instance of this class, and can be optionally
    sent with an OWM API key (references can be found at http://openweathermap.org/appid)
    
    :param API_key: An OWM API key value
    :type API_key: string (defaults to ``None``)
    :returns: an *OWM* instance

    """

    def __init__(self, API_key=None):
        if API_key is not None:
            assert type(API_key) is str, "If provided, 'API_key' must be a str"
        self.__API_key = API_key  

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
        return OWM_API_VERSION
    
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
        json_data = httputils.call_API(OBSERVATION_URL, 
                                       {'q': name}, self.__API_key)
        return jsonparser.parse_observation(json_data)

    
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
        json_data = httputils.call_API(OBSERVATION_URL, {'lon': lon, 'lat': lat},
                                       self.__API_key)
        return jsonparser.parse_observation(json_data)
    
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
            params['cnt'] = limit-1 # -1 is needed to fix a bug of the OWM API!
        json_data = httputils.call_API(FIND_OBSERVATIONS_URL, 
           params, self.__API_key)
        return jsonparser.parse_search_results(json_data)

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
        json_data = httputils.call_API(FIND_OBSERVATIONS_URL, 
           params, self.__API_key)
        return jsonparser.parse_search_results(json_data)
    
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
        json_data = httputils.call_API(THREE_HOURS_FORECAST_URL, 
                                       {'q': name}, self.__API_key)
        forecast = jsonparser.parse_forecast(json_data)
        if forecast:
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
        json_data = httputils.call_API(DAILY_FORECAST_URL, 
                                       params, self.__API_key)
        forecast = jsonparser.parse_forecast(json_data)
        if forecast:
            return Forecaster(forecast)
        else:
            return None