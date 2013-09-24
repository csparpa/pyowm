#!/usr/bin/env python

"""
Module containing weather forecast classes and data structures.
"""

from json import loads, dumps
from location import Location
from weather import Weather
from utils import converter

class ForecastIterator(object):
    """
    Iterator over the list of *Weather* objects encapsulated in a *Forecast*
    class instance
    
    :param obj: the iterable object
    :type obj: object    
    :returns:  a *ForecastIterator* instance
    
    """
    def __init__(self, obj):
        self.__obj = obj
        self.__cnt = 0
   
    def __iter__(self):
        """
        When called on a Forecast object, returns an instance of the iterator
        
        :returns: a *ForecastIterator* instance
        """
        return self

    def next(self):
        """
        Returns the next *Weather* item
        
        :returns: the next *Weather* item
        
        """
        try:
            result = self.__obj.get(self.__cnt)
            self.__cnt += 1
            return result
        except IndexError:
            raise StopIteration

class Forecast(object):
    """
    A class encapsulating weather forecast data for a certain location and 
    relative to a specific time interval (forecast for every three hours or
    for every day)
    
    :param interval: the time granularity of the forecast. May be: *'3h'* for three
        hours forecast or *'daily'* for daily ones
    :type interval: str 
    :param reception_time: GMT UNIXtime of the forecast reception from the OWM web API
    :type reception_time: long/int
    :param location: the *Location* object relative to the forecast
    :type location: Location
    :param weathers: the list of *Weather* objects composing the forecast
    :type weathers: list
    :returns:  a *Forecast* instance
    :raises: *ValueError* when negative values are provided 
    
    """

    def __init__(self, interval, reception_time, location, weathers):
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
            assert isinstance(item, Weather), "items in 'weathers' must be of type Weather"
        self.__weathers = weathers
    
    def __iter__(self):
        """
        Creates a *ForecastIterator* instance
        
        :returns: a *ForecastIterator* instance
        """
        return ForecastIterator(self)
    
    def get(self, index):
        """
        Lookups up into the *Weather* items list for the item at the specified 
        index
        
        :param index: the index of the *Weather* object in the list
        :type index: int
        :returns: a *Weather* object
        """
        return self.__weathers[index]
    
    def get_interval(self):
        """
        Returns the time granularity of the forecast
        
        :returns: str
        
        """
        return self.__interval
    
    def get_reception_time(self, timeformat='unix'):
        """Returns the GMT time telling when the forecast was received 
            from the OWM web API
    
        :param timeformat: the format for the time value. May be: 
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: a long or a str
        :raises: ValueError
    
        """
        if timeformat == 'unix':
            return self.__reception_time
        if timeformat == 'iso':
            return converter.UNIXtime_to_ISO8601(self.__reception_time)
        else:
            raise ValueError("Invalid value for parameter 'format'")

    def get_location(self):
        """
        Returns the Location object relative to the forecast
        
        :returns: a *Location* object
        
        """
        return self.__location

    def get_weathers(self):
        """
        Returns a copy of the *Weather* objects list composing the forecast
        
        :returns: a list of *Weather* objects
        
        """
        return list(self.__weathers)
    
    def count_weathers(self):
        """
        Tells how many *Weather* items compose the forecast
        
        :returns: the *Weather* objects total
        
        """
        return len(self.__weathers)
    
    def to_JSON(self):
        """Dumps object fields into a JSON formatted string
        
        :returns: the JSON string
        
        """
        d = { "interval": self.__interval,
              "reception_time": self.__reception_time, 
              "Location": loads(self.__location.to_JSON()),
              "weathers": loads("["+",".join([item.to_JSON() for item in self])+"]") 
              }
        return dumps(d)
    
    def to_XML(self):
        """Dumps object fields into a XML formatted string
        
        :returns: the XML string
        
        """
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
