"""
Module containing a concrete implementation for JSONParser abstract class,
returning an AggregatedMeasurement instance
"""

import json
from pyowm.abstractions import jsonparser
from pyowm.exceptions import parse_response_error
from pyowm.stationsapi30.measurement import AggregatedMeasurement


class AggregatedMeasurementParser(jsonparser.JSONParser):

    """
    Concrete *JSONParser* implementation building a
    *pyowm.stationsapi30.measurement.AggregatedMeasurement* instance out of
    raw JSON data

    """

    def __init__(self):
        pass

    def parse_dict(self, data_dict):
        """
        Parses a dictionary representing the attributes of a
        *pyowm.stationsapi30.smeasurement.AggregatedMeasurement* entity
        :param data_dict: dict
        :return: *pyowm.stationsapi30.measurement.AggregatedMeasurement*
        """
        assert isinstance(data_dict, dict)
        string_repr = json.dumps(data_dict)
        return self.parse_JSON(string_repr)

    def parse_JSON(self, JSON_string):
        """
        Parses a *pyowm.stationsapi30.measurement.AggregatedMeasurement*
        instance out of raw JSON data.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :return: a *pyowm.stationsapi30.measurement.AggregatedMeasurement*
          instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        station_id = d.get('station_id', None)
        ts = d.get('date', None)
        if ts is not None:
            ts = int(ts)
        aggregated_on = d.get('type', None)
        temp = d.get('temp', dict())
        humidity = d.get('humidity', dict())
        wind = d.get('wind', dict())
        pressure = d.get('pressure', dict())
        precipitation = d.get('precipitation', dict())
        return AggregatedMeasurement(station_id, ts, aggregated_on, temp=temp,
            humidity=humidity, wind=wind,
            pressure=pressure, precipitation=precipitation)
