# -*- coding: utf-8 -*-

"""
Test cases for uv_client.py
"""

import unittest
from pyowm.commons.uv_client import UltraVioletHttpClient
from pyowm.commons.http_client import HttpClient
from pyowm.caches.nullcache import NullCache
from pyowm.utils import timeformatutils


class TestOWMHttpUVClient(unittest.TestCase):

    __test_cache = NullCache()
    __instance = UltraVioletHttpClient('xyz', HttpClient(cache=__test_cache))

    def test_trim_to(self):
        ts = timeformatutils.to_date(1463041620)  # 2016-05-12T08:27:00Z
        self.assertEqual(self.__instance._trim_to(ts, 'minute'),
                          '2016-05-12T08:27Z')
        self.assertEqual(self.__instance._trim_to(ts, 'hour'),
                          '2016-05-12T08Z')
        self.assertEqual(self.__instance._trim_to(ts, 'day'),
                          '2016-05-12Z')
        self.assertEqual(self.__instance._trim_to(ts, 'month'),
                          '2016-05Z')
        self.assertEqual(self.__instance._trim_to(ts, 'year'),
                          '2016Z')
        self.assertRaises(ValueError, self.__instance._trim_to,
                          ts, 'abcdef')

    def test_get_uvi(self):
        # case: current UV index
        params = {'lon': '8.25', 'lat': '43.75'}

        def mock_func(uri, params=None, headers=None):
            return 200, (uri, params)

        self.__instance._client.cacheable_get_json = mock_func

        result = self.__instance.get_uvi(params)
        self.assertEqual('http://api.openweathermap.org/data/2.5/uvi?APPID=xyz',
                         result[0])
        self.assertEqual(params, result[1])

    def test_get_uvi_forecast(self):
        params = {'lon': '8.25', 'lat': '43.75'}

        def mock_func(uri, params=None, headers=None):
            return 200, (uri, params)

        self.__instance._client.cacheable_get_json = mock_func

        result = self.__instance.get_uvi_forecast(params)
        self.assertEqual('http://api.openweathermap.org/data/2.5/uvi/forecast?APPID=xyz',
                         result[0])
        self.assertEqual(params, result[1])
