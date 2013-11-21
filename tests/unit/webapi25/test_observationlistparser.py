#!/usr/bin/env python

"""
Test case for observationlistparser.py module
"""
import unittest
from pyowm.webapi25.observationlistparser import ObservationListParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.exceptions.api_response_error import APIResponseError
from json_test_responses import SEARCH_RESULTS_JSON, SEARCH_WITH_NO_RESULTS_JSON, \
    INTERNAL_SERVER_ERROR_JSON

class TestObservationListParser(unittest.TestCase):
    
    __instance = ObservationListParser()
    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'
    
    def test_parse_JSON(self):
        result = self.__instance.parse_JSON(SEARCH_RESULTS_JSON)
        self.assertFalse(result is None)
        self.assertTrue(isinstance(result, list))
        for item in result:
            self.assertFalse(item is None)
            self.assertFalse(item.get_reception_time() is None)
            self.assertFalse(item.get_location() is None)
            self.assertNotIn(None, item.get_location().__dict__.values())
            self.assertFalse(item.get_weather() is None)
            self.assertNotIn(None, item.get_weather().__dict__.values())
        
    def test_parse_JSON_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, self.__instance.parse_JSON,
                          self.__bad_json)
        
    def test_parse_JSON_when_no_results(self):
        result = self.__instance.parse_JSON(SEARCH_WITH_NO_RESULTS_JSON)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(0, len(result))
        
    def test_pparse_JSON_when_server_error(self):
        self.assertRaises(APIResponseError, self.__instance.parse_JSON,
                          INTERNAL_SERVER_ERROR_JSON)

if __name__ == "__main__":
    unittest.main()