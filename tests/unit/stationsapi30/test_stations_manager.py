import unittest
import json
import copy
from pyowm.stationsapi30.station import Station
from pyowm.stationsapi30.stations_manager import StationsManager
from pyowm.commons.http_client import HttpClient
from pyowm.stationsapi30.station_parser import StationParser


class MockHttpClient(HttpClient):

    test_station_json = '''{"ID": "583436dd9643a9000196b8d6",
        "created_at": "2016-11-22T12:15:25.967Z",
        "updated_at": "2016-11-22T12:15:25.967Z",
        "external_id": "SF_TEST001",
        "name": "San Francisco Test Station",
        "longitude": -122.43,
        "latitude": 37.76,
        "altitude": 150,
        "rank": 0}'''

    def get_json(self, uri, params=None, headers=None):
        return 200, [json.loads(self.test_station_json)]

    def post(self, uri, params=None, data=None, headers=None):
        return 200, json.loads(self.test_station_json)

    def put(self, uri, params=None, data=None, headers=None):
        return 200, None


class MockHttpClientOneStation(HttpClient):
    test_station_json = '''{"ID": "583436dd9643a9000196b8d6",
        "created_at": "2016-11-22T12:15:25.967Z",
        "updated_at": "2016-11-22T12:15:25.967Z",
        "external_id": "SF_TEST001",
        "name": "San Francisco Test Station",
        "longitude": -122.43,
        "latitude": 37.76,
        "altitude": 150,
        "rank": 0}'''

    def get_json(self, uri, params=None, headers=None):
        return 200, json.loads(self.test_station_json)


class TestStationManager(unittest.TestCase):

    def factory(self, _kls):
        sm = StationsManager('APIKey')
        sm.http_client = _kls()
        return sm

    def test_instantiation_fails_without_api_key(self):
        self.assertRaises(AssertionError, StationsManager, None)

    def test_get_stations_api_version(self):
        instance = StationsManager('APIKey')
        result = instance.stations_api_version()
        self.assertIsInstance(result, tuple)

    def test_get_stations(self):
        instance = self.factory(MockHttpClient)
        results = instance.get_stations()
        self.assertEqual(1, len(results))
        s = results[0]
        self.assertIsInstance(s, Station)

    def test_get_station(self):
        instance = self.factory(MockHttpClientOneStation)
        result = instance.get_station('1234')
        self.assertIsInstance(result, Station)

    def test_create_stations(self):
        instance = self.factory(MockHttpClient)
        result = instance.create_station("TEST2", "test2", 37.76, -122.43)
        self.assertIsInstance(result, Station)

    def test_create_stations_fails_with_wrong_inputs(self):
        instance = self.factory(MockHttpClient)
        with self.assertRaises(AssertionError):
            instance.create_station(None, "test2", 37.76, -122.43)
        with self.assertRaises(AssertionError):
            instance.create_station("TEST2", None, 37.76, -122.43)
        with self.assertRaises(AssertionError):
            instance.create_station("TEST2", "test2", None, -122.43)
        with self.assertRaises(AssertionError):
            instance.create_station("TEST2", "test2", 37.76, None)
        with self.assertRaises(ValueError):
            instance.create_station("TEST2", "test2", 1678, -122.43)
        with self.assertRaises(ValueError):
            instance.create_station("TEST2", "test2", 37.76, -8122.43)
        with self.assertRaises(ValueError):
            instance.create_station("TEST2", "test2", 37.76, -122.43, alt=-3)

    def test_update_station(self):
        instance = self.factory(MockHttpClient)
        parser = StationParser()
        modified_station = parser.parse_JSON(MockHttpClient.test_station_json)
        modified_station.external_id = 'CHNG'
        result = instance.update_station(modified_station)
        self.assertIsNone(result)

    def test_update_station_fails_when_id_is_none(self):
        instance = self.factory(MockHttpClient)
        parser = StationParser()
        modified_station = parser.parse_JSON(MockHttpClient.test_station_json)
        modified_station.id = None
        with self.assertRaises(AssertionError):
            result = instance.update_station(modified_station)
