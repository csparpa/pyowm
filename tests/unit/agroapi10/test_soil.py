#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from pyowm.agroapi10.soil import Soil
from pyowm.utils.formatting import UTC


class TestSoil(unittest.TestCase):

    test_reference_time = 1378459200
    test_iso_reference_time = "2013-09-06 09:20:00+00"
    test_date_reference_time = datetime.strptime(test_iso_reference_time, '%Y-%m-%d %H:%M:%S+00').replace(
        tzinfo=UTC())
    test_temperature = 294.199
    test_celsius_temperature = 21.049
    test_fahrenheit_temperature = 69.888
    test_moisture = 45.6
    test_polygon_id = 'my-polygon'
    test_instance = Soil(test_reference_time, test_temperature, test_temperature, test_moisture, test_polygon_id)

    def test_soil_fails_with_wrong_parameters(self):
        self.assertRaises(AssertionError, Soil, None, 12.4, 11.8, 80.2, 'my-polygon')
        self.assertRaises(AssertionError, Soil, 'wrong', 12.4, 11.8, 80.2, 'my-polygon')
        self.assertRaises(ValueError, Soil, -345, 12.4, 11.8, 80.2, 'my-polygon')
        self.assertRaises(AssertionError, Soil, 1234567, None, 11.8, 80.2, 'my-polygon')
        self.assertRaises(AssertionError, Soil, 1234567, 'wrong', 11.8, 80.2, 'my-polygon')
        self.assertRaises(AssertionError, Soil, 1234567, 12.4, None, 80.2, 'my-polygon')
        self.assertRaises(AssertionError, Soil, 1234567, 12.4, 'wrong', 80.2, 'my-polygon')
        self.assertRaises(AssertionError, Soil, 1234567, 12.4, 11.8, None, 'my-polygon')
        self.assertRaises(AssertionError, Soil, 1234567, 12.4, 11.8, "'wrong", 'my-polygon')
        self.assertRaises(ValueError, Soil, 1234567, 12.4, 11.8, -45.6, 'my-polygon')

    def test_reference_time_returning_different_formats(self):

        self.assertEqual(self.test_instance.reference_time(timeformat='unix'),
                         self.test_reference_time)
        self.assertEqual(self.test_instance.reference_time(timeformat='iso'),
                         self.test_iso_reference_time)
        self.assertEqual(self.test_instance.reference_time(timeformat='date'),
                         self.test_date_reference_time)

    def test_reference_time_fails_with_unknown_timeformat(self):
        self.assertRaises(ValueError, Soil.reference_time, self.test_instance, 'xyz')

    def test_from_dict(self):
        ref_time = 12345567
        surf_temp = 11.2
        ten_cm_temp = 9.5
        moisture = 8.2
        pol_id = "5abb9fb82c8897000bde3e87"
        the_dict = {
            "reference_time": ref_time,
            "surface_temp": surf_temp,
            "ten_cm_temp": ten_cm_temp,
            "moisture": moisture,
            "polygon_id": pol_id
        }
        expected = Soil(ref_time, surf_temp, ten_cm_temp, moisture, pol_id)
        result = Soil.from_dict(the_dict)
        self.assertEqual(expected.reference_time(), result.reference_time())
        self.assertEqual(expected.surface_temp(), result.surface_temp())
        self.assertEqual(expected.ten_cm_temp(), result.ten_cm_temp())
        self.assertEqual(expected.moisture, result.moisture)
        self.assertEqual(expected.polygon_id, result.polygon_id)

    def test_to_dict(self):
        expected = dict(reference_time=self.test_reference_time, surface_temp=self.test_temperature,
                        ten_cm_temp=self.test_temperature, moisture=self.test_moisture,
                        polygon_id=self.test_polygon_id)
        result = self.test_instance.to_dict()
        self.assertEqual(expected, result)

    def test_returning_different_units_for_temperatures(self):
        # Surface temp
        result_kelvin = self.test_instance.surface_temp(unit='kelvin')
        result_celsius = self.test_instance.surface_temp(unit='celsius')
        result_fahrenheit = self.test_instance.surface_temp(unit='fahrenheit')
        self.assertAlmostEqual(result_kelvin, self.test_temperature, delta=0.1)
        self.assertAlmostEqual(result_celsius, self.test_celsius_temperature, delta=0.1)
        self.assertAlmostEqual(result_fahrenheit, self.test_fahrenheit_temperature, delta=0.1)

        # 10 cm temp
        result_kelvin = self.test_instance.ten_cm_temp(unit='kelvin')
        result_celsius = self.test_instance.ten_cm_temp(unit='celsius')
        result_fahrenheit = self.test_instance.ten_cm_temp(unit='fahrenheit')
        self.assertAlmostEqual(result_kelvin, self.test_temperature, delta=0.1)
        self.assertAlmostEqual(result_celsius, self.test_celsius_temperature, delta=0.1)
        self.assertAlmostEqual(result_fahrenheit, self.test_fahrenheit_temperature, delta=0.1)

    def test_trying_unknown_units_for_temperatures(self):
        self.assertRaises(ValueError, Soil.surface_temp, self.test_instance, 'xyz')
        self.assertRaises(ValueError, Soil.ten_cm_temp, self.test_instance, 'xyz')

    def test_repr(self):
        instance = Soil(1234567, 12.4, 11.8, 80.2, 'my-polygon')
        repr(instance)
        instance = Soil(1234567, 12.4, 11.8, 80.2, None)
        repr(instance)