#!/usr/bin/env python

"""
Time and units conversion functions
"""

from datetime import datetime
from calendar import timegm

__KELVIN_OFFSET__ = 273.15
__FAHRENHEIT_OFFSET = 32.0
__FAHRENHEIT_DEGREE_SCALE = 1.8

def unix_to_ISO8601(unixtime):
    """
    Converts a int/long UNIX time to the correspondant ISO8601-formatted string
    The result is in the format: [YYYY]-[MM]-[DD] [HH]:[MM]:[SS]+00
    
    unixtime - the UNIX time (long)
    """
    if isinstance(unixtime, (long,int)):
        if unixtime < 0:
            raise ValueError(__name__+": negative time values not allowed")
        return datetime.utcfromtimestamp(unixtime). \
            strftime('%Y-%m-%d %H:%M:%S+00')
    else:
        raise TypeError(__name__+": bad argument type")
    
def ISO8601_to_unix(iso):
    """
    Converts a ISO8601-formatted string into a long UNIX time
    The supposed format for the string is [YYYY]-[MM]-[DD] [HH]:[MM]:[SS]+00
    
    iso - the ISO8601-formatted str
    """
    if isinstance(iso, str):
        try:
            d = datetime.strptime(iso,'%Y-%m-%d %H:%M:%S+00')
        except ValueError:
            raise ValueError(__name__+": bad format for input ISO8601 string")
        return datetime_to_unix(d)
    else:
        raise TypeError(__name__+": bad argument type")
    
def datetime_to_unix(date):
    """
    Converts a Python datetime.datetime object to the correspondant UNIX time
    
    date - the datetime.datetime object to be converted
    """
    if isinstance(date, datetime):
        return timegm(date.timetuple())
    else:
        raise TypeError(__name__+": bad argument type")

def kelvin_to_celsius(kelvintemp):
    """
    Converts a numeric temperature from Kelvin degrees to Celsius degrees
    
    kelvintemp - the Kelvin temperature (int/long/float)
    """
    if isinstance(kelvintemp, (long,int,float)):
        if kelvintemp < 0:
            raise ValueError(__name__+": negative temperature values not allowed")
        celsiustemp = kelvintemp - __KELVIN_OFFSET__
        return float("{0:.2f}".format(celsiustemp))
    else:
        raise TypeError(__name__+": bad argument type")

def kelvin_to_fahrenheit(kelvintemp):
    """
    Converts a numeric temperature from Kelvin degrees to Fahrenheit degrees
    
    kelvintemp - the Kelvin temperature (int/long/float)
    """
    if isinstance(kelvintemp, (long,int,float)):
        if kelvintemp < 0:
            raise ValueError(__name__+": negative temperature values not allowed")
        fahrenheittemp = (kelvintemp - __KELVIN_OFFSET__)*__FAHRENHEIT_DEGREE_SCALE \
            + __FAHRENHEIT_OFFSET
        return float("{0:.2f}".format(fahrenheittemp))
    else:
        raise TypeError(__name__+": bad argument type")