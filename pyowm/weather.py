#!/usr/bin/env python

"""
Module containing weather data classes and data structures.
"""

from utils import converter, xmlutils
from json import dumps

class Weather(object):    
    """
    A class encapsulating raw weather data.    
    A reference about OWM weather codes and icons can be found at 
    http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes
    
    :param reference_time: GMT UNIX time of weather measurement
    :type reference_time: long
    :param sunset_time: GMT UNIX time of sunset
    :type sunset_time: long
    :param sunrise_time: GMT UNIX time of sunrise
    :type sunrise_time: long
    :param clouds: cloud coverage percentage
    :type clouds: int
    :param rain: precipitation info
    :type rain: dict
    :param snow: snow info
    :type snow: dict
    :param wind: wind info
    :type wind: dict
    :param humidity: atmospheric humidity percentage
    :type humidity: int 
    :param pressure: atmospheric pressure info
    :type pressure: dict
    :param temperature: temperature info
    :type temperature: dict
    :param status: short weather status
    :type status: Unicode
    :param detailed_status: detailed weather status
    :type detailed_status: Unicode
    :param weather_code: OWM weather condition code
    :type weather_code: int
    :param weather_icon_name: weather-related icon name
    :type weather_icon_name: Unicode    
    :returns:  a *Weather* instance
    :raises: *ValueError* when negative values are provided
    
    """
    
    def __init__(self, reference_time, sunset_time, sunrise_time, clouds, rain, 
                 snow, wind, humidity, pressure, temperature, status, 
                 detailed_status, weather_code, weather_icon_name):        
        assert type(reference_time) is long or type(reference_time) is int, \
            "'reference_time' must be an int/long"
        if long(reference_time) < 0:
            raise ValueError("'reference_time' must be greater than 0")
        self.__reference_time = long(reference_time)        
        assert type(sunset_time) is long or type(sunset_time) is int, \
            "'sunset_time' must be a int/long"
        if long(sunset_time) < 0:
            raise ValueError("'sunset_time' must be greatear than 0")
        self.__sunset_time = long(sunset_time)
        assert type(sunrise_time) is long or type(sunrise_time) is int, \
            "'sunrise_time' must be a int/long"
        if long(sunrise_time) < 0:
            raise ValueError("'sunrise_time' must be greatear than 0")
        self.__sunrise_time = long(sunrise_time)
        assert type(clouds) is int, "'clouds' must be an int"
        if clouds < 0:
            raise ValueError("'clouds' must be greater than 0")
        self.__clouds = clouds
        assert type(rain) is dict, "'rain' must be a dict"
        self.__rain = rain
        assert type(snow) is dict, "'snow' must be a dict"
        self.__snow = snow
        assert type(wind) is dict, "'wind' must be a dict"
        self.__wind = wind
        assert type(humidity) is int, "'humidity' must be an int"
        if humidity < 0:
            raise ValueError("'humidity' must be greatear than 0")
        self.__humidity = humidity
        assert type(pressure) is dict, "'pressure' must be a dict"
        self.__pressure = pressure
        assert type(temperature) is dict, "'temperature' must be a dict"
        self.__temperature = temperature
        assert type(status) is unicode, "'status' must be a Unicode str"
        self.__status = status
        assert type(detailed_status) is unicode, "'detailed_status' must be a Unicode str"
        self.__detailed_status = detailed_status
        assert type(weather_code) is int, "'weather_code' must be an int"
        self.__weather_code = weather_code
        assert type(weather_icon_name) is unicode, "'iconName' must be a Unicode str"
        self.__weather_icon_name = weather_icon_name

        
    def get_reference_time(self, timeformat='unix'):
        """Returns the GMT time telling when the weather was measured
    
        :param timeformat: the format for the time value. May be: 
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: a long or a str
        :raises: ValueError when negative values are provided
    
        """
        if timeformat == 'unix':
            return self.__reference_time
        if timeformat == 'iso':
            return converter.UNIXtime_to_ISO8601(self.__reference_time)
        else:
            raise ValueError("Invalid value for parameter 'format'")


    def get_sunset_time(self, timeformat='unix'):
        """Returns the GMT time of sunset
    
        :param timeformat: the format for the time value. May be: 
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: a long or a str
        :raises: ValueError
    
        """
        if timeformat == 'unix':
            return self.__sunset_time
        if timeformat == 'iso':
            return converter.UNIXtime_to_ISO8601(self.__sunset_time)
        else:
            raise ValueError("Invalid value for parameter 'format'")


    def get_sunrise_time(self, timeformat='unix'):
        """Returns the GMT time of sunrise
    
        :param timeformat: the format for the time value. May be: 
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: a long or a str
        :raises: ValueError
    
        """
        if timeformat == 'unix':
            return self.__sunrise_time
        if timeformat == 'iso':
            return converter.UNIXtime_to_ISO8601(self.__sunrise_time)
        else:
            raise ValueError("Invalid value for parameter 'format'")


    def get_clouds(self):
        """Returns the cloud coverage percentage as an int
        
        :returns: the cloud coverage percentage
        
        """
        return self.__clouds


    def get_rain(self):
        """Returns a dict containing precipitation info
        
        :returns: a dict containing rain info
        
        """
        return self.__rain


    def get_snow(self):
        """Returns a dict containing snow info
        
        :returns: a dict containing snow info
        
        """
        return self.__snow


    def get_wind(self):
        """Returns a dict containing wind info
        
        :returns: a dict containing wind info
        
        """
        return self.__wind


    def get_humidity(self):
        """Returns the atmospheric humidity as an int
        
        :returns: the humidity
        
        """
        return self.__humidity


    def get_pressure(self):
        """Returns a dict containing atmospheric pressure info
        
        :returns: a dict containing pressure info
        
        """
        return self.__pressure


    def get_temperature(self, unit='kelvin'):
        """Returns a dict with temperature info
    
        :param unit: the unit of measure for the temperature values. May be: 
            '*kelvin*' (default), '*celsius*' or '*fahrenheit*'
        :type unit: str
        :returns: a dict containing temperature values.
        :raises: ValueError
    
        """
        if unit == 'kelvin':
            return self.__temperature
        if unit == 'celsius':
            helper = lambda x: converter.kelvin_to_celsius(x) if x > 0.0 else x
            return dict((item, helper(self.__temperature[item])) 
                for item in self.__temperature)
        if unit == 'fahrenheit':
            helper = lambda x: converter.kelvin_to_fahrenheit(x) if x > 0.0 else x
            return dict((item, helper(self.__temperature[item])) 
                for item in self.__temperature)
        else:
            raise ValueError("Invalid value for parameter 'unit'")


    def get_status(self):
        """Returns the short weather status as a Unicode string
        
        :returns: the short weather status
        
        """
        return self.__status


    def get_detailed_status(self):
        """Returns the detailed weather status as a Unicode string
        
        :returns: the detailed weather status
        
        """
        return self.__detailed_status


    def get_weather_code(self):
        """Returns the OWM weather condition code as an int
        
        :returns: the OWM weather condition code
        
        """
        return self.__weather_code


    def get_weather_icon_name(self):
        """Returns weather-related icon name as a Unicode string.
    
        :returns: the icon name.
    
        """
        return self.__weather_icon_name
        
    def to_JSON(self):
        """Dumps object fields into a JSON formatted string
        
        :returns: the JSON string
        
        """
        return dumps({ 'reference_time': self.__reference_time, 
                      'sunset_time': self.__sunset_time,
                      'sunrise_time': self.__sunrise_time, 'clouds': self.__clouds,
                      'rain': self.__rain, 'snow': self.__snow, 'wind': self.__wind,
                      'humidity': self.__humidity, 'pressure': self.__pressure,
                      'temperature': self.__temperature, 'status' : self.__status,
                      'detailed_status': self.__detailed_status,
                      'weather_code': self.__weather_code,
                      'weather_icon_name': self.__weather_icon_name })
        
    def to_XML(self):
        """Dumps object fields into a XML formatted string
    
        :returns:  the XML string
    
        """
        return '<Weather><status>%s</status><weather_code>%s</weather_code><rain>' \
            '%s</rain><snow>%s</snow><pressure>%s</pressure><sunrise_time>%s' \
            '</sunrise_time><weather_icon_name>%s</weather_icon_name><clouds>%s' \
            '</clouds><temperature>%s</temperature><detailed_status>%s' \
            '</detailed_status><reference_time>%s</reference_time><sunset_time>%s' \
            '</sunset_time><humidity>%s</humidity><wind>%s</wind></Weather>' % (
                self.__status, self.__weather_code,
                xmlutils.dict_to_XML(self.__rain),xmlutils.dict_to_XML(self.__snow),
                xmlutils.dict_to_XML(self.__pressure), self.__sunrise_time,
                self.__weather_icon_name, self.__clouds, 
                xmlutils.dict_to_XML(self.__temperature), self.__detailed_status,
                self.__reference_time, self.__sunset_time, self.__humidity,
                xmlutils.dict_to_XML(self.__wind))
    
    def __str__(self):
        """Redefine __str__ hook for pretty-printing of Weather instances"""
        prop_names = ["reference_time","sunset_time","sunrise_time","clouds",
                      "rain","snow","wind","humidity","pressure","temperature",
                      "status","detailed_status","weather_code","weather_icon_name"]
        prop_values = [self.__reference_time, self.__sunset_time, self.__sunrise_time,
                 self.__clouds, self.__rain, self.__snow, self.__wind, self.__humidity,
                 self.__pressure, self.__temperature, self.__status.encode("utf-8"), 
                 self.__detailed_status.encode("utf-8"), self.__weather_code,
                 self.__weather_icon_name.encode("utf-8")]
        string_prop_values = map(str, prop_values)
        return "[Weather:\n  "+"\n  ".join([ ": ".join([name,value]) for name,value \
                                        in zip(prop_names,string_prop_values)])+"\n]"
    