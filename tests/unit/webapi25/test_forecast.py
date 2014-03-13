#!/usr/bin/env python

"""
Test case for forecast.py module
"""

import unittest
from pyowm.webapi25.location import Location
from pyowm.webapi25.weather import Weather
from pyowm.webapi25.forecast import Forecast


class TestForecast(unittest.TestCase):

    __test_reception_time = 1234567
    __test_iso_reception_time = "1970-01-15 06:56:07+00"
    __test_location = Location(u'test', 12.3, 43.7, 987, 'IT')
    __test_weathers = [Weather(1378459200, 1378496400, 1378449600, 67,
            {"all": 20}, {"all": 0}, {"deg": 252.002, "speed": 1.100}, 57,
            {"press": 1030.119, "sea_level": 1038.589},
            {"temp": 294.199, "temp_kf": -1.899, "temp_max": 296.098,
                "temp_min": 294.199
            },
            "Clouds", "Overcast clouds", 804, "04d"),
           Weather(1378459690, 1378496480, 1378449510, 23, {"all": 10},
            {"all": 0}, {"deg": 103.4, "speed": 4.2}, 12,
            {"press": 1070.119, "sea_level": 1078.589},
            {"temp": 297.199, "temp_kf": -1.899, "temp_max": 299.0,
             "temp_min": 295.6
             },
            "Clear", "Sky is clear", 804, u"02d")
       ]
    __test_n_weathers = len(__test_weathers)
    __test_instance = Forecast("daily", __test_reception_time, __test_location,
                               __test_weathers)

    def test_init_fails_when_reception_time_is_negative(self):
        self.assertRaises(ValueError, Forecast, "3h", -1234567,
                          self.__test_location, self.__test_weathers)

    def test_get(self):
        index = 1
        self.assertEqual(self.__test_weathers[index],
                         self.__test_instance.get(index))

    def test_getters_return_expected_3h_data(self):
        """
        Test either for "3h" forecast and "daily" ones
        """
        instance = Forecast("3h", self.__test_reception_time,
                             self.__test_location, self.__test_weathers)
        self.assertEqual(instance.get_interval(), "3h")
        self.assertEqual(instance.get_reception_time(),
                         self.__test_reception_time)
        self.assertEqual(instance.get_location(), self.__test_location)
        self.assertEqual(instance.get_weathers(), self.__test_weathers)

    def test_getters_return_expected_daily_data(self):
        instance = Forecast("daily", self.__test_reception_time,
                             self.__test_location, self.__test_weathers)
        self.assertEqual(instance.get_interval(), "daily")
        self.assertEqual(instance.get_reception_time(),
                         self.__test_reception_time)
        self.assertEqual(instance.get_location(), self.__test_location)
        self.assertEqual(instance.get_weathers(), self.__test_weathers)

    def test_returning_different_formats_for_reception_time(self):
        instance = self.__test_instance
        self.assertEqual(instance.get_reception_time(timeformat='iso'),
                         self.__test_iso_reception_time)
        self.assertEqual(instance.get_reception_time(timeformat='unix'),
                         self.__test_reception_time)

    def test_count_weathers(self):
        instance = self.__test_instance
        self.assertEqual(instance.count_weathers(), self.__test_n_weathers)

    def test_forecast_iterator(self):
        instance = self.__test_instance
        counter = 0
        for weather in instance:
            self.assertTrue(isinstance(weather, Weather))
            counter += 1
        self.assertEqual(instance.count_weathers(), counter)
