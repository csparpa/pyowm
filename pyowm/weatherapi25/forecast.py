#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from pyowm.exceptions import parse_response_error, api_response_error
from pyowm.utils import timestamps, formatting
from pyowm.weatherapi25 import location
from pyowm.weatherapi25 import weather


class ForecastIterator:
    """
    Iterator over the list of *Weather* objects encapsulated in a *Forecast*
    class instance

    :param obj: the iterable object
    :type obj: object
    :returns:  a *ForecastIterator* instance

    """
    def __init__(self, obj):
        self._obj = obj
        self._cnt = 0

    def next(self):
        """
        Compatibility for Python 2.x, delegates to function: `__next__()`
        Returns the next *Weather* item

        :returns: the next *Weather* item

        """
        return self.__next__()

    def __next__(self):
        """
        Returns the next *Weather* item

        :returns: the next *Weather* item

        """
        try:
            result = self._obj.get(self._cnt)
            self._cnt += 1
            return result
        except IndexError:
            raise StopIteration


class Forecast:
    """
    A class encapsulating weather forecast data for a certain location and
    relative to a specific time interval (forecast for every three hours or
    for every day)

    :param interval: the time granularity of the forecast. May be: *'3h'* for
        three hours forecast or *'daily'* for daily ones
    :type interval: str
    :param reception_time: GMT UNIXtime of the forecast reception from the OWM
        web API
    :type reception_time: int
    :param location: the *Location* object relative to the forecast
    :type location: Location
    :param weathers: the list of *Weather* objects composing the forecast
    :type weathers: list
    :returns:  a *Forecast* instance
    :raises: *ValueError* when negative values are provided

    """

    def __init__(self, interval, reception_time, location, weathers):
        self._interval = interval
        if reception_time < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self._reception_time = reception_time
        self.location = location
        self._weathers = weathers

    def __iter__(self):
        """
        Creates a *ForecastIterator* instance

        :returns: a *ForecastIterator* instance
        """
        return ForecastIterator(self)

    def get(self, index):
        """
        Lookups up into the *Weather* items list for the item at the specified
        index

        :param index: the index of the *Weather* object in the list
        :type index: int
        :returns: a *Weather* object
        """
        return self._weathers[index]

    def get_interval(self):
        """
        Returns the time granularity of the forecast

        :returns: str

        """
        return self._interval

    def set_interval(self, interval):
        """
        Sets the time granularity of the forecast

        :param interval: the time granularity of the forecast, may be "3h" or
            "daily"
        :type interval: str

        """
        self._interval = interval

    def get_reception_time(self, timeformat='unix'):
        """Returns the GMT time telling when the forecast was received
            from the OWM Weather API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError

        """
        return formatting.timeformat(self._reception_time, timeformat)

    def get_location(self):
        """
        Returns the Location object relative to the forecast

        :returns: a *Location* object

        """
        return self.location

    def get_weathers(self):
        """
        Returns a copy of the *Weather* objects list composing the forecast

        :returns: a list of *Weather* objects

        """
        return list(self._weathers)

    def count_weathers(self):
        """
        Tells how many *Weather* items compose the forecast

        :returns: the *Weather* objects total

        """
        return len(self._weathers)

    def actualize(self):
        """
        Removes from this forecast all the *Weather* objects having a reference
        timestamp in the past with respect to the current timestamp
        """
        current_time = timestamps.now(timeformat='unix')
        for w in self._weathers:
            if w.get_reference_time(timeformat='unix') < current_time:
                self._weathers.remove(w)

    @classmethod
    def from_dict(cls, the_dict):
        """
        Parses a *Forecast* instance out of a raw data dictionary. Only certain properties of the data are used: if
        these properties are not found or cannot be parsed, an error is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: a *Forecast* instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the input dictionary embeds an HTTP status error

        """
        if the_dict is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        # Check if server returned errors: this check overcomes the lack of use
        # of HTTP error status codes by the OWM API 2.5. This mechanism is
        # supposed to be deprecated as soon as the API fully adopts HTTP for
        # conveying errors to the clients
        if 'message' in the_dict and 'cod' in the_dict:
            if the_dict['cod'] == "404":
                print("OWM API: data not found - response payload", the_dict['cod'])
                return None
            elif the_dict['cod'] != "200":
                raise api_response_error.APIResponseError("OWM API: error - response payload", the_dict['cod'])
        try:
            place = location.Location.from_dict(the_dict)
        except KeyError:
            raise parse_response_error.ParseResponseError(''.join([__name__,
                                                               ': impossible to read location info from JSON data']))
        # Handle the case when no results are found
        if 'count' in the_dict and the_dict['count'] == "0":
            weathers = []
        elif 'cnt' in the_dict and the_dict['cnt'] == 0:
            weathers = []
        else:
            if 'list' in the_dict:
                try:
                    weathers = [weather.Weather.from_dict(item) \
                                for item in the_dict['list']]
                except KeyError:
                    raise parse_response_error.ParseResponseError(
                          ''.join([__name__, ': impossible to read weather info from JSON data'])
                                  )
            else:
                raise parse_response_error.ParseResponseError(
                          ''.join([__name__, ': impossible to read weather list from JSON data'])
                          )
        current_time = int(round(time.time()))
        return Forecast(None, current_time, place, weathers)

    def to_dict(self):
        """Dumps object to a dictionary

        :returns: a `dict`

        """
        return {"interval": self._interval,
               "reception_time": self._reception_time,
               "location": self.location.to_dict(),
               "weathers": [w.to_dict() for w in self]}

    def __len__(self):
        """Redefine __len__ hook"""
        return self.count_weathers()

    def __repr__(self):
        return "<%s.%s - reception time=%s, interval=%s>" % (__name__, \
              self.__class__.__name__, self.get_reception_time('iso'),
              self._interval)
