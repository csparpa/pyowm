#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from pyowm.exceptions import parse_response_error, api_response_error
from pyowm.utils import formatting


class StationHistory:

    """
    A class representing historic weather measurements collected by a
    meteostation. Three types of historic meteostation data can be obtained by
    the OWM Weather API: ticks (one data chunk per minute) data, hourly and daily
    data.

    :param station_ID: the numeric ID of the meteostation
    :type station_ID: int
    :param interval: the time granularity of the meteostation data history
    :type interval: str
    :param reception_time: GMT UNIXtime of the data reception from the OWM web
         API
    :type reception_time: int
    :param measurements: a dictionary containing raw weather measurements
    :type measurements: dict
    :returns: a *StationHistory* instance
    :raises: *ValueError* when the supplied value for reception time is
        negative
    """

    def __init__(self, station_ID, interval, reception_time, measurements):
        self._station_ID = station_ID
        self._interval = interval
        if reception_time < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self._reception_time = reception_time
        self._measurements = measurements

    def get_station_ID(self):
        """
        Returns the ID of the meteostation

        :returns: the int station ID

        """
        return self._station_ID

    def set_station_ID(self, station_ID):
        """
        Sets the numeric ID of the meteostation

        :param station_ID: the numeric ID of the meteostation
        :type station_ID: int

        """
        self._station_ID = station_ID

    def get_interval(self):
        """
        Returns the interval of the meteostation history data

        :returns: the int interval

        """
        return self._interval

    def set_interval(self, interval):
        """
        Sets the interval of the meteostation history data

        :param interval: the time granularity of the meteostation history data,
            may be among "tick","hour" and "day"
        :type interval: string

        """
        self._interval = interval

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
        return self._measurements

    def get_reception_time(self, timeformat='unix'):
        """Returns the GMT time telling when the meteostation history data was
           received from the OWM Weather API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError

        """
        return formatting.timeformat(self._reception_time, timeformat)

    @classmethod
    def from_dict(cls, d):
        """
        Parses a *StationHistory* instance out of a data dictionary. Only certain properties of the data dictionary
        are used: if these properties are not found or cannot be parsed, an exception is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: a *StationHistory* instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the input dict embeds an HTTP status error

        """
        if d is None:
            raise parse_response_error.ParseResponseError('Data is None')
        # Check if server returned errors: this check overcomes the lack of use
        # of HTTP error status codes by the OWM API but it's supposed to be
        # deprecated as soon as the API implements a correct HTTP mechanism for
        # communicating errors to the clients. In addition, in this specific
        # case the OWM API responses are the very same either when no results
        # are found for a station and when the station does not exist!
        measurements = {}
        try:
            if 'cod' in d:
                if d['cod'] != "200":
                    raise api_response_error.APIResponseError(
                                              "OWM API: error - response payload: " + str(d), d['cod'])
            if str(d['cnt']) == "0":
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
                    if 'rain' in item and isinstance(item['rain']['today'],
                                                     dict):
                        rain = item['rain']['today']['v']
                    else:
                        rain = None
                    if 'wind' in item and isinstance(item['wind']['speed'],
                                                     dict):
                        wind = item['wind']['speed']['v']
                    else:
                        wind = None
                    measurements[item['dt']] = {"temperature": temp,
                                                "humidity": hum,
                                                "pressure": pres,
                                                "rain": rain,
                                                "wind": wind}
        except KeyError:
            raise parse_response_error.ParseResponseError(__name__ + ': impossible to read input data')
        current_time = round(time.time())
        return StationHistory(None, None, current_time, measurements)

    def to_dict(self):
        """Dumps object to a dictionary

        :returns: a `dict`

        """
        return {"station_ID": self._station_ID,
                "interval": self._interval,
                "reception_time": self._reception_time,
                "measurements": self._measurements}
