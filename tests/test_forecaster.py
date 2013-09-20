#!/usr/bin/env python

"""
Test case for forecaster.py module
"""

import unittest
from pyowm import Location
from pyowm import Weather
from pyowm import Forecast
from pyowm import Forecaster

class TestForecaster(unittest.TestCase):

    __test_start_coverage = 1379090800L
    __test_start_coverage_iso = "2013-09-13 16:46:40+00"
    __test_middle_1_coverage = 1379226100L
    __test_middle_1_coverage_iso = "2013-09-15 06:21:40+00"
    __test_middle_2_coverage = 1379361400L
    __test_middle_2_coverage_iso = "2013-09-16 19:56:40+00"
    __test_end_coverage = 1379902600L
    __test_end_coverage_iso = "2013-09-23 02:16:40+00"
    
    __test_location = Location(u'test', 12.3, 43.7, 987, u'IT')
    
    __test_weather_rain = Weather(__test_start_coverage, 1378496400, 1378449600, 67, 
            {"all": 30}, {"all": 0}, {"deg": 252.002, "speed": 4.100}, 57, 
            {"press": 1030.119, "sea_level": 1038.589},
            {"temp": 294.199, "temp_kf": -1.899, "temp_max": 296.098, 
                "temp_min": 294.199
            },
            u"Rain", u"Light rain", 500, u"10d")
    __test_weather_clouds = Weather(__test_middle_1_coverage, 1378496480, 1378449510, 23, 
            {"all": 0}, {"all": 0}, {"deg": 103.4, "speed": 1.2}, 12, 
            {"press": 1070.119, "sea_level": 1078.589},
            {"temp": 297.199, "temp_kf": -1.899, "temp_max": 299.0, 
             "temp_min": 295.6
             },
            u"Clouds", u"Overcast clouds", 804, u"02d")
    __test_weather_sun_1 = Weather(__test_middle_2_coverage, 1378496480, 1378449510, 5, 
            {"all": 0}, {"all": 0}, {"deg": 103.4, "speed": 1.2}, 12, 
            {"press": 1090.119, "sea_level": 1078.589},
            {"temp": 299.199, "temp_kf": -1.899, "temp_max": 301.0, 
             "temp_min": 297.6
             },
            u"Clear", u"Sky is clear", 800, u"01d")
    __test_weather_sun_2 = Weather(__test_end_coverage, 1378496480, 1378449510, 5, 
            {"all": 0}, {"all": 0}, {"deg": 99.4, "speed": 0.8}, 7, 
            {"press": 1091.119, "sea_level": 1079.589},
            {"temp": 299.599, "temp_kf": -1.899, "temp_max": 301.9, 
             "temp_min": 298.0
             },
            u"Clear", u"Sky is clear", 800, u"01d")
    __test_weathers = [ __test_weather_rain, __test_weather_clouds, 
                       __test_weather_sun_1, __test_weather_sun_2 ]
    
    __test_forecast = Forecast("daily", 1379089800L, __test_location,
                               __test_weathers)
    
    __test_instance = Forecaster(__test_forecast)

    def test_getter_returns_expected_data(self):
        self.assertEqual(self.__test_instance.get_forecast(), self.__test_forecast)
      
    def test_when_starts_returning_different_timeformats(self):
        """
        Test forecaster.when_starts return timestamps in the expected formats
        """
        self.assertEqual(self.__test_instance.when_starts(timeformat='iso'),
                            self.__test_start_coverage_iso)
        self.assertEqual(self.__test_instance.when_starts(timeformat='unix'),
                            self.__test_start_coverage)
        
    def test_when_ends_returning_different_timeformats(self):
        """
        Test forecaster.when_ends return timestamps in the expected formats
        """
        self.assertEqual(self.__test_instance.when_ends(timeformat='iso'),
                            self.__test_end_coverage_iso)
        self.assertEqual(self.__test_instance.when_ends(timeformat='unix'),
                            self.__test_end_coverage)

    def test_status_matches_any(self):
        self.assertTrue(self.__test_instance.status_matches_any(['rain'],
                                                    self.__test_weather_rain))
        self.assertFalse(self.__test_instance.status_matches_any(['sunnyday'],
                                                    self.__test_weather_rain))

    def test_statuses_match_any(self):
        self.assertTrue(self.__test_instance.statuses_match_any(['rain'],
                                                    self.__test_weathers))
        self.assertFalse(self.__test_instance.statuses_match_any(['sandstorm'],
                                                    self.__test_weathers))

    def test_will_have_rain(self):
        self.assertTrue(self.__test_instance.will_have_rain())
        
    def test_will_have_sun(self):
        self.assertTrue(self.__test_instance.will_have_sun())
        
    def test_will_have_clouds(self):
        self.assertTrue(self.__test_instance.will_have_clouds())
        
    def test_will_have_fog(self):
        self.assertFalse(self.__test_instance.will_have_fog())
        
    def test_will_have_snow(self):
        self.assertFalse(self.__test_instance.will_have_snow())
        
    def test_when_rain(self):
        self.assertEqual([self.__test_weather_rain],
                         self.__test_instance.when_rain())
        
    def test_when_sun(self):
        self.assertEqual([self.__test_weather_sun_1, self.__test_weather_sun_2],
                         self.__test_instance.when_sun())

    def test_when_clouds(self):
        self.assertEqual([self.__test_weather_clouds], 
                         self.__test_instance.when_clouds())

    def test_when_fog(self):
        self.assertFalse(self.__test_instance.when_fog())
    
    def test_when_snow(self):
        self.assertFalse(self.__test_instance.when_snow())

if __name__ == "__main__":
    unittest.main()