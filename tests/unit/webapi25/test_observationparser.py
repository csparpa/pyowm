"""
Test case for observationparser.py module
"""
import unittest
from pyowm.webapi25.observationparser import ObservationParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.exceptions.api_response_error import APIResponseError
from tests.unit.webapi25.json_test_responses import (
     OBSERVATION_JSON, OBSERVATION_NOT_FOUND_JSON, OBSERVATION_MALFORMED_JSON)


class TestObservationParser(unittest.TestCase):

    __instance = ObservationParser()
    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'
    __bad_json_2 = '{"message": "test", "cod": "500"}'

    def test_parse_JSON(self):
        result = self.__instance.parse_JSON(OBSERVATION_JSON)
        self.assertTrue(result is not None)
        self.assertFalse(result.get_reception_time() is None)
        loc = result.get_location()
        self.assertFalse(loc is None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = result.get_weather()
        self.assertFalse(weat is None)

    def test_parse_JSON_fails_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, ObservationParser.parse_JSON,
                          self.__instance, self.__bad_json)
        self.assertRaises(APIResponseError, ObservationParser.parse_JSON,
                          self.__instance, self.__bad_json_2)
        self.assertRaises(ParseResponseError, ObservationParser.parse_JSON,
                          self.__instance, OBSERVATION_MALFORMED_JSON)

    def test_parse_JSON_when_server_error(self):
        result = self.__instance.parse_JSON(OBSERVATION_NOT_FOUND_JSON)
        self.assertTrue(result is None)
