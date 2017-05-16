import unittest
from pyowm.webapi25.no2indexparser import NO2IndexParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from tests.unit.webapi25.json_test_responses import (
    NO2INDEX_JSON, NO2INDEX_MALFORMED_JSON)


class TestNO2IndexParser(unittest.TestCase):

    __instance = NO2IndexParser()

    def test_parse_JSON(self):
        result = self.__instance.parse_JSON(NO2INDEX_JSON)
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
        self.assertNotEquals(0, len(result.get_no2_samples()))

    def test_parse_JSON_fails_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, NO2IndexParser.parse_JSON,
                          self.__instance, NO2INDEX_MALFORMED_JSON)