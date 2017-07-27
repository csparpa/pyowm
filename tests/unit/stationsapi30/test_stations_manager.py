import unittest
from pyowm.stationsapi30.stations_manager import StationsManager


class TestStationManager(unittest.TestCase):

    def test_instantiation_fails_without_api_key(self):
        self.assertRaises(AssertionError, StationsManager, None)

    def test_get_stations_api_version(self):
        instance = StationsManager('abcdefghilmno')
        result = instance.stations_api_version()
        self.assertIsInstance(result, tuple)
