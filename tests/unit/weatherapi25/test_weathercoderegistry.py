#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pyowm.weatherapi25.weathercoderegistry import WeatherCodeRegistry


class TestWeatherCodeRegistry(unittest.TestCase):

    __test_instance = WeatherCodeRegistry({
        "abc": [{
            "start": 1,
            "end": 100
        },
        {
            "start": 120,
            "end": 160
        }],
        "xyz": [{
            "start": 345,
            "end": 345
        }]
    })

    def test_wrong_instantiation_parameters(self):
        self.assertRaises(AssertionError, WeatherCodeRegistry, 'this-is-not-a-dict')

    def test_status_for(self):
        self.assertTrue(self.__test_instance.status_for(999) is None)
        self.assertEqual("abc", self.__test_instance.status_for(150))
        self.assertEqual("xyz", self.__test_instance.status_for(345))

    def test_get_instance(self):
        result = WeatherCodeRegistry.get_instance()
        self.assertTrue(isinstance(result, WeatherCodeRegistry))

    def test_repr(self):
        print(self.__test_instance)
