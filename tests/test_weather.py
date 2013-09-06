#!/usr/bin/env python

"""
Test case for weather.py module
"""

import unittest
from pyowm import Weather


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
    __test_pressure = {"pressure": 1030.119, "sea_level": 1038.589}
    __test_temperature = {"temp": 294.199, "temp_kf": -1.899, "temp_max": 296.098, 
                       "temp_min": 294.199}
    __test_status = "Clouds"
    __test_detailed_status = "Overcast clouds"
    __test_weather_code = 804
    __test_weather_icon_name = "04d"
    
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
        
        self.assertEqual(instance.get_reference_time(), self.__test_reference_time, "")
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
                
        self.assertEqual(instance.get_reference_time(timeformat='iso'), self.__test_iso_reference_time, "")
        self.assertEqual(instance.get_reference_time(timeformat='unix'), self.__test_reference_time, "")
        self.assertEqual(instance.get_sunset_time(timeformat='iso'), self.__test_iso_sunset_time, "")
        self.assertEqual(instance.get_sunset_time(timeformat='unix'), self.__test_sunset_time, "")
        self.assertEqual(instance.get_sunrise_time(timeformat='iso'), self.__test_iso_sunrise_time, "")
        self.assertEqual(instance.get_sunrise_time(timeformat='unix'), self.__test_sunrise_time, "")


    def test_time_related_methods_fai_with_unknown_time_formats(self):
        instance = self.__test_instance
        self.assertRaises(ValueError, Weather.get_reference_time, instance, 'xyz')
        self.assertRaises(ValueError, Weather.get_sunset_time, instance, 'xyz')
        self.assertRaises(ValueError, Weather.get_sunrise_time, instance, 'xyz')
        
    #def test_returning_different_units_for_temperatures(self):
    #    self.fail('Not yet implemented')

    #def test_get_temperature_fails_with_unknown_units(self):
    #    self.fail('Not yet implemented')
    
    #def test_XML_dump()
    #    self.fail('Not yet implemented')
    
    #def test_JSON_dump()
    #    self.fail('Not yet implemented')
    
if __name__ == "__main__":
    unittest.main()