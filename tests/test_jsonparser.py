#!/usr/bin/env python

"""
Test case for jsonparser.py module
"""

import unittest
from json_test_responses import OBSERVATION_JSON, NOT_FOUND_JSON
from pyowm.utils import jsonparser
from pyowm.exceptions.parse_response_exception import ParseResponseException


class Test(unittest.TestCase):

    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'  

    def test_parse_observation(self):
        """
        Test that method returns a valid Observation object when provided
        with well-formed JSON data
        """
        result = jsonparser.parse_observation(OBSERVATION_JSON)
        self.assertFalse(result is None, "")
        self.assertFalse(result.get_reception_time() is None, "")
        self.assertFalse(result.get_location() is None, "")
        self.assertNotIn(None, result.get_location().__dict__.values(), "")
        self.assertFalse(result.get_weather() is None, "")
        self.assertNotIn(None, result.get_weather().__dict__.values(), "")
        
    def test_parse_observation_fails_with_malformed_JSON_data(self):
        """
        Test that method throws a ParseResponseException when provided with bad
        JSON data
        """
        self.assertRaises(ParseResponseException, jsonparser.parse_observation, self.__bad_json)
        
    def test_caused_HTTP_error(self):
        self.assertTrue(jsonparser.caused_HTTP_error({'message':'Error', 'cod':'404'}))
        self.assertFalse(jsonparser.caused_HTTP_error({'message':'Not an error','x':2}))
        self.assertFalse(jsonparser.caused_HTTP_error({'x':2,'y':'test'}))
        
    def test_parse_observation_when_data_not_found(self):
        result = jsonparser.parse_observation(NOT_FOUND_JSON)
        self.assertTrue(result is None, "")
        
if __name__ == "__main__":
    unittest.main()