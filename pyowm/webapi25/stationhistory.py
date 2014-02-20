#!/usr/bin/env python

"""
Module containing classes and datastructures related to meteostation history
data
"""

from json import dumps
from pyowm.utils import converter, xmlutils


class StationHistory(object):

    """
    A class representing historic weather measurements collected by a
    meteostation. Three types of historic meteostation data can be obtained by
    the OWM web API: ticks (one data chunk per minute) data, hourly and daily
    data.

    :param station_ID: the numeric ID of the meteostation
    :type station_ID: int
    :param interval: the time granularity of the meteostation data history
    :type interval: str
    :param reception_time: GMT UNIXtime of the data reception from the OWM web
         API
    :type reception_time: long/int
    :param measurements: a dictionary containing raw weather measurements
    :type measurements: dict
    :returns: a *StationHistory* instance
    :raises: *ValueError* when the supplied value for reception time is
        negative
    """

    def __init__(self, station_ID, interval, reception_time, measurements):
        self.__station_ID = station_ID
        self.__interval = interval
        if long(reception_time) < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self.__reception_time = reception_time
        self.__measurements = measurements

    def get_station_ID(self):
        """
        Returns the ID of the meteostation

        :returns: the int station ID

        """
        return self.__station_ID

    def set_station_ID(self, station_ID):
        """
        Sets the numeric ID of the meteostation

        :param station_ID: the numeric ID of the meteostation
        :type station_ID: int

        """
        self.__station_ID = station_ID

    def get_interval(self):
        """
        Returns the interval of the meteostation history data

        :returns: the int interval

        """
        return self.__interval

    def set_interval(self, interval):
        """
        Sets the interval of the meteostation history data

        :param interval: the time granularity of the meteostation history data,
            may be among "tick","hour" and "day"
        :type interval: string

        """
        self.__interval = interval

    def get_measurements(self):
        """
        Returns the measurements of the meteostation as a dict. The dictionary
        keys are UNIX timestamps and for each one the value is a dict
        containing the keys 'temperature','humidity','pressure','rain','wind'
        along with their corresponding numeric values.
        Eg: ``{1362933983: { "temperature": 266.25, "humidity": 27.3,
        "pressure": 1010.02, "rain": None, "wind": 4.7}, ... }``

        :returns: the dict containing the meteostation's measurements

        """
        return self.__measurements

    def get_reception_time(self, timeformat='unix'):
        """Returns the GMT time telling when the meteostation history data was
           received from the OWM web API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: a long or a str
        :raises: ValueError

        """
        if timeformat == 'unix':
            return self.__reception_time
        elif timeformat == 'iso':
            return converter.UNIXtime_to_ISO8601(self.__reception_time)
        else:
            raise ValueError("Invalid value for parameter 'format'")

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns: the JSON string

        """
        d = {"station_ID": self.__station_ID,
             "interval": self.__interval,
             "reception_time": self.__reception_time,
             "measurements": self.__measurements
             }
        return dumps(d)

    def to_XML(self):
        """Dumps object fields into a XML formatted string

        :returns: the XML string

        """
        return '<StationHistory><station_id>%s</station_id>' \
            '<interval>%s</interval><reception_time>%s</reception_time>' \
            '<measurements>%s</measurements></StationHistory>' % \
            (self.__station_ID, self.__interval, self.__reception_time,
             "".join([xmlutils.make_tag(str(item),
                            xmlutils.dict_to_XML(self.__measurements[item])) \
                      for item in self.__measurements])
                    )

    def __len__(self):
        return len(self.__measurements)

    def __repr__(self):
        return '<%s.%s - station ID=%s, reception time=%s, interval=%s, ' \
               'measurements:%s>' % (__name__, self.__class__.__name__,
                                     self.__station_ID,
                                     self.get_reception_time('iso'),
                                     self.__interval, str(len(self))
                                     )
