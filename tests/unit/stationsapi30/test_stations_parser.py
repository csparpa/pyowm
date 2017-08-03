import unittest
import json
from pyowm.stationsapi30.station_parser import StationParser
from pyowm.stationsapi30.station import Station
from pyowm.exceptions import parse_response_error


class TestStationsParser(unittest.TestCase):

    test_station_json = '''{"id": "583436dd9643a9000196b8d6",
        "created_at": "2016-11-22T12:15:25.967Z",
        "updated_at": "2016-11-22T12:15:25.967Z",
        "external_id": "SF_TEST001",
        "name": "San Francisco Test Station",
        "longitude": -122.43,
        "latitude": 37.76,
        "altitude": 150,
        "rank": 0}'''

    test_station = Station("583436dd9643a9000196b8d6",
                           "2016-11-22T12:15:25.967Z",
                           "2016-11-22T12:15:25.967Z",
                           "SF_TEST001",
                           "San Francisco Test Station",
                            -122.43, 37.76, 150, 0)

    def test_parse_JSON(self):
        instance = StationParser()
        result = instance.parse_JSON(self.test_station_json)
        self.assertTrue(isinstance(result, Station))
        self.assertEqual(self.test_station.id, result.id)
        self.assertEqual(self.test_station.created_at, result.created_at)
        self.assertEqual(self.test_station.updated_at, result.updated_at)
        self.assertEqual(self.test_station.name, result.name)
        self.assertEqual(self.test_station.lon, result.lon)
        self.assertEqual(self.test_station.lat, result.lat)
        self.assertEqual(self.test_station.alt, result.alt)
        self.assertEqual(self.test_station.rank, result.rank)

    def test_parse_JSON_fails_with_none_input(self):
        instance = StationParser()
        with self.assertRaises(parse_response_error.ParseResponseError):
            instance.parse_JSON(None)

    def test_parse_dict(self):
        data_dict = json.loads(self.test_station_json)
        instance = StationParser()
        result = instance.parse_dict(data_dict)
        self.assertTrue(isinstance(result, Station))
        self.assertEqual(self.test_station.id, result.id)
        self.assertEqual(self.test_station.created_at, result.created_at)
        self.assertEqual(self.test_station.updated_at, result.updated_at)
        self.assertEqual(self.test_station.name, result.name)
        self.assertEqual(self.test_station.lon, result.lon)
        self.assertEqual(self.test_station.lat, result.lat)
        self.assertEqual(self.test_station.alt, result.alt)
        self.assertEqual(self.test_station.rank, result.rank)

    def test_parse_dict_fails_with_wrong_input(self):
        instance = StationParser()
        with self.assertRaises(AssertionError):
            instance.parse_dict(1234)

