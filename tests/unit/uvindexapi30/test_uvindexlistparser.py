import unittest
from pyowm.uvindexapi30.uvindex import UVIndex
from pyowm.uvindexapi30.parsers import UVIndexListParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from tests.unit.webapi25.json_test_responses import (
    UVINDEX_LIST_JSON, UVINDEX_LIST_MALFORMED_JSON)


class TestUVListIndexParser(unittest.TestCase):

    __instance = UVIndexListParser()

    def test_parse_JSON(self):
        result = self.__instance.parse_JSON(UVINDEX_LIST_JSON)
        self.assertIsInstance(result, list)
        self.assertEqual(5, len(result))
        self.assertTrue(all([isinstance(i, UVIndex) for i in result]))

    def test_parse_JSON_fails_when_JSON_data_is_None(self):
        self.assertRaises(ParseResponseError, UVIndexListParser.parse_JSON,
                          self.__instance, None)

    def test_parse_JSON_fails_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, UVIndexListParser.parse_JSON,
                          self.__instance, UVINDEX_LIST_MALFORMED_JSON)


