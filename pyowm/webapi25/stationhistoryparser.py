#!/usr/bin/env python

"""
Module containing a concrete implementation for JSONParser abstract class,
returning a StatioHistory instance
"""

from json import loads, dumps
from time import time
from stationhistory import StationHistory
from pyowm.abstractions.jsonparser import JSONParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.exceptions.api_response_error import APIResponseError


class StationHistoryParser(JSONParser):
    """
    Concrete *JSONParser* implementation building a *StatioHistory* instance 
    out of raw JSON data coming from OWM web API responses.
    
    """
    
    def __init__(self):
        pass
    
    def parse_JSON(self, JSON_string):
        """
        Parses a *StatioHistory* instance out of raw JSON data. Only certain 
        properties of the data are used: if these properties are not found or 
        cannot be parsed, an error is issued.
        
        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: a *StatioHistory* instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the JSON 
            string embeds an HTTP status error (this is an OWM web API 2.5 bug)
            
        """
        d = loads(JSON_string)
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
            raise ParseResponseError(__name__+': impossible to read JSON data')
        current_time = long(round(time()))
        return StationHistory(None, None, current_time, measurements)
