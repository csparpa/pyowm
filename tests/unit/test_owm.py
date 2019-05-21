#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pyowm.owm import OWM
from pyowm.stationsapi30.stations_manager import StationsManager
from pyowm.alertapi30.alert_manager import AlertManager
from pyowm.agroapi10.agro_manager import AgroManager
from pyowm.airpollutionapi30.airpollution_manager import AirPollutionManager
from pyowm.uvindexapi30.uvindex_manager import UVIndexManager
from pyowm.weatherapi25.weather_manager import WeatherManager


class TestOWM(unittest.TestCase):

    __test_instance = OWM('fake-api-key')

    def test_instantiation(self):
        with self.assertRaises(AssertionError):
            OWM(None)
        with self.assertRaises(AssertionError):
            OWM('fake-api-key', 123456)

    def test_repr(self):
        print(self.__test_instance)

    def test_stations_manager(self):
        result = self.__test_instance.stations_manager()
        self.assertTrue(result is not None)
        self.assertIsInstance(result, StationsManager)

    def test_alert_manager(self):
        result = self.__test_instance.alert_manager()
        self.assertTrue(result is not None)
        self.assertIsInstance(result, AlertManager)

    def test_uvindex_manager(self):
        result = self.__test_instance.uvindex_manager()
        self.assertTrue(result is not None)
        self.assertIsInstance(result, UVIndexManager)

    def test_airpollution_manager(self):
        result = self.__test_instance.airpollution_manager()
        self.assertTrue(result is not None)
        self.assertIsInstance(result, AirPollutionManager)

    def test_agro_manager(self):
        result = self.__test_instance.agro_manager()
        self.assertTrue(result is not None)
        self.assertIsInstance(result, AgroManager)

    def test_weather_manager(self):
        result = self.__test_instance.weather_manager()
        self.assertTrue(result is not None)
        self.assertIsInstance(result, WeatherManager)
