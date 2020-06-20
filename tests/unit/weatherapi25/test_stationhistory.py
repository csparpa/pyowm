#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from datetime import datetime
from pyowm.commons.exceptions import APIResponseError, ParseAPIResponseError
from pyowm.weatherapi25.stationhistory import StationHistory
from tests.unit.weatherapi25.json_test_responses import (
     STATION_TICK_WEATHER_HISTORY_JSON, STATION_WEATHER_HISTORY_NOT_FOUND_JSON,
     INTERNAL_SERVER_ERROR_JSON)


class TestStationHistory(unittest.TestCase):

    __test_station_ID = 2865
    __test_interval = "tick"
    __test_reception_time = 1378684800
    __test_reception_time_iso = '2013-09-09 00:00:00+00:00'
    __test_date_reception_time = datetime.fromisoformat(__test_reception_time_iso)
    __test_measurements = {
        '1362933983': {
             "temperature": 266.25,
             "humidity": 27.3,
             "pressure": 1010.02,
             "rain": None,
             "wind": 4.7
         },
        '1362934043': {
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

    STATIONHISTORY_JSON_DUMP = '{"reception_time": 1378684800, "interval": ' \
                               + '"tick", "measurements": {"1362934043": {"wind": 4.7, "pressure": ' \
                               + '1010.09, "temperature": 266.85, "rain": null, "humidity": 27.7}, ' \
                               + '"1362933983": {"wind": 4.7, "pressure": 1010.02, "temperature": ' \
                               + '266.25, "rain": null, "humidity": 27.3}}, "station_ID": 2865}'

    def test_init_fails_when_negative_reception_time(self):
        self.assertRaises(ValueError, StationHistory, 1234, 'tick', -1234567,
                          self.__test_measurements)

    def test_returning_different_formats_for_reception_time(self):
        """
        Test get_reception_time returns timestamps in the expected formats
        """
        self.assertEqual(self.__test_instance.reception_time(timeformat='iso'),
                         self.__test_reception_time_iso)
        self.assertEqual(self.__test_instance.reception_time(timeformat='unix'),
                         self.__test_reception_time)
        self.assertEqual(self.__test_instance.reception_time(timeformat='date'), \
                         self.__test_date_reception_time)

    def test_from_dict(self):
        result = StationHistory.from_dict(json.loads(STATION_TICK_WEATHER_HISTORY_JSON))
        self.assertTrue(result)
        self.assertTrue(isinstance(result, StationHistory))
        self.assertTrue(result.measurements)

    def test_from_dict_fails_when_JSON_data_is_None(self):
        self.assertRaises(ParseAPIResponseError, StationHistory.from_dict, None)

    def test_from_dict_with_malformed_JSON_data(self):
        self.assertRaises(ParseAPIResponseError, StationHistory.from_dict, json.loads(self.__bad_json))

    def test_from_dict_with_empty_data(self):
        json_data = '{"message": "","cod": "200","type": "hour","station_id": ' \
            '35579,"calctime": 0.1122,"cnt": 1,"list": [{"main": "test","dt": ' \
            '1381140000}]}'
        result = StationHistory.from_dict(json.loads(json_data))
        datapoints = result.measurements
        for datapoint in datapoints:
            self.assertTrue(all(value is None for value \
                                in datapoints[datapoint].values()))

    def test_from_dict_when_station_not_found(self):
        self.assertFalse(StationHistory.from_dict(json.loads(STATION_WEATHER_HISTORY_NOT_FOUND_JSON)))

    def test_from_dict_when_server_error(self):
        self.assertRaises(APIResponseError, StationHistory.from_dict, json.loads(INTERNAL_SERVER_ERROR_JSON))

    def test_to_dict(self):
        expected = json.loads(self.STATIONHISTORY_JSON_DUMP)
        result = self.__test_instance.to_dict()
        self.assertEqual(expected, result)

    def test__repr(self):
        print(self.__test_instance)
