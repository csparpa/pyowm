#!/usr/bin/env python
# -*- coding: utf-8 -*-

from calendar import timegm
from datetime import datetime, timedelta, timezone, tzinfo

ZERO = timedelta(0)


class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


def timeformat(timeobject, timeformat):
    """
    Formats the specified time object to the target format type.

    :param timeobject: the object conveying the time value
    :type timeobject: int, ``datetime.datetime`` or ISO8601-formatted
        string with pattern ``YYYY-MM-DD HH:MM:SS+00:00``
    :param timeformat: the target format for the time conversion. May be:
        '*unix*' (outputs an int UNIXtime), '*date*' (outputs a
        ``datetime.datetime`` object) or '*iso*' (outputs an ISO8601-formatted
        string with pattern ``YYYY-MM-DD HH:MM:SS+00:00``)
    :type timeformat: str
    :returns: the formatted time
    :raises: ValueError when unknown timeformat switches are provided or
        when negative time values are provided
    """
    if timeformat == "unix":
        return to_UNIXtime(timeobject)
    elif timeformat == "iso":
        return to_ISO8601(timeobject)
    elif timeformat == "date":
        return to_date(timeobject)
    else:
        raise ValueError("Invalid value for timeformat parameter")


def to_date(timeobject):
    """
    Returns the ``datetime.datetime`` object corresponding to the time value
    conveyed by the specified object, which can be either a UNIXtime, a
    ``datetime.datetime`` object or an ISO8601-formatted string in the format
    `YYYY-MM-DD HH:MM:SS+00:00``.

    :param timeobject: the object conveying the time value
    :type timeobject: int, ``datetime.datetime`` or ISO8601-formatted
        string
    :returns: a ``datetime.datetime`` object
    :raises: *TypeError* when bad argument types are provided, *ValueError*
        when negative UNIXtimes are provided
    """
    if isinstance(timeobject, int):
        if timeobject < 0:
            raise ValueError("The time value is a negative number")
        return datetime.fromtimestamp(timeobject, tz=timezone.utc)
    elif isinstance(timeobject, datetime):
        return timeobject.replace(microsecond=0)
    elif isinstance(timeobject, str):
        return datetime.fromisoformat(timeobject)
    else:
        raise TypeError('The time value must be expressed either by an int ' \
                         'UNIX time, a datetime.datetime object or an ' \
                         'ISO8601-formatted string')


def to_ISO8601(timeobject):
    """
    Returns the ISO8601-formatted string corresponding to the time value
    conveyed by the specified object, which can be either a UNIXtime, a
    ``datetime.datetime`` object or an ISO8601-formatted string in the format
    `YYYY-MM-DD HH:MM:SS+00:00``.

    :param timeobject: the object conveying the time value
    :type timeobject: int, ``datetime.datetime`` or ISO8601-formatted
        string
    :returns: an ISO8601-formatted string with pattern
        `YYYY-MM-DD HH:MM:SS+00:00``
    :raises: *TypeError* when bad argument types are provided, *ValueError*
        when negative UNIXtimes are provided
    """
    if isinstance(timeobject, int):
        if timeobject < 0:
            raise ValueError("The time value is a negative number")
        return datetime.fromtimestamp(timeobject, tz=timezone.utc).isoformat(' ', 'seconds')
    elif isinstance(timeobject, datetime):
        return timeobject.isoformat(' ', 'seconds')
    elif isinstance(timeobject, str):
        return timeobject
    else:
        raise TypeError('The time value must be expressed either by an int ' \
                         'UNIX time, a datetime.datetime object or an ' \
                         'ISO8601-formatted string')


def to_UNIXtime(timeobject):
    """
    Returns the UNIXtime corresponding to the time value conveyed by the
    specified object, which can be either a UNIXtime, a
    ``datetime.datetime`` object or an ISO8601-formatted string in the format
    `YYYY-MM-DD HH:MM:SS+00:00``.

    :param timeobject: the object conveying the time value
    :type timeobject: int, ``datetime.datetime`` or ISO8601-formatted
        string
    :returns: an int UNIXtime
    :raises: *TypeError* when bad argument types are provided, *ValueError*
        when negative UNIXtimes are provided
    """
    if isinstance(timeobject, int):
        if timeobject < 0:
            raise ValueError("The time value is a negative number")
        return timeobject
    elif isinstance(timeobject, datetime):
        return datetime_to_UNIXtime(timeobject)
    elif isinstance(timeobject, str):
        return ISO8601_to_UNIXtime(timeobject)
    else:
        raise TypeError('The time value must be expressed either by an int ' \
                         'UNIX time, a datetime.datetime object or an ' \
                         'ISO8601-formatted string')


def ISO8601_to_UNIXtime(iso):
    """
    Converts an ISO8601-formatted string in the format
    ``YYYY-MM-DD HH:MM:SS+00:00`` to the correspondent UNIXtime

    :param iso: the ISO8601-formatted string
    :type iso: string
    :returns: an int UNIXtime
    :raises: *TypeError* when bad argument types are provided, *ValueError*
        when the ISO8601 string is badly formatted

    """
    try:
        d = datetime.fromisoformat(iso)
    except ValueError:
        raise ValueError(__name__ + ": bad format for input ISO8601 string, ' \
                'should have been: YYYY-MM-DD HH:MM:SS+00:00")
    return datetime_to_UNIXtime(d)


def datetime_to_UNIXtime(date):
    """
    Converts a ``datetime.datetime`` object to its correspondent UNIXtime

    :param date: the ``datetime.datetime`` object
    :type date: ``datetime.datetime``
    :returns: an int UNIXtime
    :raises: *TypeError* when bad argument types are provided
    """
    return int(date.timestamp())
