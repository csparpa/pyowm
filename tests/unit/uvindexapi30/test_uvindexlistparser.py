import unittest
from pyowm.uvindexapi30.uvindex import UVIndex
from pyowm.uvindexapi30.parsers import UVIndexListParser
from pyowm.exceptions.parse_response_error import ParseResponseError


UVINDEX_LIST_JSON = '[{"lat":37.75,"lon":-122.37,"date_iso":"2017-06-22T12:00:00Z",' \
                    '"date":1498132800,"value":9.92},{"lat":37.75,"lon":-122.37,' \
                    '"date_iso":"2017-06-23T12:00:00Z","date":1498219200,' \
                    '"value":10.09},{"lat":37.75,"lon":-122.37,"date_iso":' \
                    '"2017-06-24T12:00:00Z","date":1498305600,"value":10.95},' \
                    '{"lat":37.75,"lon":-122.37,"date_iso":"2017-06-25T12:00:00Z",' \
                    '"date":1498392000,"value":11.03},{"lat":37.75,"lon":-122.37,' \
                    '"date_iso":"2017-06-26T12:00:00Z","date":1498478400,"value":10.06}]'
UVINDEX_LIST_MALFORMED_JSON = '[{"lat":43.75,"lon":8.25,"zzz":"2016-09-27T12:00:00Z",' \
               '"date":1474977600,"test":4.58}]'


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


