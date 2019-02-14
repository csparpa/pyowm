import json
import unittest
from datetime import datetime
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.exceptions.api_response_error import APIResponseError
from pyowm.utils.formatting import UTC
from pyowm.weatherapi25.stationhistory import StationHistory
from tests.unit.weatherapi25.json_test_dumps import STATIONHISTORY_JSON_DUMP
from tests.unit.weatherapi25.json_test_responses import (
     STATION_TICK_WEATHER_HISTORY_JSON, STATION_WEATHER_HISTORY_NOT_FOUND_JSON,
     INTERNAL_SERVER_ERROR_JSON)
from tests.unit.weatherapi25.xml_test_dumps import STATIONHISTORY_XML_DUMP


class TestStationHistory(unittest.TestCase):

    __test_station_ID = 2865
    __test_interval = "tick"
    __test_reception_time = 1378684800
    __test_reception_time_iso = '2013-09-09 00:00:00+00'
    __test_date_reception_time = datetime.strptime(__test_reception_time_iso,
                                   '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
    __test_measurements = {
        1362933983: {
             "temperature": 266.25,
             "humidity": 27.3,
             "pressure": 1010.02,
             "rain": None,
             "wind": 4.7
         },
        1362934043: {
             "temperature": 266.85,
             "humidity": 27.7,
             "pressure": 1010.09,
             "rain": None,
             "wind": 4.7
        }
    }

    __test_instance = StationHistory(__test_station_ID, 'tick',
                                     __test_reception_time,
                                     __test_measurements)

    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'

    def test_init_fails_when_negative_reception_time(self):
        self.assertRaises(ValueError, StationHistory, 1234, 'tick', -1234567,
                          self.__test_measurements)

    def test_getters_return_expected_3h_data(self):
        self.assertEqual(self.__test_instance.get_interval(),
                         self.__test_interval)
        self.assertEqual(self.__test_instance.get_station_ID(),
                         self.__test_station_ID)
        self.assertEqual(self.__test_instance.get_reception_time(),
                         self.__test_reception_time)
        self.assertEqual(self.__test_instance.get_measurements(),
                         self.__test_measurements)

    def test_returning_different_formats_for_reception_time(self):
        """
        Test get_reception_time returns timestamps in the expected formats
        """
        self.assertEqual(self.__test_instance.get_reception_time(timeformat='iso'),
                         self.__test_reception_time_iso)
        self.assertEqual(self.__test_instance.get_reception_time(timeformat='unix'),
                         self.__test_reception_time)
        self.assertEqual(self.__test_instance.get_reception_time(timeformat='date'), \
                         self.__test_date_reception_time)

    # Test JSON and XML comparisons by ordering strings (this overcomes
    # interpeter-dependant serialization of XML/JSON objects)

    def test_to_JSON(self):
        ordered_base_json = ''.join(sorted(STATIONHISTORY_JSON_DUMP))
        ordered_actual_json = ''.join(sorted(self.__test_instance.to_JSON()))
        self.assertEqual(ordered_base_json, ordered_actual_json)

    def test_to_XML(self):
        ordered_base_xml = ''.join(sorted(STATIONHISTORY_XML_DUMP))
        ordered_actual_xml = ''.join(sorted(self.__test_instance.to_XML()))
        self.assertEqual(ordered_base_xml, ordered_actual_xml)

    def test_from_dict(self):
        result = StationHistory.from_dict(json.loads(STATION_TICK_WEATHER_HISTORY_JSON))
        self.assertTrue(result)
        self.assertTrue(isinstance(result, StationHistory))
        self.assertTrue(result.get_measurements())

    def test_from_dict_fails_when_JSON_data_is_None(self):
        self.assertRaises(ParseResponseError, StationHistory.from_dict, None)

    def test_from_dict_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, StationHistory.from_dict, json.loads(self.__bad_json))

    def test_from_dict_with_empty_data(self):
        json_data = '{"message": "","cod": "200","type": "hour","station_id": ' \
            '35579,"calctime": 0.1122,"cnt": 1,"list": [{"main": "test","dt": ' \
            '1381140000}]}'
        result = StationHistory.from_dict(json.loads(json_data))
        datapoints = result.get_measurements()
        for datapoint in datapoints:
            self.assertTrue(all(value is None for value \
                                in datapoints[datapoint].values()))

    def test_from_dict_when_station_not_found(self):
        self.assertFalse(StationHistory.from_dict(json.loads(STATION_WEATHER_HISTORY_NOT_FOUND_JSON)))

    def test_from_dict_when_server_error(self):
        self.assertRaises(APIResponseError, StationHistory.from_dict, json.loads(INTERNAL_SERVER_ERROR_JSON))
