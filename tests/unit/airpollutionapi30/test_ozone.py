#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
from datetime import datetime
from pyowm.exceptions import parse_response_error
from pyowm.weatherapi25.location import Location
from pyowm.airpollutionapi30.ozone import Ozone
from pyowm.utils.formatting import UTC, datetime_to_UNIXtime
from tests.unit.airpollutionapi30.json_test_dumps import OZONE_JSON_DUMP

OZONE_JSON = '{"time":"2016-10-06T13:32:53Z","location":{"latitude":1.3841,"longitude":9.8633},"data":276.8447570800781}'
OZONE_MALFORMED_JSON = '{"time":"2016-10-06T13:32:53Z", "x": 1234}'


class TestOzone(unittest.TestCase):

    __test_reception_time = 1475283600
    __test_iso_reception_time = "2016-10-01 01:00:00+00"
    __test_date_reception_time = datetime.strptime(__test_iso_reception_time,
                               '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())

    __test_reference_time = 1234567
    __test_iso_reference_time = "1970-01-15 06:56:07+00"
    __test_date_reference_time = datetime.strptime(__test_iso_reference_time,
                               '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())

    __test_location = Location('test', 12.3, 43.7, 987, 'UK')
    __test_du_value = 6.8
    __test_interval = 'day'
    __test_exposure_risk = 'high'
    __test_instance = Ozone(
        __test_reference_time, __test_location, __test_interval,
        __test_du_value, __test_reception_time)

    def test_init_fails_when_reference_time_is_negative(self):
        self.assertRaises(ValueError, Ozone, -1234567,
                          self.__test_location,
                          self.__test_interval,
                          self.__test_du_value,
                          self.__test_reception_time)

    def test_init_fails_when_reception_time_is_negative(self):
        self.assertRaises(ValueError, Ozone,
                          self.__test_reference_time,
                          self.__test_location,
                          self.__test_interval,
                          self.__test_du_value,
                          -1234567)

    def test_init_fails_when_uv_intensity_is_negative(self):
        self.assertRaises(ValueError, Ozone, self.__test_reference_time,
                          self.__test_location, self.__test_interval, -8.9,
                          self.__test_reception_time)

    def test_getters_return_expected_data(self):
        self.assertEqual(self.__test_instance.get_reception_time(),
                         self.__test_reception_time)
        self.assertEqual(self.__test_instance.get_reference_time(),
                         self.__test_reference_time)
        self.assertEqual(self.__test_instance.get_location(),
                         self.__test_location)
        self.assertEqual(self.__test_instance.get_du_value(),
                         self.__test_du_value)
        self.assertEqual(self.__test_instance.get_interval(),
                         self.__test_interval)

    def test_returning_different_formats_for_reception_time(self):
        self.assertEqual(self.__test_instance.get_reception_time(timeformat='iso'), \
                         self.__test_iso_reception_time)
        self.assertEqual(self.__test_instance.get_reception_time(timeformat='unix'), \
                         self.__test_reception_time)
        self.assertEqual(self.__test_instance.get_reception_time(timeformat='date'), \
                         self.__test_date_reception_time)

    def test_returning_different_formats_for_reference_time(self):
        self.assertEqual(self.__test_instance.get_reference_time(timeformat='iso'), \
                         self.__test_iso_reference_time)
        self.assertEqual(self.__test_instance.get_reference_time(timeformat='unix'), \
                         self.__test_reference_time)
        self.assertEqual(self.__test_instance.get_reference_time(timeformat='date'), \
                         self.__test_date_reference_time)

    def test_is_forecast(self):
        self.assertFalse(self.__test_instance.is_forecast())
        in_a_year = datetime_to_UNIXtime(datetime.utcnow()) + 31536000
        uvindex = Ozone(in_a_year,
                          self.__test_location,
                          self.__test_interval,
                          self.__test_du_value,
                          self.__test_reception_time)
        self.assertTrue(uvindex.is_forecast())

    def test_from_dict(self):
        d = json.loads(OZONE_JSON)
        result = Ozone.from_dict(d)
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

    def test_from_dict_fails_when_JSON_data_is_None(self):
        self.assertRaises(parse_response_error.ParseResponseError, Ozone.from_dict, None)

    def test_from_dict_fails_with_malformed_JSON_data(self):
        self.assertRaises(parse_response_error.ParseResponseError, Ozone.from_dict, json.loads(OZONE_MALFORMED_JSON))

    def test_to_dict(self):
        expected = json.loads(OZONE_JSON_DUMP)
        result = self.__test_instance.to_dict()
        self.assertEqual(expected, result)
