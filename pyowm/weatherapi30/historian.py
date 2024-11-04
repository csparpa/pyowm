#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter
from pyowm.utils import measurables


class Historian:
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
        self.station_history = station_history

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
        for tstamp in self.station_history.measurements:
            t = self.station_history.measurements[tstamp]['temperature']
            if unit == 'kelvin':
                temp = t
            elif unit == 'celsius':
                temp = measurables.kelvin_to_celsius(t)
            else:
                temp = measurables.kelvin_to_fahrenheit(t)
            result.append((tstamp, temp))
        return result

    def humidity_series(self):
        """Returns the humidity time series relative to the meteostation, in
        the form of a list of tuples, each one containing the couple
        timestamp-value

        :returns: a list of tuples
        """
        return [(tstamp, \
                self.station_history.measurements[tstamp]['humidity']) \
                for tstamp in self.station_history.measurements]

    def pressure_series(self):
        """Returns the atmospheric pressure time series relative to the
        meteostation, in the form of a list of tuples, each one containing the
        couple timestamp-value

        :returns: a list of tuples
        """
        return [(tstamp, \
                self.station_history.measurements[tstamp]['pressure']) \
                for tstamp in self.station_history.measurements]

    def rain_series(self):
        """Returns the precipitation time series relative to the
        meteostation, in the form of a list of tuples, each one containing the
        couple timestamp-value

        :returns: a list of tuples
        """
        return [(tstamp, \
                self.station_history.measurements[tstamp]['rain']) \
                for tstamp in self.station_history.measurements]

    def wind_series(self):
        """Returns the wind speed time series relative to the
        meteostation, in the form of a list of tuples, each one containing the
        couple timestamp-value

        :returns: a list of tuples
        """
        return [(timestamp, \
                self.station_history.measurements[timestamp]['wind']) \
                for timestamp in self.station_history.measurements]

    def max_temperature(self,  unit='kelvin'):
        """Returns a tuple containing the max value in the temperature
        series preceded by its timestamp
        
        :param unit: the unit of measure for the temperature values. May be
            among: '*kelvin*' (default), '*celsius*' or '*fahrenheit*'
        :type unit: str
        :returns: a tuple
        :raises: ValueError when invalid values are provided for the unit of
            measure or the measurement series is empty
        """
        if unit not in ('kelvin', 'celsius', 'fahrenheit'):
            raise ValueError("Invalid value for parameter 'unit'")
        maximum = max(self._purge_none_samples(self.temperature_series()),
                   key=itemgetter(1))
        if unit == 'kelvin':
            return maximum
        elif unit == 'celsius':
            return (maximum[0], measurables.kelvin_to_celsius(maximum[1]))
        else:
            return (maximum[0], measurables.kelvin_to_fahrenheit(maximum[1]))
        
    def min_temperature(self, unit='kelvin'):
        """Returns a tuple containing the min value in the temperature
        series preceded by its timestamp
        
        :param unit: the unit of measure for the temperature values. May be
            among: '*kelvin*' (default), '*celsius*' or '*fahrenheit*'
        :type unit: str
        :returns: a tuple
        :raises: ValueError when invalid values are provided for the unit of
            measure or the measurement series is empty
        """
        if unit not in ('kelvin', 'celsius', 'fahrenheit'):
            raise ValueError("Invalid value for parameter 'unit'")
        minimum = min(self._purge_none_samples(self.temperature_series()),
                   key=itemgetter(1))
        if unit == 'kelvin':
            return minimum
        elif unit == 'celsius':
            return (minimum[0], measurables.kelvin_to_celsius(minimum[1]))
        else:
            return (minimum[0], measurables.kelvin_to_fahrenheit(minimum[1]))
        
    def average_temperature(self, unit='kelvin'):
        """Returns the average value in the temperature series
        
        :param unit: the unit of measure for the temperature values. May be
            among: '*kelvin*' (default), '*celsius*' or '*fahrenheit*'
        :type unit: str
        :returns: a float
        :raises: ValueError when invalid values are provided for the unit of
            measure or the measurement series is empty
        """
        if unit not in ('kelvin', 'celsius', 'fahrenheit'):
            raise ValueError("Invalid value for parameter 'unit'")
        average = self._average(self._purge_none_samples(
                                                  self.temperature_series()))
        if unit == 'kelvin':
            return average
        elif unit == 'celsius':
            return measurables.kelvin_to_celsius(average)
        else:
            return measurables.kelvin_to_fahrenheit(average)
    
    def max_humidity(self):
        """Returns a tuple containing the max value in the humidity
        series preceded by its timestamp

        :returns: a tuple
        :raises: ValueError when the measurement series is empty
        """
        return max(self._purge_none_samples(self.humidity_series()),
                   key=itemgetter(1))
        
    def min_humidity(self):
        """Returns a tuple containing the min value in the humidity
        series preceded by its timestamp

        :returns: a tuple
        :raises: ValueError when the measurement series is empty
        """
        return min(self._purge_none_samples(self.humidity_series()),
                   key=itemgetter(1))

    def average_humidity(self):
        """Returns the average value in the humidity series

        :returns: a float
        :raises: ValueError when the measurement series is empty
        """
        return self._average(self._purge_none_samples(
                                                  self.humidity_series()))

    def max_pressure(self):
        """Returns a tuple containing the max value in the pressure
        series preceded by its timestamp

        :returns: a tuple
        :raises: ValueError when the measurement series is empty
        """
        return max(self._purge_none_samples(self.pressure_series()),
                   key=itemgetter(1))
        
    def min_pressure(self):
        """Returns a tuple containing the min value in the pressure
        series preceded by its timestamp

        :returns: a tuple
        :raises: ValueError when the measurement series is empty
        """
        return min(self._purge_none_samples(self.pressure_series()),
                   key=itemgetter(1))

    def average_pressure(self):
        """Returns the average value in the pressure series

        :returns: a float
        :raises: ValueError when the measurement series is empty
        """
        return self._average(self._purge_none_samples(
                                                  self.pressure_series()))

    def max_rain(self):
        """Returns a tuple containing the max value in the rain
        series preceded by its timestamp

        :returns: a tuple
        :raises: ValueError when the measurement series is empty
        """
        return max(self._purge_none_samples(self.rain_series()),
                   key=lambda item:item[1])
        
    def min_rain(self):
        """Returns a tuple containing the min value in the rain
        series preceded by its timestamp

        :returns: a tuple
        :raises: ValueError when the measurement series is empty
        """
        return min(self._purge_none_samples(self.rain_series()),
                   key=itemgetter(1))

    def average_rain(self):
        """Returns the average value in the rain series

        :returns: a float
        :raises: ValueError when the measurement series is empty
        """
        return self._average(self._purge_none_samples(
                                                  self.rain_series()))

    def _purge_none_samples(self, list_of_tuples):
        return [item for item in list_of_tuples if item[1] is not None]

    def _average(self, list_of_tuples):
        if len(list_of_tuples) == 0:
            raise ValueError("Empty data series: impossible to compute average")
        total = 0.0
        for tpl in list_of_tuples:
            total += tpl[1]
        return total/len(list_of_tuples)

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)
