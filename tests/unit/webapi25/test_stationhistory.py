#!/usr/bin/env python

"""
Test case for stationhistory.py module
"""

import unittest
from pyowm.webapi25.stationhistory import StationHistory


class TestStationHistory(unittest.TestCase):
    
    __test_station_ID = 2865
    __test_interval = "tick"
    __test_reception_time = 1378684800L
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
    
    __test_instance = StationHistory(__test_station_ID, 'tick', __test_reception_time,
                                     __test_measurements)
    
    def test_init_fails_when_negative_reception_time(self):
        self.assertRaises(ValueError, StationHistory, 1234, 'tick', -1234567L, 
                          self.__test_measurements)

    def test_getters_return_expected_3h_data(self):
        self.assertEqual(self.__test_instance.get_interval(), self.__test_interval)
        self.assertEqual(self.__test_instance.get_station_ID(), self.__test_station_ID)
        self.assertEqual(self.__test_instance.get_reception_time(),
                         self.__test_reception_time)
        self.assertEqual(self.__test_instance.get_measurements(),
                         self.__test_measurements)

    def test_returning_different_formats_for_reception_time(self):
        """
        Test get_reception_time returns timestamps in the expected formats
        """
        self.assertEqual(self.__test_instance.get_reception_time(timeformat='iso'), 
                         self.__test_reception_time_iso)
        self.assertEqual(self.__test_instance.get_reception_time(timeformat='unix'), 
                         self.__test_reception_time)
        
    def test_temperature_series(self):
        expected = [(1362934043, 266.85),(1362933983, 266.25)]
        self.assertEqual(expected, self.__test_instance.temperature_series())
        
    def test_temperature_series_with_different_temperature_units(self):
        expected_kelvin = [(1362934043, 266.85),(1362933983, 266.25)]
        expected_celsius = [(1362934043, -6.3), (1362933983, -6.9)]
        expected_fahrenheit = [(1362934043, 20.66), (1362933983, 19.58)]
        self.assertEqual(expected_kelvin,
                         self.__test_instance.temperature_series(unit='kelvin'))
        self.assertEqual(expected_celsius,
                         self.__test_instance.temperature_series(unit='celsius'))
        self.assertEqual(expected_fahrenheit,
                         self.__test_instance.temperature_series(unit='fahrenheit'))
        
    def test_temperature_series_fails_with_unknown_temperature_unit(self):
        self.assertRaises(ValueError, StationHistory.temperature_series, 
                          self.__test_instance, 'xyz')
        
    def test_humidity_series(self):
        expected = [(1362934043, 27.7),(1362933983, 27.3)]
        self.assertEqual(expected, self.__test_instance.humidity_series())
        
    def test_pressure_series(self):
        expected = [(1362934043, 1010.09),(1362933983, 1010.02)]
        self.assertEqual(expected, self.__test_instance.pressure_series())
        
    def test_rain_series(self):
        expected = [(1362934043, None),(1362933983, None)]
        self.assertEqual(expected, self.__test_instance.rain_series())
        
    def test_wind_series(self):
        expected = [(1362934043, 4.7),(1362933983, 4.7)]
        self.assertEqual(expected, self.__test_instance.wind_series())
        
    def test_JSON_dump(self):
        expected_output = '{"reception_time": 1378684800, "interval": "tick", ' \
            '"measurements": {"1362934043": {"wind": 4.7, "pressure": 1010.09, ' \
            '"temperature": 266.85, "rain": null, "humidity": 27.7}, "1362933983": {"wind": ' \
            '4.7, "pressure": 1010.02, "temperature": 266.25, "rain": null, "humidity": ' \
            '27.3}}, "station_ID": 2865}'
        self.assertEqual(expected_output, self.__test_instance.to_JSON())
        
    def test_XML_dump(self):
        expected_output = '<StationHistory><station_id>2865</station_id><interval>' \
            'tick</interval><reception_time>1378684800</reception_time>' \
            '<measurements><1362934043><wind>4.7</wind><pressure>1010.09</pressure>' \
            '<temperature>266.85</temperature><humidity>27.7</humidity></1362934043>' \
            '<1362933983><wind>4.7</wind><pressure>1010.02</pressure><temperature>' \
            '266.25</temperature><humidity>27.3</humidity></1362933983>' \
            '</measurements></StationHistory>'
        self.assertEqual(expected_output, self.__test_instance.to_XML())