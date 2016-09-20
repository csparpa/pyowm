"""
Test case for forecaster.py module
"""

import unittest
from datetime import datetime
from pyowm.webapi25.location import Location
from pyowm.webapi25.weather import Weather
from pyowm.webapi25.forecast import Forecast
from pyowm.webapi25.forecaster import Forecaster
from pyowm.utils.timeformatutils import UTC


class TestForecaster(unittest.TestCase):

    __test_time_1 = 1379090800
    __test_start_coverage_iso = "2013-09-13 16:46:40+00"
    __test_date_start_coverage = datetime.strptime(__test_start_coverage_iso,
                               '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
    __test_middle_1_coverage = 1379226100
    __test_middle_1_coverage_iso = "2013-09-15 06:21:40+00"
    __test_date_middle_1_coverage = datetime.strptime(__test_middle_1_coverage_iso,
                              '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
    __test_time_2 = 1379361400
    __test_middle_2_coverage_iso = "2013-09-16 19:56:40+00"
    __test_date_middle_2_coverage = datetime.strptime(__test_middle_2_coverage_iso,
                              '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
    __test_end_coverage = 1379902600
    __test_end_coverage_iso = "2013-09-23 02:16:40+00"
    __test_date_end_coverage = datetime.strptime(__test_end_coverage_iso,
                                '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())

    __test_location = Location('test', 12.3, 43.7, 987, 'IT')

    __test_weather_rainsnow = Weather(__test_time_1, 1378496400, 1378449600,
              67, {"all": 30}, {"all": 1}, {"deg": 252.002, "speed": 4.100},
              57, {"press": 1030.119, "sea_level": 1038.589},
            {"temp": 294.199, "temp_kf": -1.899, "temp_max": 296.098,
                "temp_min": 294.199
            },
            "Rain", "Light rain", 500, "10d", 1000, 300.0, 298.0, 296.0)
    __test_weather_clouds = Weather(__test_middle_1_coverage, 1378496480,
                                    1378449510, 23,
            {"all": 0}, {}, {"deg": 103.4, "speed": 1.2}, 12,
            {"press": 1070.119, "sea_level": 1078.589},
            {"temp": 297.199, "temp_kf": -1.899, "temp_max": 299.0,
             "temp_min": 295.6
             },
            "Clouds", "Overcast clouds", 804, "02d", 1000, 300.0, 298.0, 296.0)
    __test_weather_sun_1 = Weather(__test_time_2, 1378496480, 1378449510, 5,
            {"all": 0}, {}, {"deg": 103.4, "speed": 1.2}, 12,
            {"press": 1090.119, "sea_level": 1078.589},
            {"temp": 299.199, "temp_kf": -1.899, "temp_max": 301.0,
             "temp_min": 297.6
             },
            "Clear", "Sky is clear", 800, "01d", 1000, 300.0, 298.0, 296.0)
    __test_weather_sun_2 = Weather(__test_end_coverage, 1378496480, 1378449510,
                                   5,
            {"all": 0}, {}, {"deg": 99.4, "speed": 0.8}, 7,
            {"press": 1091.119, "sea_level": 1079.589},
            {"temp": 299.599, "temp_kf": -1.899, "temp_max": 301.9,
             "temp_min": 298.0
             },
            "Clear", "Sky is clear", 800, "01d", 1000, 300.0, 298.0, 296.0)

    __test_weather_storm = Weather(__test_end_coverage, 1378496480, 1378449510,
                                   5,
            {"all": 0}, {}, {"deg": 99.4, "speed": 0.8}, 7,
            {"press": 1071.119, "sea_level": 1059.589},
            {"temp": 299.599, "temp_kf": -1.899, "temp_max": 301.9,
             "temp_min": 298.0
             },
            "Storm", "Violent storm", 961, "01d", 1000, 300.0, 298.0, 296.0)

    __test_weather_hurricane = Weather(__test_end_coverage, 1378496480, 1378449510,
                                   5,
            {"all": 0}, {}, {"deg": 99.4, "speed": 0.8}, 7,
            {"press": 1071.119, "sea_level": 1059.589},
            {"temp": 299.599, "temp_kf": -1.899, "temp_max": 301.9,
             "temp_min": 298.0
             },
            "Hurricane", "Hurricane", 962, "01d", 1000, 300.0, 298.0, 296.0)

    __test_none_values = Weather(__test_end_coverage, 1378496480, 1378449510,
             5, {}, {}, {}, 7, {"press": 1091.119, "sea_level": 1079.589},
            {"temp": 299.599, "temp_kf": -1.899},
            "Clear", "Sky is clear", 800, "01d", 1000, 300.0, 298.0, 296.0)
    __test_weathers = [__test_weather_rainsnow, __test_weather_clouds,
                       __test_weather_sun_1, __test_weather_sun_2,
                       __test_weather_storm, __test_weather_hurricane]

    __test_forecast = Forecast("daily", 1379089800, __test_location,
                               __test_weathers)

    __test_instance = Forecaster(__test_forecast)

    def test_getter_returns_expected_data(self):
        self.assertEqual(self.__test_instance.get_forecast(),
                         self.__test_forecast)

    def test_when_starts_returning_different_timeformats(self):
        self.assertEqual(self.__test_instance.when_starts(timeformat='iso'),
                            self.__test_start_coverage_iso)
        self.assertEqual(self.__test_instance.when_starts(timeformat='unix'),
                            self.__test_time_1)
        self.assertEqual(self.__test_instance.when_starts(timeformat='date'),
                         self.__test_date_start_coverage)

    def test_when_ends_returning_different_timeformats(self):
        self.assertEqual(self.__test_instance.when_ends(timeformat='iso'),
                            self.__test_end_coverage_iso)
        self.assertEqual(self.__test_instance.when_ends(timeformat='unix'),
                            self.__test_end_coverage)
        self.assertEqual(self.__test_instance.when_ends(timeformat='date'),
                         self.__test_date_end_coverage)

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

    def test_will_have_storm(self):
        self.assertTrue(self.__test_instance.will_have_storm())

    def test_will_have_tornado(self):
        self.assertFalse(self.__test_instance.will_have_tornado())

    def test_will_have_hurricane(self):
        self.assertTrue(self.__test_instance.will_have_hurricane())

    def test_when_rain(self):
        self.assertEqual([self.__test_weather_rainsnow],
                         self.__test_instance.when_rain())

    def test_when_sun(self):
        self.assertEqual([self.__test_weather_sun_1,
                          self.__test_weather_sun_2],
                         self.__test_instance.when_sun())

    def test_when_clouds(self):
        self.assertEqual([self.__test_weather_clouds],
                         self.__test_instance.when_clouds())

    def test_when_fog(self):
        self.assertFalse(self.__test_instance.when_fog())

    def test_when_snow(self):
        self.assertFalse(self.__test_instance.when_snow())

    def test_when_storm(self):
        self.assertTrue(self.__test_instance.when_storm())

    def test_when_tornado(self):
        self.assertFalse(self.__test_instance.when_tornado())

    def test_when_hurricane(self):
        self.assertTrue(self.__test_instance.when_hurricane())

    def test_will_be_rainy_at(self):
        time_1 = datetime(2013, 9, 13, 16, 47, 0)
        time_2 = 1379226110
        time_3 = "2013-09-16 19:56:50+00"
        self.assertTrue(self.__test_instance.will_be_rainy_at(time_1))
        self.assertFalse(self.__test_instance.will_be_rainy_at(time_2))
        self.assertFalse(self.__test_instance.will_be_rainy_at(time_3))

    def test_will_be_rainy_at_fails_with_bad_parameters(self):
        self.assertRaises(TypeError, Forecaster.will_be_rainy_at,
                          self.__test_instance, 45.7)

    def test_will_be_sunny_at(self):
        time_1 = datetime(2013, 9, 13, 16, 47, 0)
        time_2 = 1379226110
        time_3 = "2013-09-16 19:56:50+00"
        self.assertFalse(self.__test_instance.will_be_sunny_at(time_1))
        self.assertFalse(self.__test_instance.will_be_sunny_at(time_2))
        self.assertTrue(self.__test_instance.will_be_sunny_at(time_3))

    def test_will_be_sunny_at_fails_with_bad_parameters(self):
        self.assertRaises(TypeError, Forecaster.will_be_sunny_at,
                          self.__test_instance, 45.7)

    def test_will_be_snowy_at(self):
        time_1 = datetime(2013, 9, 13, 16, 47, 0)
        time_2 = 1379226110
        time_3 = "2013-09-16 19:56:50+00"
        self.assertFalse(self.__test_instance.will_be_snowy_at(time_1))
        self.assertFalse(self.__test_instance.will_be_snowy_at(time_2))
        self.assertFalse(self.__test_instance.will_be_snowy_at(time_3))

    def test_will_be_snowy_at_fails_with_bad_parameters(self):
        self.assertRaises(TypeError, Forecaster.will_be_snowy_at,
                          self.__test_instance, 45.7)

    def test_will_be_cloudy_at(self):
        time_1 = datetime(2013, 9, 13, 16, 47, 0)
        time_2 = 1379226110
        time_3 = "2013-09-16 19:56:50+00"
        self.assertFalse(self.__test_instance.will_be_cloudy_at(time_1))
        self.assertTrue(self.__test_instance.will_be_cloudy_at(time_2))
        self.assertFalse(self.__test_instance.will_be_cloudy_at(time_3))

    def test_will_be_cloudy_at_fails_with_bad_parameters(self):
        self.assertRaises(TypeError, Forecaster.will_be_cloudy_at,
                          self.__test_instance, 45.7)

    def test_will_be_foggy_at(self):
        time_1 = datetime(2013, 9, 13, 16, 47, 0)
        time_2 = 1379226110
        time_3 = "2013-09-16 19:56:50+00"
        self.assertFalse(self.__test_instance.will_be_foggy_at(time_1))
        self.assertFalse(self.__test_instance.will_be_foggy_at(time_2))
        self.assertFalse(self.__test_instance.will_be_foggy_at(time_3))

    def test_will_be_foggy_at_fails_with_bad_parameters(self):
        self.assertRaises(TypeError, Forecaster.will_be_foggy_at,
                          self.__test_instance, 45.7)

    def test_will_be_stormy_at(self):
        time_1 = datetime(2013, 9, 13, 16, 47, 0)
        time_2 = 1379226110
        time_3 = "2013-09-16 19:56:50+00"
        self.assertFalse(self.__test_instance.will_be_stormy_at(time_1))
        self.assertFalse(self.__test_instance.will_be_stormy_at(time_2))
        self.assertFalse(self.__test_instance.will_be_stormy_at(time_3))

    def test_will_be_stormy_at_fails_with_bad_parameters(self):
        self.assertRaises(TypeError, Forecaster.will_be_stormy_at,
                          self.__test_instance, 45.7)

    def test_will_be_tornado_at(self):
        time_1 = datetime(2013, 9, 13, 16, 47, 0)
        time_2 = 1379226110
        time_3 = "2013-09-16 19:56:50+00"
        self.assertFalse(self.__test_instance.will_be_tornado_at(time_1))
        self.assertFalse(self.__test_instance.will_be_tornado_at(time_2))
        self.assertFalse(self.__test_instance.will_be_tornado_at(time_3))

    def test_will_be_tornado_at_fails_with_bad_parameters(self):
        self.assertRaises(TypeError, Forecaster.will_be_tornado_at,
                          self.__test_instance, 45.7)

    def test_will_be_hurricane_at(self):
        time_1 = datetime(2013, 9, 13, 16, 47, 0)
        time_2 = 1379226110
        time_3 = "2013-09-16 19:56:50+00"
        self.assertFalse(self.__test_instance.will_be_hurricane_at(time_1))
        self.assertFalse(self.__test_instance.will_be_hurricane_at(time_2))
        self.assertFalse(self.__test_instance.will_be_hurricane_at(time_3))

    def test_will_be_hurricane_at_fails_with_bad_parameters(self):
        self.assertRaises(TypeError, Forecaster.will_be_hurricane_at,
                          self.__test_instance, 45.7)





    def test_get_weather_at(self):
        time_1 = datetime(2013, 9, 13, 16, 47, 0)
        time_2 = 1379226110
        time_3 = "2013-09-16 19:56:50+00"
        self.assertEqual(self.__test_instance.get_weather_at(time_1),
                         self.__test_weather_rainsnow)
        self.assertEqual(self.__test_instance.get_weather_at(time_2),
                         self.__test_weather_clouds)
        self.assertEqual(self.__test_instance.get_weather_at(time_3),
                         self.__test_weather_sun_1)

    def test_get_weather_at_fails_with_bad_parameter(self):
        self.assertRaises(TypeError, Forecaster.get_weather_at,
                          self.__test_instance, 45.7)

    def test_most_hot(self):
        self.assertEqual(self.__test_weather_sun_2,
                         self.__test_instance.most_hot())

    def test_most_hot_returning_None(self):
        fcstr = Forecaster(Forecast("daily", 1379089800, self.__test_location,
                                   [self.__test_none_values]))
        self.assertFalse(fcstr.most_hot())

    def test_most_cold(self):
        self.assertEqual(self.__test_weather_rainsnow,
                         self.__test_instance.most_cold())

    def test_most_cold_returning_None(self):
        fcstr = Forecaster(Forecast("daily", 1379089800, self.__test_location,
                                   [self.__test_none_values]))
        self.assertFalse(fcstr.most_hot())

    def test_most_humid(self):
        self.assertEqual(self.__test_weather_rainsnow,
                         self.__test_instance.most_humid())

    def test_most_rainy(self):
        self.assertEqual(self.__test_weather_rainsnow,
                         self.__test_instance.most_rainy())

    def test_most_snowy(self):
        self.assertEqual(self.__test_weather_rainsnow,
                         self.__test_instance.most_snowy())

    def test_most_rainy_returning_None(self):
        fcstr = Forecaster(Forecast("daily", 1379089800, self.__test_location,
                                   [self.__test_none_values]))
        self.assertFalse(fcstr.most_rainy())

    def test_most_windy(self):
        self.assertEqual(self.__test_weather_rainsnow,
                         self.__test_instance.most_windy())

    def test_most_windy_returning_None(self):
        fcstr = Forecaster(Forecast("daily", 1379089800, self.__test_location,
                                   [self.__test_none_values]))
        self.assertFalse(fcstr.most_windy())
