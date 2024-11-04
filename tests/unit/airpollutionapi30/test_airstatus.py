#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
from datetime import datetime
import pyowm.commons.exceptions
from pyowm.weatherapi30.location import Location
from pyowm.airpollutionapi30.airstatus import AirStatus


AIRSTATUS_JSON = '{"coord":{"lon":-0.1278,"lat":51.5074},"list":[{"main":{"aqi":1},"components":{"co":250.34,"no":0.19,"no2":35.99,"o3":30.76,"so2":8.11,"pm2_5":3.15,"pm10":3.81,"nh3":0.74},"dt":1611597600}]}'
AIRSTATUS_MULTIPLE_JSON = '{"coord":{"lon":50,"lat":50},"list":[{"main":{"aqi":1},"components":{"co":240.33,"no":0,"no2":1.07,"o3":79.39,"so2":0.97,"pm2_5":1.84,"pm10":1.9,"nh3":1.25},"dt":1613606400},{"main":{"aqi":1},"components":{"co":240.33,"no":0,"no2":0.98,"o3":79.39,"so2":0.69,"pm2_5":1.92,"pm10":1.97,"nh3":1.36},"dt":1613610000}]}'
AIRSTATUS_MALFORMED_JSON = '{"time":"2016-10-01T13:07:01Z","xyz":[]}'
AIRSTATUS_JSON_DUMP = '{"reference_time": 1234567, "location": {"name": "test", "coordinates": {"lon": 12.3, "lat": 43.7}, "ID": 987, "country": "UK"}, "air_quality_data": {"aqi": 1, "co": 250.34, "no": 0.19, "no2": 35.99, "o3": 30.76, "so2": 8.11, "pm2_5": 3.15, "pm10": 3.81, "nh3": 0.74}, "reception_time": 1475283600}'


class TestAirStatus(unittest.TestCase):

    __test_reception_time = 1475283600
    __test_iso_reception_time = "2016-10-01 01:00:00+00:00"
    __test_date_reception_time = datetime.fromisoformat(__test_iso_reception_time)

    __test_reference_time = 1234567
    __test_iso_reference_time = "1970-01-15 06:56:07+00:00"
    __test_date_reference_time = datetime.fromisoformat(__test_iso_reference_time)
    __test_location = Location('test', 12.3, 43.7, 987, 'UK')
    __test_air_quality_data = {"aqi": 1, "co": 250.34, "no": 0.19, "no2": 35.99, "o3": 30.76, "so2": 8.11, "pm2_5": 3.15, "pm10": 3.81, "nh3": 0.74}
    __test_interval = 'day'
    __test_instance = AirStatus(
        __test_reference_time, __test_location, __test_air_quality_data, __test_reception_time)

    def test_init_fails_when_reference_time_is_negative(self):
        self.assertRaises(ValueError, AirStatus, -1234567,
                          self.__test_location,
                          self.__test_air_quality_data,
                          self.__test_reception_time)

    def test_init_fails_when_reception_time_is_negative(self):
        self.assertRaises(ValueError, AirStatus,
                          self.__test_reference_time,
                          self.__test_location,
                          self.__test_air_quality_data,
                          -1234567)

    def test_init_fails_when_air_quality_data_is_not_a_dict(self):
        self.assertRaises(ValueError, AirStatus, self.__test_reference_time,
                          self.__test_location, 'test',
                          self.__test_reception_time)

    def test_returning_different_formats_for_reference_time(self):
        self.assertEqual(self.__test_instance.reference_time(timeformat='iso'), \
                         self.__test_iso_reference_time)
        self.assertEqual(self.__test_instance.reference_time(timeformat='unix'), \
                         self.__test_reference_time)
        self.assertEqual(self.__test_instance.reference_time(timeformat='date'), \
                         self.__test_date_reference_time)

    def test_returning_different_formats_for_reception_time(self):
        self.assertEqual(self.__test_instance.reception_time(timeformat='iso'), \
                         self.__test_iso_reception_time)
        self.assertEqual(self.__test_instance.reception_time(timeformat='unix'), \
                         self.__test_reception_time)
        self.assertEqual(self.__test_instance.reception_time(timeformat='date'), \
                         self.__test_date_reception_time)

    def test_from_dict(self):
        # one item
        d = json.loads(AIRSTATUS_JSON)
        result = AirStatus.from_dict(d)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.reference_time())
        loc = result.location
        self.assertIsNotNone(loc)
        self.assertIsNone(loc.name)
        self.assertIsNone(loc.id)
        self.assertIsNotNone(loc.lon)
        self.assertIsNotNone(loc.lat)
        for key in self.__test_air_quality_data:
            getattr(result, key)

        # multiple items
        d = json.loads(AIRSTATUS_MULTIPLE_JSON)
        result = AirStatus.from_dict(d)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, AirStatus)
            self.assertIsNotNone(item.reference_time())
            loc = item.location
            self.assertIsNotNone(loc)
            self.assertIsNone(loc.name)
            self.assertIsNone(loc.id)
            self.assertIsNotNone(loc.lon)
            self.assertIsNotNone(loc.lat)
            for key in self.__test_air_quality_data:
                getattr(item, key)

    def test_from_dict_fails_when_JSON_data_is_None(self):
        self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError, AirStatus.from_dict, None)

    def test_from_dict_fails_with_malformed_JSON_data(self):
        self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError, AirStatus.from_dict, json.loads(AIRSTATUS_MALFORMED_JSON))

    def test_to_dict(self):
        expected = json.loads(AIRSTATUS_JSON_DUMP)
        result = self.__test_instance.to_dict()

        ordered_str_expected = sorted(str(expected))
        ordered_str_result = sorted(str(result))
        self.assertEqual(ordered_str_expected, ordered_str_result)

    def test_repr(self):
        print(self.__test_instance)
