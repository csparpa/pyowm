# -*- coding: utf-8 -*-

"""
Test cases for uv_client.py
"""

import unittest
from pyowm.commons.uv_client import UltraVioletHttpClient
from pyowm.caches.nullcache import NullCache
from pyowm.utils import timeformatutils


class TestOWMHttpUVClient(unittest.TestCase):

    __test_cache = NullCache()
    __instance = UltraVioletHttpClient('xyz', __test_cache)

    def test_trim_to(self):
        ts = timeformatutils.to_date(1463041620)  # 2016-05-12T08:27:00Z
        self.assertEquals(self.__instance._trim_to(ts, 'minute'),
                          '2016-05-12T08:27Z')
        self.assertEquals(self.__instance._trim_to(ts, 'hour'),
                          '2016-05-12T08Z')
        self.assertEquals(self.__instance._trim_to(ts, 'day'),
                          '2016-05-12Z')
        self.assertEquals(self.__instance._trim_to(ts, 'month'),
                          '2016-05Z')
        self.assertEquals(self.__instance._trim_to(ts, 'year'),
                          '2016Z')
        self.assertRaises(ValueError, self.__instance._trim_to,
                          ts, 'abcdef')

    def test_get_uvi(self):

        # case: current UV index
        params = {'lon': 8.25, 'lat': 43.75, 'start': None, 'interval': None}
        bkp = self.__instance._lookup_cache_or_invoke_API

        def mock_func(cache, API_full_url, timeout):
            return API_full_url

        self.__instance._lookup_cache_or_invoke_API = mock_func

        expected_url = 'http://api.openweathermap.org/data/2.5/uvi?appid=xyz&lat=43.75&lon=8.25'
        result = self.__instance.get_uvi(params)
        self.assertEquals(expected_url, result)
        self.__instance._lookup_cache_or_invoke_API = bkp