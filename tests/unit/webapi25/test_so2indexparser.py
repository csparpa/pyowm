import unittest
from pyowm.webapi25.so2indexparser import SO2IndexParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from tests.unit.webapi25.json_test_responses import (
    SO2INDEX_JSON, SO2INDEX_MALFORMED_JSON)


class TestSO2IndexParser(unittest.TestCase):

    __instance = SO2IndexParser()

    def test_parse_JSON(self):
        result = self.__instance.parse_JSON(SO2INDEX_JSON)
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
        self.assertNotEquals(0, len(result.get_so2_samples()))

    def test_parse_JSON_fails_when_JSON_data_is_None(self):
        self.assertRaises(ParseResponseError, SO2IndexParser.parse_JSON,
                          self.__instance, None)

    def test_parse_JSON_fails_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, SO2IndexParser.parse_JSON,
                          self.__instance, SO2INDEX_MALFORMED_JSON)
