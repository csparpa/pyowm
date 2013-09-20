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
    
    # Utility methods
    def status_matches_any(self, word_list, weather):
        """
        Checks if one or more words in a given list is contained into the
        detailed weather statuses of a Weather object
        
        word_list - list of str
        weather - Weather object
        """
        detailed_status = weather.get_detailed_status().lower()
        for word in word_list:
            if word in detailed_status:
                return True
        return False
    
    def statuses_match_any(self, word_list, weathers):
        """
        Checks if one or more of the detailed statuses of the Weather objects 
        into the given list contain at least one of the words in the given word 
        list
        
        word_list - list of str
        weathers - list of Weather objects
        """
        for weather in weathers:
            if self.status_matches_any(word_list, weather):
                return True
        return False
            
    def filter_by_matching_statuses(self, word_list, weathers):
        """
        Returns a sublist of the given list of Weather objects, whose items
        have at least one of the words in the given list as part of their
        detailed statuses
        
        word_list - list of str
        weathers - list of Weather objects
        """
        result = []
        for weather in weathers:
            if self.status_matches_any(word_list, weather):
                result.append(weather)
        return result
    
    
    # Convenience methods
    def will_have_rain(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to rain/drizzle
        """
        return self.statuses_match_any(['rain','drizzle'], self.__forecast.get_weathers())
        
    def will_have_sun(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to sun
        """
        return self.statuses_match_any(['clear'], self.__forecast.get_weathers())
    
    def will_have_fog(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to fog/haze/mist
        """
        return self.statuses_match_any(['fog','haze','mist'], 
                                   self.__forecast.get_weathers())
        
    def will_have_clouds(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to clouds
        """
        return self.statuses_match_any(['clouds'], 
                                   self.__forecast.get_weathers())
        
    def will_have_snow(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to snow
        """
        return self.statuses_match_any(['snow','sleet'],
                                   self.__forecast.get_weathers())
        
    def when_rain(self):
        """
        Returns a sublist of the Weather objects list in the forecast, which
        only contains items having rain/drizzle as weather condition.
        """
        return self.filter_by_matching_statuses(['rain', 'drizzle'],
                                           self.__forecast.get_weathers())
    
    def when_sun(self):
        """
        Returns a sublist of the Weather objects list in the forecast, which
        only contains items having clear as weather condition.
        """
        return self.filter_by_matching_statuses(['clear'],
                                           self.__forecast.get_weathers())
    
    def when_fog(self):
        """
        Returns a sublist of the Weather objects list in the forecast, which
        only contains items having fog/haze/mist as weather condition.
        """
        return self.filter_by_matching_statuses(['fog','haze','mist'],
                                           self.__forecast.get_weathers())
        
    def when_clouds(self):
        """
        Returns a sublist of the Weather objects list in the forecast, which
        only contains items having clouds as weather condition.
        """
        return self.filter_by_matching_statuses(['clouds'],
                                           self.__forecast.get_weathers())
    
    def when_snow(self):
        """
        Returns a sublist of the Weather objects list in the forecast, which
        only contains items having snow/sleet as weather condition.
        """
        return self.filter_by_matching_statuses(['snow', 'sleet'],
                                           self.__forecast.get_weathers())
        

        