#!/usr/bin/env python

"""
Test case for weather.py module
"""

import unittest
from pyowm import Weather
from pyowm.utils import xmlutils


class Test(unittest.TestCase):

    __test_reference_time = 1378459200
    __test_iso_reference_time = "2013-09-06 09:20:00+00"    
    __test_sunset_time = 1378496400
    __test_iso_sunset_time = "2013-09-06 19:40:00+00"
    __test_sunrise_time = 1378449600
    __test_iso_sunrise_time = "2013-09-06 06:40:00+00"
    __test_clouds = 67
    __test_rain = {"all": 20}
    __test_snow = {"all": 0}
    __test_wind = {"deg": 252.002, "speed": 1.100}
    __test_humidity = 57
    __test_pressure = {"press": 1030.119, "sea_level": 1038.589}
    __test_temperature = {"temp": 294.199, "temp_kf": -1.899, "temp_max": 296.098, 
                       "temp_min": 294.199}
    __test_celsius_temperature = {"temp": 21.049, "temp_kf": -1.899, "temp_max": 22.948, 
                       "temp_min": 21.049}
    __test_fahrenheit_temperature = {"temp": 69.888, "temp_kf": -1.899, "temp_max": 73.306, 
                       "temp_min": 69.888}
    __test_status = u"Clouds"
    __test_detailed_status = u"Overcast clouds"
    __test_weather_code = 804
    __test_weather_icon_name = u"04d"
    
    __test_instance = Weather(__test_reference_time, __test_sunset_time, __test_sunrise_time, 
                         __test_clouds, __test_rain,  __test_snow, __test_wind,
                         __test_humidity, __test_pressure, __test_temperature, 
                         __test_status, __test_detailed_status, __test_weather_code,
                         __test_weather_icon_name)

    def test_init_fails_when_negative_data_provided(self):
        """
        Test failure when providing negative: referenceTime, sunset, sunrise,
        clouds and humidity 
        """
        self.assertRaises(ValueError, Weather, -9876543210, 
              self.__test_sunset_time, self.__test_sunrise_time, self.__test_clouds, self.__test_rain,
              self.__test_snow, self.__test_wind, self.__test_humidity, self.__test_pressure,
              self.__test_temperature, self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name)
        self.assertRaises(ValueError, Weather, self.__test_reference_time, 
              -9876543210, self.__test_sunrise_time, self.__test_clouds, self.__test_rain,
              self.__test_snow, self.__test_wind, self.__test_humidity, self.__test_pressure,
              self.__test_temperature, self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name)
        self.assertRaises(ValueError, Weather, self.__test_reference_time, 
              self.__test_sunset_time, -9876543210, self.__test_clouds, self.__test_rain,
              self.__test_snow, self.__test_wind, self.__test_humidity, self.__test_pressure,
              self.__test_temperature, self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name)
        self.assertRaises(ValueError, Weather, self.__test_reference_time, 
              self.__test_sunset_time, self.__test_sunrise_time, -45, self.__test_rain,
              self.__test_snow, self.__test_wind, self.__test_humidity, self.__test_pressure,
              self.__test_temperature, self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name)
        self.assertRaises(ValueError, Weather, self.__test_reference_time, 
              self.__test_sunset_time, self.__test_sunrise_time, self.__test_clouds, self.__test_rain,
              self.__test_snow, self.__test_wind, -16, self.__test_pressure,
              self.__test_temperature, self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name)

    def test_getters_return_expected_data(self):
        """
        Test getters do their job
        """
        instance = self.__test_instance
        
        self.assertEqual(instance.get_reception_time(), self.__test_reference_time, "")
        self.assertEqual(instance.get_sunset_time(), self.__test_sunset_time, "")
        self.assertEqual(instance.get_sunrise_time(), self.__test_sunrise_time, "")
        self.assertEqual(instance.get_clouds(), self.__test_clouds, "")
        self.assertEqual(instance.get_rain(), self.__test_rain, "")
        self.assertEqual(instance.get_snow(), self.__test_snow, "")
        self.assertEqual(instance.get_wind(), self.__test_wind, "")
        self.assertEqual(instance.get_humidity(), self.__test_humidity, "")
        self.assertEqual(instance.get_pressure(), self.__test_pressure, "")
        self.assertEqual(instance.get_temperature(), self.__test_temperature, "")
        self.assertEqual(instance.get_status(), self.__test_status, "")
        self.assertEqual(instance.get_detailed_status(), self.__test_detailed_status, "")
        self.assertEqual(instance.get_weather_code(), self.__test_weather_code, "")
        self.assertEqual(instance.get_weather_icon_name(), self.__test_weather_icon_name, "")

    def test_returning_different_formats_for_times(self):
        """
        Test time-related methods return timestamps in the expected formats
        """
        instance = self.__test_instance
                
        self.assertEqual(instance.get_reception_time(timeformat='iso'), self.__test_iso_reference_time, "")
        self.assertEqual(instance.get_reception_time(timeformat='unix'), self.__test_reference_time, "")
        self.assertEqual(instance.get_sunset_time(timeformat='iso'), self.__test_iso_sunset_time, "")
        self.assertEqual(instance.get_sunset_time(timeformat='unix'), self.__test_sunset_time, "")
        self.assertEqual(instance.get_sunrise_time(timeformat='iso'), self.__test_iso_sunrise_time, "")
        self.assertEqual(instance.get_sunrise_time(timeformat='unix'), self.__test_sunrise_time, "")

    def test_time_related_methods_fai_with_unknown_time_formats(self):
        """
        Test time-related methods fail when provided with unknown time formats
        """
        instance = self.__test_instance
        self.assertRaises(ValueError, Weather.get_reception_time, instance, 'xyz')
        self.assertRaises(ValueError, Weather.get_sunset_time, instance, 'xyz')
        self.assertRaises(ValueError, Weather.get_sunrise_time, instance, 'xyz')
        
    def test_returning_different_units_for_temperatures(self):
        """
        Test get_temperature return temperatures in the expected units
        """
        result_kelvin = self.__test_instance.get_temperature(unit='kelvin')
        result_celsius = self.__test_instance.get_temperature(unit='celsius')
        result_fahrenheit = self.__test_instance.get_temperature(unit='fahrenheit')
        
        for item in self.__test_temperature:
            self.assertAlmostEqual(result_kelvin[item], self.__test_temperature[item], delta=0.1)
            self.assertAlmostEqual(result_celsius[item], self.__test_celsius_temperature[item], delta=0.1)
            self.assertAlmostEqual(result_fahrenheit[item], self.__test_fahrenheit_temperature[item], delta=0.1)
        
    def test_get_temperature_fails_with_unknown_units(self):
        self.assertRaises(ValueError, Weather.get_temperature, self.__test_instance, 'xyz')
    
    def test_JSON_dump(self):
        """
        Test correct object data dump to a JSON string
        """
        expectedOutput = """{"status": "Clouds", "weather_code": 804, "rain": {"all": 20}, "snow": {"all": 0}, "pressure": {"press": 1030.119, "sea_level": 1038.589}, "sunrise_time": 1378449600, "weather_icon_name": "04d", "clouds": 67, "temperature": {"temp_kf": -1.899, "temp_min": 294.199, "temp": 294.199, "temp_max": 296.098}, "detailed_status": "Overcast clouds", "reference_time": 1378459200, "sunset_time": 1378496400, "humidity": 57, "wind": {"speed": 1.1, "deg": 252.002}}"""
        self.assertEqual(self.__test_instance.to_JSON(), expectedOutput, "")
    
    def test_XML_dump(self):
        """
        Test correct object data dump to an XML string
        """
        expectedOutput = """<Weather><status>%s</status><weather_code>%s</weather_code><rain>%s</rain><snow>%s</snow><pressure>%s</pressure><sunrise_time>%s</sunrise_time><weather_icon_name>%s</weather_icon_name><clouds>%s</clouds><temperature>%s</temperature><detailed_status>%s</detailed_status><reference_time>%s</reference_time><sunset_time>%s</sunset_time><humidity>%s</humidity><wind>%s</wind></Weather>""" % (self.__test_status,
            self.__test_weather_code, xmlutils.dict_to_XML(self.__test_rain), 
            xmlutils.dict_to_XML(self.__test_snow), xmlutils.dict_to_XML(self.__test_pressure),
            self.__test_sunrise_time, self.__test_weather_icon_name, self.__test_clouds, 
            xmlutils.dict_to_XML(self.__test_temperature), self.__test_detailed_status, 
            self.__test_reference_time, self.__test_sunset_time, self.__test_humidity, 
            xmlutils.dict_to_XML(self.__test_wind))    
        
        self.assertEqual(self.__test_instance.to_XML(), expectedOutput, "")

if __name__ == "__main__":
    unittest.main()