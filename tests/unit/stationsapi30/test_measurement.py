#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import json
import unittest
from datetime import datetime as dt
import pyowm.commons.exceptions
from pyowm.stationsapi30.measurement import AggregatedMeasurement, Measurement
from pyowm.utils.formatting import UTC


class TestAggregatedMeasurement(unittest.TestCase):

    ts = 1378459200
    iso_ts = "2013-09-06 09:20:00+00"
    date_ts = dt.strptime(iso_ts, '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())

    _test_instance = AggregatedMeasurement('mytest', ts, 'm',
                                           temp=dict(min=0, max=100),
                                           humidity=dict(min=10, max=110),
                                           wind=dict(speed=2.1, gust=67),
                                           pressure=None,
                                           precipitation=None)

    def test_assertions_on_instantation(self):
        with self.assertRaises(AssertionError):
            AggregatedMeasurement(None, self.ts, 'h', temp=None, humidity=None,
                                  wind=None, pressure=None, precipitation=None)
        with self.assertRaises(AssertionError):
            AggregatedMeasurement('test', None, 'h', temp=None, humidity=None,
                                  wind=None, pressure=None, precipitation=None)
        with self.assertRaises(AssertionError):
            AggregatedMeasurement('test', '1234', 'h', temp=None, humidity=None,
                                  wind=None, pressure=None, precipitation=None)
        with self.assertRaises(AssertionError):
            AggregatedMeasurement('test', -123, 'h', temp=None, humidity=None,
                                  wind=None, pressure=None, precipitation=None)
        with self.assertRaises(AssertionError):
            AggregatedMeasurement('test', self.ts, None, temp=None, humidity=None,
                                  wind=None, pressure=None, precipitation=None)

    def test_aggregated_on_with_wrong_values(self):
        with self.assertRaises(ValueError):
            wrong = 'xyz'
            AggregatedMeasurement('mytest', self.ts, wrong,
                                   temp=dict(min=0, max=100),
                                   humidity=dict(min=10, max=110),
                                   wind=dict(speed=2.1, gust=67),
                                   pressure=None,
                                   precipitation=None)

    def test_creation_time(self):
        result = self._test_instance.creation_time()
        self.assertEqual(self.ts, result)
        result = self._test_instance.creation_time(timeformat='iso')
        self.assertEqual(self.iso_ts, result)
        result = self._test_instance.creation_time(timeformat='date')
        self.assertEqual(self.date_ts, result)
        with self.assertRaises(ValueError):
            self._test_instance.creation_time(timeformat='unknown')

        test_instance_none_timestamp = copy.deepcopy(self._test_instance)
        test_instance_none_timestamp.timestamp = None
        self.assertIsNone(test_instance_none_timestamp.creation_time())

    def test_from_dict(self):
        the_dict = {
            "station_id": "mytest",
            "date": 123456789,
            "type": "m",
            "temp":{"min": 0, "max": 100},
            "humidity": {"min": 10, "max": 110},
            "wind": {"speed": 2.1,"gust": 67},
            "pressure": {},
            "precipitation": {}}

        expected = AggregatedMeasurement('mytest', 123456789, 'm',
                                          temp=dict(min=0, max=100),
                                          humidity=dict(min=10, max=110),
                                          wind=dict(speed=2.1, gust=67),
                                          pressure=None,
                                          precipitation=None)

        result = AggregatedMeasurement.from_dict(the_dict)
        self.assertTrue(isinstance(result, AggregatedMeasurement))

        self.assertEqual(expected.station_id, result.station_id)
        self.assertEqual(expected.timestamp, result.timestamp)
        self.assertEqual(expected.aggregated_on, result.aggregated_on)
        self.assertEqual(expected.temp, result.temp)
        self.assertEqual(expected.humidity, result.humidity)
        self.assertEqual(expected.wind, result.wind)
        self.assertEqual(expected.pressure, result.pressure)
        self.assertEqual(expected.precipitation, result.precipitation)

        with self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError):
            AggregatedMeasurement.from_dict(None)

        with self.assertRaises(AssertionError):
            none_timestamp = copy.deepcopy(the_dict)
            none_timestamp['date'] = None
            AggregatedMeasurement.from_dict(none_timestamp)

    def test_to_dict(self):
        expected_dict = {
            "station_id": "mytest",
            "timestamp": 1378459200,
            "aggregated_on": "m",
            "temp":{"min": 0, "max": 100},
            "humidity": {"min": 10, "max": 110},
            "wind": {"speed": 2.1,"gust": 67},
            "pressure": {},
            "precipitation": {}}
        result_dict = self._test_instance.to_dict()
        self.assertTrue(all(item in result_dict.items()
                            for item in expected_dict.items()))


class TestMeasurement(unittest.TestCase):

    ts = 1378459200
    iso_ts = "2013-09-06 09:20:00+00"
    date_ts = dt.strptime(iso_ts, '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())

    _test_instance = Measurement('mytest', ts, temperature=dict(min=0, max=100),
        wind_speed=2.1, wind_gust=67, humidex=77, weather_other=dict(key='val'))

    def test_assertions_on_instantation(self):
        with self.assertRaises(AssertionError):
            Measurement(None, self.ts, temperature=dict(min=0, max=100),
                    wind_speed=2.1, wind_gust=67, humidex=77,
                    weather_other=dict(key='val'))
        with self.assertRaises(AssertionError):
            Measurement(None, '12345', temperature=dict(min=0, max=100),
                    wind_speed=2.1, wind_gust=67, humidex=77,
                    weather_other=dict(key='val'))
        with self.assertRaises(AssertionError):
            Measurement(None, -123, temperature=dict(min=0, max=100),
                    wind_speed=2.1, wind_gust=67, humidex=77,
                    weather_other=dict(key='val'))

    def test_creation_time(self):
        result = self._test_instance.creation_time()
        self.assertEqual(self.ts, result)
        result = self._test_instance.creation_time(timeformat='iso')
        self.assertEqual(self.iso_ts, result)
        result = self._test_instance.creation_time(timeformat='date')
        self.assertEqual(self.date_ts, result)
        with self.assertRaises(ValueError):
            self._test_instance.creation_time(timeformat='unknown')

        test_instance_none_timestamp = copy.deepcopy(self._test_instance)
        test_instance_none_timestamp.timestamp = None
        self.assertIsNone(test_instance_none_timestamp.creation_time())

    def test_from_dict(self):
        _the_dict = dict(station_id='mytest', timestamp=1378459200,
                         temperature=dict(min=0, max=100), wind_speed=2.1,
                         wind_gust=67, humidex=77, weather_other=dict(key='val'))
        result = Measurement.from_dict(_the_dict)
        self.assertEqual(self._test_instance.station_id, result.station_id)
        self.assertEqual(self._test_instance.timestamp, result.timestamp)
        self.assertEqual(self._test_instance.temperature, result.temperature)
        self.assertEqual(self._test_instance.wind_gust, result.wind_gust)
        self.assertEqual(self._test_instance.wind_speed, result.wind_speed)
        self.assertEqual(self._test_instance.humidex, result.humidex)
        self.assertEqual(self._test_instance.weather_other, result.weather_other)

    def test_from_dict_with_missing_values(self):
        with self.assertRaises(KeyError):
            Measurement.from_dict(dict(timestamp=123456789))
        with self.assertRaises(KeyError):
            Measurement.from_dict(dict(station_id='mytest'))

    def test_to_dict(self):
        expected_dict = {
            "station_id": "mytest",
            "timestamp": 1378459200,
            "temperature": {"min":0, "max": 100},
            "wind_speed": 2.1,
            "wind_gust": 67,
            "humidex": 77,
            "weather_other": {"key": "val"}}
        result_dict = self._test_instance.to_dict()
        self.assertTrue(all(item in result_dict.items()
                            for item in expected_dict.items()))

    def test_to_JSON(self):
        expected = '''
        {"station_id": "mytest",
        "timestamp": 1378459200,
        "temperature":{"min":0, "max": 100},
        "wind_speed":2.1,
        "wind_gust":67,
        "humidex":77,
        "weather_other":{"key":"val"}}
        '''
        result_dict = json.loads(self._test_instance.to_JSON())
        expected_dict = json.loads(expected)
        self.assertTrue(all(item in result_dict.items()
                            for item in expected_dict.items()))

    def test_repr(self):
        str(self._test_instance)

