#!/usr/bin/env python

"""
PyOWM library entry point
"""

from constants import OWM_API_VERSION, PYOWM_VERSION, OBSERVATION_URL
from utils import httputils, jsonparser

class OWM(object):
    """
    A global facade representing the OWM web API
    """

    def __init__(self, API_key=None):
        """
        API_key - An OpenWeatherMap API key (str, may be None)
        
        For reference about OWM API keys visit:
          http://openweathermap.org/appid
        """
        if API_key is not None:
            assert type(API_key) is str, "If provided, 'API_key' must be a str"
        self.__API_key = API_key  

    def get_API_key(self):
        """Returns the OWM API key"""
        return self.__API_key

    def set_API_key(self, API_key):
        """Updates the OWM API key"""
        self.__API_key = API_key    
    
    def get_API_version(self):
        """Returns the currently supported OWM API version"""
        return OWM_API_VERSION
    
    def get_version(self):
        """Returns the current version of the PyOWM library"""
        return PYOWM_VERSION


    # Main OWM web API querying methods

    def observation_for_name(self, place):
        """
        Queries the OWM API for the currently observed weather at the specified
        toponym (eg: "London,uk"). Returns an Observation object instance
        
        place - a toponym (str)
        """
        assert type(place) is str, "'place' must be a str"
        json_data = httputils.call_API(OBSERVATION_URL, {'q': place}, self.__API_key)
        return jsonparser.parse_observation(json_data)

    
    def observation_for_coords(self, lon, lat):
        """
        Queries the OWM API for the currently observed weather at the specified
        lon/lat coordinates (eg: -0.107331,51.503614).
        
        lon - location longitude (int/float between -180 and 180 degrees)
        lat - location latitude (int/float between -90 and 90 degress)
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
