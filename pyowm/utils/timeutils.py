#!/usr/bin/env python

"""
Module containing utility functions for time values generation/management
"""

from datetime import datetime, date, timedelta


def tomorrow(hour=None, minute=None):
    """
    Gives the ``datetime.datetime`` object corresponding to tomorrow. The
    default value for optional parameters is the current value of hour and
    minute. I.e: when called without specifying values for parameters, the
    resulting object will refer to the time = now + 24 hours; when called with
    only hour specified, the resulting object will refer to tomorrow at the
    specified hour and at the current minute.

    :param hour: the hour for tomorrow, in the format *0-23* (defaults to
        ``None``)
    :type hour: int
    :param minute: the minute for tomorrow, in the format *0-59* (defaults to
        ``None``)
    :type minute: int
    :returns: a ``datetime.datetime`` object
    :raises: *ValueError* when hour or minute have bad values

    """
    if hour is None:
        hour = datetime.now().hour
    if minute is None:
        minute = datetime.now().minute
    tomorrow_date = date.today() + timedelta(days=1)
    return datetime(tomorrow_date.year, tomorrow_date.month, tomorrow_date.day,
                    hour, minute, 0)


def yesterday(hour=None, minute=None):
    """
    Gives the ``datetime.datetime`` object corresponding to yesterday. The
    default value for optional parameters is the current value of hour and
    minute. I.e: when called without specifying values for parameters, the
    resulting object will refer to the time = now - 24 hours; when called with
    only hour specified, the resulting object will refer to yesterday at the
    specified hour and at the current minute.

    :param hour: the hour for yesterday, in the format *0-23* (defaults to
        ``None``)
    :type hour: int
    :param minute: the minute for yesterday, in the format *0-59* (defaults to
        ``None``)
    :type minute: int
    :returns: a ``datetime.datetime`` object
    :raises: *ValueError* when hour or minute have bad values
    """
    if hour is None:
        hour = datetime.now().hour
    if minute is None:
        minute = datetime.now().minute
    yesterday_date = date.today() + timedelta(days=-1)
    return datetime(yesterday_date.year, yesterday_date.month,
                    yesterday_date.day, hour, minute, 0)


def next_three_hours(date=None):
    """
    Gives the ``datetime.datetime`` object corresponding to the next three
    hours from now or from the specified ``datetime.datetime`` object.

    :param date: the date you want three hours to be added (if left ``None``,
        the current date and time will be used)
    :type date: ``datetime.datetime`` object
    :returns: a ``datetime.datetime`` object
    """
    if date is None:
        return datetime.now() + timedelta(hours=3)
    else:
        assert isinstance(date, datetime), __name__ + \
            ": 'date' must be a datetime.datetime object"
        return date + timedelta(hours=3)


def last_three_hours(date=None):
    """
    Gives the ``datetime.datetime`` object corresponding to last next three
    hours from now or from the specified ``datetime.datetime`` object.

    :param date: the date you want three hours to be subtracted (if left
        ``None``, the current date and time will be used)
    :type date: ``datetime.datetime`` object
    :returns: a ``datetime.datetime`` object
    """
    if date is None:
        return datetime.now() + timedelta(hours=-3)
    else:
        assert isinstance(date, datetime), __name__ + \
            ": 'date' must be a datetime.datetime object"
        return date + timedelta(hours=-3)
