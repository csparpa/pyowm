#!/usr/bin/env python

"""
Test case for observationparser.py module
"""
import unittest
from pyowm.webapi25.observationparser import ObservationParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from json_test_responses import OBSERVATION_JSON, OBSERVATION_NOT_FOUND_JSON

class TestObservationParser(unittest.TestCase):
    
    __instance = ObservationParser()
    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'

    def test_parse_JSON(self):
        result = self.__instance.parse_JSON(OBSERVATION_JSON)
        self.assertTrue(result)
        self.assertFalse(result.get_reception_time() is None)
        self.assertFalse(result.get_location() is None)
        self.assertNotIn(None, result.get_location().__dict__.values())
        self.assertFalse(result.get_weather() is None)
        self.assertNotIn(None, result.get_weather().__dict__.values())

    def test_parse_JSON_fails_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, ObservationParser.parse_JSON,
                          self.__instance, self.__bad_json)
        
    def test_parse_JSON_when_server_error(self):
        result = self.__instance.parse_JSON(OBSERVATION_NOT_FOUND_JSON)
        self.assertTrue(result is None)

if __name__ == "__main__":
    unittest.main()