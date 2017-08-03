import unittest
import json
from pyowm.stationsapi30.station import Station


class TestStation(unittest.TestCase):

    _test_instance = Station("583436dd9643a9000196b8d6",
                             "2016-11-22T12:15:25.967Z",
                             "2016-11-22T12:15:25.967Z",
                             "SF_TEST001",
                             "San Francisco Test Station",
                             -122.43, 37.76, 150, 0)

    def test_failing_instantiations(self):
        with self.assertRaises(AssertionError):
            Station(None,
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -122.43, 37.76, 150, 0)
        with self.assertRaises(AssertionError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    None,
                    "San Francisco Test Station",
                    -122.43, 37.76, 150, 0)
        with self.assertRaises(AssertionError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    None, 37.76, 150, 0)
        with self.assertRaises(AssertionError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -122.43, None, 150, 0)

    def test_instantiations_failing_upon_wrong_geocoords(self):
        with self.assertRaises(ValueError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -422.43, 37.76, 150, 0)
        with self.assertRaises(ValueError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -122.43, -97.76, 150, 0)
        with self.assertRaises(ValueError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -122.43, 37.76, -56.9, 0)

    def test_repr(self):
        print(self._test_instance)

    def test_to_JSON(self):
        expected = '''{
            "alt": 150,
            "name": "San Francisco Test Station",
            "lat": 37.76,
            "lon": -122.43,
            "created_at": "2016-11-22 12:15:25+00",
            "external_id": "SF_TEST001",
            "id": "583436dd9643a9000196b8d6",
            "rank": 0,
            "updated_at": "2016-11-22 12:15:25+00"}'''
        instance = Station("583436dd9643a9000196b8d6",
                           "2016-11-22T12:15:25.967Z",
                           "2016-11-22T12:15:25.967Z",
                           "SF_TEST001",
                           "San Francisco Test Station",
                           -122.43, 37.76, 150, 0)
        result = instance.to_JSON()
        self.assertEquals(json.loads(expected), json.loads(result))
