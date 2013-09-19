#!/usr/bin/env python

"""
Weather observation classes and data structures.
"""

from json import dumps, loads
from location import Location
from weather import Weather
from utils import converter

class Observation(object):
    """
    A databox containing weather data observed in a certain location and at a
    certain time.
    """

    def __init__(self, reception_time, location, weather):
        """
        reception_time - GMT UNIXtime of data reception from the OWM API (long/int)
        location - the location relative to this observation (Location)
        weather - the observed weather data (Weather)
        """
        assert type(reception_time) is long or type(reception_time) is int, \
            "'reception_time' must be an int/long"
        if long(reception_time) < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self.__reception_time = long(reception_time)
        assert isinstance(location, Location), "'location' must be a Location object"
        self.__location = location
        assert isinstance(weather, Weather), "'weather' must be a Weather object"
        self.__weather = weather

    def get_reception_time(self, timeformat='unix'):
        """
        Returns the GMT time of the observation reception
            format - how to format the result:
                unix (default) - returns a long
                iso - returns a ISO 8601-formatted str
        """
        if timeformat == 'unix':
            return self.__reception_time
        if timeformat == 'iso':
            return converter.unix_to_ISO8601(self.__reception_time)
        else:
            raise ValueError("Invalid value for parameter 'format'")

    def get_location(self):
        """Returns the Location object"""
        return self.__location

    def get_weather(self):
        """Returns the Weather object"""
        return self.__weather
    
    def to_JSON(self):
        """Dumps object fields into a JSON formatted string"""
        d = {"reception_time": self.__reception_time, 
              "Location": loads(self.__location.to_JSON()),
              "Weather": loads(self.__weather.to_JSON())
              }
        return dumps(d)
    
    def to_XML(self):
        """Dumps object fields into a XML formatted string"""
        return '<Observation><reception_time>%s</reception_time>%s%s</Observation>' % \
            (self.__reception_time, self.__location.to_XML(), 
             self.__weather.to_XML())
    
    def __str__(self):
        """Redefine __str__ hook for pretty-printing of Observation instances"""
        return "[Observation:\nreception time="+str(self.__reception_time)+ \
            "\n"+str(self.__location)+"\n"+str(self.__weather)+"\n]"