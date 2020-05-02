#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pyowm.owm import OWM
from pyowm.agroapi10.agro_manager import AgroManager
from pyowm.airpollutionapi30.airpollution_manager import AirPollutionManager
from pyowm.alertapi30.alert_manager import AlertManager
from pyowm.commons.cityidregistry import CityIDRegistry
from pyowm.stationsapi30.stations_manager import StationsManager
from pyowm.tiles.tile_manager import TileManager
from pyowm.uvindexapi30.uvindex_manager import UVIndexManager
from pyowm.weatherapi25.weather_manager import WeatherManager


class TestOWM(unittest.TestCase):

    __test_instance = OWM('fake-api-key')

    def test_instantiation(self):
        with self.assertRaises(TypeError):
            OWM()
        with self.assertRaises(AssertionError):
            OWM(None)
        with self.assertRaises(AssertionError):
            OWM('fake-api-key', 123456)
        result = OWM('fake-api-key', dict())
        self.assertIsInstance(result, OWM)

    def test_properties(self):
        version = self.__test_instance.version
        self.assertIsInstance(version, tuple)

        config = self.__test_instance.configuration
        self.assertIsInstance(config, dict)

    def test_repr(self):
        print(self.__test_instance)

    def test_city_id_registry(self):
        result = self.__test_instance.city_id_registry()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, CityIDRegistry)

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

    def test_tile_manager(self):
        result = self.__test_instance.tile_manager('test')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, TileManager)
