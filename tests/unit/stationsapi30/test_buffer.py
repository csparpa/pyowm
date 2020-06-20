#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
from copy import deepcopy
from datetime import datetime as dt
from pyowm.stationsapi30.measurement import Measurement
from pyowm.stationsapi30.buffer import Buffer
from pyowm.utils.formatting import to_date, to_ISO8601


class TestBuffer(unittest.TestCase):

    ts = 1378459200
    iso_ts = "2013-09-06 09:20:00+00:00"
    date_ts = dt.fromisoformat(iso_ts)

    station_id = 'mytest'

    m1 = Measurement(station_id, ts, temperature=dict(min=0, max=100),
        wind_speed=2.1, wind_gust=67, humidex=77, weather_other=dict(key='val'))
    m2 = Measurement(station_id, ts+500, temperature=dict(min=30, max=800),
        wind_speed=8.5, wind_gust=0, humidex=0)
    m3 = Measurement(station_id, ts-1000, temperature=dict(min=0, max=20),
        wind_speed=4.4, wind_gust=-12, humidex=2)

    def test_assertions_on_instantiation(self):
        with self.assertRaises(AssertionError):
            Buffer(None)

    def test_creation_time(self):
        buf = Buffer(self.station_id)
        ts = buf.creation_time()
        iso_result = buf.creation_time(timeformat='iso')
        self.assertEqual(to_ISO8601(ts), iso_result)
        date_result = buf.creation_time(timeformat='date')
        self.assertEqual(to_date(ts), date_result)
        with self.assertRaises(ValueError):
            buf.creation_time(timeformat='unknown')

        buf.created_at = None
        self.assertIsNone(buf.creation_time())

    def test_append(self):
        buf = Buffer(self.station_id)
        self.assertEqual(0, len(buf))
        buf.append(self.m1)
        self.assertEqual(1, len(buf))
        self.assertTrue(self.m1 in buf)

        buf = Buffer(self.station_id)

        with self.assertRaises(AssertionError):
            buf.append('not_a_measurement')

        msmt = deepcopy(self.m1)
        msmt.station_id = 'another_id'
        with self.assertRaises(AssertionError):
            buf.append(msmt)

    def test_append_from_dict(self):
        buf = Buffer(self.station_id)
        self.assertEqual(0, len(buf))
        the_dict = dict(station_id='mytest', timestamp=1378459200,
                        temperature=dict(min=0, max=100), wind_speed=2.1,
                        wind_gust=67, humidex=77, weather_other=dict(key='val'))
        buf.append_from_dict(the_dict)
        self.assertEqual(1, len(buf))

    def test_append_from_json(self):
        buf = Buffer(self.station_id)
        self.assertEqual(0, len(buf))
        the_dict = dict(station_id='mytest', timestamp=1378459200,
                        temperature=dict(min=0, max=100), wind_speed=2.1,
                        wind_gust=67, humidex=77, weather_other=dict(key='val'))
        json_str = json.dumps(the_dict)
        buf.append_from_json(json_str)
        self.assertEqual(1, len(buf))

    def test_empty(self):
        buf = Buffer(self.station_id)
        self.assertEqual(0, len(buf))
        buf.append(self.m1)
        buf.append(self.m2)
        buf.append(self.m3)
        self.assertEqual(3, len(buf))
        self.assertTrue(self.m1 in buf)
        self.assertTrue(self.m2 in buf)
        self.assertTrue(self.m3 in buf)
        buf.empty()
        self.assertEqual(0, len(buf))

    def test_sort_chronologically(self):
        ordered_chrono = [self.m3, self.m1, self.m2]
        buf = Buffer(station_id=self.station_id)
        buf.append(self.m1)
        buf.append(self.m2)
        buf.append(self.m3)
        self.assertNotEqual(buf.measurements, ordered_chrono)
        buf.sort_chronologically()
        self.assertEqual(buf.measurements, ordered_chrono)

    def test_sort_reverse_chronologically(self):
        ordered_reverse_chrono = [self.m2, self.m1, self.m3]
        buf = Buffer(station_id=self.station_id)
        buf.append(self.m1)
        buf.append(self.m2)
        buf.append(self.m3)
        self.assertNotEqual(buf.measurements, ordered_reverse_chrono)
        buf.sort_reverse_chronologically()
        self.assertEqual(buf.measurements, ordered_reverse_chrono)

    def test_iteration(self):
        buf = Buffer(station_id=self.station_id)
        buf.append(self.m1)
        buf.append(self.m2)
        buf.append(self.m3)
        for item in buf:
            self.assertTrue(isinstance(item, Measurement))
            self.assertTrue(item in [self.m1, self.m2, self.m3])

    def test_contains(self):
        buf = Buffer(station_id=self.station_id)
        buf.append(self.m1)
        self.assertFalse(self.m3 in buf)
        self.assertTrue(self.m1 in buf)
        self.assertFalse(self.m2 in buf)

    def test_add(self):
        buf1 = Buffer(station_id=self.station_id)
        buf1.append(self.m1)
        buf2 = Buffer(station_id=self.station_id)
        buf2.append(self.m2)
        buf2.append(self.m3)
        result = buf1 + buf2
        self.assertEqual(3, len(result))

    def test_repr(self):
        buf = Buffer(self.station_id)
        buf.append(self.m2)
        str(buf)
