#!/usr/bin/env python

"""
Weather forecast abstraction classes and data structures.
"""

from datetime import datetime
from forecast import Forecast
from utils import converter, weatherutils
from constants import CLOUDS_KEYWORDS, FOG_KEYWORDS, RAIN_KEYWORDS, \
    SNOW_KEYWORDS, SUN_KEYWORDS

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
    
    def will_have_rain(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to rain/drizzle
        """
        return weatherutils.statuses_match_any(RAIN_KEYWORDS, 
                                               self.__forecast.get_weathers())
        
    def will_have_sun(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to sun
        """
        return weatherutils.statuses_match_any(SUN_KEYWORDS, 
                                               self.__forecast.get_weathers())
    
    def will_have_fog(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to fog/haze/mist
        """
        return weatherutils.statuses_match_any(FOG_KEYWORDS, 
                                   self.__forecast.get_weathers())
        
    def will_have_clouds(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to clouds
        """
        return weatherutils.statuses_match_any(CLOUDS_KEYWORDS, 
                                   self.__forecast.get_weathers())
        
    def will_have_snow(self):
        """
        Returns a boolean indicating if during the forecast coverage exist one
        or more items related to snow
        """
        return weatherutils.statuses_match_any(SNOW_KEYWORDS,
                                   self.__forecast.get_weathers())
        
    def when_rain(self):
        """
        Returns a sublist of the Weather objects list in the forecast, which
        only contains items having rain/drizzle as weather condition.
        """
        return weatherutils.filter_by_matching_statuses(RAIN_KEYWORDS,
                                           self.__forecast.get_weathers())
    
    def when_sun(self):
        """
        Returns a sublist of the Weather objects list in the forecast, which
        only contains items having clear as weather condition.
        """
        return weatherutils.filter_by_matching_statuses(SUN_KEYWORDS,
                                           self.__forecast.get_weathers())
    
    def when_fog(self):
        """
        Returns a sublist of the Weather objects list in the forecast, which
        only contains items having fog/haze/mist as weather condition.
        """
        return weatherutils.filter_by_matching_statuses(FOG_KEYWORDS,
                                           self.__forecast.get_weathers())
        
    def when_clouds(self):
        """
        Returns a sublist of the Weather objects list in the forecast, which
        only contains items having clouds as weather condition.
        """
        return weatherutils.filter_by_matching_statuses(CLOUDS_KEYWORDS,
                                           self.__forecast.get_weathers())
    
    def when_snow(self):
        """
        Returns a sublist of the Weather objects list in the forecast, which
        only contains items having snow/sleet as weather condition.
        """
        return weatherutils.filter_by_matching_statuses(SNOW_KEYWORDS,
                                           self.__forecast.get_weathers())
    
    def _to_UNIXtime(self, timeobject):
        """
        Returns the UNIXtime corresponding to the time value conveyed by the 
        specified 'timeobject', which can be either a UNIXtime, a 
        datetime.datetime object or an ISO8601-formatted string.
        
        timeobject - the time value (long/int, datetime.datetime, str)
        """
        if isinstance(timeobject, (long, int)):
            return timeobject
        elif isinstance(timeobject, datetime):
            return converter.datetime_to_unix(timeobject)
        elif isinstance(timeobject, str):
            return converter.ISO8601_to_unix(timeobject)
        else:
            raise ValueError('The time value must be espressed either by a long ' \
                             'UNIX time, a datetime.datetime object or an ' \
                             'ISO8601-formatted string')
    
    
    def will_be_rainy_at(self, timeobject):
        """
        Returns a boolean value telling if at the specified time the weather is
        rainy. The check will be performed on the _Weather_ object of
        the encapsulated Forecast instance which is closest to 'timeobject'.
        'timeobject' value can be either a UNIXtime, a datetime.datetime object 
        or an ISO8601-formatted string.
        
        timeobject - the time value (long/int, datetime.datetime, str)
        """
        time = self._to_UNIXtime(timeobject)
        closest_weather = weatherutils.find_closest_weather(
                                        self.__forecast.get_weathers(), time)
        return weatherutils.status_matches_any(RAIN_KEYWORDS, closest_weather)

                
    def will_be_sunny_at(self, timeobject):
        """
        Returns a boolean value telling if at the specified time the weather is
        sunny. The check will be performed on the _Weather_ object of
        the encapsulated Forecast instance which is closest to 'timeobject'.
        'timeobject' value can be either a UNIXtime, a datetime.datetime object 
        or an ISO8601-formatted string.
        
        timeobject - the time value (long/int, datetime.datetime, str)
        """
        time = self._to_UNIXtime(timeobject)
        closest_weather = weatherutils.find_closest_weather(
                                        self.__forecast.get_weathers(), time)
        return weatherutils.status_matches_any(SUN_KEYWORDS, closest_weather)
        
    def will_be_snowy_at(self, timeobject):
        """
        Returns a boolean value telling if at the specified time the weather is
        snowy. The check will be performed on the _Weather_ object of
        the encapsulated Forecast instance which is closest to 'timeobject'.
        'timeobject' value can be either a UNIXtime, a datetime.datetime object 
        or an ISO8601-formatted string.
        
        timeobject - the time value (long/int, datetime.datetime, str)
        """
        time = self._to_UNIXtime(timeobject)
        closest_weather = weatherutils.find_closest_weather(
                                        self.__forecast.get_weathers(), time)
        return weatherutils.status_matches_any(SNOW_KEYWORDS, closest_weather)
        
    def will_be_cloudy_at(self, timeobject):
        """
        Returns a boolean value telling if at the specified time the weather is
        cloudy. The check will be performed on the _Weather_ object of
        the encapsulated Forecast instance which is closest to 'timeobject'.
        'timeobject' value can be either a UNIXtime, a datetime.datetime object 
        or an ISO8601-formatted string.
        
        timeobject - the time value (long/int, datetime.datetime, str)
        """
        time = self._to_UNIXtime(timeobject)
        closest_weather = weatherutils.find_closest_weather(
                                        self.__forecast.get_weathers(), time)
        return weatherutils.status_matches_any(CLOUDS_KEYWORDS, closest_weather)
        
    def will_be_foggy_at(self, timeobject):
        """
        Returns a boolean value telling if at the specified time the weather is
        foggy. The check will be performed on the _Weather_ object of
        the encapsulated Forecast instance which is closest to 'timeobject'.
        'timeobject' value can be either a UNIXtime, a datetime.datetime object 
        or an ISO8601-formatted string.
        
        timeobject - the time value (long/int, datetime.datetime, str)
        """
        time = self._to_UNIXtime(timeobject)
        closest_weather = weatherutils.find_closest_weather(
                                        self.__forecast.get_weathers(), time)
        return weatherutils.status_matches_any(FOG_KEYWORDS, closest_weather)
    
    def get_weather_at(self, timeobject):
        """
        Returns the Weather object in the forecast that is closest in time to
        the time value specified using 'timeobject'.'timeobject' value can be 
        either a UNIXtime, a datetime.datetime object or an ISO8601-formatted 
        string.
        
        timeobject - the time value (long/int, datetime.datetime, str)
        """
        return weatherutils.find_closest_weather(self.__forecast.get_weathers(),
                                                 self._to_UNIXtime(timeobject))