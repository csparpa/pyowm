#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.exceptions import parse_response_error
from pyowm.utils import formatting, timestamps
from pyowm.weatherapi25 import location


class COIndex:
    """
    A class representing the Carbon monOxide Index observed in a certain location
    in the world. The index is made up of several measurements, each one at a
    different atmospheric pressure. The location is represented by the
    encapsulated *Location* object.

    :param reference_time: GMT UNIXtime telling when the CO data has been measured
    :type reference_time: int
    :param location: the *Location* relative to this CO observation
    :type location: *Location*
    :param interval: the time granularity of the CO observation
    :type interval: str
    :param co_samples: the CO samples
    :type co_samples: list of dicts
    :param reception_time: GMT UNIXtime telling when the CO observation has
        been received from the OWM Weather API
    :type reception_time: int
    :returns: an *COIndex* instance
    :raises: *ValueError* when negative values are provided as reception time,
      CO samples are not provided in a list

    """

    def __init__(self, reference_time, location, interval, co_samples,
                 reception_time):
        if reference_time < 0:
            raise ValueError("'reference_time' must be greater than 0")
        self._reference_time = reference_time
        self.location = location
        self._interval = interval
        if not isinstance(co_samples, list):
            raise ValueError("'co_samples' must be a list")
        self._co_samples = sorted(co_samples, key=lambda k: k['value'], reverse=True)
        if reception_time < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self._reception_time = reception_time

    def get_reference_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the CO samples have been measured

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError when negative values are provided

        """
        return formatting.timeformat(self._reference_time, timeformat)

    def get_reception_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the CO observation has been received
        from the OWM Weather API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError when negative values are provided

        """
        return formatting.timeformat(self._reception_time, timeformat)

    def get_location(self):
        """
        Returns the *Location* object for this CO index measurement

        :returns: the *Location* object

        """
        return self.location

    def get_interval(self):
        """
        Returns the time granularity interval for this CO index measurement

        :return: str
        """
        return self._interval

    def get_co_samples(self):
        """
        Returns the CO samples for this index

        :returns: list of dicts

        """
        return self._co_samples

    def get_co_sample_with_highest_vmr(self):
        """
        Returns the CO sample with the highest Volume Mixing Ratio value
        :return: dict
        """
        return max(self._co_samples, key=lambda x: x['value'])

    def get_co_sample_with_lowest_vmr(self):
        """
        Returns the CO sample with the lowest Volume Mixing Ratio value
        :return: dict
        """
        return min(self._co_samples, key=lambda x: x['value'])

    def is_forecast(self):
        """
        Tells if the current CO observation refers to the future with respect
        to the current date
        :return: bool
        """
        return timestamps.now(timeformat='unix') < \
               self.get_reference_time(timeformat='unix')

    @classmethod
    def from_dict(cls, the_dict):
        """
        Parses a *COIndex* instance out of a data dictionary. Only certain properties of the data dictionary
        are used: if these properties are not found or cannot be parsed, an exception is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: a *COIndex* instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the data needed to build the result

        """
        if the_dict is None:
            raise parse_response_error.ParseResponseError('Data is None')
        try:
            # -- reference time (strip away Z and T on ISO8601 format)
            t = the_dict['time'].replace('Z', '+00').replace('T', ' ')
            reference_time = formatting.ISO8601_to_UNIXtime(t)

            # -- reception time (now)
            reception_time = timestamps.now('unix')

            # -- location
            lon = float(the_dict['location']['longitude'])
            lat = float(the_dict['location']['latitude'])
            place = location.Location(None, lon, lat, None)

            # -- CO samples
            co_samples = the_dict['data']

        except KeyError:
            raise parse_response_error.ParseResponseError(
                      ''.join([__name__, ': impossible to parse COIndex']))

        return COIndex(reference_time, place, None, co_samples, reception_time)

    def to_dict(self):
        """Dumps object to a dictionary

        :returns: a `dict`

        """
        return {"reference_time": self._reference_time,
                "location": self.location.to_dict(),
                "interval": self._interval,
                "co_samples": self._co_samples,
                "reception_time": self._reception_time}

    def __repr__(self):
        return "<%s.%s - reference time=%s, reception time=%s, location=%s, " \
               "interval=%s>" % (
                    __name__,
                    self.__class__.__name__,
                    self.get_reference_time('iso'),
                    self.get_reception_time('iso'),
                    str(self.location),
                    self._interval)
