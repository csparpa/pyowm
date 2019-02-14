"""
Test case for temperature.py module
"""

import unittest
from pyowm.utils import temperature


class TestTempUtils(unittest.TestCase):

    def test_kelvin_dict_to(self):
        kelvin_dict = {'a': 301.0, 'b': 280}
        celsius_dict = {'a': 27.85, 'b': 6.85}
        fahrenheit_dict = {'a': 82.13, 'b': 44.33}
        self.assertEqual(celsius_dict,
                         temperature.kelvin_dict_to(
                             kelvin_dict,
                             "celsius")
                         )
        self.assertEqual(fahrenheit_dict,
                         temperature.kelvin_dict_to(
                             kelvin_dict,
                             "fahrenheit")
                         )
        self.assertEqual(kelvin_dict,
                         temperature.kelvin_dict_to(
                             kelvin_dict,
                             "kelvin")
                         )

    def test_kelvin_dict_to_fails_with_unknown_temperature_units(self):
        self.assertRaises(ValueError, temperature.kelvin_dict_to, {}, "xyz")

    def test_kelvin_to_celsius(self):
        kelvin = 301.0
        expected = 27.85
        result = temperature.kelvin_to_celsius(kelvin)
        self.assertEqual(expected, result)

    def test_kelvin_to_celsius_fails_with_negative_values(self):
        self.assertRaises(ValueError, temperature.kelvin_to_celsius, -137.0)

    def test_kelvin_to_fahrenheit(self):
        kelvin = 301.0
        expected = 82.13
        result = temperature.kelvin_to_fahrenheit(kelvin)
        self.assertEqual(expected, result)

    def test_kelvin_to_fahrenheit_fails_with_negative_values(self):
        self.assertRaises(ValueError, temperature.kelvin_to_fahrenheit, -137.0)

    def test_metric_wind_dict_to_imperial(self):
        input = {
            'speed': 2,
            'gust': 3,
            'deg': 7.89
        }
        expected = {
            'speed': 4.47388,
            'gust': 6.71082,
            'deg': 7.89
        }
        result = temperature.metric_wind_dict_to_imperial(input)
        self.assertEqual(expected, result)

    def test_metric_wind_dict_to_km_h(self):
        input = {
            'speed': 2,
            'gust': 3,
            'deg': 7.89
        }
        expected = {
            'speed': 7.2,
            'gust': 10.8,
            'deg': 7.89
        }
        result = temperature.metric_wind_dict_to_km_h(input)
        self.assertEqual(expected, result)
