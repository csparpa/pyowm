"""
Module containing a concrete implementation for JSONParser abstract class,
returning a Station instance
"""

import json
from pyowm.abstractions import jsonparser
from pyowm.exceptions import parse_response_error
from pyowm.stationsapi30.station import Station


class StationParser(jsonparser.JSONParser):

    """
    Concrete *JSONParser* implementation building a
    *pyowm.stationsapi30.station.Station* instance out of raw JSON data

    """

    def __init__(self):
        pass

    def parse_dict(self, data_dict):
        """
        Parses a dictionary representing the attributes of a
        *pyowm.stationsapi30.station.Station* entity
        :param data_dict: dict
        :return: *pyowm.stationsapi30.station.Station*
        """
        assert isinstance(data_dict, dict)
        string_repr = json.dumps(data_dict)
        return self.parse_JSON(string_repr)

    def parse_JSON(self, JSON_string):
        """
        Parses a *pyowm.stationsapi30.station.Station* instance out of raw JSON
        data.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :return: a *pyowm.stationsapi30.station.Station* instance or ``None``
            if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        try:
            id = d.get('ID', None) or d.get('id', None)
            external_id = d.get('external_id', None)
            lon = d.get('longitude', None)
            lat = d.get('latitude', None)
            alt = d.get('altitude', None)
        except KeyError as e:
            raise parse_response_error.ParseResponseError('Impossible to parse JSON: %s' % e)
        name = d.get('name', None)
        rank = d.get('rank', None)
        created_at = d.get('created_at', None)
        updated_at = d.get('updated_at', None)
        return Station(id, created_at, updated_at, external_id, name, lon, lat,
                       alt, rank)
