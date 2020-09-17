#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from datetime import datetime

from pyowm.commons.exceptions import APIResponseError, ParseAPIResponseError
from pyowm.weatherapi25.uris import ICONS_BASE_URI
from pyowm.weatherapi25.weather import Weather
from tests.unit.weatherapi25.json_test_responses import (CITY_WEATHER_HISTORY_JSON,
                                                         CITY_WEATHER_HISTORY_NO_RESULTS_JSON,
                                                         CITY_WEATHER_HISTORY_NOT_FOUND_JSON,
                                                         INTERNAL_SERVER_ERROR_JSON)


class TestWeather(unittest.TestCase):
    __test_reference_time = 1378459200
    __test_iso_reference_time = "2013-09-06 09:20:00+00:00"
    __test_date_reference_time = datetime.fromisoformat(__test_iso_reference_time)
    __test_sunset_time = 1378496400
    __test_iso_sunset_time = "2013-09-06 19:40:00+00:00"
    __test_date_sunset_time = datetime.fromisoformat(__test_iso_sunset_time)
    __test_sunrise_time = 1378449600
    __test_iso_sunrise_time = "2013-09-06 06:40:00+00:00"
    __test_date_sunrise_time = datetime.fromisoformat(__test_iso_sunrise_time)
    __test_clouds = 67
    __test_rain = {"all": 20}
    __test_snow = {"all": 0}
    __test_wind = {"deg": 252.002, "speed": 1.100, "gust": 2.09}
    __test_imperial_wind = {"deg": 252.002, "speed": 2.460634, "gust": 4.6752046}
    __test_knots_wind = {'deg': 252.002, 'speed': 2.138224, 'gust': 4.0626256}
    __test_beaufort_wind = {"deg": 252.002, "speed": 1, "gust": 2}
    __test_kmh_wind = {'deg': 252.002, 'speed': 3.9600000000000004, 'gust': 7.524}
    __test_humidity = 57
    __test_pressure = {"press": 1030.119, "sea_level": 1038.589, "grnd_level": 1038.773}
    __test_temperature = {"temp": 294.199, "temp_kf": -1.899,
                          "temp_max": 296.098, "temp_min": 294.199,
                          "feels_like": 298.0}
    __test_celsius_temperature = {"temp": 21.049, "temp_kf": -1.899,
                                  "temp_max": 22.948, "temp_min": 21.049,
                                  "feels_like": 24.85}
    __test_fahrenheit_temperature = {"temp": 69.888, "temp_kf": -1.899,
                                     "temp_max": 73.306, "temp_min": 69.888,
                                     "feels_like": 76.73}
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

    WEATHER_JSON_DUMP = '{"status": "Clouds", "visibility_distance": 1000, ' \
                        '"clouds": 67, "temperature": {"temp_kf": -1.899, ' \
                        '"temp_min": 294.199, "temp": 294.199, "temp_max": 296.098, "feels_like": 298.0},' \
                        ' "dewpoint": 300.0, "humidex": 298.0, "detailed_status": ' \
                        '"Overcast clouds", "reference_time": 1378459200, ' \
                        '"weather_code": 804, "sunset_time": 1378496400, "rain": ' \
                        '{"all": 20}, "snow": {"all": 0}, "pressure": ' \
                        '{"press": 1030.119, "sea_level": 1038.589, "grnd_level": 1038.773}, ' \
                        '"sunrise_time": 1378449600, "heat_index": 40.0, ' \
                        '"weather_icon_name": "04d", "humidity": 57, "wind": ' \
                        '{"speed": 1.1, "deg": 252.002, "gust": 2.09}, "utc_offset": null, "uvi": null}'

    def test_init_fails_when_wrong_data_provided(self):
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
        self.assertRaises(ValueError, Weather, self.__test_reference_time,
                          self.__test_sunset_time, self.__test_sunrise_time,
                          self.__test_clouds, self.__test_rain, self.__test_snow,
                          self.__test_wind, self.__test_humidity,
                          self.__test_pressure, self.__test_temperature,
                          self.__test_status, self.__test_detailed_status,
                          self.__test_weather_code, self.__test_weather_icon_name,
                          self.__test_visibility_distance, self.__test_dewpoint,
                          self.__test_humidex, self.__test_heat_index, uvi=-1)

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

    def test_init_fails_with_non_integer_utc_offset(self):
        self.assertRaises(AssertionError, Weather, self.__test_reference_time,
                          self.__test_sunset_time, self.__test_sunrise_time,
                          self.__test_clouds, self.__test_rain, self.__test_snow,
                          self.__test_wind, self.__test_humidity,
                          self.__test_pressure, self.__test_temperature,
                          self.__test_status, self.__test_detailed_status,
                          self.__test_weather_code, self.__test_weather_icon_name,
                          self.__test_visibility_distance, self.__test_dewpoint,
                          self.__test_humidex, self.__test_heat_index,
                          'non_string_utc_offset')

    def test_from_dict_fails_when_dict_is_none(self):
        self.assertRaises(ParseAPIResponseError, Weather.from_dict, None)

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
                 'calc': {
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
        dict3 = {"station": {
            "name": "KPPQ",
            "type": 1,
            "status": 50,
            "id": 1000,
            "coord": {"lon": -90.47, "lat": 39.38}
        },
            "last": {
                "main": {
                    "temp": 276.15,
                    "pressure": 1031},
                "wind": {
                    "speed": 3.1,
                    "deg": 140
                },
                "visibility": {
                    "distance": 11265,
                    "prefix": 0
                },
                "calc": {
                    "dewpoint": 273.15,
                    "humidex": 57.8,
                    "heatindex": 1.2
                },
                "clouds": [
                    {"distance": 427,
                     "condition": "SCT"}
                ],
                "dt": 1417977300
            },
            "params": ["temp", "pressure", "wind", "visibility"],
            "timezone": 1234567
        }
        dict4 = {'clouds': {'all': 92}, 'name': 'London',
                 'coord': {'lat': 51.50853, 'lon': -0.12574},
                 'sys': {'country': 'GB', 'sunset': 1378923812,
                         'sunrise': 1378877413
                         },
                 'weather': [
                     {'main': 'Clouds', 'id': 804, 'icon': '04d',
                      'description': 'overcastclouds'}
                 ],
                 'cod': 200, 'base': 'gdpsstations',
                 'main': {
                     'pressure': 1022,
                     'humidity': 75,
                     'temp_max': 289.82,
                     'temp': 288.44,
                     'temp_min': 287.59
                 },
                 'id': 2643743,
                 'wind': {'gust': 2.57, 'speed': 1.54, 'deg': 31},
                 'calc': {},
                 'last': {},
                 'snow': {'tot': 76.3}
         }
        dict5 = {'clouds': {'all': 92}, 'name': 'London',
                 'coord': {'lat': 51.50853, 'lon': -0.12574},
                 'sys': {'country': 'GB', 'sunset': 1378923812,
                         'sunrise': 1378877413
                         },
                 'weather': [
                     {'main': 'Clouds', 'id': 804, 'icon': '04d',
                      'description': 'overcastclouds'}
                 ],
                 'cod': 200, 'base': 'gdpsstations',
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
                 "last": {}
         }
        dict6 = {'clouds': {'all': 92}, 'name': 'London',
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
                     'temp_max': 289.82,
                     'temp': 288.44,
                     'temp_min': 287.59
                 },
                 'id': 2643743,
                 'wind': {'gust': 2.57, 'speed': 1.54, 'deg': 31},
                 'last': {
                     "dt": 1417977300,
                     "calc": {},
                     'visibility': 2.34,
                     'main': {
                         "humidity": 77.2
                     }
                 },
                 'snow': 66.1
         }
        result1 = Weather.from_dict(dict1)
        self.assertTrue(isinstance(result1, Weather))
        result2 = Weather.from_dict(dict2)
        self.assertTrue(isinstance(result2, Weather))
        result3 = Weather.from_dict(dict3)
        self.assertTrue(isinstance(result3, Weather))
        result4 = Weather.from_dict(dict4)
        self.assertTrue(isinstance(result4, Weather))
        result5 = Weather.from_dict(dict5)
        self.assertTrue(isinstance(result5, Weather))
        result6 = Weather.from_dict(dict6)
        self.assertTrue(isinstance(result6, Weather))

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
                 'calc': {
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

        dict2 = {"station": {
            "name": "KPPQ",
            "type": 1,
            "status": 50,
            "id": 1000,
            "coord": {"lon": -90.47, "lat": 39.38}
        },
            "last": {
                "main": {
                    "temp": 276.15,
                    "pressure": 1031},
                "wind": None,
                "visibility": {
                    "distance": 11265,
                    "prefix": 0
                },
                "calc": {
                    "dewpoint": 273.15
                },
                "clouds": [
                    {"distance": 427,
                     "condition": "SCT"}
                ],
                "dt": 1417977300
            },
            "params": ["temp", "pressure", "wind", "visibility"]
        }
        result2 = Weather.from_dict(dict2)
        self.assertTrue(isinstance(result2, Weather))
        self.assertEqual(0, len(result2.wind()))

    def test_to_dict(self):
        expected = json.loads(self.WEATHER_JSON_DUMP)
        result = self.__test_instance.to_dict()
        self.assertEqual(expected, result)

    def test_from_dict_of_lists(self):
        result = Weather.from_dict_of_lists(json.loads(CITY_WEATHER_HISTORY_JSON))
        self.assertTrue(result)
        self.assertTrue(isinstance(result, list))
        for weather in result:
            self.assertTrue(weather is not None)

    def test_from_dict_of_lists_fails_when_JSON_data_is_None(self):
        self.assertRaises(ParseAPIResponseError, Weather.from_dict_of_lists, None)

    def test_from_dict_of_lists_with_malformed_JSON_data(self):
        self.assertRaises(ParseAPIResponseError, Weather.from_dict_of_lists, json.loads(self.__bad_json))
        self.assertRaises(ParseAPIResponseError, Weather.from_dict_of_lists, json.loads(self.__bad_json_2))

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
        self.assertEqual(self.__test_instance.sunset_time(timeformat='date'),
                         self.__test_date_sunset_time)

    def test_sunrise_time_returning_different_formats(self):
        self.assertEqual(self.__test_instance.sunrise_time(timeformat='iso'),
                         self.__test_iso_sunrise_time)
        self.assertEqual(self.__test_instance.sunrise_time(timeformat='unix'),
                         self.__test_sunrise_time)
        self.assertEqual(self.__test_instance.sunrise_time(timeformat='date'),
                         self.__test_date_sunrise_time)

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
        result_metric_ms = self.__test_instance.wind(unit='meters_sec')
        result_metric_kmh = self.__test_instance.wind(unit='km_hour')
        result_knots = self.__test_instance.wind(unit='knots')
        result_beaufort = self.__test_instance.wind(unit='beaufort')
        result_unspecified = self.__test_instance.wind()
        self.assertEqual(result_unspecified, result_metric_ms)
        self.assertDictEqual(result_metric_kmh, self.__test_kmh_wind)
        for item in self.__test_wind:
            self.assertEqual(result_metric_ms[item],
                             self.__test_wind[item])
            self.assertEqual(result_imperial[item],
                             self.__test_imperial_wind[item])
            self.assertEqual(result_knots[item],
                             self.__test_knots_wind[item])
            self.assertEqual(result_beaufort[item],
                             self.__test_beaufort_wind[item])

    def test_get_wind_fails_with_unknown_units(self):
        self.assertRaises(ValueError, Weather.wind, self.__test_instance, 'xyz')

    def test_weather_icon_url(self):
        expected_unspecified = ICONS_BASE_URI % (self.__test_instance.weather_icon_name, "")
        expected_2x = ICONS_BASE_URI % (self.__test_instance.weather_icon_name, "@2x")
        expected_4x = ICONS_BASE_URI % (self.__test_instance.weather_icon_name, "@4x")
        result_unspecified = self.__test_instance.weather_icon_url()
        result_2x = self.__test_instance.weather_icon_url(size="2x")
        result_4x = self.__test_instance.weather_icon_url(size="4x")
        self.assertEqual(expected_unspecified, result_unspecified)
        self.assertEqual(expected_2x, result_2x)
        self.assertEqual(expected_4x, result_4x)

    def test_repr(self):
        print(self.__test_instance)

    def test_one_call_current_from_dic(self):
        current1 = {
            "dt": 1586001851,
            "sunrise": 1586003020,
            "sunset": 1586048382,
            "temp": 280.15,
            "feels_like": 277.75,
            "pressure": 1017,
            "humidity": 93,
            "uvi": 9.63,
            "clouds": 90,
            "visibility": 6437,
            "wind_speed": 2.1,
            "wind_deg": 70,
            "weather": [
                {
                    "id": 501,
                    "main": "Rain",
                    "description": "moderate rain",
                    "icon": "10n"
                },
                {
                    "id": 701,
                    "main": "Mist",
                    "description": "mist",
                    "icon": "50n"
                }
            ],
            "rain": {
                "1h": 1.02
            }
        }

        result1 = Weather.from_dict(current1)
        self.assertTrue(isinstance(result1, Weather))
        self.assertEqual(9.63, result1.uvi)
        self.assertEqual(501, result1.weather_code)
        self.assertEqual(1.02, result1.rain["1h"])
        self.assertEqual(280.15, result1.temperature()["temp"])
        self.assertEqual(277.75, result1.temperature()["feels_like"])

        current2 = {
            "dt": 1587678355,
            "sunrise": 1587615127,
            "sunset": 1587665513,
            "temp": 281.78,
            "feels_like": 277.4,
            "pressure": 1017,
            "humidity": 39,
            "dew_point": 269.13,
            "uvi": 7.52,
            "clouds": 2,
            "visibility": 10000,
            "wind_speed": 2.6,
            "wind_deg": 170,
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01n"
                }
            ]
        }

        result2 = Weather.from_dict(current2)
        self.assertTrue(isinstance(result2, Weather))
        self.assertEqual(7.52, result2.uvi)
        self.assertEqual(800, result2.weather_code)
        self.assertEqual(170, result2.wind()["deg"])
        self.assertEqual(0, len(result2.rain))
        self.assertEqual(281.78, result2.temperature()["temp"])
        self.assertEqual(277.4, result2.temperature()["feels_like"])

    def test_one_call_hourly_from_dic(self):
        hourly1 = {
            "dt": 1587675600,
            "temp": 294.16,
            "feels_like": 292.47,
            "pressure": 1009,
            "humidity": 88,
            "dew_point": 292.1,
            "clouds": 90,
            "wind_speed": 7,
            "wind_deg": 189,
            "weather": [
                {
                    "id": 501,
                    "main": "Rain",
                    "description": "moderate rain",
                    "icon": "10d"
                }
            ],
            "rain": {
                "1h": 2.28
            }
        }

        result1 = Weather.from_dict(hourly1)
        self.assertTrue(isinstance(result1, Weather))
        self.assertEqual(292.47, result1.temperature()["feels_like"])
        self.assertEqual(501, result1.weather_code)
        self.assertEqual(2.28, result1.rain["1h"])
        self.assertEqual(294.16, result1.temperature()["temp"])
        self.assertEqual(292.47, result1.temperature()["feels_like"])

        hourly2 = {
            "dt": 1587682800,
            "temp": 279.64,
            "feels_like": 276.77,
            "pressure": 1020,
            "humidity": 54,
            "dew_point": 271.26,
            "clouds": 3,
            "wind_speed": 0.84,
            "wind_deg": 119,
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01n"
                }
            ]
        }

        result2 = Weather.from_dict(hourly2)
        self.assertTrue(isinstance(result2, Weather))
        self.assertEqual(3, result2.clouds)
        self.assertEqual(800, result2.weather_code)
        self.assertEqual(119, result2.wind()["deg"])
        self.assertEqual(0, len(result2.rain))
        self.assertEqual(279.64, result2.temperature()["temp"])
        self.assertEqual(276.77, result2.temperature()["feels_like"])

    def test_one_call_daily_from_dic(self):
        daily1 = {
            "dt": 1587747600,
            "sunrise": 1587725080,
            "sunset": 1587772792,
            "temp": {
                "day": 300.75,
                "min": 290.76,
                "max": 300.75,
                "night": 290.76,
                "eve": 295.22,
                "morn": 291.44
            },
            "feels_like": {
                "day": 300.69,
                "night": 291.63,
                "eve": 296.8,
                "morn": 292.73
            },
            "pressure": 1009,
            "humidity": 55,
            "dew_point": 291.24,
            "wind_speed": 3.91,
            "wind_deg": 262,
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "light rain",
                    "icon": "10d"
                }
            ],
            "clouds": 95,
            "rain": 0.82,
            "uvi": 9.46
        }

        result1 = Weather.from_dict(daily1)
        self.assertTrue(isinstance(result1, Weather))
        self.assertEqual(9.46, result1.uvi)
        self.assertEqual(500, result1.weather_code)
        self.assertEqual(262, result1.wind()["deg"])
        self.assertEqual(0.82, result1.rain["all"])
        self.assertRaises(KeyError, lambda: result1.temperature()["temp"])
        self.assertRaises(KeyError, lambda: result1.temperature()["feels_like"])
        self.assertEqual(300.75, result1.temperature()["day"])
        self.assertEqual(290.76, result1.temperature()["min"])
        self.assertEqual(300.75, result1.temperature()["max"])
        self.assertEqual(290.76, result1.temperature()["night"])
        self.assertEqual(295.22, result1.temperature()["eve"])
        self.assertEqual(291.44, result1.temperature()["morn"])
        self.assertEqual(300.69, result1.temperature()["feels_like_day"])
        self.assertEqual(291.63, result1.temperature()["feels_like_night"])
        self.assertEqual(296.8, result1.temperature()["feels_like_eve"])
        self.assertEqual(292.73, result1.temperature()["feels_like_morn"])

        daily2 = {
            "dt": 1587639600,
            "sunrise": 1587615127,
            "sunset": 1587665513,
            "temp": {
                "day": 281.78,
                "min": 279.88,
                "max": 281.78,
                "night": 279.88,
                "eve": 281.78,
                "morn": 281.78
            },
            "feels_like": {
                "day": 278.55,
                "night": 276.84,
                "eve": 278.55,
                "morn": 278.55
            },
            "pressure": 1017,
            "humidity": 39,
            "dew_point": 269.13,
            "wind_speed": 0.96,
            "wind_deg": 116,
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01n"
                }
            ],
            "clouds": 2,
            "uvi": 7.52
        }

        result2 = Weather.from_dict(daily2)
        self.assertTrue(isinstance(result2, Weather))
        self.assertEqual(7.52, result2.uvi)
        self.assertEqual(800, result2.weather_code)
        self.assertEqual(116, result2.wind()["deg"])
        self.assertEqual(0, len(result2.rain))
        self.assertRaises(KeyError, lambda: result2.temperature()["temp"])
        self.assertRaises(KeyError, lambda: result2.temperature()["feels_like"])
        self.assertEqual(281.78, result2.temperature()["day"])
        self.assertEqual(279.88, result2.temperature()["min"])
        self.assertEqual(281.78, result2.temperature()["max"])
        self.assertEqual(279.88, result2.temperature()["night"])
        self.assertEqual(281.78, result2.temperature()["eve"])
        self.assertEqual(281.78, result2.temperature()["morn"])
        self.assertEqual(278.55, result2.temperature()["feels_like_day"])
        self.assertEqual(276.84, result2.temperature()["feels_like_night"])
        self.assertEqual(278.55, result2.temperature()["feels_like_eve"])
        self.assertEqual(278.55, result2.temperature()["feels_like_morn"])
