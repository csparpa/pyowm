#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.commons import exceptions
from pyowm.weatherapi25 import location
from pyowm.utils import formatting, timestamps


class SO2Index:
    """
    A class representing the Sulphur Dioxide Index observed in a certain location
    in the world. The index is made up of several measurements, each one at a
    different atmospheric pressure. The location is represented by the
    encapsulated *Location* object.

    :param reference_time: GMT UNIXtime telling when the SO2 data has been measured
    :type reference_time: int
    :param location: the *Location* relative to this SO2 observation
    :type location: *Location*
    :param interval: the time granularity of the SO2 observation
    :type interval: str
    :param so2_samples: the SO2 samples
    :type so2_samples: list of dicts
    :param reception_time: GMT UNIXtime telling when the SO2 observation has
        been received from the OWM Weather API
    :type reception_time: int
    :returns: an *SOIndex* instance
    :raises: *ValueError* when negative values are provided as reception time,
      SO2 samples are not provided in a list

    """

    def __init__(self, reference_time, location, interval, so2_samples, reception_time):
        if reference_time < 0:
            raise ValueError("'reference_time' must be greater than 0")
        self.ref_time = reference_time
        self.location = location
        self.interval = interval
        if not isinstance(so2_samples, list):
            raise ValueError("'so2_samples' must be a list")
        self.so2_samples = so2_samples
        if reception_time < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self.rec_time = reception_time

    def reference_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the SO2 samples have been measured

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00:00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError when negative values are provided

        """
        return formatting.timeformat(self.ref_time, timeformat)

    def reception_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the SO2 observation has been received
        from the OWM Weather API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00:00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError when negative values are provided

        """
        return formatting.timeformat(self.rec_time, timeformat)

    def is_forecast(self):
        """
        Tells if the current SO2 observation refers to the future with respect
        to the current date
        :return: bool
        """
        return timestamps.now(timeformat='unix') < \
               self.reference_time(timeformat='unix')

    @classmethod
    def from_dict(cls, the_dict):
        """
        Parses a *SO2Index* instance out of a data dictionary. Only certain properties of the data dictionary
        are used: if these properties are not found or cannot be parsed, an exception is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: a *SO2Index* instance or ``None`` if no data is available
        :raises: *ParseAPIResponseError* if it is impossible to find or parse the data needed to build the result

        """
        if the_dict is None:
            raise exceptions.ParseAPIResponseError('Data is None')
        try:
            # -- reference time (strip away Z and T on ISO8601 format)
            t = the_dict['time'].replace('Z', '+00:00').replace('T', ' ')
            reference_time = formatting.ISO8601_to_UNIXtime(t)

            # -- reception time (now)
            reception_time = timestamps.now('unix')

            # -- location
            lon = float(the_dict['location']['longitude'])
            lat = float(the_dict['location']['latitude'])
            place = location.Location(None, lon, lat, None)

            # -- SO2 samples
            so2_samples = the_dict['data']

        except KeyError:
            raise exceptions.ParseAPIResponseError(
                      ''.join([__name__, ': impossible to parse COIndex']))

        return SO2Index(reference_time, place, None, so2_samples, reception_time)

    def to_dict(self):
        """Dumps object to a dictionary

        :returns: a `dict`

        """
        return {"reference_time": self.ref_time,
                "location": self.location.to_dict(),
                "interval": self.interval,
                "so2_samples": self.so2_samples,
                "reception_time": self.rec_time}

    def __repr__(self):
        return "<%s.%s - reference time=%s, reception time=%s, location=%s, " \
               "interval=%s>" % (
                    __name__,
                    self.__class__.__name__,
                    self.reference_time('iso'),
                    self.reception_time('iso'),
                    str(self.location),
                    self.interval)
