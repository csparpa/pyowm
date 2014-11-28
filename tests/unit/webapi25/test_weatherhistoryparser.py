"""
Test case for weatherhistoryparser.py module
"""
import unittest
from pyowm.webapi25.weatherhistoryparser import WeatherHistoryParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.exceptions.api_response_error import APIResponseError
from tests.unit.webapi25.json_test_responses import (CITY_WEATHER_HISTORY_JSON,
    CITY_WEATHER_HISTORY_NO_RESULTS_JSON, CITY_WEATHER_HISTORY_NOT_FOUND_JSON,
    INTERNAL_SERVER_ERROR_JSON)


class TestWeatherHistoryParser(unittest.TestCase):

    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'
    __bad_json_2 = '{"list": [{"test":"fake"}] }'
    __no_items_json = '{"cnt": "0"}'
    __instance = WeatherHistoryParser()

    def test_parse_JSON(self):
        result = self.__instance.parse_JSON(CITY_WEATHER_HISTORY_JSON)
        self.assertTrue(result)
        self.assertTrue(isinstance(result, list))
        for weather in result:
            self.assertTrue(weather is not None)

    def test_parse_JSON_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, WeatherHistoryParser.parse_JSON,
                          self.__instance, self.__bad_json)
        self.assertRaises(ParseResponseError, WeatherHistoryParser.parse_JSON,
                          self.__instance, self.__bad_json_2)

    def test_parse_JSON_when_no_results(self):
        result = \
            self.__instance.parse_JSON(CITY_WEATHER_HISTORY_NO_RESULTS_JSON)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(0, len(result))
        result = self.__instance.parse_JSON(self.__no_items_json)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(0, len(result))

    def test_parse_JSON_when_location_not_found(self):
        self.assertFalse(
             self.__instance.parse_JSON(CITY_WEATHER_HISTORY_NOT_FOUND_JSON))

    def test_parse_JSON_when_server_error(self):
        self.assertRaises(APIResponseError, WeatherHistoryParser.parse_JSON,
                          self.__instance, INTERNAL_SERVER_ERROR_JSON)
