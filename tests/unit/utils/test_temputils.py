"""
Test case for temputils.py module
"""

import unittest
from pyowm.utils import temputils


class TestTempUtils(unittest.TestCase):

    def test_kelvin_dict_to(self):
        kelvin_dict = {'a': 301.0, 'b': 280}
        celsius_dict = {'a': 27.85, 'b': 6.85}
        fahrenheit_dict = {'a': 82.13, 'b': 44.33}
        self.assertEqual(celsius_dict,
                         temputils.kelvin_dict_to(
                                                  kelvin_dict,
                                                  "celsius")
                         )
        self.assertEqual(fahrenheit_dict,
                         temputils.kelvin_dict_to(
                                                  kelvin_dict,
                                                  "fahrenheit")
                         )
        self.assertEqual(kelvin_dict,
                         temputils.kelvin_dict_to(
                                                  kelvin_dict,
                                                  "kelvin")
                         )

    def test_kelvin_dict_to_fails_with_unknown_temperature_units(self):
        self.assertRaises(ValueError, temputils.kelvin_dict_to, {}, "xyz")

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
