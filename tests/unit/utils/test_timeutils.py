"""
Test case for timeutils.py module
"""

import unittest
from datetime import datetime, date, timedelta
from pyowm.utils import timeutils, timeformatutils


class TestTimeUtils(unittest.TestCase):

    def test_tomorrow(self):
        now = datetime.now()
        tomorrow = date.today() + timedelta(days=1)
        result = timeutils.tomorrow()
        expected = datetime(tomorrow.year, tomorrow.month, tomorrow.day,
                            now.hour, now.minute, 0)
        self.assertEqual(expected, result)

    def test_tomorrow_with_hour_and_minute(self):
        tomorrow = date.today() + timedelta(days=1)
        result = timeutils.tomorrow(18, 56)
        expected = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 18,
                            56, 0)
        self.assertEqual(expected, result)

    def test_tomorrow_with_hour_only(self):
        now = datetime.now()
        tomorrow = date.today() + timedelta(days=1)
        result = timeutils.tomorrow(6)
        expected = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 6,
                            now.minute, 0)
        self.assertEqual(expected, result)

    def test_yesterday(self):
        now = datetime.now()
        yesterday = date.today() + timedelta(days=-1)
        result = timeutils.yesterday()
        expected = datetime(yesterday.year, yesterday.month, yesterday.day,
                            now.hour, now.minute, 0)
        self.assertEqual(expected, result)

    def test_yesterday_with_hour_and_minute(self):
        yesterday = date.today() + timedelta(days=-1)
        result = timeutils.yesterday(18, 56)
        expected = datetime(yesterday.year, yesterday.month, yesterday.day, 18,
                            56, 0)
        self.assertEqual(expected, result)

    def test_yesterday_with_hour_only(self):
        now = datetime.now()
        yesterday = date.today() + timedelta(days=-1)
        result = timeutils.yesterday(6)
        expected = datetime(yesterday.year, yesterday.month, yesterday.day, 6,
                            now.minute, 0)
        self.assertEqual(expected, result)

    def test_next_three_hours(self):
        result = timeutils.next_three_hours()
        expected = datetime.now() + timedelta(hours=3)
        self.assertAlmostEqual(
           float(timeformatutils.to_UNIXtime(expected)),
           float(timeformatutils.to_UNIXtime(result)))

    def test_next_three_hours_after_specified_time(self):
        d = datetime(2013, 12, 7, 15, 46, 12)
        expected = d + timedelta(hours=3)
        result = timeutils.next_three_hours(d)
        self.assertAlmostEqual(expected, result)

    def test_last_three_hours(self):
        result = timeutils.last_three_hours()
        expected = datetime.now() + timedelta(hours=-3)
        self.assertAlmostEqual(
           float(timeformatutils.to_UNIXtime(expected)),
           float(timeformatutils.to_UNIXtime(result)))

    def test_last_three_hours_before_specified_time(self):
        d = datetime(2013, 12, 7, 15, 46, 12)
        expected = d + timedelta(hours=-3)
        result = timeutils.last_three_hours(d)
        self.assertAlmostEqual(expected, result)

    def test_next_hour(self):
        result = timeutils.next_hour()
        expected = datetime.now() + timedelta(hours=1)
        self.assertAlmostEqual(
           float(timeformatutils.to_UNIXtime(expected)),
           float(timeformatutils.to_UNIXtime(result)))

    def test_next_hour_after_specified_time(self):
        d = datetime(2013, 12, 7, 15, 46, 12)
        expected = d + timedelta(hours=1)
        result = timeutils.next_hour(d)
        self.assertAlmostEqual(expected, result)

    def test_next_week(self):
        result = timeutils.next_week()
        expected = datetime.now() + timedelta(days=7)
        self.assertAlmostEqual(
           float(timeformatutils.to_UNIXtime(expected)),
           float(timeformatutils.to_UNIXtime(result)))

    def test_next_week_after_specified_time(self):
        d = datetime(2013, 12, 7, 15, 46, 12)
        expected = d + timedelta(days=7)
        result = timeutils.next_week(d)
        self.assertAlmostEqual(expected, result)

    def test_last_week(self):
        result = timeutils.last_week()
        expected = datetime.now() + timedelta(days=-7)
        self.assertAlmostEqual(
           float(timeformatutils.to_UNIXtime(expected)),
           float(timeformatutils.to_UNIXtime(result)))

    def test_last_week_after_specified_time(self):
        d = datetime(2013, 12, 7, 15, 46, 12)
        expected = d + timedelta(days=-7)
        result = timeutils.last_week(d)
        self.assertAlmostEqual(expected, result)

    def test_last_hour(self):
        result = timeutils.last_hour()
        expected = datetime.now() + timedelta(hours=-1)
        self.assertAlmostEqual(
           float(timeformatutils.to_UNIXtime(expected)),
           float(timeformatutils.to_UNIXtime(result)))

    def test_last_hour_after_specified_time(self):
        d = datetime(2013, 12, 7, 15, 46, 12)
        expected = d + timedelta(hours=-1)
        result = timeutils.last_hour(d)
        self.assertAlmostEqual(expected, result)
        
    def test_now(self):
        expected = datetime.now()
        result = timeutils.now()
        self.assertTrue((result - expected) < timedelta(microseconds = 100))
