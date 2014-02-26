#!/usr/bin/env python

"""
Test case for temputils.py module
"""

import unittest
from pyowm.utils import temputils


class TestTempUtils(unittest.TestCase):

    def test_kelvin_to_celsius(self):
        kelvin = 301.0
        expected = 27.85
        result = temputils.kelvin_to_celsius(kelvin)
        self.assertEqual(expected, result)

    def test_kelvin_to_celsius_fails_with_negative_values(self):
        self.assertRaises(ValueError, temputils.kelvin_to_celsius, -137.0)

    def test_kelvin_to_fahrenheit(self):
        kelvin = 301.0
        expected = 82.13
        result = temputils.kelvin_to_fahrenheit(kelvin)
        self.assertEqual(expected, result)

    def test_kelvin_to_fahrenheit_fails_with_negative_values(self):
        self.assertRaises(ValueError, temputils.kelvin_to_fahrenheit, -137.0)

if __name__ == "__main__":
    unittest.main()
