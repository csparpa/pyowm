#!/usr/bin/env python

"""
Weather observation classes and data structures.
"""

class Observation(object):
    """
    A databox containing weather data observed in a certain location and at a
    certain time.
    """

    def __init__(self, receptionTime, location, weather):
        """
        receptionTime - GMT UNIXtime of data reception from the OWM API (int)
        location - the location relative to this observation (Lcation)
        weather - the observed weather data (Weather)
        """
        raise Exception('Not yet implemented')