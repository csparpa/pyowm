#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from pyowm.exceptions.api_response_error import APIResponseError
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.utils.formatting import UTC
from pyowm.weatherapi25.uris import ICONS_BASE_URI
from pyowm.weatherapi25.weather import Weather
from tests.unit.weatherapi25.json_test_dumps import WEATHER_JSON_DUMP
from tests.unit.weatherapi25.json_test_responses import (CITY_WEATHER_HISTORY_JSON, CITY_WEATHER_HISTORY_NO_RESULTS_JSON,
                                                         CITY_WEATHER_HISTORY_NOT_FOUND_JSON, INTERNAL_SERVER_ERROR_JSON)
from datetime import datetime


class TestWeather(unittest.TestCase):

    __test_reference_time = 1378459200
    __test_iso_reference_time = "2013-09-06 09:20:00+00"
    __test_date_reference_time = datetime.strptime(__test_iso_reference_time,
                                   '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
    __test_sunset_time = 1378496400
    __test_iso_sunset_time = "2013-09-06 19:40:00+00"
    __test_sunrise_time = 1378449600
    __test_iso_sunrise_time = "2013-09-06 06:40:00+00"
    __test_clouds = 67
    __test_rain = {"all": 20}
    __test_snow = {"all": 0}
    __test_wind = {"deg": 252.002, "speed": 1.100, "gust": 2.09}
    __test_imperial_wind = {"deg": 252.002, "speed": 2.460634, "gust": 4.6752046}
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
    __test_status = "Clouds"
    __test_detailed_status = "Overcast clouds"
    __test_weather_code = 804
    __test_weather_icon_name = "04d"
    __test_visibility_distance = 1000
    __test_dewpoint = 300.0
    __test_humidex = 298.0
    __test_heat_index = 40.0

    __test_instance = Weather(__test_reference_time, __test_sunset_time,
                              __test_sunrise_time, __test_clouds, __test_rain,
                              __test_snow, __test_wind, __test_humidity,
                              __test_pressure, __test_temperature,
                              __test_status, __test_detailed_status,
                              __test_weather_code, __test_weather_icon_name,
                              __test_visibility_distance, __test_dewpoint,
                              __test_humidex, __test_heat_index)

    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'
    __bad_json_2 = '{"list": [{"test":"fake"}] }'
    __no_items_json = '{"cnt": "0"}'

    def test_init_fails_when_negative_data_provided(self):
        self.assertRaises(ValueError, Weather, -9876543210,
              self.__test_sunset_time, self.__test_sunrise_time, self.__test_clouds,
              self.__test_rain, self.__test_snow, self.__test_wind,
              self.__test_humidity, self.__test_pressure, self.__test_temperature,
              self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name,
              self.__test_visibility_distance, self.__test_dewpoint,
              self.__test_humidex, self.__test_heat_index)
        self.assertRaises(ValueError, Weather, self.__test_reference_time,
              self.__test_sunset_time, self.__test_sunrise_time, -45,
              self.__test_rain, self.__test_snow, self.__test_wind,
              self.__test_humidity, self.__test_pressure, self.__test_temperature,
              self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name,
              self.__test_visibility_distance, self.__test_dewpoint,
              self.__test_humidex, self.__test_heat_index)
        self.assertRaises(ValueError, Weather, self.__test_reference_time,
              self.__test_sunset_time, self.__test_sunrise_time,
              self.__test_clouds, self.__test_rain, self.__test_snow,
              self.__test_wind, -16, self.__test_pressure, self.__test_temperature,
              self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name,
              self.__test_visibility_distance, self.__test_dewpoint,
              self.__test_humidex, self.__test_heat_index)
        self.assertRaises(ValueError, Weather, self.__test_reference_time,
              self.__test_sunset_time, self.__test_sunrise_time,
              self.__test_clouds, self.__test_rain, self.__test_snow,
              self.__test_wind, self.__test_humidity,
              self.__test_pressure, self.__test_temperature,
              self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name,
              -12, self.__test_dewpoint,
              self.__test_humidex, self.__test_heat_index)
        self.assertRaises(ValueError, Weather, self.__test_reference_time,
              self.__test_sunset_time, self.__test_sunrise_time,
              self.__test_clouds, self.__test_rain, self.__test_snow,
              self.__test_wind, self.__test_humidity,
              self.__test_pressure, self.__test_temperature,
              self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name,
              self.__test_visibility_distance, self.__test_dewpoint,
              -10.0, self.__test_heat_index)
        self.assertRaises(ValueError, Weather, self.__test_reference_time,
              self.__test_sunset_time, self.__test_sunrise_time,
              self.__test_clouds, self.__test_rain, self.__test_snow,
              self.__test_wind, self.__test_humidity,
              self.__test_pressure, self.__test_temperature,
              self.__test_status, self.__test_detailed_status,
              self.__test_weather_code, self.__test_weather_icon_name,
              self.__test_visibility_distance, self.__test_dewpoint,
              self.__test_humidex, -10.0)

    def test_init_when_wind_is_none(self):
        instance = Weather(self.__test_reference_time,
                           self.__test_sunset_time, self.__test_sunrise_time,
                           self.__test_clouds,
                           self.__test_rain, self.__test_snow,
                           None,
                           self.__test_humidity, self.__test_pressure,
                           self.__test_temperature,
                           self.__test_status, self.__test_detailed_status,
                           self.__test_weather_code,
                           self.__test_weather_icon_name,
                           self.__test_visibility_distance,
                           self.__test_dewpoint,
                           self.__test_humidex, self.__test_heat_index)

        self.assertIsNone(instance.wind())

    def test_init_stores_negative_sunset_time_as_none(self):
        instance = Weather(self.__test_reference_time,
                          -9876543210, self.__test_sunrise_time,
                          self.__test_clouds,
                          self.__test_rain, self.__test_snow, self.__test_wind,
                          self.__test_humidity, self.__test_pressure,
                          self.__test_temperature,
                          self.__test_status, self.__test_detailed_status,
                          self.__test_weather_code,
                          self.__test_weather_icon_name,
                          self.__test_visibility_distance, self.__test_dewpoint,
                          self.__test_humidex, self.__test_heat_index)
        self.assertIsNone(instance.sunset_time())

    def test_init_stores_negative_sunrise_time_as_none(self):
        instance = Weather(self.__test_reference_time,
                          self.__test_sunset_time, -9876543210, self.__test_clouds,
                          self.__test_rain, self.__test_snow, self.__test_wind,
                          self.__test_humidity, self.__test_pressure,
                          self.__test_temperature,
                          self.__test_status, self.__test_detailed_status,
                          self.__test_weather_code, self.__test_weather_icon_name,
                          self.__test_visibility_distance, self.__test_dewpoint,
                          self.__test_humidex, self.__test_heat_index)
        self.assertIsNone(instance.sunrise_time())

    def test_from_dict(self):
        dict1 = {'clouds': {'all': 92}, 'name': 'London',
                 'coord': {'lat': 51.50853, 'lon': -0.12574},
                 'sys': {'country': 'GB', 'sunset': 1378923812,
                         'sunrise': 1378877413
                         },
                 'weather': [
                 {'main': 'Clouds', 'id': 804, 'icon': '04d',
                  'description': 'overcastclouds'}
                 ],
                 'cod': 200, 'base': 'gdpsstations', 'dt': 1378895177,
                 'main': {
                      'pressure': 1022,
                      'humidity': 75,
                      'temp_max': 289.82,
                      'temp': 288.44,
                      'temp_min': 287.59
                  },
                  'id': 2643743,
                  'wind': {'gust': 2.57, 'speed': 1.54, 'deg': 31},
                  'visibility': {'distance': 1000},
                  'calc':{
                      'dewpoint': 300.0,
                      'humidex': 298.0,
                      'heatindex': 296.0
                  }
        }
        dict2 = {"dt": 1378897200,
                   "temp": {"day": 289.37, "min": 284.88, "max": 289.37,
                            "night": 284.88, "eve": 287.53, "morn": 289.37
                            },
                   "pressure": 1025.35,
                   "humidity": 71,
                   "weather": [
                   {"id": 500, "main": "Rain", "description": "light rain",
                    "icon": "u10d"}
                   ], "speed": 3.76, "deg": 338, "clouds": 48, "rain": 3
                }
        dict3 = {"station":{
                    "name":"KPPQ",
                    "type":1,
                    "status":50,
                    "id":1000,
                    "coord":{"lon":-90.47,"lat":39.38}
                },
                "last":{
                    "main":{
                        "temp":276.15,
                        "pressure":1031},
                        "wind":{
                            "speed":3.1,
                            "deg":140
                        },
                        "visibility":{
                            "distance":11265,
                            "prefix":0
                        },
                        "calc":{
                            "dewpoint":273.15
                        },
                        "clouds":[
                            {"distance":427,
                             "condition":"SCT"}
                        ],
                        "dt":1417977300
                },
                "params":["temp","pressure","wind","visibility"]
        }
        result1 = Weather.from_dict(dict1)
        self.assertTrue(isinstance(result1, Weather))
        self.assertTrue(all(v is not None for v in result1.__dict__.values()))
        result2 = Weather.from_dict(dict2)
        self.assertTrue(isinstance(result2, Weather))
        self.assertFalse(all(v is not None for v in result2.__dict__.values()))
        result3 = Weather.from_dict(dict3)
        self.assertTrue(isinstance(result3, Weather))

    def test_from_dict_when_data_fields_are_none(self):
        dict1 = {'clouds': {'all': 92}, 'name': 'London',
                 'coord': {'lat': 51.50853, 'lon': -0.12574},
                 'sys': {'country': 'GB', 'sunset': 1378923812,
                         'sunrise': 1378877413
                         },
                 'weather': [
                 {'main': 'Clouds', 'id': 804, 'icon': '04d',
                  'description': 'overcastclouds'}
                 ],
                 'cod': 200, 'base': 'gdpsstations', 'dt': 1378895177,
                 'main': {
                      'pressure': 1022,
                      'humidity': 75,
                      'temp_max': 289.82,
                      'temp': 288.44,
                      'temp_min': 287.59
                  },
                  'id': 2643743,
                  'wind': None,
                  'visibility': {'distance': 1000},
                  'calc':{
                      'dewpoint': 300.0,
                      'humidex': 298.0,
                      'heatindex': 296.0
                  },
                 'rain': None,
                 'snow': None
        }
        result1 = Weather.from_dict(dict1)
        self.assertTrue(isinstance(result1, Weather))
        self.assertEqual(0, len(result1.wind()))
        self.assertEqual(0, len(result1.rain))
        self.assertEqual(0, len(result1.snow))

        dict2 = {"station":{
                    "name":"KPPQ",
                    "type":1,
                    "status":50,
                    "id":1000,
                    "coord":{"lon":-90.47,"lat":39.38}
                },
                "last":{
                    "main":{
                        "temp":276.15,
                        "pressure":1031},
                        "wind":None,
                        "visibility":{
                            "distance":11265,
                            "prefix":0
                        },
                        "calc":{
                            "dewpoint":273.15
                        },
                        "clouds":[
                            {"distance":427,
                             "condition":"SCT"}
                        ],
                        "dt":1417977300
                },
                "params":["temp","pressure","wind","visibility"]
        }
        result2 = Weather.from_dict(dict2)
        self.assertTrue(isinstance(result2, Weather))
        self.assertEqual(0, len(result2.wind()))

    def test_to_dict(self):
        expected = json.loads(WEATHER_JSON_DUMP)
        result = self.__test_instance.to_dict()
        self.assertEqual(expected, result)

    def test_from_dict_of_lists(self):
        result = Weather.from_dict_of_lists(json.loads(CITY_WEATHER_HISTORY_JSON))
        self.assertTrue(result)
        self.assertTrue(isinstance(result, list))
        for weather in result:
            self.assertTrue(weather is not None)

    def test_from_dict_of_lists_fails_when_JSON_data_is_None(self):
        self.assertRaises(ParseResponseError, Weather.from_dict_of_lists, None)

    def test_from_dict_of_lists_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, Weather.from_dict_of_lists, json.loads(self.__bad_json))
        self.assertRaises(ParseResponseError, Weather.from_dict_of_lists, json.loads(self.__bad_json_2))

    def test_from_dict_of_lists_when_no_results(self):
        result = Weather.from_dict_of_lists(json.loads(CITY_WEATHER_HISTORY_NO_RESULTS_JSON))
        self.assertTrue(isinstance(result, list))
        self.assertEqual(0, len(result))
        result = Weather.from_dict_of_lists(json.loads(self.__no_items_json))
        self.assertTrue(isinstance(result, list))
        self.assertEqual(0, len(result))

    def test_parse_JSON_when_location_not_found(self):
        self.assertFalse(Weather.from_dict_of_lists(json.loads(CITY_WEATHER_HISTORY_NOT_FOUND_JSON)))

    def test_parse_JSON_when_server_error(self):
        self.assertRaises(APIResponseError, Weather.from_dict_of_lists, json.loads(INTERNAL_SERVER_ERROR_JSON))

    def test_reference_time_returning_different_formats(self):
        self.assertEqual(self.__test_instance.reference_time(timeformat='iso'),
                         self.__test_iso_reference_time)
        self.assertEqual(self.__test_instance.reference_time(timeformat='unix'),
                         self.__test_reference_time)
        self.assertEqual(self.__test_instance.reference_time(timeformat='date'),
                         self.__test_date_reference_time)

    def test_sunset_time_returning_different_formats(self):
        self.assertEqual(self.__test_instance.sunset_time(timeformat='iso'),
                         self.__test_iso_sunset_time)
        self.assertEqual(self.__test_instance.sunset_time(timeformat='unix'),
                         self.__test_sunset_time)

    def test_sunrise_time_returning_different_formats(self):
        self.assertEqual(self.__test_instance.sunrise_time(timeformat='iso'),
                         self.__test_iso_sunrise_time)
        self.assertEqual(self.__test_instance.sunrise_time(timeformat='unix'),
                         self.__test_sunrise_time)

    def test_get_reference_time_fails_with_unknown_timeformat(self):
        self.assertRaises(ValueError, Weather.reference_time,
                          self.__test_instance, 'xyz')

    def test_sunset_time_fails_with_unknown_timeformat(self):
        self.assertRaises(ValueError, Weather.sunset_time,
                          self.__test_instance, 'xyz')

    def test_sunrise_time_fails_with_unknown_timeformat(self):
        self.assertRaises(ValueError, Weather.sunrise_time,
                          self.__test_instance, 'xyz')

    def test_returning_different_units_for_temperatures(self):
        result_kelvin = self.__test_instance.temperature(unit='kelvin')
        result_celsius = self.__test_instance.temperature(unit='celsius')
        result_fahrenheit = self.__test_instance.temperature(
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
        self.assertRaises(ValueError, Weather.temperature,
                          self.__test_instance, 'xyz')

    def test_returning_different_units_for_wind_values(self):
        result_imperial = self.__test_instance.wind(unit='miles_hour')
        result_metric = self.__test_instance.wind(unit='meters_sec')
        result_unspecified = self.__test_instance.wind()
        self.assertEqual(result_unspecified, result_metric)
        for item in self.__test_wind:
            self.assertEqual(result_metric[item],
                             self.__test_wind[item])
            self.assertEqual(result_imperial[item],
                             self.__test_imperial_wind[item])

    def test_get_wind_fails_with_unknown_units(self):
        self.assertRaises(ValueError, Weather.wind, self.__test_instance, 'xyz')

    def test_weather_icon_url(self):
        expected = ICONS_BASE_URI % self.__test_instance.weather_icon_name
        result = self.__test_instance.weather_icon_url()
        self.assertEqual(expected, result)