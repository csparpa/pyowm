#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
from datetime import datetime
import pyowm.commons.exceptions
from pyowm.weatherapi25.location import Location
from pyowm.airpollutionapi30.coindex import COIndex
from pyowm.utils.formatting import UTC, datetime_to_UNIXtime


COINDEX_JSON = '{"time":"2016-10-01T13:07:01Z","location":{"latitude":0,"longitude":9.2359},"data":[{"precision":-4.999999987376214e-07,"pressure":1000,"value":8.609262636127823e-08},{  "precision":-4.999999987376214e-07,"pressure":681.2920532226562,"value":1.1352169337897067e-07},{  "precision":-4.999999987376214e-07,"pressure":464.15887451171875,"value":1.1864428017815953e-07}]}'
COINDEX_MALFORMED_JSON = '{"time":"2016-10-01T13:07:01Z","xyz":[]}'
COINDEX_JSON_DUMP = '{"reference_time": 1234567, "co_samples": [{"pressure": ' \
                    '1000, "value": 8.168363052618588e-08, "precision": ' \
                    '-4.999999987376214e-07}, {"pressure": 681.2920532226562, ' \
                    '"value": 8.686949115599418e-08, "precision": ' \
                    '-4.999999987376214e-07}, {"pressure": 464.15887451171875, ' \
                    '"value": 8.871462853221601e-08, "precision": ' \
                    '-4.999999987376214e-07}], "location": {"country": "UK", ' \
                    '"name": "test", "coordinates": {"lat": 43.7, "lon": 12.3}, ' \
                    '"ID": 987}, "interval": "day", "reception_time": 1475283600}'


class TestCOIndex(unittest.TestCase):

    __test_reception_time = 1475283600
    __test_iso_reception_time = "2016-10-01 01:00:00+00"
    __test_date_reception_time = datetime.strptime(__test_iso_reception_time,
                               '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())

    __test_reference_time = 1234567
    __test_iso_reference_time = "1970-01-15 06:56:07+00"
    __test_date_reference_time = datetime.strptime(__test_iso_reference_time,
                               '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
    __test_location = Location('test', 12.3, 43.7, 987, 'UK')
    __test_co_samples = [
        {
            "precision": -4.999999987376214e-7,
            "pressure": 1000,
            "value": 8.168363052618588e-8
        },
        {
            "precision": -4.999999987376214e-7,
            "pressure": 681.2920532226562,
            "value": 8.686949115599418e-8
        },
        {
            "precision": -4.999999987376214e-7,
            "pressure": 464.15887451171875,
            "value": 8.871462853221601e-8
        }
    ]
    __test_interval = 'day'
    __test_instance = COIndex(
        __test_reference_time, __test_location, __test_interval,
        __test_co_samples, __test_reception_time)

    def test_init_fails_when_reference_time_is_negative(self):
        self.assertRaises(ValueError, COIndex, -1234567,
                          self.__test_location,
                          self.__test_interval,
                          self.__test_co_samples,
                          self.__test_reception_time)

    def test_init_fails_when_reception_time_is_negative(self):
        self.assertRaises(ValueError, COIndex,
                          self.__test_reference_time,
                          self.__test_location,
                          self.__test_interval,
                          self.__test_co_samples,
                          -1234567)

    def test_init_fails_when_co_samples_is_not_a_list(self):
        self.assertRaises(ValueError, COIndex, self.__test_reference_time,
                          self.__test_location, self.__test_interval, 'test',
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

    def test_is_forecast(self):
        self.assertFalse(self.__test_instance.is_forecast())
        in_a_year = datetime_to_UNIXtime(datetime.utcnow()) + 31536000
        uvindex = COIndex(in_a_year,
                          self.__test_location, self.__test_interval,
                          [], self.__test_reception_time)
        self.assertTrue(uvindex.is_forecast())

    def test_co_sample_with_highest_vmr(self):
        expected = {
            "precision": -4.999999987376214e-7,
            "pressure": 464.15887451171875,
            "value": 8.871462853221601e-8
        }
        result = self.__test_instance.sample_with_highest_vmr()
        self.assertEqual(expected, result)

    def test_co_sample_with_lowest_vmr(self):
        expected = {
            "precision": -4.999999987376214e-7,
            "pressure": 1000,
            "value": 8.168363052618588e-8
        }
        result = self.__test_instance.sample_with_lowest_vmr()
        self.assertEqual(expected, result)

    def test_from_dict(self):
        d = json.loads(COINDEX_JSON)
        result = COIndex.from_dict(d)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.reference_time())
        self.assertIsNotNone(result.reference_time())
        loc = result.location
        self.assertIsNotNone(loc)
        self.assertIsNone(loc.name)
        self.assertIsNone(loc.id)
        self.assertIsNotNone(loc.lon)
        self.assertIsNotNone(loc.lat)
        self.assertIsNone(result.interval)
        self.assertNotEqual(0, len(result.co_samples))

    def test_from_dict_fails_when_JSON_data_is_None(self):
        self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError, COIndex.from_dict, None)

    def test_from_dict_fails_with_malformed_JSON_data(self):
        self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError, COIndex.from_dict, json.loads(COINDEX_MALFORMED_JSON))

    def test_to_dict(self):
        expected = json.loads(COINDEX_JSON_DUMP)
        result = self.__test_instance.to_dict()
        ordered_str_expected = sorted(str(expected))
        ordered_str_result = sorted(str(result))
        self.assertEqual(ordered_str_expected, ordered_str_result)

    def test_repr(self):
        print(self.__test_instance)
