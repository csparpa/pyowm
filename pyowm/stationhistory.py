#!/usr/bin/env python

"""
Module containing classes and datastructures related to meteostation history data  
"""

from os import linesep
from json import dumps
from utils import converter, xmlutils

class StationHistory(object):

    """
    A class representing historic weather measurements collected by a meteostation.
    Three types of historic meteostation data can be obtained by the OWM web API:
    ticks (one data chunk per minute) data, hourly and daily data.
       
    :param station_ID: the numeric ID of the meteostation
    :type station_ID: int
    :param interval: the time granularity of the meteostation data history, must
        be among 'tick','hour' and 'day'
    :type interval: str
    :param reception_time: GMT UNIXtime of the data reception from the OWM web API
    :type reception_time: long/int
    :param measurements: a dictionary containing raw weather measurements
    :type measurements: dict
    :returns: a *StationHistory* instance
    :raises: *ValueError* when the supplied value for reception time is negative
        or when bad values for history interval are given
    """
    
    def __init__(self, station_ID, interval, reception_time, measurements):
        assert isinstance(station_ID, int), "'station_ID' must be int"
        self.__station_ID = station_ID
        assert type(interval) is str, "'interval' must be a str"
        if interval is not "tick" and interval is not "hour" and interval is not "day":
            raise ValueError("'interval' value must be 'tick', 'hour' or 'day'")
        self.__interval = interval
        assert isinstance(reception_time, long) or isinstance(reception_time, int), \
            "'reception_time' must be an long/int"
        if long(reception_time) < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self.__reception_time = reception_time
        assert isinstance(measurements, dict), "'measurements' must be a dict"
        self.__measurements = measurements
        
    def get_station_ID(self):
        """
        Returns the ID of the meteostation
        
        :returns: the int station ID
        
        """
        return self.__station_ID
    
    def get_interval(self):
        """
        Returns the interval of the meteostation history data
        
        :returns: the int interval
        
        """
        return self.__interval
    
    def get_measurements(self):
        """
        Returns the measurements of the meteostation
        
        :returns: the dict containing the meteostation's measurements
        
        """
        return self.__measurements
    
    def get_reception_time(self, timeformat='unix'):
        """Returns the GMT time telling when the meteostation history data was
           received from the OWM web API

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


    def temperature_serie(self, unit='kelvin'):
        """Returns the temperature time series relative to the meteostation, in 
        the form of a list of tuples, each one containing the couple timestamp-value
    
        :param unit: the unit of measure for the temperature values. May be among: 
            '*kelvin*' (default), '*celsius*' or '*fahrenheit*'
        :type unit: str
        :returns: a list of tuples
        :raises: ValueError when invalid values are provided for the unit of 
            measure
    
        """
        if unit not in ('kelvin','celsius','fahrenheit'):
            raise ValueError("Invalid value for parameter 'unit'")
        result = []
        for timestamp in self.__measurements:
            t = self.__measurements[timestamp]['temperature']
            if unit == 'kelvin':
                temp = t
            if unit == 'celsius':
                temp = converter.kelvin_to_celsius(t)
            if unit == 'fahrenheit':
                temp = converter.kelvin_to_fahrenheit(t)
            result.append((timestamp, temp))
        return result
    
    def humidity_serie(self):
        """Returns the humidity time series relative to the meteostation, in 
        the form of a list of tuples, each one containing the couple timestamp-value

        :returns: a list of tuples
    
        """
        return [(timestamp, self.__measurements[timestamp]['humidity']) \
                for timestamp in self.__measurements]
        
    def pressure_serie(self):
        """Returns the atmospheric pressure time series relative to the 
        meteostation, in the form of a list of tuples, each one containing the
        couple timestamp-value

        :returns: a list of tuples
    
        """
        return [(timestamp, self.__measurements[timestamp]['pressure']) \
                for timestamp in self.__measurements]
        
    def rain_serie(self):
        """Returns the precipitation time series relative to the 
        meteostation, in the form of a list of tuples, each one containing the
        couple timestamp-value

        :returns: a list of tuples
    
        """
        return [(timestamp, self.__measurements[timestamp]['rain']) \
                for timestamp in self.__measurements]
        
    def wind_serie(self):
        """Returns the wind speed time series relative to the 
        meteostation, in the form of a list of tuples, each one containing the
        couple timestamp-value

        :returns: a list of tuples
    
        """
        return [(timestamp, self.__measurements[timestamp]['wind']) \
                for timestamp in self.__measurements]

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string
        
        :returns: the JSON string
        
        """
        d = { "station_ID": self.__station_ID,
              "interval": self.__interval,
              "reception_time": self.__reception_time,
              "measurements": self.__measurements 
              }
        return dumps(d)
    
    def to_XML(self):
        """Dumps object fields into a XML formatted string
        
        :returns: the XML string
        
        """
        return '<StationHistory><station_id>%s</station_id><interval>%s</interval>' \
            '<reception_time>%s</reception_time><measurements>%s</measurements>' \
            '</StationHistory>' % \
            (self.__station_ID, self.__interval, self.__reception_time,
             "".join([ "<"+str(item)+">"+xmlutils.dict_to_XML(self.__measurements[item])+ \
                      "</"+str(item)+">" for item in self.__measurements]))
    
    def __str__(self):
        """Redefine __str__ hook for pretty-printing of StationHistory instances"""
        return '[StationHistory: station_ID=%s reception_time= data='+linesep + \
            str(self.__measurements) % self.__station_ID