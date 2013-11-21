#!/usr/bin/env python

"""
Test case for forecast.py module
"""

import unittest
from pyowm.webapi25.location import Location
from pyowm.webapi25.weather import Weather
from pyowm.webapi25.forecast import Forecast

class TestForecast(unittest.TestCase):

    __test_reception_time = 1234567L
    __test_iso_reception_time = "1970-01-15 06:56:07+00"
    __test_location = Location(u'test', 12.3, 43.7, 987, u'IT')
    __test_weathers = [ Weather(1378459200, 1378496400, 1378449600, 67, 
            {"all": 20}, {"all": 0}, {"deg": 252.002, "speed": 1.100}, 57, 
            {"press": 1030.119, "sea_level": 1038.589},
            {"temp": 294.199, "temp_kf": -1.899, "temp_max": 296.098, 
                "temp_min": 294.199
            },
            u"Clouds", u"Overcast clouds", 804, u"04d"),
           Weather(1378459690, 1378496480, 1378449510, 23, {"all": 10},
            {"all": 0}, {"deg": 103.4, "speed": 4.2}, 12, 
            {"press": 1070.119, "sea_level": 1078.589},
            {"temp": 297.199, "temp_kf": -1.899, "temp_max": 299.0, 
             "temp_min": 295.6
             },
            u"Clear", u"Sky is clear", 804, u"02d")
       ]
    __test_n_weathers = len(__test_weathers)
    __test_instance = Forecast("daily", __test_reception_time, __test_location,
                               __test_weathers)

    def test_init_fails_when_reception_time_is_negative(self):
        self.assertRaises(ValueError, Forecast, "3h", -1234567L, 
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

    def test_JSON_dump(self):
        """
        Test correct object data dump to a JSON string
        """
        expected_output = '{"reception_time": 1234567, "interval": "daily", ' \
            '"Location": {"country": "IT", "name": "test", "coordinates": {"lat":' \
            ' 43.7, "lon": 12.3}, "ID": 987}, "weathers": [{"status": "Clouds", ' \
            '"clouds": 67, ' \
            '"temperature": {"temp_kf": -1.899, "temp_max": 296.098, "temp": ' \
            '294.199, "temp_min": 294.199}, "detailed_status": "Overcast clouds"' \
            ', "reference_time": 1378459200, "weather_code": 804, "snow": {"all":' \
            ' 0}, "rain": {"all": 20}, "weather_icon_name": "04d", "pressure": ' \
            '{"press": 1030.119, "sea_level": 1038.589}, "sunrise_time": 1378449600,' \
            ' "sunset_time": 1378496400, "humidity": 57, "wind": {"speed": 1.1, ' \
            '"deg": 252.002}}, {"status": "Clear", "clouds": 23, "temperature": ' \
            '{"temp_kf": -1.899, "temp_max": 299.0, "temp": 297.199, "temp_min": ' \
            '295.6}, "detailed_status": "Sky is clear", "reference_time": 1378459690,' \
            ' "weather_code": 804, "snow": {"all": 0}, "rain": {"all": 10}, ' \
            '"weather_icon_name": "02d", "pressure": {"press": 1070.119, "sea_level":' \
            ' 1078.589}, "sunrise_time": 1378449510, "sunset_time": 1378496480, ' \
            '"humidity": 12, "wind": {"speed": 4.2, "deg": 103.4}}]}'
        self.assertEqual(expected_output, self.__test_instance.to_JSON())
        
    def test_XML_dump(self):
        """
        Test correct object data dump to an XML string
        """
        expectedOutput = '<Forecast><interval>daily</interval><reception_time>' \
            '1234567</reception_time><Location><name>test</name><coordinates>' \
            '<lon>12.3</lon><lat>43.7</lat></coordinates><ID>987</ID><country>IT</country></Location>' \
            '<weathers><Weather><status>Clouds</status><weather_code>804</weather_code>' \
            '<rain><all>20</all></rain><snow><all>0</all></snow><pressure>' \
            '<press>1030.119</press><sea_level>1038.589</sea_level></pressure>' \
            '<sunrise_time>1378449600</sunrise_time><weather_icon_name>04d' \
            '</weather_icon_name><clouds>67</clouds><temperature><temp_kf>-1.899' \
            '</temp_kf><temp_min>294.199</temp_min><temp>294.199</temp><temp_max>' \
            '296.098</temp_max></temperature><detailed_status>Overcast clouds' \
            '</detailed_status><reference_time>1378459200</reference_time>' \
            '<sunset_time>1378496400</sunset_time><humidity>57</humidity><wind>' \
            '<speed>1.1</speed><deg>252.002</deg></wind></Weather><Weather>' \
            '<status>Clear</status><weather_code>804</weather_code><rain><all>10' \
            '</all></rain><snow><all>0</all></snow><pressure><press>1070.119' \
            '</press><sea_level>1078.589</sea_level></pressure><sunrise_time>' \
            '1378449510</sunrise_time><weather_icon_name>02d</weather_icon_name>' \
            '<clouds>23</clouds><temperature><temp_kf>-1.899</temp_kf><temp_min>' \
            '295.6</temp_min><temp>297.199</temp><temp_max>299.0</temp_max>' \
            '</temperature><detailed_status>Sky is clear</detailed_status>' \
            '<reference_time>1378459690</reference_time><sunset_time>1378496480' \
            '</sunset_time><humidity>12</humidity><wind><speed>4.2</speed><deg>' \
            '103.4</deg></wind></Weather></weathers></Forecast>'
        self.assertEqual(expectedOutput, self.__test_instance.to_XML())

if __name__ == "__main__":
    unittest.main()