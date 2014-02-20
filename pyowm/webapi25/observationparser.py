#!/usr/bin/env python

"""
Module containing a concrete implementation for JSONParser abstract class,
returning Observation objects
"""

from json import loads, dumps
from time import time
from observation import Observation
from location import Location
from weather import Weather
from pyowm.abstractions.jsonparser import JSONParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.exceptions.api_response_error import APIResponseError


class ObservationParser(JSONParser):
    """
    Concrete *JSONParser* implementation building an *Observation* instance out
    of raw JSON data coming from OWM web API responses.

    """

    def __init__(self):
        pass

    def parse_JSON(self, JSON_string):
        """
        Parses an *Observation* instance out of raw JSON data. Only certain
        properties of the data are used: if these properties are not found or
        cannot be parsed, an error is issued.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: an *Observation* instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the JSON
            string embeds an HTTP status error (this is an OWM web API 2.5 bug)

        """
        d = loads(JSON_string)
        # Check if server returned errors: this check overcomes the lack of use
        # of HTTP error status codes by the OWM API 2.5. This mechanism is
        # supposed to be deprecated as soon as the API fully adopts HTTP for
        # conveying errors to the clients
        if 'message' in d and 'cod' in d:
            if d['cod'] == "404":
                print "OWM API: observation data not available - response " \
                    "payload: " + dumps(d)
                return None
            else:
                raise APIResponseError("OWM API: error - response payload: " + \
                                       dumps(d))
        try:
            location = Location.from_dictionary(d)
        except KeyError:
            raise ParseResponseError(''.join([__name__, ': impossible to ' \
              'read location info from JSON data']))
        try:
            weather = Weather.from_dictionary(d)
        except KeyError:
            raise ParseResponseError(''.join([__name__, ': impossible to ' \
              'read weather info from JSON data']))
        current_time = long(round(time()))
        return Observation(current_time, location, weather)

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)
