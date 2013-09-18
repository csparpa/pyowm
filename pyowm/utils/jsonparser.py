#!/usr/bin/env python

"""
Parser for the JSON data found into the OWM web API responses
"""

from json import loads, dumps
from time import time
from pyowm.location import Location
from pyowm.weather import Weather
from pyowm.observation import Observation
from pyowm.exceptions.parse_response_exception import ParseResponseException
from pyowm.forecast import Forecast

def build_location_from(d):
    """
    Builds a Location object from the provided dictionary d
    
    d - a weather data dictionary (dict)
    """
    if 'city' in d:
        data = d['city']
    else:
        data = d
    try:
        name = data['name']
        lon = data['coord']['lon']
        lat = data['coord']['lat']
        ID = data['id']
    except KeyError:
        raise ParseResponseException("Impossible to read location info") 
    return Location(name, lon, lat, ID)

def build_weather_from(d):
    """
    Builds a Weather object from the provided dictionary d
    
    d - a weather data dictionary (dict)
    """
    try:
        reference_time = d['dt']
        if 'sys' in d and 'sunset' in d['sys']:
            sunset_time = d['sys']['sunset']
        else:
            sunset_time = 0L
        if 'sys' in d and 'sunrise' in d['sys']:
            sunrise_time = d['sys']['sunrise']
        else:
            sunrise_time = 0L
        if 'clouds' in d:
            if isinstance(d['clouds'], int) or isinstance(d['clouds'], float):
                clouds = d['clouds']
            elif 'all' in d['clouds']: 
                clouds = d['clouds']['all']
            else:
                clouds = 0
        else:
            clouds = 0
        if 'rain' in d:
            if isinstance(d['rain'], int) or isinstance(d['rain'], float):
                rain = {'all': d['rain']}
            else:
                rain = d['rain'].copy()
        else:
            rain = {}
        if 'wind' in d:
            wind = d['wind'].copy()
        else:
            wind = {}
        if 'humidity' in d:
            humidity = d['humidity']
        elif 'main' in d and 'humidity' in d['main']:
            humidity = d['main']['humidity']
        else:
            humidity = 0
        # -- snow is not a mandatory field
        if 'snow' in d:
            snow = d['snow'].copy()
        else:
            snow = {}
        # -- pressure
        if 'pressure' in d:
            atm_press = d['pressure']
        elif 'main' in d and 'pressure' in d['main']:
            atm_press = d['main']['pressure']
        else:
            atm_press = None
        if 'main' in d and 'sea_level' in d['main']:
            sea_level_press = d['main']['sea_level']
        else:
            sea_level_press = None
        pressure = {'press': atm_press,'sea_level': sea_level_press}
        # -- temperature
        if 'temp' in d:
            temperature = d['temp'].copy()
        elif 'main' in d and 'temp' in d['main']:
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
        else:
            temperature = {}
        if 'weather' in d:
            status = d['weather'][0]['main'].lower() #Sometimes provided with a leading upper case!
            detailed_status = d['weather'][0]['description'].lower()
            weather_code = d['weather'][0]['id']
            weather_icon_name = d['weather'][0]['icon']
        else:
            status = u''
            detailed_status = u''
            weather_code = 0
            weather_icon_name = u''
    except KeyError:
        raise ParseResponseException("Impossible to read weather info")
    else:
        return Weather(reference_time, sunset_time, sunrise_time, clouds,
                    rain, snow, wind, humidity, pressure, temperature, 
                    status, detailed_status, weather_code, 
                    weather_icon_name)

def parse_observation(json_data):
    """
    Factory method that builds an Observation instance from the JSON data
    returned from the OWM web API.
    Fallback policies are implemented: missing non mandatory JSON attributes will 
    result in empty data structures while missing mandatory JSON attributes
    will result into a ParseResponseException
    
    json_data - the JSON payload of an OWM web API response
    """
    d = loads(json_data)
    
    # Check if server returned errors: this check overcomes the lack of use of 
    # HTTP error status codes by the OWM API but it's supposed to be deprecated 
    # as soon as the API implements a correct HTTP mechanism for communicating 
    # errors to the clients
    if 'message' in d and 'cod' in d:
        if d['cod'] is not "200":
            print "Unable to fulfill the request - Server response: "+dumps(d)
            return None
    l = build_location_from(d)
    w = build_weather_from(d)
    return Observation(long(round(time())), l, w)

def parse_search_results(json_data):
    """
    Factory method that builds a list of Observation instances from the JSON data
    returned from the OWM web API.
    Fallback policies are implemented: when parsing each Observation instance, missing 
    non mandatory JSON attributes will result in empty data structures while 
    missing mandatory JSON attributes will result into a ParseResponseException
    
    json_data - the JSON payload of an OWM web API response
    """
    d = loads(json_data)
    
    # Check if server returned errors: this check overcomes the lack of use of 
    # HTTP error status codes by the OWM API but it's supposed to be deprecated 
    # as soon as the API implements a correct HTTP mechanism for communicating 
    # errors to the clients
    if 'cod' in d and d['cod'] != "200":
        print "Unable to fulfill the request - Server response: "+dumps(d)
        return None
    
    # Handle the case when no results are found
    if 'count' in d and d['count'] is "0":
        return []
    else:
        if 'list' in d:
            return [Observation(long(round(time())), 
                                build_location_from(item), 
                                build_weather_from(item)) for item in d['list']]
        else:
            raise ParseResponseException("Impossible to read observations list") 


def parse_forecast(json_data):
    """
    Factory method that builds a Forecast instance from the JSON data
    returned from the OWM web API.
    Fallback policies are implemented: missing non mandatory JSON attributes will 
    result in empty data structures while missing mandatory JSON attributes
    will result into a ParseResponseException
    
    json_data - the JSON payload of an OWM web API response
    """
    d = loads(json_data)
    
    # Check if server returned errors: this check overcomes the lack of use of 
    # HTTP error status codes by the OWM API but it's supposed to be deprecated 
    # as soon as the API implements a correct HTTP mechanism for communicating 
    # errors to the clients
    if 'message' in d and 'cod' in d:
        if d['cod'] != "200":
            print "Unable to fulfill the request - Server response: "+dumps(d)
            return None
    l = build_location_from(d)
    
    # Handle the case when no results are found
    if 'count' in d and d['count'] is "0":
        weathers = []
    elif 'cnt' in d and d['cnt'] is 0:
        weathers = []
    else:
        if 'list' in d:
            weathers = [build_weather_from(item) for item in d['list']]
        else:
            raise ParseResponseException("Impossible to read observations list")
        
    return Forecast("3h", long(round(time())), l, weathers)
