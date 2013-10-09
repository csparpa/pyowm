#!/usr/bin/env python

"""
Module containing utility functions for parsing of JSON data coming from OWM 
web API responses
"""

from json import loads, dumps
from time import time
from os import linesep
from pyowm.location import Location
from pyowm.weather import Weather
from pyowm.observation import Observation
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.exceptions.api_response_error import APIResponseError
from pyowm.forecast import Forecast
from pyowm.stationhistory import StationHistory

def build_location_from(d):
    """
    Factory method that builds a *Location* object out of a data dictionary data.
    Only certain properties of the dictionary are used: if these properties are 
    not found or cannot be parsed, an error is issued.
    
    :param d: a data dictionary
    :type d: dict
    :returns: a *Location* instance
    :raises: *ParseResponseError* if it is impossible to find or parse the data
        needed to build the instance
        
    """
    country = None
    if 'sys' in d and 'country' in d['sys']:
        country = d['sys']['country']
    if 'city' in d:
        data = d['city']
    else:
        data = d
    try:
        name = data['name']
        lon = data['coord']['lon']
        lat = data['coord']['lat']
        ID = int(data['id'])
        if 'country' in data:
            country = data['country']
    except KeyError:
        raise ParseResponseError(''.join([__name__,': impossible to read ' \
              'location info from JSON data', linesep, str(data)]))
    else:
        return Location(name, lon, lat, ID, country)

def build_weather_from(d):
    """
    Factory method that builds a *Weather* object out of a data dictionary data.
    Only certain properties of the dictionary are used: if these properties are
    not found or cannot be parsed, an error is issued.
    
    :param d: a data dictionary
    :type d: dict
    :returns: a *Weather* instance
    :raises: *ParseResponseError* if it is impossible to find or parse the data
        needed to build the instance
        
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
        raise ParseResponseError(''.join([__name__,': impossible to read ' \
              'weather info from JSON data', linesep, str(d)]))
    else:
        return Weather(reference_time, sunset_time, sunrise_time, clouds,
                    rain, snow, wind, humidity, pressure, temperature, 
                    status, detailed_status, weather_code, 
                    weather_icon_name)

def parse_observation(json_data):
    """
    Parses an *Observation* instance out of raw JSON data coming from OWM web 
    API responses. Only certain properties of the data are used:
    if these properties are not found or cannot be parsed, an error is issued.
    
    :param json_data: a raw JSON string
    :type json_data: str
    :returns: an *Observation* instance or ``None`` if no data is available
    :raises: *ParseResponseError* if it is impossible to find or parse the data
        needed to build the result, *APIResponseError* if the OWM API returns
        a HTTP status error
        
    """
    d = loads(json_data)
    # Check if server returned errors: this check overcomes the lack of use of 
    # HTTP error status codes by the OWM API but it's supposed to be deprecated 
    # as soon as the API implements a correct HTTP mechanism for communicating 
    # errors to the clients
    if 'message' in d and 'cod' in d:
        if d['cod'] == "404":
            print "OWM API: data not found - response payload: "+dumps(d)
            return None
        else:
            raise APIResponseError("OWM API: error - response payload: "+dumps(d))
    l = build_location_from(d)
    w = build_weather_from(d)
    return Observation(long(round(time())), l, w)

def parse_weather_search_results(json_data):
    """
    Parses a list of *Observation* instances out of raw JSON data coming from 
    OWM web API responses. Only certain properties of the data are used:
    if these properties are not found or cannot be parsed, an error is issued.
    
    :param json_data: a raw JSON string
    :type json_data: str
    :returns: a list of *Observation* instances or ``None`` if no data is available
    :raises: *ParseResponseError* if it is impossible to find or parse the data
        needed to build the result, *APIResponseError* if the OWM API returns
        a HTTP status error
        
    """
    d = loads(json_data)
    # Check if server returned errors: this check overcomes the lack of use of 
    # HTTP error status codes by the OWM API but it's supposed to be deprecated 
    # as soon as the API implements a correct HTTP mechanism for communicating 
    # errors to the clients
    if 'cod' in d:
        if d['cod'] == "404":
            print "OWM API: data not found - response payload: "+dumps(d)
            return None
        elif d['cod'] == "200":
            # Handle the case when no results are found
            if 'count' in d and d['count'] is "0":
                return []
            else:
                if 'list' in d:
                    return [Observation(long(round(time())), 
                                        build_location_from(item), 
                                        build_weather_from(item)) for item in d['list']]
                else:
                    raise ParseResponseError(''.join([__name__,': impossible to read ' \
                      'observation list from JSON data', linesep, str(d)]))
        else:
            raise APIResponseError("OWM API: error - response payload: "+dumps(d))
    else:
            raise ParseResponseError(''.join([__name__,': impossible to read ' \
              'JSON data', linesep, str(d)]))

def parse_forecast(json_data, interval):
    """
    Parses a *Forecast* instance out of raw JSON data coming from OWM web 
    API responses. Only certain properties of the data are used:
    if these properties are not found or cannot be parsed, an error is issued.
    
    :param json_data: a raw JSON string
    :type json_data: str
    :param interval: the time granularity for this weather forecast
    :type interval: string
    :returns: a *Forecast* instance  or ``None`` if no data is available
    :raises: *ParseResponseError* if it is impossible to find or parse the data
        needed to build the result, *APIResponseError* if the OWM API returns
        a HTTP status error
        
    """
    d = loads(json_data)
    # Check if server returned errors: this check overcomes the lack of use of 
    # HTTP error status codes by the OWM API but it's supposed to be deprecated 
    # as soon as the API implements a correct HTTP mechanism for communicating 
    # errors to the clients
    if 'message' in d and 'cod' in d:
        if d['cod'] == "404":
            print "OWM API: data not found - response payload: "+dumps(d)
            return None
        elif d['cod'] != "200" :
            raise APIResponseError("OWM API: error - response payload: "+dumps(d))
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
            raise ParseResponseError(''.join([__name__,': impossible to read ' \
              'observation list from JSON data', linesep, str(d)])) 
    return Forecast(interval, long(round(time())), l, weathers)

def parse_weather_history(json_data):
    """
    Parses a list of *Weather* instance out of raw JSON data coming from OWM web 
    API responses when querying for city weather history. Only certain properties
    of the data are used: if these properties are not found or cannot be parsed,
    an error is issued.
    
    :param json_data: a raw JSON string
    :type json_data: str
    :returns: a list of *Weather* instances or ``None`` if no data is available 
    :raises: *ParseResponseError* if it is impossible to find or parse the data
        needed to build the result, *APIResponseError* if the OWM API returns
        a HTTP status error
        
    """
    d = loads(json_data)
    # Check if server returned errors: this check overcomes the lack of use of 
    # HTTP error status codes by the OWM API but it's supposed to be deprecated 
    # as soon as the API implements a correct HTTP mechanism for communicating 
    # errors to the clients
    if 'message' in d and 'cod' in d:
        if d['cod'] == "404":
            print "OWM API: data not found - response payload: "+dumps(d)
            return None
        elif d['cod'] != "200" :
            raise APIResponseError("OWM API: error - response payload: "+dumps(d))
    # Handle the case when no results are found
    if 'cnt' in d and d['cnt'] is "0":
        return []
    else:
        if 'list' in d:
            return [build_weather_from(item) for item in d['list']]
        else:
            raise ParseResponseError(''.join([__name__,': impossible to read ' \
              'JSON data', linesep, str(d)]))
            
def parse_station_history(json_data, station_ID, interval):
    """
    Parses a *StationHistory* instance out of raw JSON data coming from OWM web 
    API responses when querying for meteostation weather history. Only certain 
    properties of the data are used: if these properties are not found or cannot
    be parsed, an error is issued.
    
    :param json_data: a raw JSON string
    :type json_data: str
    :param station_ID: the meteostation ID
    :type station_ID: int
    :param interval: the time granularity for this historic weather dataset
    :type interval: string
    :returns: a *StationHistory* or ``None`` if no data is available 
    :raises: *ParseResponseError* if it is impossible to find or parse the data
        needed to build the result, *APIResponseError* if the OWM API returns
        a HTTP status error
        
    """
    d = loads(json_data)
    # Check if server returned errors: this check overcomes the lack of use of 
    # HTTP error status codes by the OWM API but it's supposed to be deprecated 
    # as soon as the API implements a correct HTTP mechanism for communicating 
    # errors to the clients. In addition, in this specific case the OWM API 
    # responses are the very same either when no results are found for a station
    # and when the station does not exist!
    measurements = {}
    try:
        if 'cod' in d:
            if d['cod'] != "200":
                raise APIResponseError("OWM API: error - response payload: "+dumps(d))
        if str(d['cnt']) is "0":
            return None
        else:
            for item in d['list']:
                if 'temp' not in item:
                    temp = None
                elif isinstance(item['temp'], dict):
                    temp = item['temp']['v']
                else:
                    temp = item['temp']
                if 'humidity' not in item:
                    hum = None
                elif isinstance(item['humidity'], dict):
                    hum = item['humidity']['v']
                else:
                    hum = item['humidity']
                if 'pressure' not in item:
                    pres = None
                elif isinstance(item['pressure'], dict):
                    pres = item['pressure']['v']
                else:
                    pres = item['pressure']
                if 'rain' in item and isinstance(item['rain']['today'], dict):
                    rain = item['rain']['today']['v']
                else:
                    rain = None
                if 'wind' in item and isinstance(item['wind']['speed'], dict):
                    wind = item['wind']['speed']['v']
                else:
                    wind = None
                measurements[item['dt']] = {
                 "temperature": temp,
                 "humidity": hum,
                 "pressure": pres,
                 "rain": rain,
                 "wind": wind
                }
    except KeyError:
        raise ParseResponseError(''.join([__name__,': impossible to read JSON data',
                                   linesep, str(d)]))
    return StationHistory(station_ID, interval, long(round(time())),
                              measurements)
        