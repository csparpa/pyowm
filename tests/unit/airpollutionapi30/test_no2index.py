#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
from datetime import datetime
from pyowm.weatherapi25.location import Location
from pyowm.commons.exceptions import ParseAPIResponseError
from pyowm.airpollutionapi30.no2index import NO2Index
from pyowm.utils.formatting import datetime_to_UNIXtime

NO2INDEX_JSON = '{"time":"2016-03-03T12:00:00Z","location":{"latitude":0.0,"longitude":10.0},"data":{"no2":{"precision":1.436401748934656e+15,"value":2.550915831693312e+15},"no2_strat":{"precision":2.00000000753664e+14,"value":1.780239650783232e+15},"no2_trop":{"precision":1.464945698930688e+15,"value":7.7067618091008e+14}}}'
NO2INDEX_MALFORMED_JSON = '{"time":"2016-10-01T13:07:01Z","abc":[]}'
NO2INDEX_JSON_DUMP = '{"reference_time": 1234567, "no2_samples": [{"label": ' \
                    '"no2", "value": 8.168363052618588e-08, "precision": ' \
                    '-4.999999987376214e-07}, {"label": "no2_strat", ' \
                    '"value": 8.686949115599418e-08, "precision": ' \
                    '-4.999999987376214e-07}, {"label": "no2_trop", ' \
                    '"value": 8.871462853221601e-08, "precision": ' \
                    '-4.999999987376214e-07}], "location": {"country": "UK", ' \
                    '"name": "test", "coordinates": {"lat": 43.7, "lon": 12.3}, ' \
                    '"ID": 987}, "interval": "day", "reception_time": 1475283600}'


class TestNO2Index(unittest.TestCase):

    __test_reception_time = 1475283600
    __test_iso_reception_time = "2016-10-01 01:00:00+00:00"
    __test_date_reception_time = datetime.fromisoformat(__test_iso_reception_time)

    __test_reference_time = 1234567
    __test_iso_reference_time = "1970-01-15 06:56:07+00:00"
    __test_date_reference_time = datetime.fromisoformat(__test_iso_reference_time)
    __test_location = Location('test', 12.3, 43.7, 987, 'UK')
    __test_no2_samples = [
        {
            "precision": -4.999999987376214e-7,
            "label": "no2",
            "value": 8.168363052618588e-8
        },
        {
            "precision": -4.999999987376214e-7,
            "label": "no2_strat",
            "value": 8.686949115599418e-8
        },
        {
            "precision": -4.999999987376214e-7,
            "label": "no2_trop",
            "value": 8.871462853221601e-8
        }
    ]
    __test_interval = 'day'
    __test_instance = NO2Index(
        __test_reference_time, __test_location, __test_interval,
        __test_no2_samples, __test_reception_time)

    def test_init_fails_when_reference_time_is_negative(self):
        self.assertRaises(ValueError, NO2Index, -1234567,
                          self.__test_location,
                          self.__test_interval,
                          self.__test_no2_samples,
                          self.__test_reception_time)

    def test_init_fails_when_reception_time_is_negative(self):
        self.assertRaises(ValueError, NO2Index,
                          self.__test_reference_time,
                          self.__test_location,
                          self.__test_interval,
                          self.__test_no2_samples,
                          -1234567)

    def test_init_fails_when_co_samples_is_not_a_list(self):
        self.assertRaises(ValueError, NO2Index, self.__test_reference_time,
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
        uvindex = NO2Index(in_a_year,
                           self.__test_location, self.__test_interval,
                           [], self.__test_reception_time)
        self.assertTrue(uvindex.is_forecast())

    def test_get_sample_by_label(self):
        expected = {
            "precision": -4.999999987376214e-7,
            "label": "no2_strat",
            "value": 8.686949115599418e-8
        }

        result = self.__test_instance.get_sample_by_label('no2_strat')
        self.assertEqual(expected, result)

        self.assertIsNone(self.__test_instance.get_sample_by_label('unexistent'))

    def test_from_dict(self):
        result = NO2Index.from_dict(json.loads(NO2INDEX_JSON))
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
        self.assertNotEqual(0, len(result.no2_samples))

    def test_test_from_dict_fails_when_JSON_data_is_None(self):
        self.assertRaises(ParseAPIResponseError, NO2Index.from_dict, None)

    def test_test_from_dict_fails_with_malformed_JSON_data(self):
        self.assertRaises(ParseAPIResponseError, NO2Index.from_dict, json.loads(NO2INDEX_MALFORMED_JSON))

    def test_to_dict(self):
        expected = json.loads(NO2INDEX_JSON_DUMP)
        result = self.__test_instance.to_dict()
        self.assertEqual(expected, result)

    def test_repr(self):
        print(self.__test_instance)
