#!/usr/bin/env python

"""
Module containing utility functions for time values generation/management
"""

from datetime import datetime, date, timedelta

def tomorrow(hour=datetime.now().hour, minute=datetime.now().minute):
    """
    Gives the ``datetime.datetime`` object corresponding to tomorrow. The default
    value for optional parameters is the current value of hour and minute. I.e: 
    when called without specifying values for parameters, the resulting object
    will refer to the time = now + 24 hours; when called with only hour specified,
    the resulting object will refer to the tomorrow at the specified hour and at
    the current minute. 
    
    :param hour: the hour for tomorrow, in the format *0-23* (defaults to 
        ``None``)
    :type hour: int
    :param minute: the minute for tomorrow, in the format *0-59* (defaults to 
        ``None``)
    :type minute: int
    :returns: a ``datetime.datetime`` object
    :raises: *ValueError* when hour or minute have bad values
        
    """
    tomorrow_date = date.today() + timedelta(days=1) 
    return datetime(tomorrow_date.year, tomorrow_date.month, tomorrow_date.day,
                    hour, minute, 0)