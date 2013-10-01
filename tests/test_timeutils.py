#!/usr/bin/env python

"""
Test case for timeutils.py module
"""

import unittest
from datetime import datetime, date, timedelta
from pyowm.utils import timeutils

class TestTimeUtils(unittest.TestCase):

    def test_tomorrow(self):
        now_1 = datetime.now()
        tomorrow_1 = date.today() + timedelta(days=1) 
        result_1 = timeutils.tomorrow()
        expected_1 = datetime(tomorrow_1.year, tomorrow_1.month, tomorrow_1.day, now_1.hour,
                            now_1.minute, 0)
        self.assertEqual(expected_1, result_1)
        
        tomorrow_2 = date.today() + timedelta(days=1) 
        result_2 = timeutils.tomorrow(18, 56)
        expected_2 = datetime(tomorrow_2.year, tomorrow_2.month, tomorrow_2.day, 18,
                            56, 0)
        self.assertEqual(expected_2, result_2)
        
        now_3 = datetime.now()
        tomorrow_3 = date.today() + timedelta(days=1) 
        result_3 = timeutils.tomorrow(6)
        expected_3 = datetime(tomorrow_3.year, tomorrow_3.month, tomorrow_3.day, 6,
                            now_3.minute, 0)
        self.assertEqual(expected_3, result_3)
        
    def test_yesterday(self):
        now_1 = datetime.now()
        yesterday_1 = date.today() + timedelta(days=-1) 
        result_1 = timeutils.yesterday()
        expected_1 = datetime(yesterday_1.year, yesterday_1.month, yesterday_1.day, now_1.hour,
                            now_1.minute, 0)
        self.assertEqual(expected_1, result_1)
        
        yesterday_2 = date.today() + timedelta(days=-1) 
        result_2 = timeutils.yesterday(18, 56)
        expected_2 = datetime(yesterday_2.year, yesterday_2.month, yesterday_2.day, 18,
                            56, 0)
        self.assertEqual(expected_2, result_2)
        
        now_3 = datetime.now()
        yesterday_3 = date.today() + timedelta(days=-1) 
        result_3 = timeutils.yesterday(6)
        expected_3 = datetime(yesterday_3.year, yesterday_3.month, yesterday_3.day, 6,
                            now_3.minute, 0)
        self.assertEqual(expected_3, result_3)