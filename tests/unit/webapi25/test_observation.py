#!/usr/bin/env python

"""
Test case for observation.py module
"""

import unittest
from pyowm.webapi25.location import Location
from pyowm.webapi25.weather import Weather
from pyowm.webapi25.observation import Observation


class TestObservation(unittest.TestCase):

    __test_reception_time = 1234567
    __test_iso_reception_time = "1970-01-15 06:56:07+00"
    __test_location = Location('test', 12.3, 43.7, 987, 'UK')
    __test_weather = Weather(1378459200, 1378496400, 1378449600, 67, {"all": 20},
            {"all": 0}, {"deg": 252.002, "speed": 1.100}, 57,
            {"press": 1030.119, "sea_level": 1038.589},
            {"temp": 294.199, "temp_kf": -1.899, "temp_max": 296.098,
                "temp_min": 294.199
            },
            "Clouds", "Overcast clouds", 804, "04d")
    __test_instance = Observation(__test_reception_time, __test_location,
                                  __test_weather)

    def test_init_fails_when_reception_time_is_negative(self):
        self.assertRaises(ValueError, Observation, -1234567, \
                          self.__test_location, self.__test_weather)

    def test_getters_return_expected_data(self):
        self.assertEqual(self.__test_instance.get_reception_time(),
                         self.__test_reception_time)
        self.assertEqual(self.__test_instance.get_location(),
                         self.__test_location)
        self.assertEqual(self.__test_instance.get_weather(),
                         self.__test_weather)

    def test_returning_different_formats_for_reception_time(self):
        self.assertEqual(self.__test_instance.get_reception_time(timeformat='iso'), \
                         self.__test_iso_reception_time)
        self.assertEqual(self.__test_instance.get_reception_time(timeformat='unix'), \
                         self.__test_reception_time)
