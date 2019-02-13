import unittest
from pyowm.pollutionapi30.parsers import COIndexParser, NO2IndexParser, SO2IndexParser
from pyowm.exceptions.parse_response_error import ParseResponseError


# JSON
COINDEX_JSON = '{"time":"2016-10-01T13:07:01Z","location":{"latitude":0,"longitude":9.2359},"data":[{"precision":-4.999999987376214e-07,"pressure":1000,"value":8.609262636127823e-08},{  "precision":-4.999999987376214e-07,"pressure":681.2920532226562,"value":1.1352169337897067e-07},{  "precision":-4.999999987376214e-07,"pressure":464.15887451171875,"value":1.1864428017815953e-07}]}'
COINDEX_MALFORMED_JSON = '{"time":"2016-10-01T13:07:01Z","xyz":[]}'
NO2INDEX_JSON = '{"time":"2016-03-03T12:00:00Z","location":{"latitude":0.0,"longitude":10.0},"data":{"no2":{"precision":1.436401748934656e+15,"value":2.550915831693312e+15},"no2_strat":{"precision":2.00000000753664e+14,"value":1.780239650783232e+15},"no2_trop":{"precision":1.464945698930688e+15,"value":7.7067618091008e+14}}}'
NO2INDEX_MALFORMED_JSON = '{"time":"2016-10-01T13:07:01Z","abc":[]}'
SO2INDEX_JSON = '{"time":"2016-10-01T13:07:01Z","location":{"latitude":0,"longitude":9.2359},"data":[{"precision":-4.999999987376214e-07,"pressure":1000,"value":8.609262636127823e-08},{  "precision":-4.999999987376214e-07,"pressure":681.2920532226562,"value":1.1352169337897067e-07},{  "precision":-4.999999987376214e-07,"pressure":464.15887451171875,"value":1.1864428017815953e-07}]}'
SO2INDEX_MALFORMED_JSON = '{"time":"2016-10-01T13:07:01Z","xyz":[]}'


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

    def test_parse_JSON_fails_when_JSON_data_is_None(self):
        self.assertRaises(ParseResponseError, COIndexParser.parse_JSON,
                          self.__instance, None)

    def test_parse_JSON_fails_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, COIndexParser.parse_JSON,
                          self.__instance, COINDEX_MALFORMED_JSON)


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

    def test_parse_JSON_fails_when_JSON_data_is_None(self):
        self.assertRaises(ParseResponseError, NO2IndexParser.parse_JSON,
                          self.__instance, None)

    def test_parse_JSON_fails_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, NO2IndexParser.parse_JSON,
                          self.__instance, NO2INDEX_MALFORMED_JSON)


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

