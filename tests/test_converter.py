#!/usr/bin/env python

"""
Test case for converter.py module
"""

import unittest
from pyowm.utils import converter


class Test(unittest.TestCase):

    def test_unix_to_ISO8601(self):
        unixtime = 1378459200
        expected = "2013-09-06 09:20:00+00" 
        result = converter.unix_to_ISO8601(unixtime)
        self.assertEqual(expected, result, "")

    def test_kelvin_to_celsius(self):
        kelvin = 301.0
        expected = 27.85
        result = converter.kelvin_to_celsius(kelvin)
        self.assertEqual(expected, result, "")
        
    def test_kelvin_to_fahrenheit(self):
        kelvin = 301.0
        expected = 82.13
        result = converter.kelvin_to_fahrenheit(kelvin)
        self.assertEqual(expected, result, "")
        
if __name__ == "__main__":
    unittest.main()