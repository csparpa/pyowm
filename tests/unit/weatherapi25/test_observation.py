#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
from datetime import datetime
from pyowm.weatherapi25.location import Location
from pyowm.weatherapi25.weather import Weather
from pyowm.weatherapi25.observation import Observation
from pyowm.commons.exceptions import APIResponseError, ParseAPIResponseError
from tests.unit.weatherapi25.json_test_responses import (
     OBSERVATION_JSON, OBSERVATION_NOT_FOUND_JSON, OBSERVATION_MALFORMED_JSON)
from tests.unit.weatherapi25.json_test_responses import (
    SEARCH_RESULTS_JSON, SEARCH_WITH_NO_RESULTS_1_JSON,
    SEARCH_WITH_NO_RESULTS_2_JSON, INTERNAL_SERVER_ERROR_JSON)


class TestObservation(unittest.TestCase):

    __test_reception_time = 1234567
    __test_iso_reception_time = "1970-01-15 06:56:07+00:00"
    __test_date_reception_time = datetime.fromisoformat(__test_iso_reception_time)
    __test_location = Location('test', 12.3, 43.7, 987, 'UK')
    __test_weather = Weather(1378459200, 1378496400, 1378449600, 67, {"all": 20},
            {"all": 0}, {"deg": 252.002, "speed": 1.100}, 57,
            {"press": 1030.119, "sea_level": 1038.589},
            {"temp": 294.199, "temp_kf": -1.899, "temp_max": 296.098,
                "temp_min": 294.199
            },
            "Clouds", "Overcast clouds", 804, "04d", 1000, 300.0, 298.0, 296.0)
    __test_instance = Observation(__test_reception_time, __test_location,
                                  __test_weather)

    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'
    __bad_json_2 = '{"message": "test", "cod": "500"}'
    __no_items_json = '{"cod": "200", "count": "0" }'
    __404_json = '{"cod": "404" }'

    OBSERVATION_JSON_DUMP = '{"reception_time": 1234567, "location": ' \
                            '{"country": "UK", "name": "test", "coordinates": ' \
                            '{"lat": 43.7, "lon": 12.3}, "ID": 987}, "weather": ' \
                            '{"status": "Clouds", "visibility_distance": 1000, ' \
                            '"humidity": 57, "clouds": 67, "temperature": ' \
                            '{"temp_kf": -1.899, "temp_max": 296.098, ' \
                            '"temp": 294.199, "temp_min": 294.199}, ' \
                            '"dewpoint": 300.0, "snow": {"all": 0}, ' \
                            '"detailed_status": "Overcast clouds", ' \
                            '"reference_time": 1378459200, "weather_code": 804, ' \
                            '"humidex": 298.0, "rain": {"all": 20}, ' \
                            '"sunset_time": 1378496400, "pressure": ' \
                            '{"press": 1030.119, "sea_level": 1038.589}, ' \
                            '"sunrise_time": 1378449600, "heat_index": 296.0, ' \
                            '"weather_icon_name": "04d", "wind": ' \
                            '{"speed": 1.1, "deg": 252.002}, "utc_offset": null, ' \
                            '"uvi": null}}'

    def test_init_fails_when_reception_time_is_negative(self):
        self.assertRaises(ValueError, Observation, -1234567, \
                          self.__test_location, self.__test_weather)

    def test_getters_return_expected_data(self):
        self.assertEqual(self.__test_instance.reception_time(),
                         self.__test_reception_time)
        self.assertEqual(self.__test_instance.location,
                         self.__test_location)
        self.assertEqual(self.__test_instance.weather,
                         self.__test_weather)

    def test_returning_different_formats_for_reception_time(self):
        self.assertEqual(self.__test_instance.reception_time(timeformat='iso'), \
                         self.__test_iso_reception_time)
        self.assertEqual(self.__test_instance.reception_time(timeformat='unix'), \
                         self.__test_reception_time)
        self.assertEqual(self.__test_instance.reception_time(timeformat='date'), \
                         self.__test_date_reception_time)

    def test_from_dict(self):
        d = json.loads(OBSERVATION_JSON)
        result = Observation.from_dict(d)
        self.assertTrue(result is not None)
        self.assertFalse(result.reception_time() is None)
        loc = result.location
        self.assertFalse(loc is None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = result.weather
        self.assertFalse(weat is None)

    def test_from_dict_fails_when_JSON_data_is_None(self):
        with self.assertRaises(ParseAPIResponseError):
            Observation.from_dict(None)

    def test_from_dict_fails_with_malformed_JSON_data(self):
        with self.assertRaises(ParseAPIResponseError):
            Observation.from_dict(json.loads(self.__bad_json))
        with self.assertRaises(APIResponseError):
            Observation.from_dict(json.loads(self.__bad_json_2))
        with self.assertRaises(ParseAPIResponseError):
            Observation.from_dict(json.loads(OBSERVATION_MALFORMED_JSON))

    def test_from_dict_when_server_error(self):
        result = self.__test_instance.from_dict(json.loads(OBSERVATION_NOT_FOUND_JSON))
        self.assertTrue(result is None)

    def test_to_dict(self):
        expected = json.loads(self.OBSERVATION_JSON_DUMP)
        result = self.__test_instance.to_dict()
        self.assertEqual(expected, result)

    def test_from_dict_of_lists(self):
        result = self.__test_instance.from_dict_of_lists(json.loads(SEARCH_RESULTS_JSON))
        self.assertFalse(result is None)
        self.assertTrue(isinstance(result, list))
        for item in result:
            self.assertFalse(item is None)
            self.assertFalse(item.reception_time() is None)
            loc = item.location
            self.assertFalse(loc is None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.weather
            self.assertFalse(weat is None)

    def test_from_dict_of_lists_fails_when_JSON_data_is_None(self):
        with self.assertRaises(ParseAPIResponseError):
            Observation.from_dict_of_lists(None)

    def test_from_dict_of_lists_with_malformed_JSON_data(self):
        with self.assertRaises(ParseAPIResponseError):
            Observation.from_dict_of_lists(json.loads(self.__bad_json))
        with self.assertRaises(APIResponseError):
            Observation.from_dict_of_lists(json.loads(self.__bad_json_2))
        with self.assertRaises(ParseAPIResponseError):
            Observation.from_dict_of_lists(json.loads(OBSERVATION_MALFORMED_JSON))

    def test_from_dict_of_lists_when_no_items_returned(self):
        self.assertFalse(Observation.from_dict_of_lists(json.loads(self.__no_items_json)))

    def test_from_dict_of_lists_when_resource_not_found(self):
        self.assertIsNone(Observation.from_dict_of_lists(json.loads(self.__404_json)))

    def test_from_dict_of_lists_when_no_results(self):
        result = Observation.from_dict_of_lists(json.loads(SEARCH_WITH_NO_RESULTS_1_JSON))
        self.assertTrue(isinstance(result, list))
        self.assertEqual(0, len(result))

        result = Observation.from_dict_of_lists(json.loads(SEARCH_WITH_NO_RESULTS_2_JSON))
        self.assertTrue(isinstance(result, list))
        self.assertEqual(0, len(result))

    def test_from_dict_of_lists_when_server_error(self):
        with self.assertRaises(APIResponseError):
            Observation.from_dict_of_lists(json.loads(INTERNAL_SERVER_ERROR_JSON))

    def test__repr(self):
        print(self.__test_instance)
