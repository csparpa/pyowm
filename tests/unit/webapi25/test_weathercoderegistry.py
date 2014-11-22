"""
Test case for weathercoderegistry.py module
"""

import unittest
from pyowm.webapi25.weathercoderegistry import WeatherCodeRegistry

class TestWeatherCodeRegistry(unittest.TestCase):

    _test_instance = WeatherCodeRegistry({
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

    def test_status_for(self):
        self.assertTrue(self._test_instance.status_for(999) is None)
        self.assertEqual("abc", self._test_instance.status_for(150))
        self.assertEqual("xyz", self._test_instance.status_for(345))