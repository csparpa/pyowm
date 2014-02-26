#!/usr/bin/env python

"""
Test case for weather.py module
"""

import unittest
from pyowm.webapi25.weather import Weather, weather_from_dictionary


class TestWeather(unittest.TestCase):

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
    __test_temperature = {"temp": 294.199, "temp_kf": -1.899,
                          "temp_max": 296.098, "temp_min": 294.199
                          }
    __test_celsius_temperature = {"temp": 21.049, "temp_kf": -1.899,
                                  "temp_max": 22.948, "temp_min": 21.049
                                  }
    __test_fahrenheit_temperature = {"temp": 69.888, "temp_kf": -1.899,
                                     "temp_max": 73.306, "temp_min": 69.888
                                     }
    __test_status = u"Clouds"
    __test_detailed_status = u"Overcast clouds"
    __test_weather_code = 804
    __test_weather_icon_name = u"04d"

    __test_instance = Weather(__test_reference_time, __test_sunset_time,
                              __test_sunrise_time, __test_clouds, __test_rain,
                              __test_snow, __test_wind, __test_humidity,
                              __test_pressure, __test_temperature, __test_status,
                              __test_detailed_status, __test_weather_code,
                              __test_weather_icon_name)

    def test_init_fails_when_negative_data_provided(self):
        self.assertRaises(ValueError, Weather, -9876543210,
              self.__test_sunset_time, self.__test_sunrise_time, self.__test_clouds, 
                self.__test_rain, self.__test_snow, self.__test_wind,
                self.__test_humidity, self.__test_pressure, self.__test_temperature,
                self.__test_status, self.__test_detailed_status,
                self.__test_weather_code, self.__test_weather_icon_name)
        self.assertRaises(ValueError, Weather, self.__test_reference_time,
              -9876543210, self.__test_sunrise_time, self.__test_clouds,
              self.__test_rain, self.__test_snow, self.__test_wind,
              self.__test_humidity, self.__test_pressure, self.__test_temperature,
              self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name)
        self.assertRaises(ValueError, Weather, self.__test_reference_time,
              self.__test_sunset_time, -9876543210, self.__test_clouds,
              self.__test_rain, self.__test_snow, self.__test_wind,
              self.__test_humidity, self.__test_pressure, self.__test_temperature,
              self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name)
        self.assertRaises(ValueError, Weather, self.__test_reference_time,
              self.__test_sunset_time, self.__test_sunrise_time, -45,
              self.__test_rain, self.__test_snow, self.__test_wind,
              self.__test_humidity, self.__test_pressure, self.__test_temperature,
              self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name)
        self.assertRaises(ValueError, Weather, self.__test_reference_time,
              self.__test_sunset_time, self.__test_sunrise_time,
              self.__test_clouds, self.__test_rain, self.__test_snow,
              self.__test_wind, -16, self.__test_pressure, self.__test_temperature,
              self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name)

    def test_from_dictionary(self):
        dict1 = {'clouds': {'all': 92}, 'name': u'London',
                 'coord': {'lat': 51.50853, 'lon': -0.12574},
                 'sys': {'country': u'GB', 'sunset': 1378923812,
                         'sunrise': 1378877413
                         },
                 'weather': [
                 {'main': u'Clouds', 'id': 804, 'icon': u'04d',
                  'description': u'overcastclouds'}
                 ],
                 'cod': 200, 'base': u'gdpsstations', 'dt': 1378895177,
                 'main': {
                      'pressure': 1022,
                      'humidity': 75,
                      'temp_max': 289.82,
                      'temp': 288.44,
                      'temp_min': 287.59
                  },
                  'id': 2643743,
                  'wind': {'gust': 2.57, 'speed': 1.54, 'deg': 31}
        }
        dict2 = {"dt": 1378897200,
                   "temp": {"day": 289.37, "min": 284.88, "max": 289.37,
                            "night": 284.88, "eve": 287.53, "morn": 289.37
                            },
                   "pressure": 1025.35,
                   "humidity": 71,
                   "weather": [
                   {"id": 500, "main": u"Rain", "description": u"light rain",
                    "icon": u"u10d"}
                   ], "speed": 3.76, "deg": 338, "clouds": 48, "rain": 3
                }
        result1 = weather_from_dictionary(dict1)
        self.assertTrue(isinstance(result1, Weather))
        self.assertNotIn(None, result1.__dict__.values())
        result2 = weather_from_dictionary(dict2)
        self.assertTrue(isinstance(result2, Weather))
        self.assertNotIn(None, result2.__dict__.values())

    def test_getters_return_expected_data(self):
        self.assertEqual(self.__test_instance.get_reference_time(),
                         self.__test_reference_time)
        self.assertEqual(self.__test_instance.get_sunset_time(),
                         self.__test_sunset_time)
        self.assertEqual(self.__test_instance.get_sunrise_time(),
                         self.__test_sunrise_time)
        self.assertEqual(self.__test_instance.get_clouds(),
                         self.__test_clouds)
        self.assertEqual(self.__test_instance.get_rain(),
                         self.__test_rain)
        self.assertEqual(self.__test_instance.get_snow(),
                         self.__test_snow)
        self.assertEqual(self.__test_instance.get_wind(),
                         self.__test_wind)
        self.assertEqual(self.__test_instance.get_humidity(),
                         self.__test_humidity)
        self.assertEqual(self.__test_instance.get_pressure(),
                         self.__test_pressure)
        self.assertEqual(self.__test_instance.get_temperature(),
                         self.__test_temperature)
        self.assertEqual(self.__test_instance.get_status(),
                         self.__test_status)
        self.assertEqual(self.__test_instance.get_detailed_status(),
                         self.__test_detailed_status)
        self.assertEqual(self.__test_instance.get_weather_code(),
                         self.__test_weather_code)
        self.assertEqual(self.__test_instance.get_weather_icon_name(),
                         self.__test_weather_icon_name)

    def test_get_reference_time_returning_different_formats(self):
        self.assertEqual(self.__test_instance.get_reference_time(timeformat='iso'),
                         self.__test_iso_reference_time)
        self.assertEqual(self.__test_instance.get_reference_time(timeformat='unix'),
                         self.__test_reference_time)

    def test_get_sunset_time_returning_different_formats(self):
        self.assertEqual(self.__test_instance.get_sunset_time(timeformat='iso'),
                         self.__test_iso_sunset_time)
        self.assertEqual(self.__test_instance.get_sunset_time(timeformat='unix'),
                         self.__test_sunset_time)

    def test_get_sunrise_time_returning_different_formats(self):
        self.assertEqual(self.__test_instance.get_sunrise_time(timeformat='iso'),
                         self.__test_iso_sunrise_time)
        self.assertEqual(self.__test_instance.get_sunrise_time(timeformat='unix'),
                         self.__test_sunrise_time)

    def test_get_reference_time_fails_with_unknown_timeformat(self):
        self.assertRaises(ValueError, Weather.get_reference_time,
                          self.__test_instance, 'xyz')

    def test_get_sunset_time_fails_with_unknown_timeformat(self):
        self.assertRaises(ValueError, Weather.get_sunset_time,
                          self.__test_instance, 'xyz')

    def test_get_sunrise_time_fails_with_unknown_timeformat(self):
        self.assertRaises(ValueError, Weather.get_sunrise_time,
                          self.__test_instance, 'xyz')

    def test_returning_different_units_for_temperatures(self):
        result_kelvin = self.__test_instance.get_temperature(unit='kelvin')
        result_celsius = self.__test_instance.get_temperature(unit='celsius')
        result_fahrenheit = self.__test_instance.get_temperature(
                                                             unit='fahrenheit')
        for item in self.__test_temperature:
            self.assertAlmostEqual(result_kelvin[item],
                                   self.__test_temperature[item], delta=0.1)
            self.assertAlmostEqual(result_celsius[item],
                                   self.__test_celsius_temperature[item],
                                   delta=0.1)
            self.assertAlmostEqual(result_fahrenheit[item],
                                   self.__test_fahrenheit_temperature[item],
                                   delta=0.1)

    def test_get_temperature_fails_with_unknown_units(self):
        self.assertRaises(ValueError, Weather.get_temperature,
                          self.__test_instance, 'xyz')

    def test_JSON_dump(self):
        expectedOutput = '{"status": "Clouds", "weather_code": 804, "rain": ' \
            '{"all": 20}, "snow": {"all": 0}, "pressure": {"press": 1030.119, ' \
            '"sea_level": 1038.589}, "sunrise_time": 1378449600, ' \
            '"weather_icon_name": "04d", "clouds": 67, "temperature": {"temp_kf":' \
            ' -1.899, "temp_min": 294.199, "temp": 294.199, "temp_max": 296.098},' \
            ' "detailed_status": "Overcast clouds", "reference_time": 1378459200, ' \
            '"sunset_time": 1378496400, "humidity": 57, "wind": {"speed": 1.1, ' \
            '"deg": 252.002}}'
        self.assertEqual(self.__test_instance.to_JSON(), expectedOutput)

    def test_XML_dump(self):
        expectedOutput = "<?xml version='1.0' encoding='utf8'?>\n<weather>" \
            "<status>Clouds</status><weather_code>804</weather_code>" \
            "<rain><all>20</all></rain><snow><all>0</all></snow>" \
            "<pressure><press>1030.119</press>" \
            "<sea_level>1038.589</sea_level></pressure>" \
            "<sunrise_time>1378449600</sunrise_time>" \
            "<weather_icon_name>04d</weather_icon_name><clouds>67</clouds>" \
            "<temperature><temp_kf>-1.899</temp_kf>" \
            "<temp_min>294.199</temp_min><temp>294.199</temp>" \
            "<temp_max>296.098</temp_max></temperature>" \
            "<detailed_status>Overcast clouds</detailed_status>" \
            "<reference_time>1378459200</reference_time>" \
            "<sunset_time>1378496400</sunset_time><humidity>57</humidity>" \
            "<wind><speed>1.1</speed><deg>252.002</deg></wind></weather>"
        self.assertEqual(self.__test_instance.to_XML(), expectedOutput)

if __name__ == "__main__":
    unittest.main()
