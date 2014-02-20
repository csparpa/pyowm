#!/usr/bin/env python

"""
Module containing utility functions for time and temperature units conversion
"""

from datetime import datetime
from calendar import timegm

__KELVIN_OFFSET__ = 273.15
__FAHRENHEIT_OFFSET = 32.0
__FAHRENHEIT_DEGREE_SCALE = 1.8


def UNIXtime_to_ISO8601(unixtime):
    """
    Converts a UNIXtime to the correspondant ISO8601-formatted string
    The result string is in the format ``YYYY-MM-DD HH:MM:SS+00``

    :param unixtime: the UNIXtime
    :type unixtime: int/long
    :returns: an ISO8601-formatted string
    :raises: *TypeError* when bad argument types are provided, *ValueError* for
        negative values of UNIX time

    """
    if unixtime < 0:
        raise ValueError(__name__ + ": negative time values not allowed")
    return datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S+00')


def ISO8601_to_UNIXtime(iso):
    """
    Converts an ISO8601-formatted string in the format
    ``YYYY-MM-DD HH:MM:SS+00`` to the correspondant UNIXtime

    :param iso: the ISO8601-formatted string
    :type iso: string
    :returns: a long UNIXtime
    :raises: *TypeError* when bad argument types are provided, *ValueError*
        when the ISO8601 string is badly formatted

    """
    try:
        d = datetime.strptime(iso, '%Y-%m-%d %H:%M:%S+00')
    except ValueError:
        raise ValueError(__name__ + ": bad format for input ISO8601 string, ' \
            'should have been: YYYY-MM-DD HH:MM:SS+00")
    return datetime_to_UNIXtime(d)


def to_UNIXtime(timeobject):
    """
    Returns the UNIXtime corresponding to the time value conveyed by the
    specified object, which can be either a UNIXtime, a
    ``datetime.datetime`` object or an ISO8601-formatted string in the format
    `YYYY-MM-DD HH:MM:SS+00``.

    :param timeobject: the object conveying the time value
    :type timeobject: int/long, ``datetime.datetime`` or ISO8601-formatted
        string
    :returns: a long UNIXtime
    :raises: *TypeError* when bad argument types are provided, *ValueError*
        when negative UNIXtimes are provided
    """
    if isinstance(timeobject, (long, int)):
        if(timeobject < 0):
            raise ValueError("The time value is a negative number")
        return timeobject
    elif isinstance(timeobject, datetime):
        return datetime_to_UNIXtime(timeobject)
    elif isinstance(timeobject, str):
        return ISO8601_to_UNIXtime(timeobject)
    else:
        raise TypeError('The time value must be espressed either by a long ' \
                         'UNIX time, a datetime.datetime object or an ' \
                         'ISO8601-formatted string')


def datetime_to_UNIXtime(date):
    """
    Converts a ``datetime.datetime`` object to its correspondent UNIXtime

    :param date: the ``datetime.datetime`` object
    :type date: ``datetime.datetime``
    :returns: a long UNIXtime
    :raises: *TypeError* when bad argument types are provided
    """
    return timegm(date.timetuple())


def kelvin_to_celsius(kelvintemp):
    """
    Converts a numeric temperature from Kelvin degrees to Celsius degrees

    :param kelvintemp: the Kelvin temperature
    :type kelvintemp: int/long/float
    :returns: the float Celsius temperature
    :raises: *TypeError* when bad argument types are provided

    """
    if kelvintemp < 0:
        raise ValueError(__name__ + ": negative temperature values not allowed")
    celsiustemp = kelvintemp - __KELVIN_OFFSET__
    return float("{0:.2f}".format(celsiustemp))


def kelvin_to_fahrenheit(kelvintemp):
    """
    Converts a numeric temperature from Kelvin degrees to Fahrenheit degrees

    :param kelvintemp: the Kelvin temperature
    :type kelvintemp: int/long/float
    :returns: the float Fahrenheit temperature

    :raises: *TypeError* when bad argument types are provided
    """
    if kelvintemp < 0:
        raise ValueError(__name__ + ": negative temperature values not allowed")
    fahrenheittemp = (kelvintemp - __KELVIN_OFFSET__) * \
        __FAHRENHEIT_DEGREE_SCALE + __FAHRENHEIT_OFFSET
    return float("{0:.2f}".format(fahrenheittemp))
