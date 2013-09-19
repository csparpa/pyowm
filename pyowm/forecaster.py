#!/usr/bin/env python

"""
Weather forecast abstraction classes and data structures.
"""

from forecast import Forecast
from utils import converter

class Forecaster(object):
    """
    A class providing convenience methods for manipulating weather forecast data
    """

    def __init__(self, forecast):
        """
        forecast - a Forecast object
        """
        assert isinstance(forecast, Forecast), "'forecast' must be a Forecast object"
        self.__forecast = forecast
        
    def get_forecast(self):
        """Returns the Forecast object"""
        return self.__forecast
        
        
    def when_starts(self, timeformat='unix'):
        """
        Returns the GMT time of the most ancient item of the forecast
            format - how to format the result:
                unix (default) - returns a long
                iso - returns a ISO 8601-formatted str
        """
        start_coverage = min([item.get_reference_time() for item in self.__forecast])
        if timeformat == 'unix':
            return start_coverage
        if timeformat == 'iso':
            return converter.unix_to_ISO8601(start_coverage)
        else:
            raise ValueError("Invalid value for parameter 'format'")
        
    def when_ends(self, timeformat='unix'):
        """
        Returns the GMT time of the most recent item of the forecast
            format - how to format the result:
                unix (default) - returns a long
                iso - returns a ISO 8601-formatted str
        """
        end_coverage = max([item.get_reference_time() for item in self.__forecast])
        if timeformat == 'unix':
            return end_coverage
        if timeformat == 'iso':
            return converter.unix_to_ISO8601(end_coverage)
        else:
            raise ValueError("Invalid value for parameter 'format'")
    
    def check_status(self, words, weathers):
        """
        Checks if one or more words in a given list is contained into the
        detailed weather statuses of the Forecast objects in the given list
        """
        for item in weathers:
            status = item.get_detailed_status().lower()
            for word in words:
                if word in status:
                    return True
        return False
    
    def will_have_rain(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to rain
        """
        return self.check_status(['rain','drizzle'], self.__forecast.get_weathers())
        
    def will_have_sun(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to sun
        """
        return self.check_status(['clear'], self.__forecast.get_weathers())
    
    def will_have_fog(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to fog
        """
        return self.check_status(['fog','haze','mist'], 
                                   self.__forecast.get_weathers())
        
    def will_have_snow(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to sun
        """
        return self.check_status(['snow','sleet'],
                                   self.__forecast.get_weathers())