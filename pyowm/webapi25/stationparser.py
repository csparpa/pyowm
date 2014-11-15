#!/usr/bin/env python

"""
Module containing a concrete implementation for JSONParser abstract class,
returning a Station instance
"""

import json
import time

from pyowm.webapi25 import station
from pyowm.webapi25 import weather
from pyowm.abstractions import jsonparser
from pyowm.exceptions import parse_response_error, api_response_error


class StationParser(jsonparser.JSONParser):
    """
    Concrete *JSONParser* implementation building a *Station* instance
    out of raw JSON data coming from OWM web API responses.

    """

    def __init__(self):
        pass

    def parse_JSON(self, JSON_string):
        """
        Parses a *Station* instance out of raw JSON data. Only certain
        properties of the data are used: if these properties are not found or
        cannot be parsed, an error is issued.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: a *Station* instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the JSON
            string embeds an HTTP status error (this is an OWM web API 2.5 bug)

        """
        d = json.loads(JSON_string)
        try:
            name = d['station']['name']
            station_ID = d['station']['id']
            station_type = d['station']['type']
            status = d['station']['status']
            lat = d['station']['coord']['lat']
            lon = d['station']['coord']['lon']

            if 'distance' in d:
                distance = d['distance']
            else:
                distance = None

            if 'last' in d:
                last_weather = weather.weather_from_dictionary(d['last'])
            else:
                last_weather = None
        
        except KeyError, e:
            error_msg = ''.join((__name__, ': unable to read JSON data', ))
            raise parse_response_error.ParseResponseError(error_msg)

        return station.Station(name, station_ID, station_type, status, lat, lon,
                               distance, last_weather)
