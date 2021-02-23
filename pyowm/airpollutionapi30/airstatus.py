#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.commons import exceptions
from pyowm.utils import formatting, timestamps
from pyowm.weatherapi25 import location


class AirStatus:
    """
    A class representing a dataset about air quality

    :param reference_time: GMT UNIXtime telling when the data has been measured
    :type reference_time: int
    :param location: the *Location* relative to this measurement
    :type location: *Location*
    :param interval: the time granularity of the CO observation
    :type interval: str
    :param air_quality_data: the dataset
    :type air_quality_data: dict
    :param reception_time: GMT UNIXtime telling when the CO observation has
        been received from the OWM Weather API
    :type reception_time: int
    :returns: an *COIndex* instance
    :raises: *ValueError* when negative values are provided as reception time,
      CO samples are not provided in a list

    """

    def __init__(self, reference_time, location, air_quality_data, reception_time):
        if reference_time < 0:
            raise ValueError("'reference_time' must be greater than 0")
        self.ref_time = reference_time
        self.location = location
        if not isinstance(air_quality_data, dict):
            raise ValueError("'air_quality_data' must be a list")
        self.air_quality_data = air_quality_data
        for key, val in air_quality_data.items():
            setattr(self, key, val)
        if reception_time < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self.rec_time = reception_time

    def reference_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the air quality data have been measured

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
        Returns the GMT time telling when the air quality data has been received
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


    @classmethod
    def from_dict(cls, the_dict):
        """
        Parses an *AirStatus* instance or `list` of instances out of a data dictionary.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: a *AirStatus* instance or ``list` of such instances
        :raises: *ParseAPIResponseError* if it is impossible to find or parse the data needed to build the result

        """
        if the_dict is None:
            raise exceptions.ParseAPIResponseError('Data is None')
        try:
            # -- location
            lon = float(the_dict['coord']['lat'])
            lat = float(the_dict['coord']['lon'])
            place = location.Location(None, lon, lat, None)

            # -- reception time (now)
            rcp_time = timestamps.now('unix')

            def build_air_status(item_dict, location, reception_time):
                # -- reference time (strip away Z and T on ISO8601 format)
                reference_time = item_dict['dt']

                # -- air quality data
                data = item_dict['components']
                data['aqi'] = item_dict['main']['aqi']

                return AirStatus(reference_time, location, data, reception_time)

            items = the_dict['list']

            # one datapoint
            if len(items) == 1:
                return build_air_status(items[0], place, rcp_time)
            # multiple datapoints
            else:
                return [build_air_status(item, place, rcp_time) for item in items]

        except KeyError:
            raise exceptions.ParseAPIResponseError(
                      ''.join([__name__, ': impossible to parse AirStatus']))

    def to_dict(self):
        """Dumps object to a dictionary

        :returns: a `dict`

        """
        return {"reference_time": self.ref_time,
                "location": self.location.to_dict(),
                "air_quality_data": self.air_quality_data,
                "reception_time": self.rec_time}

    def __repr__(self):
        return "<%s.%s - reference time=%s, reception time=%s, location=%s" % (
                    __name__,
                    self.__class__.__name__,
                    self.reference_time('iso'),
                    self.reception_time('iso'),
                    str(self.location))
