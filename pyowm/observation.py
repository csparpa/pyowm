#!/usr/bin/env python

"""
Weather observation classes and data structures.
"""

from json import dumps, loads
from utils import converter

class Observation(object):
    """
    A class representing the weather which is currently being observed in a certain
    location in the world. The location is represented by the encapsulated
    *Location* object while the observed weather data are held by the encapsulated
    *Weather* object.

    :param reception_time: GMT UNIXtime telling when the weather obervation has 
        been received from the OWM web API
    :type reception_time: long/int
    :param location: the *Location* relative to this observation
    :type location: *Location*
    :param weather: the *Weather* relative to this observation
    :type weather: *Weather*
    :returns: an *Observation* instance
    :raises: *ValueError* when negative values are provided as reception time

    """

    def __init__(self, reception_time, location, weather):
        if long(reception_time) < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self.__reception_time = long(reception_time)
        self.__location = location
        self.__weather = weather

    def get_reception_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the observation has been received
          from the OWM web API
    
        :param timeformat: the format for the time value. May be: 
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: a long or a str
        :raises: ValueError when negative values are provided
    
        """
        if timeformat == 'unix':
            return self.__reception_time
        elif timeformat == 'iso':
            return converter.UNIXtime_to_ISO8601(self.__reception_time)
        else:
            raise ValueError("Invalid value for parameter 'format'")

    def get_location(self):
        """
        Returns the *Location* object for this observation
        
        :returns: the *Location* object
        
        """
        return self.__location

    def get_weather(self):
        """
        Returns the *Weather* object for this observation
        
        :returns: the *Weather* object
        
        """
        return self.__weather
    
    def to_JSON(self):
        """Dumps object fields into a JSON formatted string
    
        :returns:  the JSON string
    
        """
        d = {"reception_time": self.__reception_time, 
              "Location": loads(self.__location.to_JSON()),
              "Weather": loads(self.__weather.to_JSON())
              }
        return dumps(d)
    
    def to_XML(self):
        """Dumps object fields into a XML formatted string
    
        :returns:  the XML string
    
        """
        return '<Observation><reception_time>%s</reception_time>%s%s</Observation>' % \
            (self.__reception_time, self.__location.to_XML(), 
             self.__weather.to_XML())