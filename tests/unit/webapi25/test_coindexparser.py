"""
Test case for coindexparser.py module
"""
import unittest
from pyowm.webapi25.coindexparser import COIndexParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from tests.unit.webapi25.json_test_responses import (
    COINDEX_JSON, COINDEX_MALFORMED_JSON)


class TestCOIndexParser(unittest.TestCase):

    __instance = COIndexParser()

    def test_parse_JSON(self):
        result = self.__instance.parse_JSON(COINDEX_JSON)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.get_reference_time())
        self.assertIsNotNone(result.get_reference_time())
        loc = result.get_location()
        self.assertIsNotNone(loc)
        self.assertIsNone(loc.get_name())
        self.assertIsNone(loc.get_ID())
        self.assertIsNotNone(loc.get_lon())
        self.assertIsNotNone(loc.get_lat())
        self.assertIsNone(result.get_interval())
        self.assertNotEquals(0, len(result.get_co_samples()))

    def test_parse_JSON_fails_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, COIndexParser.parse_JSON,
                          self.__instance, COINDEX_MALFORMED_JSON)