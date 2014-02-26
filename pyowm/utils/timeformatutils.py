#!/usr/bin/env python

"""
Module containing utility functions for time formats conversion
"""

from datetime import datetime
from calendar import timegm


def to_ISO8601(timeobject):
    """
    Returns the ISO8601-formatted string corresponding to the time value
    conveyed by the specified object, which can be either a UNIXtime, a
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
        if timeobject < 0:
            raise ValueError("The time value is a negative number")
        return datetime.utcfromtimestamp(timeobject). \
            strftime('%Y-%m-%d %H:%M:%S+00')
    elif isinstance(timeobject, datetime):
        return timeobject.strftime('%Y-%m-%d %H:%M:%S+00')
    elif isinstance(timeobject, str):
        return timeobject
    else:
        raise TypeError('The time value must be espressed either by a long ' \
                         'UNIX time, a datetime.datetime object or an ' \
                         'ISO8601-formatted string')


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
        if timeobject < 0:
            raise ValueError("The time value is a negative number")
        return timeobject
    elif isinstance(timeobject, datetime):
        return _datetime_to_UNIXtime(timeobject)
    elif isinstance(timeobject, str):
        return _ISO8601_to_UNIXtime(timeobject)
    else:
        raise TypeError('The time value must be espressed either by a long ' \
                         'UNIX time, a datetime.datetime object or an ' \
                         'ISO8601-formatted string')


def _ISO8601_to_UNIXtime(iso):
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
    return _datetime_to_UNIXtime(d)


def _datetime_to_UNIXtime(date):
    """
    Converts a ``datetime.datetime`` object to its correspondent UNIXtime

    :param date: the ``datetime.datetime`` object
    :type date: ``datetime.datetime``
    :returns: a long UNIXtime
    :raises: *TypeError* when bad argument types are provided
    """
    return timegm(date.timetuple())
