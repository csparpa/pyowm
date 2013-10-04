#!/usr/bin/env python

"""
Test case for converter.py module
"""

import unittest
from datetime import datetime
from pyowm.utils import converter


class TestConverter(unittest.TestCase):

    def test_UNIXtime_to_ISO8601(self):
        unixtime = 1378459200
        expected = "2013-09-06 09:20:00+00" 
        self.assertEqual(expected, converter.UNIXtime_to_ISO8601(unixtime))
        
    def test_UNIXtime_to_ISO8601_fails_with_bad_arugment(self):
        self.assertRaises(TypeError, converter.UNIXtime_to_ISO8601, "test")
        
    def test_UNIXtime_to_ISO8601_fails_with_negative_values(self):
        self.assertRaises(ValueError, converter.UNIXtime_to_ISO8601, -1378459200)
        
    def test_ISO8601_to_UNIXtime(self):
        iso = "2013-09-06 09:20:00+00"
        expected = 1378459200
        self.assertEqual(expected, converter.ISO8601_to_UNIXtime(iso))

    def test_ISO8601_to_UNIXtime_fails_with_bad_arugments(self):
        self.assertRaises(TypeError, converter.ISO8601_to_UNIXtime, 1234)
        self.assertRaises(ValueError, converter.ISO8601_to_UNIXtime, "Tue, Sep 16 2013")
    
    def test_to_UNIXtime(self):
        unix = 1378459200
        iso = "2013-09-06 09:20:00+00"
        date = datetime(2013, 9, 6, 9, 20, 0)
        self.assertEqual(unix, converter.to_UNIXtime(unix))
        self.assertEqual(unix, converter.to_UNIXtime(iso))
        self.assertEqual(unix, converter.to_UNIXtime(date))
    
    def test_to_UNIXtime_fails_with_bad_argument(self):
        self.assertRaises(TypeError, converter.to_UNIXtime, None)
        
    def test_to_UNIXtime_fails_with_negative_unixtime(self):
        self.assertRaises(ValueError, converter.to_UNIXtime, -1234L)
    
    def test_datetime_to_UNIXtime(self):
        date = datetime(2013, 9, 19, 12, 0)
        expected = 1379592000L
        self.assertEqual(converter.datetime_to_UNIXtime(date), expected)
        
    def test_datetime_to_UNIXtime_fails_with_bad_argument(self):
        self.assertRaises(TypeError, converter.datetime_to_UNIXtime, None)
        self.assertRaises(TypeError, converter.datetime_to_UNIXtime, "test")

    def test_kelvin_to_celsius(self):
        kelvin = 301.0
        expected = 27.85
        result = converter.kelvin_to_celsius(kelvin)
        self.assertEqual(expected, result)
        
    def test_kelvin_to_celsius_fails_with_negative_values(self):
        self.assertRaises(ValueError, converter.kelvin_to_celsius, -137.0)
        
    def test_kelvin_to_celsius_fails_with_bad_argument(self):
        self.assertRaises(TypeError, converter.kelvin_to_celsius, "test")
        
    def test_kelvin_to_fahrenheit(self):
        kelvin = 301.0
        expected = 82.13
        result = converter.kelvin_to_fahrenheit(kelvin)
        self.assertEqual(expected, result)
        
    def test_kelvin_to_fahrenheit_fails_with_negative_values(self):
        self.assertRaises(ValueError, converter.kelvin_to_fahrenheit, -137.0)
        
    def test_kelvin_to_fahrenheit_fails_with_bad_argument(self):
        self.assertRaises(TypeError, converter.kelvin_to_fahrenheit, "test")
        
if __name__ == "__main__":
    unittest.main()