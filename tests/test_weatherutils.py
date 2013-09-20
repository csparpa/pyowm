#!/usr/bin/env python

"""
Test case for weatherutils.py module
"""

import unittest
from pyowm.weather import Weather
from pyowm.utils import weatherutils

class TestWeatherUtils(unittest.TestCase):
    
    __test_time_1 = 1379090800L
    __test_time_1_iso = "2013-09-13 16:46:40+00"
    __test_time_2 = 1379361400L
    __test_time_2_iso = "2013-09-16 19:56:40+00"

    __test_weather_rain = Weather(__test_time_1, 1378496400, 1378449600, 67, 
            {"all": 30}, {"all": 0}, {"deg": 252.002, "speed": 4.100}, 57, 
            {"press": 1030.119, "sea_level": 1038.589},
            {"temp": 294.199, "temp_kf": -1.899, "temp_max": 296.098, 
                "temp_min": 294.199
            },
            u"Rain", u"Light rain", 500, u"10d")
    __test_weather_sun = Weather(__test_time_2, 1378496480, 1378449510, 5, 
            {"all": 0}, {"all": 0}, {"deg": 103.4, "speed": 1.2}, 12, 
            {"press": 1090.119, "sea_level": 1078.589},
            {"temp": 299.199, "temp_kf": -1.899, "temp_max": 301.0, 
             "temp_min": 297.6
             },
            u"Clear", u"Sky is clear", 800, u"01d")
    __test_weathers = [__test_weather_rain, __test_weather_sun]

    def test_status_matches_any(self):
        self.assertTrue(weatherutils.status_matches_any(['rain'],
                                                    self.__test_weather_rain))
        self.assertFalse(weatherutils.status_matches_any(['sunnyday'],
                                                    self.__test_weather_rain))

    def test_statuses_match_any(self):
        self.assertTrue(weatherutils.statuses_match_any(['rain'],
                                                    self.__test_weathers))
        self.assertFalse(weatherutils.statuses_match_any(['sandstorm'],
                                                    self.__test_weathers))

    def test_filter_by_matching_statuses(self):
        self.assertEqual([self.__test_weather_rain], 
             weatherutils.filter_by_matching_statuses(['rain'],
                                          self.__test_weathers))
        self.assertEqual([self.__test_weather_sun], 
             weatherutils.filter_by_matching_statuses(['clear'],
                                          self.__test_weathers))
        self.assertFalse(weatherutils.filter_by_matching_statuses(['test'],
                                          self.__test_weathers))


    def test_find_closest_weather(self):
        time_1 = 1379361300L
        time_2 = 1379050800L
        self.assertEqual(self.__test_weather_sun, 
                         weatherutils.find_closest_weather(self.__test_weathers,
                                                           time_1))
        self.assertEqual(self.__test_weather_rain, 
                         weatherutils.find_closest_weather(self.__test_weathers,
                                                           time_2))

if __name__ == "__main__":
    unittest.main()