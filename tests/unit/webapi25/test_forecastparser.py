#!/usr/bin/env python

"""
Test case for forecastparser.py module
"""
#from __future__ import absolute_import  # Python 2.x compatibility
import unittest
from pyowm.webapi25.forecastparser import ForecastParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.exceptions.api_response_error import APIResponseError
from tests.unit.webapi25.json_test_responses import (
     THREE_HOURS_FORECAST_JSON, FORECAST_NOT_FOUND_JSON,
     INTERNAL_SERVER_ERROR_JSON)


class TestForecastParser(unittest.TestCase):

    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'
    __instance = ForecastParser()

    def test_parse_JSON(self):
        result = self.__instance.parse_JSON(THREE_HOURS_FORECAST_JSON)
        self.assertTrue(result is not None)
        self.assertTrue(result.get_reception_time() is not None)
        self.assertFalse(result.get_interval() is not None)
        loc = result.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        self.assertTrue(isinstance(result.get_weathers(), list))
        for weather in result:
            self.assertTrue(weather is not None)
            self.assertTrue(all(v is not None \
                                for v in weather.__dict__.values()))

    def test_parse_JSON_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, ForecastParser.parse_JSON,
                          self.__instance, self.__bad_json)

    def test_parse_JSON_when_no_results(self):
        result = self.__instance.parse_JSON(FORECAST_NOT_FOUND_JSON)
        self.assertFalse(result is None)
        self.assertEqual(0, len(result))

    def test_parse_JSON_when_server_error(self):
        self.assertRaises(APIResponseError, ForecastParser.parse_JSON,
                          self.__instance, INTERNAL_SERVER_ERROR_JSON)
