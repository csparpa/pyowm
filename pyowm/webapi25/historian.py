#!/usr/bin/env python

"""
Module containing weather history abstraction classes and data structures.
"""

from pyowm.utils import converter


class Historian(object):
    """
    A class providing convenience methods for manipulating meteostation weather
    history data. The class encapsulates a *StationHistory* instance and
    provides abstractions on the top of it in order to let programmers exploit
    meteostation weather history data in a human-friendly fashion

    :param station_history: a *StationHistory* instance
    :type station_history: *StationHistory*
    :returns: a *Historian* instance
    """

    def __init__(self, station_history):
        self.__station_history = station_history

    def get_station_history(self):
        """
        Returns the *StationHistory* instance

        :returns: the *StationHistory* instance
        """
        return self.__station_history

    def temperature_series(self, unit='kelvin'):
        """Returns the temperature time series relative to the meteostation, in
        the form of a list of tuples, each one containing the couple
        timestamp-value

        :param unit: the unit of measure for the temperature values. May be
            among: '*kelvin*' (default), '*celsius*' or '*fahrenheit*'
        :type unit: str
        :returns: a list of tuples
        :raises: ValueError when invalid values are provided for the unit of
            measure
        """
        if unit not in ('kelvin', 'celsius', 'fahrenheit'):
            raise ValueError("Invalid value for parameter 'unit'")
        result = []
        for tstamp in self.__station_history.get_measurements():
            t = self.__station_history.get_measurements()[tstamp]['temperature']
            if unit == 'kelvin':
                temp = t
            if unit == 'celsius':
                temp = converter.kelvin_to_celsius(t)
            if unit == 'fahrenheit':
                temp = converter.kelvin_to_fahrenheit(t)
            result.append((tstamp, temp))
        return result

    def humidity_series(self):
        """Returns the humidity time series relative to the meteostation, in
        the form of a list of tuples, each one containing the couple
        timestamp-value

        :returns: a list of tuples
        """
        return [(tstamp, \
                self.__station_history.get_measurements()[tstamp]['humidity']) \
                for tstamp in self.__station_history.get_measurements()]

    def pressure_series(self):
        """Returns the atmospheric pressure time series relative to the
        meteostation, in the form of a list of tuples, each one containing the
        couple timestamp-value

        :returns: a list of tuples
        """
        return [(tstamp, \
                self.__station_history.get_measurements()[tstamp]['pressure']) \
                for tstamp in self.__station_history.get_measurements()]

    def rain_series(self):
        """Returns the precipitation time series relative to the
        meteostation, in the form of a list of tuples, each one containing the
        couple timestamp-value

        :returns: a list of tuples
        """
        return [(tstamp, \
                self.__station_history.get_measurements()[tstamp]['rain']) \
                for tstamp in self.__station_history.get_measurements()]

    def wind_series(self):
        """Returns the wind speed time series relative to the
        meteostation, in the form of a list of tuples, each one containing the
        couple timestamp-value

        :returns: a list of tuples
        """
        return [(timestamp, \
                self.__station_history.get_measurements()[timestamp]['wind']) \
                for timestamp in self.__station_history.get_measurements()]

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)
