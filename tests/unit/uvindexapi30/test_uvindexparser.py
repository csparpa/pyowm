"""
Test case for parsers.py module
"""
import unittest
from pyowm.uvindexapi30.parsers import UVIndexParser
from pyowm.exceptions.parse_response_error import ParseResponseError


UVINDEX_JSON = '{"lat":43.75,"lon":8.25,"date_iso":"2016-09-27T12:00:00Z",' \
               '"date":1474977600,"value":4.58}'
UVINDEX_MALFORMED_JSON = '{"lat":43.75,"lon":8.25,"zzz":"2016-09-27T12:00:00Z",' \
               '"date":1474977600,"test":4.58}'


class TestUVIndexParser(unittest.TestCase):

    __instance = UVIndexParser()

    def test_parse_JSON(self):
        result = self.__instance.parse_JSON(UVINDEX_JSON)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.get_reference_time())
        self.assertIsNotNone(result.get_reception_time())
        loc = result.get_location()
        self.assertIsNotNone(loc)
        self.assertIsNone(loc.get_name())
        self.assertIsNone(loc.get_ID())
        self.assertIsNotNone(loc.get_lon())
        self.assertIsNotNone(loc.get_lat())
        self.assertIsNotNone(result.get_value())

    def test_parse_JSON_fails_when_JSON_data_is_None(self):
        self.assertRaises(ParseResponseError, UVIndexParser.parse_JSON,
                          self.__instance, None)

    def test_parse_JSON_fails_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, UVIndexParser.parse_JSON,
                          self.__instance, UVINDEX_MALFORMED_JSON)


