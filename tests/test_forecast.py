#!/usr/bin/env python

"""
Test case for forecast.py module
"""

import unittest
from pyowm import Location
from pyowm import Weather
from pyowm import Forecast

class Test(unittest.TestCase):

    __test_reception_time = 1234567L
    __test_iso_reception_time = "1970-01-15 06:56:07+00"
    __test_location = Location(u'test', 12.3, 43.7, 987)
    __test_weathers = [ Weather(1378459200, 1378496400, 1378449600, 67, {"all": 20},
            {"all": 0}, {"deg": 252.002, "speed": 1.100}, 57, 
            {"press": 1030.119, "sea_level": 1038.589},
            {"temp": 294.199, "temp_kf": -1.899, "temp_max": 296.098, "temp_min": 294.199},
            u"Clouds", u"Overcast clouds", 804, u"04d"),
           Weather(1378459690, 1378496480, 1378449510, 23, {"all": 10},
            {"all": 0}, {"deg": 103.4, "speed": 4.2}, 12, 
            {"press": 1070.119, "sea_level": 1078.589},
            {"temp": 297.199, "temp_kf": -1.899, "temp_max": 299.0, "temp_min": 295.6},
            u"Clear", u"Sky is clear", 804, u"02d")
       ]

    def test_init_fails_when_reception_time_is_negative(self):
        self.assertRaises(ValueError, Forecast, "3h", -1234567L, self.__test_location, self.__test_weathers)

    def test_init_fails_with_unknown_interval(self):
        """
        Test method failure providing a bad value for 'interval'
        """
        self.assertRaises(ValueError, Forecast, "xyz", self.__test_reception_time,
                          self.__test_location, self.__test_weathers)
        
    def test_getters_return_expected_data(self):
        instance1 = Forecast("3h", self.__test_reception_time, self.__test_location,
                             self.__test_weathers)
        self.assertEqual(instance1.get_interval(), "3h", "")
        self.assertEqual(instance1.get_reception_time(), self.__test_reception_time, "")
        self.assertEqual(instance1.get_location(), self.__test_location, "")
        self.assertEqual(instance1.get_weathers(), self.__test_weathers, "")
        instance2 = Forecast("daily", self.__test_reception_time, 
                             self.__test_location, self.__test_weathers)
        self.assertEqual(instance2.get_interval(), "daily", "")
        self.assertEqual(instance2.get_reception_time(), self.__test_reception_time, "")
        self.assertEqual(instance2.get_location(), self.__test_location, "")
        self.assertEqual(instance2.get_weathers(), self.__test_weathers, "")

    def test_returning_different_formats_for_reception_time(self):
        """
        Test get_reception_time returns timestamps in the expected formats
        """
        instance = Forecast("3h", self.__test_reception_time, self.__test_location,
                             self.__test_weathers)
        self.assertEqual(instance.get_reception_time(timeformat='iso'), self.__test_iso_reception_time, "")
        self.assertEqual(instance.get_reception_time(timeformat='unix'), self.__test_reception_time, "")

if __name__ == "__main__":
    unittest.main()