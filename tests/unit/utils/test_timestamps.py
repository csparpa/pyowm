#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, date, timedelta
from pyowm.utils import timestamps, formatting


class TestTimeUtils(unittest.TestCase):

    def test_tomorrow(self):
        now = datetime.now()
        tomorrow = date.today() + timedelta(days=1)
        result = timestamps.tomorrow()
        expected = datetime(tomorrow.year, tomorrow.month, tomorrow.day,
                            now.hour, now.minute, 0)
        self.assertEqual(expected, result)

    def test_tomorrow_with_hour_and_minute(self):
        tomorrow = date.today() + timedelta(days=1)
        result = timestamps.tomorrow(18, 56)
        expected = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 18,
                            56, 0)
        self.assertEqual(expected, result)

    def test_tomorrow_with_hour_only(self):
        now = datetime.now()
        tomorrow = date.today() + timedelta(days=1)
        result = timestamps.tomorrow(6)
        expected = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 6,
                            now.minute, 0)
        self.assertEqual(expected, result)

    def test_yesterday(self):
        now = datetime.now()
        yesterday = date.today() + timedelta(days=-1)
        result = timestamps.yesterday()
        expected = datetime(yesterday.year, yesterday.month, yesterday.day,
                            now.hour, now.minute, 0)
        self.assertEqual(expected, result)

    def test_yesterday_with_hour_and_minute(self):
        yesterday = date.today() + timedelta(days=-1)
        result = timestamps.yesterday(18, 56)
        expected = datetime(yesterday.year, yesterday.month, yesterday.day, 18,
                            56, 0)
        self.assertEqual(expected, result)

    def test_yesterday_with_hour_only(self):
        now = datetime.now()
        yesterday = date.today() + timedelta(days=-1)
        result = timestamps.yesterday(6)
        expected = datetime(yesterday.year, yesterday.month, yesterday.day, 6,
                            now.minute, 0)
        self.assertEqual(expected, result)

    def test_next_three_hours(self):
        result = timestamps.next_three_hours()
        expected = datetime.now() + timedelta(hours=3)
        self.assertAlmostEqual(
           float(formatting.to_UNIXtime(expected)),
           float(formatting.to_UNIXtime(result)))

    def test_next_three_hours_after_specified_time(self):
        d = datetime(2013, 12, 7, 15, 46, 12)
        expected = d + timedelta(hours=3)
        result = timestamps.next_three_hours(d)
        self.assertAlmostEqual(expected, result)

    def test_last_three_hours(self):
        result = timestamps.last_three_hours()
        expected = datetime.now() + timedelta(hours=-3)
        self.assertAlmostEqual(
           float(formatting.to_UNIXtime(expected)),
           float(formatting.to_UNIXtime(result)))

    def test_last_three_hours_before_specified_time(self):
        d = datetime(2013, 12, 7, 15, 46, 12)
        expected = d + timedelta(hours=-3)
        result = timestamps.last_three_hours(d)
        self.assertAlmostEqual(expected, result)

    def test_next_hour(self):
        result = timestamps.next_hour()
        expected = datetime.now() + timedelta(hours=1)
        self.assertAlmostEqual(
           float(formatting.to_UNIXtime(expected)),
           float(formatting.to_UNIXtime(result)))

    def test_next_hour_after_specified_time(self):
        d = datetime(2013, 12, 7, 15, 46, 12)
        expected = d + timedelta(hours=1)
        result = timestamps.next_hour(d)
        self.assertAlmostEqual(expected, result)

    def test_next_week(self):
        result = timestamps.next_week()
        expected = datetime.now() + timedelta(days=7)
        self.assertAlmostEqual(
           float(formatting.to_UNIXtime(expected)),
           float(formatting.to_UNIXtime(result)))

    def test_next_week_after_specified_time(self):
        d = datetime(2013, 12, 7, 15, 46, 12)
        expected = d + timedelta(days=7)
        result = timestamps.next_week(d)
        self.assertAlmostEqual(expected, result)

    def test_last_week(self):
        result = timestamps.last_week()
        expected = datetime.now() + timedelta(days=-7)
        self.assertAlmostEqual(
           float(formatting.to_UNIXtime(expected)),
           float(formatting.to_UNIXtime(result)))

    def test_last_week_after_specified_time(self):
        d = datetime(2013, 12, 7, 15, 46, 12)
        expected = d + timedelta(days=-7)
        result = timestamps.last_week(d)
        self.assertAlmostEqual(expected, result)

    def test_last_hour(self):
        result = timestamps.last_hour()
        expected = datetime.now() + timedelta(hours=-1)
        self.assertAlmostEqual(
           float(formatting.to_UNIXtime(expected)),
           float(formatting.to_UNIXtime(result)))

    def test_last_hour_after_specified_time(self):
        d = datetime(2013, 12, 7, 15, 46, 12)
        expected = d + timedelta(hours=-1)
        result = timestamps.last_hour(d)
        self.assertAlmostEqual(expected, result)
        
    def test_now(self):
        expected = datetime.now()
        result = timestamps.now()
        self.assertEquals(result.year, expected.year)
        self.assertEquals(result.month, expected.month)
        self.assertEquals(result.day, expected.day)
        self.assertEquals(result.hour, expected.hour)
        self.assertEquals(result.minute, expected.minute)
        self.assertEquals(result.second, expected.second)

    def test_last_month(self):
        result = timestamps.last_month()
        expected = datetime.now() + timedelta(days=-30)
        self.assertAlmostEqual(
            float(formatting.to_UNIXtime(expected)),
            float(formatting.to_UNIXtime(result)))

    def test_last_month_after_specified_time(self):
        d = datetime(2015, 10, 1, 15, 46, 12)
        expected = d + timedelta(days=-30)
        result = timestamps.last_month(d)
        self.assertAlmostEqual(expected, result)

    def test_next_month(self):
        result = timestamps.next_month()
        expected = datetime.now() + timedelta(days=30)
        self.assertAlmostEqual(
            float(formatting.to_UNIXtime(expected)),
            float(formatting.to_UNIXtime(result)))

    def test_next_month_after_specified_time(self):
        d = datetime(2015, 10, 1, 15, 46, 12)
        expected = d + timedelta(days=30)
        result = timestamps.next_month(d)
        self.assertAlmostEqual(expected, result)

    def test_last_year(self):
        result = timestamps.last_year()
        expected = datetime.now() + timedelta(days=-365)
        self.assertAlmostEqual(
            float(formatting.to_UNIXtime(expected)),
            float(formatting.to_UNIXtime(result)))

    def test_last_year_after_specified_time(self):
        d = datetime(2015, 10, 1, 15, 46, 12)
        expected = d + timedelta(days=-365)
        result = timestamps.last_year(d)
        self.assertAlmostEqual(expected, result)

    def test_next_year(self):
        result = timestamps.next_year()
        expected = datetime.now() + timedelta(days=365)
        self.assertAlmostEqual(
            float(formatting.to_UNIXtime(expected)),
            float(formatting.to_UNIXtime(result)))

    def test_next_year_after_specified_time(self):
        d = datetime(2015, 10, 1, 15, 46, 12)
        expected = d + timedelta(days=365)
        result = timestamps.next_year(d)
        self.assertAlmostEqual(expected, result)

    def test_millis_offset_between_epochs(self):
        # test failures
        with self.assertRaises(AssertionError):
            timestamps.millis_offset_between_epochs('test', 123456)
        with self.assertRaises(AssertionError):
            timestamps.millis_offset_between_epochs(123456, 'test')

        # test normal behaviour
        reference_epoch = 1525176000
        target_epoch_1 = 1525176060
        target_epoch_2 = 1522584000

        expected_1 = (target_epoch_1 - reference_epoch) * 1000
        expected_2 = (target_epoch_2 - reference_epoch) * 1000

        self.assertEqual(expected_1, timestamps.millis_offset_between_epochs(reference_epoch, target_epoch_1))
        self.assertEqual(expected_2, timestamps.millis_offset_between_epochs(reference_epoch, target_epoch_2))
        self.assertEqual(0, timestamps.millis_offset_between_epochs(reference_epoch, reference_epoch))
