"""
Object that can read/write meteostations metadata and extract related
measurements
"""

import requests
import json
from pyowm.commons.http_client import HttpClient
from pyowm.stationsapi30.station_parser import StationParser


class StationsManager(object):

    STATIONS_API_VERSION = (3, 0, 0)

    """
    A manager objects that provides a full interface to OWM Stations API. Mainly
    it implements CRUD methods on Station entities and the corresponding
    measured datapoints.

    :param API_key: the OWM web API key (defaults to ``None``)
    :type API_key: str
    :returns: a *StationsManager* instance
    :raises: *AssertionError* when no API Key is provided

    """

    def __init__(self, API_key):
        assert API_key is not None, 'You must provide a valid API Key'
        self.API_key = API_key
        self.stations_parser = StationParser()

    def stations_api_version(self):
        return self.STATIONS_API_VERSION

    # STATIONS Methods

    def get_stations(self):
        """
        Retrieves all of the user's stations registered on the Stations API.

        :returns: list of *pyowm.stationsapi30.station.Station* objects

        """

        status, data = HttpClient.get_json(
            'http://api.openweathermap.org/data/3.0/stations',
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})
        return [self.stations_parser.parse_dict(item) for item in data]

    def get_station(self, id):
        """
        Retrieves a named station registered on the Stations API.

        :param id: the ID of the station
        :type id: str
        :returns: a *pyowm.stationsapi30.station.Station* object

        """
        status, data = HttpClient.get_json(
            'http://api.openweathermap.org/data/3.0/stations/%s' % id,
             params={'appid': self.API_key},
             headers={'Content-Type': 'application/json'})
        self.stations_parser.parse_dict(data)
