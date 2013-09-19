#!/usr/bin/env python

"""
Test case for converter.py module
"""

import unittest
from pyowm.utils import converter


class TestConverter(unittest.TestCase):

    def test_unix_to_ISO8601(self):
        unixtime = 1378459200
        expected = "2013-09-06 09:20:00+00" 
        result = converter.unix_to_ISO8601(unixtime)
        self.assertEqual(expected, result)
        
    def test_unix_to_ISO8601_fails_with_negative_values(self):
        self.assertRaises(ValueError, converter.unix_to_ISO8601, -1378459200)

    def test_kelvin_to_celsius(self):
        kelvin = 301.0
        expected = 27.85
        result = converter.kelvin_to_celsius(kelvin)
        self.assertEqual(expected, result)
        
    def test_kelvin_to_celsius_fails_with_negative_values(self):
        self.assertRaises(ValueError, converter.kelvin_to_celsius, -137.0)
        
    def test_kelvin_to_fahrenheit(self):
        kelvin = 301.0
        expected = 82.13
        result = converter.kelvin_to_fahrenheit(kelvin)
        self.assertEqual(expected, result)
        
    def test_kelvin_to_fahrenheit_fails_with_negative_values(self):
        self.assertRaises(ValueError, converter.kelvin_to_fahrenheit, -137.0)
        
if __name__ == "__main__":
    unittest.main()