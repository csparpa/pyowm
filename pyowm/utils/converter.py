#!/usr/bin/env python

"""
Time and units conversion functions
"""

from datetime import datetime

def unix_to_ISO8601(unixtime):
    """
    Converts a int/long UNIX time to the correspondant ISO 8601 string
    The result is in the format: [YYYY]-[MM]-[DD] [HH]:[MM]:[SS]+00
    """
    if type(unixtime) is long or type(unixtime) is int: 
        return datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S+00')
    else:
        raise ValueError(__name__+": unable to convert to ISO 8601 string")