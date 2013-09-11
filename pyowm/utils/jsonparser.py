#!/usr/bin/env python

"""
Parser for the JSON data found into the OWM web API responses
"""

from json import loads
from time import time
from pyowm.location import Location
from pyowm.weather import Weather
from pyowm.observation import Observation
from pyowm.exceptions.parse_response_exception import ParseResponseException

    
def parse_observation(json_data):
    """
    Factory method that builds an Observation instance from the JSON data
    returned from the OWM web API.
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
    
    l = Location(name, lon, lat, ID)

    # Weather object construction
    try:
        reference_time = d['dt']
        sunset_time = d['sys']['sunset']
        sunrise_time = d['sys']['sunrise']
        clouds = d['clouds']['all']
        if 'rain' in d:
            rain = d['rain'].copy()
        else:
            rain = {}
        if 'wind' in d:
            wind = d['wind'].copy()
        else:
            wind = {}
        humidity = d['main']['humidity']
        # -- snow is not a mandatory field
        if 'snow' in d:
            snow = d['snow'].copy()
        else:
            snow = {}
        # -- pressure
        atm_press = d['main']['pressure']
        if 'sea_level' in d['main']:
            sea_level_press = d['main']['sea_level']
        else:
            sea_level_press = None
        pressure = {'press': atm_press,'sea_level': sea_level_press}
        # -- temperature
        if 'temp' in d:
            temperature = d['temp'].copy()
        else:
            temp = d['main']['temp']
            if 'temp_kf' in d['main']:
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


def parse_forecast(json_data):
    """
    Factory method that builds a Forecast instance from the JSON data
    returned from the OWM web API.
    Fallback policies are used: missing non mandatory JSON attributes will 
    result in empty data structures while missing mandatory JSON attributes
    will result into a ParseResponseException  
    """
    raise Exception("Not yet implemented")
