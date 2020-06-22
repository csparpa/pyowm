#!/usr/bin/env python
# -*- coding: utf-8 -*-e for historian.py module

import unittest
from pyowm.weatherapi25.stationhistory import StationHistory
from pyowm.weatherapi25.historian import Historian
from pyowm.utils import measurables


class TestHistorian(unittest.TestCase):

    __test_station_ID = 2865
    __test_interval = "tick"
    __test_reception_time = 1378684800
    __test_reception_time_iso = '2013-09-09 00:00:00+00:00'
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
             "rain": 2.5,
             "wind": 4.7
        }
    }
    __test_empty_measurements = {
        1362933983: {
             "temperature": None,
             "humidity": None,
             "pressure": None,
             "rain": None,
             "wind": None
         },
        1362934043: {
             "temperature": None,
             "humidity": None,
             "pressure": None,
             "rain": None,
             "wind": None
        }
    }
    __test_station_history = StationHistory(__test_station_ID, 'tick',
                                    __test_reception_time, __test_measurements)
    __test_empty_station_history = StationHistory(__test_station_ID, 'tick',
                                    __test_reception_time,
                                    __test_empty_measurements)
    __instance = Historian(__test_station_history)
    __empty_instance = Historian(__test_empty_station_history)

    def test_temperature_series(self):
        expected = [(1362934043, 266.85), (1362933983, 266.25)]
        self.assertEqual(set(expected), set(self.__instance.temperature_series()))

    def test_temperature_series_with_different_temperature_units(self):
        expected_kelvin = [(1362934043, 266.85), (1362933983, 266.25)]
        expected_celsius = [(1362934043, -6.3), (1362933983, -6.9)]
        expected_fahrenheit = [(1362934043, 20.66), (1362933983, 19.58)]
        self.assertEqual(set(expected_kelvin),
                         set(self.__instance.temperature_series(unit='kelvin')))
        self.assertEqual(set(expected_celsius),
                         set(self.__instance.temperature_series(unit='celsius')))
        self.assertEqual(set(expected_fahrenheit),
                         set(self.__instance.temperature_series(unit='fahrenheit')))

    def test_temperature_series_fails_with_unknown_temperature_unit(self):
        self.assertRaises(ValueError, Historian.temperature_series,
                          self.__instance, 'xyz')

    def test_humidity_series(self):
        expected = [(1362934043, 27.7), (1362933983, 27.3)]
        self.assertEqual(set(expected), set(self.__instance.humidity_series()))

    def test_pressure_series(self):
        expected = [(1362934043, 1010.09), (1362933983, 1010.02)]
        self.assertEqual(set(expected), set(self.__instance.pressure_series()))

    def test_rain_series(self):
        expected = [(1362934043, 2.5), (1362933983, None)]
        self.assertEqual(set(expected), set(self.__instance.rain_series()))

    def test_wind_series(self):
        expected = [(1362934043, 4.7), (1362933983, 4.7)]
        self.assertEqual(set(expected), set(self.__instance.wind_series()))

    def test_max_temperature(self):
        expected = (1362934043, 266.85)
        self.assertEqual(expected, self.__instance.max_temperature())
        
    def test_max_temperature_with_different_temperature_units(self):
        expected_kelvin = (1362934043, 266.85)
        expected_celsius = (1362934043, -6.3)
        expected_fahrenheit = (1362934043, 20.66)
        self.assertEqual(expected_kelvin,
                         self.__instance.max_temperature(unit='kelvin'))
        self.assertEqual(expected_celsius,
                         self.__instance.max_temperature(unit='celsius'))
        self.assertEqual(expected_fahrenheit,
                         self.__instance.max_temperature(unit='fahrenheit'))

    def test_max_temperature_fails_with_unknown_temperature_unit(self):
        self.assertRaises(ValueError, Historian.max_temperature,
                          self.__instance, 'xyz')
        
    def test_max_temperature_on_empty_measurements(self):
        self.assertRaises(ValueError, Historian.max_temperature,
                          self.__empty_instance)
        
    def test_min_temperature(self):
        expected = (1362933983, 266.25)
        self.assertEqual(expected, self.__instance.min_temperature())
        
    def test_min_temperature_with_different_temperature_units(self):
        expected_kelvin = (1362933983, 266.25)
        expected_celsius = (1362933983, -6.9)
        expected_fahrenheit = (1362933983, 19.58)
        self.assertEqual(expected_kelvin,
                         self.__instance.min_temperature(unit='kelvin'))
        self.assertEqual(expected_celsius,
                         self.__instance.min_temperature(unit='celsius'))
        self.assertEqual(expected_fahrenheit,
                         self.__instance.min_temperature(unit='fahrenheit'))
        
    def test_min_temperature_fails_with_unknown_temperature_unit(self):
        self.assertRaises(ValueError, Historian.min_temperature,
                          self.__instance, 'xyz')
        
    def test_min_temperature_on_empty_measurements(self):
        self.assertRaises(ValueError, Historian.min_temperature,
                          self.__empty_instance)

    def test_average_temperature(self):
        expected = (266.85 + 266.25)/2.0
        self.assertEqual(expected, self.__instance.average_temperature())

    def test_average_temperature_with_different_temperature_units(self):
        avg = (266.85 + 266.25)/2.0
        expected_kelvin = avg
        expected_celsius = measurables.kelvin_to_celsius(avg)
        expected_fahrenheit = measurables.kelvin_to_fahrenheit(avg)
        self.assertEqual(expected_kelvin,
                         self.__instance.average_temperature(unit='kelvin'))
        self.assertEqual(expected_celsius,
                         self.__instance.average_temperature(unit='celsius'))
        self.assertEqual(expected_fahrenheit,
                         self.__instance.average_temperature(unit='fahrenheit'))
        
    def test_average_temperature_fails_with_unknown_temperature_unit(self):
        self.assertRaises(ValueError, Historian.average_temperature,
                          self.__instance, 'xyz')

    def test_average_temperature_on_empty_measurements(self):
        self.assertRaises(ValueError, Historian.average_temperature,
                          self.__empty_instance)

    def test_max_humidity(self):
        expected = (1362934043, 27.7)
        self.assertEqual(expected, self.__instance.max_humidity())
        
    def test_max_humidity_on_empty_measurements(self):
        self.assertRaises(ValueError, Historian.max_humidity,
                          self.__empty_instance)
        
    def test_min_humidity(self):
        expected = (1362933983, 27.3)
        self.assertEqual(expected, self.__instance.min_humidity())
        
    def test_min_humidity_on_empty_measurements(self):
        self.assertRaises(ValueError, Historian.min_humidity,
                          self.__empty_instance)

    def test_average_humidity(self):
        expected = (27.3 + 27.7)/2.0
        self.assertEqual(expected, self.__instance.average_humidity())

    def test_average_humidity_on_empty_measurements(self):
        self.assertRaises(ValueError, Historian.average_humidity,
                          self.__empty_instance)
        
    def test_max_pressure(self):
        expected = (1362934043, 1010.09)
        self.assertEqual(expected, self.__instance.max_pressure())
        
    def test_max_pressure_on_empty_measurements(self):
        self.assertRaises(ValueError, Historian.max_pressure,
                          self.__empty_instance)
        
    def test_min_pressure(self):
        expected = (1362933983, 1010.02)
        self.assertEqual(expected, self.__instance.min_pressure())

    def test_min_pressure_on_empty_measurements(self):
        self.assertRaises(ValueError, Historian.min_pressure,
                          self.__empty_instance)

    def test_average_pressure(self):
        expected = (1010.02 + 1010.09)/2.0
        self.assertEqual(expected, self.__instance.average_pressure())

    def test_average_pressure_on_empty_measurements(self):
        self.assertRaises(ValueError, Historian.average_pressure,
                          self.__empty_instance)
        
    def test_max_rain(self):
        expected = (1362934043, 2.5)
        self.assertEqual(expected, self.__instance.max_rain())

    def test_max_rain_on_empty_measurements(self):
        self.assertRaises(ValueError, Historian.max_rain,
                          self.__empty_instance)
        
    def test_min_rain(self):
        expected = (1362934043, 2.5)
        self.assertEqual(expected, self.__instance.min_rain())

    def test_min_rain_on_empty_measurements(self):
        self.assertRaises(ValueError, Historian.min_rain,
                          self.__empty_instance)

    def test_average_rain(self):
        expected = (2.5 + 2.5)/2.0
        self.assertEqual(expected, self.__instance.average_rain())

    def test_average_rain_on_empty_measurements(self):
        self.assertRaises(ValueError, Historian.average_rain,
                          self.__empty_instance)

    def test_purge_none_samples(self):
        input_list = [("a", 1), ("b", 2), ("c", None), ("d", None), ("e", 5)]
        expected = [("a", 1), ("b", 2), ("e", 5)]
        self.assertEqual(set(expected),
                         set(self.__instance._purge_none_samples(input_list)))

    def test_average(self):
        input_list = [("a", 1.0), ("b", 2.0), ("c", 3.0), ("d", 4.0)]
        expected = 10.0/len(input_list)
        self.assertEqual(expected,
                         self.__instance._average(input_list))

    def test__repr(self):
        print(self.__instance)
