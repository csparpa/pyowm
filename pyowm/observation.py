#!/usr/bin/env python

"""
Weather observation classes and data structures.
"""

from json import loads
from time import time
from location import Location
from weather import Weather
from exceptions.parse_response_exception import ParseResponseException

class Observation(object):
    """
    A databox containing weather data observed in a certain location and at a
    certain time.
    """

    def __init__(self, reception_time, location, weather):
        """
        reception_time - GMT UNIXtime of data reception from the OWM API (int)
        location - the location relative to this observation (Lcation)
        weather - the observed weather data (Weather)
        """
        assert type(reception_time) is long or type(reception_time) is int, "'reception_time' must be an int/long"
        if long(reception_time) < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self.__reference_time = long(reception_time)
        assert isinstance(location, Location), "'location' must be a Location object"
        self.__location = location
        assert isinstance(weather, Weather), "'weather' must be a Weather object"
        self.__weather = weather

    def get_reference_time(self):
        """Returns the reference time as a long"""
        return self.__reference_time

    def get_location(self):
        """Returns the Location object"""
        return self.__location

    def get_weather(self):
        """Returns the Weather object"""
        return self.__weather
        
    def from_JSON(json_data):
        """
        Factory method that builds an Observation instance from JSON data.
        Fallback policies are used: missing non mandatory JSON attributes will 
        result in empty data structures while missing mandatory JSON attributes
        will result into a ParseResponseException  
        """
        d = loads(json_data)
        
        # Location object construction
        try:
            name = d['name']
            lon = d['coord']['lon']
            lat = d['coord']['lat']
            ID = d['id']
        except KeyError:
            raise ParseResponseException("Impossible to read location info")
        else:
            l = Location(name, lon, lat, ID)
        
        # Weather object construction
        try:
            reference_time = d['dt']
            sunset_time = d['sys']['sunset']
            sunrise_time = d['sys']['sunrise']
            clouds = d['clouds']['all']
            rain = d['rain'].copy()
            wind = d['wind'].copy()
            humidity = d['main']['humidity']
            # -- snow is not a mandatory field
            if hasattr(d, 'snow'):
                snow = d['snow'].copy()
            else:
                snow = {}
            # -- pressure
            atm_press = d['main']['pressure']
            if hasattr(d['main'], 'sea_level'):
                sea_level_press = d['main']['sea_level']
            else:
                sea_level_press = None
            pressure = {'press': atm_press,'sea_level': sea_level_press}
            # -- temperature
            if hasattr(d, 'temp'):
                temperature = d['temp'].copy()
            else:
                temp = d['main']['temp']
                if hasattr(d['main'], 'temp_kf'):
                    temp_kf = d['main']['temp_kf']
                else:
                    temp_kf = None
                temp_max = d['main']['temp_max']
                temp_min = d['main']['temp_min']
                temperature = {'temp': temp, 
                               'temp_kf': temp_kf,
                               'temp_max': temp_max,
                               'temp_min': temp_min
                               }
            status = d['weather'][0]['main'].lower() #Sometimes provided with a leading upper case!
            detailed_status = d['weather'][0]['description'].lower()
            weather_code = d['weather'][0]['id']
            weather_icon_name = d['weather'][0]['icon']
        except KeyError:
            raise ParseResponseException("Impossible to read weather info")
        else:
            w = Weather(reference_time, sunset_time, sunrise_time, clouds,
                        rain, snow, wind, humidity, pressure, temperature, 
                        status, detailed_status, weather_code, 
                        weather_icon_name)

        return Observation(long(round(time())), l, w)
    
    #Static methods
    from_JSON = staticmethod(from_JSON)
