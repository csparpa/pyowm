#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timezone
from pyowm.utils import formatting


class TestTimeFormatUtils(unittest.TestCase):

    def test_timeformat(self):
        unixtime = 1378459200
        iso = "2013-09-06 09:20:00+00:00"
        date = datetime(2013, 9, 6, 9, 20, 0, 0, timezone.utc)
        self.assertEqual(unixtime, formatting.timeformat(unixtime, "unix"))
        self.assertEqual(iso, formatting.timeformat(unixtime, "iso"))
        self.assertEqual(date, formatting.timeformat(unixtime, "date"))
        self.assertEqual(unixtime, formatting.timeformat(iso, "unix"))
        self.assertEqual(iso, formatting.timeformat(iso, "iso"))
        self.assertEqual(date, formatting.timeformat(iso, "date"))
        self.assertEqual(unixtime, formatting.timeformat(date, "unix"))
        self.assertEqual(iso, formatting.timeformat(date, "iso"))
        self.assertEqual(date, formatting.timeformat(date, "date"))

    def test_timeformat_when_bad_timeformat_values(self):
        self.assertRaises(ValueError,
                          formatting.timeformat, 1378459200, "xyz")

    def test_to_date(self):
        unixtime = 1378459200
        iso = "2013-09-06 09:20:00+00:00"
        date = datetime(2013, 9, 6, 9, 20, 0, 0, timezone.utc)
        self.assertEqual(date, formatting.to_date(unixtime))
        self.assertEqual(date, formatting.to_date(iso))
        self.assertEqual(date, formatting.to_date(date))

    def test_to_date_fails_with_negative_values(self):
        self.assertRaises(ValueError,
                          formatting.to_date,
                          -1378459200)

    def test_to_date_fails_with_unproper_argument_type(self):
        self.assertRaises(TypeError,
                          formatting.to_date,
                          list())

    def test_to_ISO8601(self):
        unixtime = 1378459200
        iso = "2013-09-06 09:20:00+00:00"
        date = datetime(2013, 9, 6, 9, 20, 0, 0, timezone.utc)
        self.assertEqual(iso, formatting.to_ISO8601(unixtime))
        self.assertEqual(iso, formatting.to_ISO8601(iso))
        self.assertEqual(iso, formatting.to_ISO8601(date))

    def test_to_ISO8601_fails_with_negative_values(self):
        self.assertRaises(ValueError,
                          formatting.to_ISO8601,
                          -1378459200)

    def test_to_ISO8601_fails_with_unproper_argument_type(self):
        self.assertRaises(TypeError,
                          formatting.to_ISO8601,
                          list())

    def test_ISO8601_to_UNIXtime(self):
        iso = "2013-09-06 09:20:00+00:00"
        expected = 1378459200
        self.assertEqual(expected,
                         formatting.ISO8601_to_UNIXtime(iso))

    def test_datetime_to_UNIXtime(self):
        date = datetime(2013, 9, 19, 12, 0, 0, 0, timezone.utc)
        expected = 1379592000
        self.assertEqual(formatting.datetime_to_UNIXtime(date), expected)

    def test_ISO8601_to_UNIXtime_fails_with_bad_arugments(self):
        self.assertRaises(ValueError,
                          formatting.ISO8601_to_UNIXtime,
                          "Tue, Sep 16 2013")

    def test_to_UNIXtime(self):
        unix = 1378459200
        iso = "2013-09-06 09:20:00+00:00"
        date = datetime(2013, 9, 6, 9, 20, 0, 0, timezone.utc)
        self.assertEqual(unix, formatting.to_UNIXtime(unix))
        self.assertEqual(unix, formatting.to_UNIXtime(iso))
        self.assertEqual(unix, formatting.to_UNIXtime(date))

    def test_to_UNIXtime_fails_with_bad_argument(self):
        self.assertRaises(TypeError, formatting.to_UNIXtime, None)

    def test_to_UNIXtime_fails_with_negative_unixtime(self):
        self.assertRaises(ValueError, formatting.to_UNIXtime, -1234)
