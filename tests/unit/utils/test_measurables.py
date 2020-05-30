#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pyowm.utils import measurables


class TestMeasurablesUtils(unittest.TestCase):

    def test_kelvin_dict_to(self):
        kelvin_dict = {'a': 301.0, 'b': 280}
        celsius_dict = {'a': 27.85, 'b': 6.85}
        fahrenheit_dict = {'a': 82.13, 'b': 44.33}
        self.assertEqual(celsius_dict,
                         measurables.kelvin_dict_to(
                             kelvin_dict,
                             "celsius")
                         )
        self.assertEqual(fahrenheit_dict,
                         measurables.kelvin_dict_to(
                             kelvin_dict,
                             "fahrenheit")
                         )
        self.assertEqual(kelvin_dict,
                         measurables.kelvin_dict_to(
                             kelvin_dict,
                             "kelvin")
                         )

    def test_kelvin_dict_to_fails_with_unknown_temperature_units(self):
        self.assertRaises(ValueError, measurables.kelvin_dict_to, {}, "xyz")

    def test_kelvin_to_celsius(self):
        kelvin = 301.0
        expected = 27.85
        result = measurables.kelvin_to_celsius(kelvin)
        self.assertEqual(expected, result)

    def test_kelvin_to_celsius_fails_with_negative_values(self):
        self.assertRaises(ValueError, measurables.kelvin_to_celsius, -137.0)

    def test_kelvin_to_fahrenheit(self):
        kelvin = 301.0
        expected = 82.13
        result = measurables.kelvin_to_fahrenheit(kelvin)
        self.assertEqual(expected, result)

    def test_kelvin_to_fahrenheit_fails_with_negative_values(self):
        self.assertRaises(ValueError, measurables.kelvin_to_fahrenheit, -137.0)

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
        result = measurables.metric_wind_dict_to_imperial(input)
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
        result = measurables.metric_wind_dict_to_km_h(input)
        self.assertEqual(expected, result)

    def test_metric_wind_dict_to_knots(self):
        input = {
            'speed': 2,
            'gust': 3,
            'deg': 7.89
        }
        expected = {'speed': 3.88768, 'gust': 5.83152, 'deg': 7.89}
        result = measurables.metric_wind_dict_to_knots(input)
        self.assertEqual(expected, result)

    def test_metric_wind_dict_to_beaufort(self):
        corner_values = {
            'lower': 0.01,
            'a': 0.2,
            'b': 1.5,
            'c': 3.3,
            'd': 5.4,
            'e': 7.9,
            'f': 10.7,
            'g': 13.8,
            'h': 17.1,
            'i': 20.7,
            'j': 24.4,
            'k': 28.4,
            'l': 32.6,
            'upper': 345,
            'deg': 7.89
        }
        expected_corner_values_beaufort = {
            'lower': 0,
            'a': 0,
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
            'g': 6,
            'h': 7,
            'i': 8,
            'j': 9,
            'k': 10,
            'l': 11,
            'upper': 12,
            'deg': 7.89
        }
        result_corner_values = measurables.metric_wind_dict_to_beaufort(corner_values)
        self.assertEqual(result_corner_values, expected_corner_values_beaufort)

        input = {
            'speed': 17.9,
            'gust': 2.89,
            'deg': 7.89
        }
        expected = {'speed': 8, 'gust': 2, 'deg': 7.89}
        result = measurables.metric_wind_dict_to_beaufort(input)
        self.assertEqual(expected, result)
