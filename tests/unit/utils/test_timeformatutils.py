#!/usr/bin/env python

"""
Test case for timeformatutils.py module
"""

import unittest
from datetime import datetime
from pyowm.utils import timeformatutils


class TestTimeFormatUtils(unittest.TestCase):

    def test_timeformat(self):
        unixtime = 1378459200
        iso = "2013-09-06 09:20:00+00"
        self.assertEqual(unixtime, timeformatutils.timeformat(unixtime, "unix"))
        self.assertEqual(iso, timeformatutils.timeformat(unixtime, "iso"))
        self.assertEqual(unixtime, timeformatutils.timeformat(iso, "unix"))
        self.assertEqual(iso, timeformatutils.timeformat(iso, "iso"))

    def test_timeformat_when_bad_timeformat_values(self):
        self.assertRaises(ValueError,
                          timeformatutils.timeformat, 1378459200, "xyz")

    def test_to_ISO8601(self):
        unixtime = 1378459200
        iso = "2013-09-06 09:20:00+00"
        date = datetime(2013, 9, 6, 9, 20, 0)
        self.assertEqual(iso, timeformatutils.to_ISO8601(unixtime))
        self.assertEqual(iso, timeformatutils.to_ISO8601(iso))
        self.assertEqual(iso, timeformatutils.to_ISO8601(date))

    def test_to_ISO8601_fails_with_negative_values(self):
        self.assertRaises(ValueError,
                          timeformatutils.to_ISO8601,
                          -1378459200)

    def test_ISO8601_to_UNIXtime(self):
        iso = "2013-09-06 09:20:00+00"
        expected = 1378459200
        self.assertEqual(expected,
                         timeformatutils._ISO8601_to_UNIXtime(iso))

    def test_datetime_to_UNIXtime(self):
        date = datetime(2013, 9, 19, 12, 0)
        expected = 1379592000L
        self.assertEqual(timeformatutils._datetime_to_UNIXtime(date), expected)

    def test_ISO8601_to_UNIXtime_fails_with_bad_arugments(self):
        self.assertRaises(ValueError,
                          timeformatutils._ISO8601_to_UNIXtime,
                          "Tue, Sep 16 2013")

    def test_to_UNIXtime(self):
        unix = 1378459200
        iso = "2013-09-06 09:20:00+00"
        date = datetime(2013, 9, 6, 9, 20, 0)
        self.assertEqual(unix, timeformatutils.to_UNIXtime(unix))
        self.assertEqual(unix, timeformatutils.to_UNIXtime(iso))
        self.assertEqual(unix, timeformatutils.to_UNIXtime(date))

    def test_to_UNIXtime_fails_with_bad_argument(self):
        self.assertRaises(TypeError, timeformatutils.to_UNIXtime, None)

    def test_to_UNIXtime_fails_with_negative_unixtime(self):
        self.assertRaises(ValueError, timeformatutils.to_UNIXtime, -1234L)

if __name__ == "__main__":
    unittest.main()