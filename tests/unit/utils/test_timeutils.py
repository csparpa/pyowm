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
        self.assertEquals(result.year, expected.year)
        self.assertEquals(result.month, expected.month)
        self.assertEquals(result.day, expected.day)
        self.assertEquals(result.hour, expected.hour)
        self.assertEquals(result.minute, expected.minute)
        self.assertEquals(result.second, expected.second)

    def test_last_month(self):
        result = timeutils.last_month()
        expected = datetime.now() + timedelta(days=-30)
        self.assertAlmostEqual(
            float(timeformatutils.to_UNIXtime(expected)),
            float(timeformatutils.to_UNIXtime(result)))

    def test_last_month_after_specified_time(self):
        d = datetime(2015, 10, 1, 15, 46, 12)
        expected = d + timedelta(days=-30)
        result = timeutils.last_month(d)
        self.assertAlmostEqual(expected, result)

    def test_next_month(self):
        result = timeutils.next_month()
        expected = datetime.now() + timedelta(days=30)
        self.assertAlmostEqual(
            float(timeformatutils.to_UNIXtime(expected)),
            float(timeformatutils.to_UNIXtime(result)))

    def test_next_month_after_specified_time(self):
        d = datetime(2015, 10, 1, 15, 46, 12)
        expected = d + timedelta(days=30)
        result = timeutils.next_month(d)
        self.assertAlmostEqual(expected, result)

    def test_last_year(self):
        result = timeutils.last_year()
        expected = datetime.now() + timedelta(days=-365)
        self.assertAlmostEqual(
            float(timeformatutils.to_UNIXtime(expected)),
            float(timeformatutils.to_UNIXtime(result)))

    def test_last_year_after_specified_time(self):
        d = datetime(2015, 10, 1, 15, 46, 12)
        expected = d + timedelta(days=-365)
        result = timeutils.last_year(d)
        self.assertAlmostEqual(expected, result)

    def test_next_year(self):
        result = timeutils.next_year()
        expected = datetime.now() + timedelta(days=365)
        self.assertAlmostEqual(
            float(timeformatutils.to_UNIXtime(expected)),
            float(timeformatutils.to_UNIXtime(result)))

    def test_next_year_after_specified_time(self):
        d = datetime(2015, 10, 1, 15, 46, 12)
        expected = d + timedelta(days=365)
        result = timeutils.next_year(d)
        self.assertAlmostEqual(expected, result)
