import unittest
from pyowm.webapi25.ozone_parser import OzoneParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from tests.unit.webapi25.json_test_responses import (
    OZONE_JSON, OZONE_MALFORMED_JSON)


class TestObservationParser(unittest.TestCase):

    __instance = OzoneParser()

    def test_parse_JSON(self):
        result = self.__instance.parse_JSON(OZONE_JSON)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.get_reference_time())
        self.assertIsNotNone(result.get_reception_time())
        loc = result.get_location()
        self.assertIsNotNone(loc)
        self.assertIsNone(loc.get_name())
        self.assertIsNone(loc.get_ID())
        self.assertIsNotNone(loc.get_lon())
        self.assertIsNotNone(loc.get_lat())
        self.assertIsNone(result.get_interval())
        self.assertIsNotNone(result.get_du_value())

    def test_parse_JSON_fails_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, OzoneParser.parse_JSON,
                          self.__instance, OZONE_MALFORMED_JSON)


