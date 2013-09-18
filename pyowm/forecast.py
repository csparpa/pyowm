#!/usr/bin/env python

"""
Forecast observation classes and data structures.
"""

from json import loads, dumps
from location import Location
from weather import Weather
from utils import converter

class ForecastIterator:
    """
    An iterator over the list of Weather objects encapsulated in a Forecast
    instance
    """
    def __init__(self, obj):
        """
        obj - the iterable to be iterated over
        """
        self.__obj = obj
        self.__cnt = 0
   
    def __iter__(self):
        """Returns an instance of the iterator"""
        return self

    def next(self):
        """Returns the next item from the iterable"""
        try:
            result = self.__obj.get(self.__cnt)
            self.__cnt += 1
            return result
        except IndexError:
            raise StopIteration

class Forecast(object):
    """
    A databox containing weather forecast data for a certain location and with
    a specific time interval
    """

    def __init__(self, interval, reception_time, location, weathers):
        """
        interval - the time granularity of the forecast, may be: '3h' or 'daily' 
        reception_time - GMT UNIXtime of data reception from the OWM API (long/int)
        location - the location relative to the forecast (Location)
        weather - a list of Weather objects (Weather)
        """
        assert type(interval) is str, "'interval' must be a str"
        if interval is not "3h" and interval is not "daily":
            raise ValueError("'interval' value must be '3h' or 'daily'")
        self.__interval = interval
        assert type(reception_time) is long or type(reception_time) is int, \
            "'reception_time' must be an long/int"
        if long(reception_time) < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self.__reception_time = long(reception_time)
        assert isinstance(location, Location), "'location' must be a Location object"
        self.__location = location
        assert isinstance(weathers, list), "'weathers' must be a list"
        for item in weathers:
            assert isinstance(item, Weather), "items in 'weathers' must be Weather objects"
        self.__weathers = weathers
    
    def __iter__(self):
        """Creates a ForecastIterator"""
        return ForecastIterator(self)
    
    def get(self, index):
        """
        Lookup method to be used by iterators
        
        index - the index of the Weather object in list (int)
        """
        return self.__weathers[index]
    
    def get_interval(self):
        """Returns the time granularity of the forecast"""
        return self.__interval
    
    def get_reception_time(self, timeformat='unix'):
        """
        Returns the GMT UNIX time of the forecast reception
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

    def get_weathers(self):
        """Returns a copy of the Weather objects list"""
        return list(self.__weathers)
    
    def count_weathers(self):
        """Returns how many Weather objects are in list"""
        return len(self.__weathers)
    
    def to_JSON(self):
        """Dumps object fields into a JSON formatted string"""
        
        #[item.to_JSON() for item in self.__weathers]
        
        d = { "interval": self.__interval,
              "reception_time": self.__reception_time, 
              "Location": loads(self.__location.to_JSON()),
              "weathers": loads("["+",".join([item.to_JSON() for item in self])+"]") 
              }
        return dumps(d)
    
    def to_XML(self):
        """Dumps object fields into a XML formatted string"""
        return '<Forecast><interval>%s</interval><reception_time>%s</reception_time>' \
            '%s<weathers>%s</weathers></Forecast>' % \
            (self.__interval, self.__reception_time, self.__location.to_XML(), \
                "".join([item.to_XML() for item in self]))
    
    def __str__(self):
        """Redefine __str__ hook for pretty-printing of Forecast instances"""
        return "[Forecast:\n"+str(self.__location)+"\n"+str(self.__weather)+"\n]"
    
    def __len__(self):
        """Redefine __len__ hook"""
        return self.count_weathers()
