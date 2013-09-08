#!/usr/bin/env python

"""
Time and units conversion functions
"""

from datetime import datetime

__KELVIN_OFFSET__ = 273.15
__FAHRENHEIT_OFFSET = 32.0
__FAHRENHEIT_DEGREE_SCALE = 1.8

def unix_to_ISO8601(unixtime):
    """
    Converts a int/long UNIX time to the correspondant ISO 8601 string
    The result is in the format: [YYYY]-[MM]-[DD] [HH]:[MM]:[SS]+00
    """
    if isinstance(unixtime, (long,int)):
        if unixtime < 0:
            raise ValueError(__name__+": negative time values not allowed")
        return datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S+00')
    else:
        raise TypeError(__name__+": unable to convert to ISO 8601 string")

def kelvin_to_celsius(kelvintemp):
    """
    Converts a numeric temperature from Kelvin degrees to Celsius degrees
    """
    if isinstance(kelvintemp, (long,int,float)):
        if kelvintemp < 0:
            raise ValueError(__name__+": negative temperature values not allowed")
        celsiustemp = kelvintemp - __KELVIN_OFFSET__
        return float("{0:.2f}".format(celsiustemp))
    else:
        raise TypeError(__name__+": unable to convert from Kelvin to Celsius degrees")

def kelvin_to_fahrenheit(kelvintemp):
    """
    Converts a numeric temperature from Kelvin degrees to Fahrenheit degrees
    """
    if isinstance(kelvintemp, (long,int,float)):
        if kelvintemp < 0:
            raise ValueError(__name__+": negative temperature values not allowed")
        fahrenheittemp = (kelvintemp - __KELVIN_OFFSET__)*__FAHRENHEIT_DEGREE_SCALE + __FAHRENHEIT_OFFSET
        return float("{0:.2f}".format(fahrenheittemp))
    else:
        raise TypeError(__name__+": unable to convert from Kelvin to Fahrenheit degrees")