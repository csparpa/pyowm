#!/usr/bin/env python

"""
Test case for historian.py module
"""

import unittest
from pyowm.webapi25.stationhistory import StationHistory
from pyowm.webapi25.historian import Historian


class TestHistorian(unittest.TestCase):

    __test_station_ID = 2865
    __test_interval = "tick"
    __test_reception_time = 1378684800
    __test_reception_time_iso = '2013-09-09 00:00:00+00'
    __test_measurements = {
        1362933983: {
             "temperature": 266.25,
             "humidity": 27.3,
             "pressure": 1010.02,
             "rain": None,
             "wind": 4.7
         },
        1362934043: {
             "temperature": 266.85,
             "humidity": 27.7,
             "pressure": 1010.09,
             "rain": None,
             "wind": 4.7
        }
    }
    __test_station_history = StationHistory(__test_station_ID, 'tick',
                                    __test_reception_time, __test_measurements)
    __instance = Historian(__test_station_history)

    def test_temperature_series(self):
        expected = [(1362934043, 266.85), (1362933983, 266.25)]
        self.assertEqual(expected, self.__instance.temperature_series())

    def test_temperature_series_with_different_temperature_units(self):
        expected_kelvin = [(1362934043, 266.85), (1362933983, 266.25)]
        expected_celsius = [(1362934043, -6.3), (1362933983, -6.9)]
        expected_fahrenheit = [(1362934043, 20.66), (1362933983, 19.58)]
        self.assertEqual(expected_kelvin,
                         self.__instance.temperature_series(unit='kelvin'))
        self.assertEqual(expected_celsius,
                         self.__instance.temperature_series(unit='celsius'))
        self.assertEqual(expected_fahrenheit,
                         self.__instance.temperature_series(unit='fahrenheit'))

    def test_temperature_series_fails_with_unknown_temperature_unit(self):
        self.assertRaises(ValueError, Historian.temperature_series,
                          self.__instance, 'xyz')

    def test_humidity_series(self):
        expected = [(1362934043, 27.7), (1362933983, 27.3)]
        self.assertEqual(expected, self.__instance.humidity_series())

    def test_pressure_series(self):
        expected = [(1362934043, 1010.09), (1362933983, 1010.02)]
        self.assertEqual(expected, self.__instance.pressure_series())

    def test_rain_series(self):
        expected = [(1362934043, None), (1362933983, None)]
        self.assertEqual(expected, self.__instance.rain_series())

    def test_wind_series(self):
        expected = [(1362934043, 4.7), (1362933983, 4.7)]
        self.assertEqual(expected, self.__instance.wind_series())

    def test_max_temperature(self):
        expected = (1362934043, 266.85)
        self.assertEqual(expected, self.__instance.max_temperature())
        
    def test_min_temperature(self):
        expected = (1362933983, 266.25)
        self.assertEqual(expected, self.__instance.min_temperature())
        
    def test_max_humidity(self):
        expected = (1362934043, 27.7)
        self.assertEqual(expected, self.__instance.max_humidity())
        
    def test_min_humidity(self):
        expected = (1362933983, 27.3)
        self.assertEqual(expected, self.__instance.min_humidity())
        
    def test_max_pressure(self):
        expected = (1362934043, 1010.09)
        self.assertEqual(expected, self.__instance.max_pressure())
        
    def test_min_pressure(self):
        expected = (1362933983, 1010.02)
        self.assertEqual(expected, self.__instance.min_pressure())