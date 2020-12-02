#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from pyowm.commons import exceptions
from pyowm.utils import formatting
from pyowm.weatherapi25 import location
from pyowm.weatherapi25 import weather


class Observation:
    """
    A class representing the weather which is currently being observed in a
    certain location in the world. The location is represented by the
    encapsulated *Location* object while the observed weather data are held by
    the encapsulated *Weather* object.

    :param reception_time: GMT UNIXtime telling when the weather obervation has
        been received from the OWM Weather API
    :type reception_time: int
    :param location: the *Location* relative to this observation
    :type location: *Location*
    :param weather: the *Weather* relative to this observation
    :type weather: *Weather*
    :returns: an *Observation* instance
    :raises: *ValueError* when negative values are provided as reception time

    """

    def __init__(self, reception_time, location, weather):
        if reception_time < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self.rec_time = reception_time
        self.location = location
        self.weather = weather

    def reception_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the observation has been received
          from the OWM Weather API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError when negative values are provided

        """
        return formatting.timeformat(self.rec_time, timeformat)

    @classmethod
    def from_dict(cls, the_dict):
        """
        Parses an *Observation* instance out of a data dictionary. Only certain properties of the data dictionary
        are used: if these properties are not found or cannot be parsed, an exception is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: an *Observation* instance or ``None`` if no data is available
        :raises: *ParseAPIResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the input dict embeds an HTTP status error

        """
        if the_dict is None:
            raise exceptions.ParseAPIResponseError('JSON data is None')

        # Check if server returned errors: this check overcomes the lack of use
        # of HTTP error status codes by the OWM API 2.5. This mechanism is
        # supposed to be deprecated as soon as the API fully adopts HTTP for
        # conveying errors to the clients
        if 'message' in the_dict and 'cod' in the_dict:
            if the_dict['cod'] != "404":
                raise exceptions.APIResponseError(
                                      "OWM API: error - response payload", the_dict['cod'])
            print("OWM API: observation data not available")
            return None
        try:
            place = location.Location.from_dict(the_dict)
        except KeyError:
            raise exceptions.ParseAPIResponseError(
                                      ''.join([__name__, ': impossible to read location info from JSON data']))
        try:
            w = weather.Weather.from_dict(the_dict)
        except KeyError:
            raise exceptions.ParseAPIResponseError(
                                      ''.join([__name__, ': impossible to read weather info from JSON data']))
        current_time = int(time.time())
        return Observation(current_time, place, w)

    def to_dict(self):
        """Dumps object to a dictionary

        :returns: a `dict`

        """
        return {"reception_time": self.rec_time,
                "location": self.location.to_dict(),
                "weather": self.weather.to_dict()}

    def __repr__(self):
        return "<%s.%s - reception_time=%s>" % (__name__, self.__class__.__name__,
                                                self.reception_time('iso'))

    @classmethod
    def from_dict_of_lists(self, the_dict):
        """
        Parses a list of *Observation* instances out of raw input dict containing a list. Only certain properties of
        the data are used: if these properties are not found or cannot be parsed, an error is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: a `list` of *Observation* instances or ``None`` if no data is available
        :raises: *ParseAPIResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the OWM API returns an HTTP status error

        """
        if the_dict is None:
            raise exceptions.ParseAPIResponseError('JSON data is None')
        if 'cod' in the_dict:
            # Check if server returned errors: this check overcomes the lack of use
            # of HTTP error status codes by the OWM API 2.5. This mechanism is
            # supposed to be deprecated as soon as the API fully adopts HTTP for
            # conveying errors to the clients
            if the_dict['cod'] == "200" or the_dict['cod'] == 200:
                pass
            else:
                if the_dict['cod'] == "404" or the_dict['cod'] == 404:
                    print("OWM API: data not found")
                    return None
                else:
                    raise exceptions.APIResponseError("OWM API: error - response payload", the_dict['cod'])

        # Handle the case when no results are found
        if 'count' in the_dict and the_dict['count'] == "0":
            return []
        if 'cnt' in the_dict and the_dict['cnt'] == 0:
            return []
        if 'list' in the_dict:
            return [Observation.from_dict(item) for item in the_dict['list']]

        # no way out..
        raise exceptions.ParseAPIResponseError(''.join([__name__, ': impossible to read JSON data']))