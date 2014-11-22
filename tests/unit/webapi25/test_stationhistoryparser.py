"""
Test case for stationhistoryparser.py module
"""
import unittest
from pyowm.webapi25.stationhistoryparser import StationHistoryParser
from pyowm.webapi25.stationhistory import StationHistory
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.exceptions.api_response_error import APIResponseError
from tests.unit.webapi25.json_test_responses import (
     STATION_TICK_WEATHER_HISTORY_JSON, STATION_WEATHER_HISTORY_NOT_FOUND_JSON,
     INTERNAL_SERVER_ERROR_JSON)


class TestStationHistoryParser(unittest.TestCase):

    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'
    __instance = StationHistoryParser()

    def test_parse_JSON(self):
        result = self.__instance.parse_JSON(STATION_TICK_WEATHER_HISTORY_JSON)
        self.assertTrue(result)
        self.assertTrue(isinstance(result, StationHistory))
        self.assertTrue(result.get_measurements())

    def test_parse_JSON_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, StationHistoryParser.parse_JSON, 
                          self.__instance, self.__bad_json)

    def test_parse_station_history_with_empty_data(self):
        json_data = '{"message": "","cod": "200","type": "hour","station_id": ' \
            '35579,"calctime": 0.1122,"cnt": 1,"list": [{"main": "test","dt": ' \
            '1381140000}]}'
        result = self.__instance.parse_JSON(json_data)
        datapoints = result.get_measurements()
        for datapoint in datapoints:
            self.assertTrue(all(value is None for value \
                                in datapoints[datapoint].values()))

    def test_parse_station_history_when_station_not_found(self):
        self.assertFalse(
             self.__instance.parse_JSON(STATION_WEATHER_HISTORY_NOT_FOUND_JSON))

    def test_parse_station_history_when_server_error(self):
        self.assertRaises(APIResponseError, StationHistoryParser.parse_JSON, \
                          self.__instance, INTERNAL_SERVER_ERROR_JSON)
