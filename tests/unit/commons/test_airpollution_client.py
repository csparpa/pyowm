# -*- coding: utf-8 -*-

import unittest
from pyowm.commons.airpollution_client import AirPollutionHttpClient
from pyowm.caches.nullcache import NullCache
from pyowm.utils import timeformatutils


class TestAirPollutionHttpClient(unittest.TestCase):

    __test_cache = NullCache()
    __instance = AirPollutionHttpClient('xyz', __test_cache)

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

    def test_get_coi(self):

        # case: current CO index
        params = {'lon': 8.25, 'lat': 43.75, 'start': None, 'interval': None}
        bkp = self.__instance._lookup_cache_or_invoke_API

        def mock_func(cache, API_full_url, timeout):
            return API_full_url

        self.__instance._lookup_cache_or_invoke_API = mock_func

        expected_url = 'http://api.openweathermap.org/pollution/v1/co/43.75,8.25/current.json?appid=xyz'
        result = self.__instance.get_coi(params)
        self.assertEquals(expected_url, result)

        ts = timeformatutils.to_date(1463041620)  # 2016-05-12T08:27:00Z

        # case: no interval specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': None}
        expected_url = 'http://api.openweathermap.org/pollution/v1/co/43.75,8.25/2016Z.json?appid=xyz'
        result = self.__instance.get_coi(params)
        self.assertEquals(expected_url, result)

        # case: 'minute' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'minute'}
        expected_url = 'http://api.openweathermap.org/pollution/v1/co/43.75,8.25/2016-05-12T08:27Z.json?appid=xyz'
        result = self.__instance.get_coi(params)
        self.assertEquals(expected_url, result)

        # case: 'hour' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'hour'}
        expected_url = 'http://api.openweathermap.org/pollution/v1/co/43.75,8.25/2016-05-12T08Z.json?appid=xyz'
        result = self.__instance.get_coi(params)
        self.assertEquals(expected_url, result)

        # case: 'day' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'day'}
        expected_url = 'http://api.openweathermap.org/pollution/v1/co/43.75,8.25/2016-05-12Z.json?appid=xyz'
        result = self.__instance.get_coi(params)
        self.assertEquals(expected_url, result)

        # case: 'month' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'month'}
        expected_url = 'http://api.openweathermap.org/pollution/v1/co/43.75,8.25/2016-05Z.json?appid=xyz'
        result = self.__instance.get_coi(params)
        self.assertEquals(expected_url, result)

        # case: 'year' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'year'}
        expected_url = 'http://api.openweathermap.org/pollution/v1/co/43.75,8.25/2016Z.json?appid=xyz'
        result = self.__instance.get_coi(params)
        self.assertEquals(expected_url, result)

        self.__instance._lookup_cache_or_invoke_API = bkp

    def test_get_o3(self):
        # case: current O3 index
        params = {'lon': 8.25, 'lat': 43.75, 'start': None, 'interval': None}
        bkp = self.__instance._lookup_cache_or_invoke_API

        def mock_func(cache, API_full_url, timeout):
            return API_full_url

        self.__instance._lookup_cache_or_invoke_API = mock_func

        expected_url = 'http://api.openweathermap.org/pollution/v1/o3/43.75,8.25/current.json?appid=xyz'
        result = self.__instance.get_o3(params)
        self.assertEquals(expected_url, result)

        ts = timeformatutils.to_date(1463041620)  # 2016-05-12T08:27:00Z

        # case: no interval specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': None}
        expected_url = 'http://api.openweathermap.org/pollution/v1/o3/43.75,8.25/2016Z.json?appid=xyz'
        result = self.__instance.get_o3(params)
        self.assertEquals(expected_url, result)

        # case: 'minute' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'minute'}
        expected_url = 'http://api.openweathermap.org/pollution/v1/o3/43.75,8.25/2016-05-12T08:27Z.json?appid=xyz'
        result = self.__instance.get_o3(params)
        self.assertEquals(expected_url, result)

        # case: 'hour' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'hour'}
        expected_url = 'http://api.openweathermap.org/pollution/v1/o3/43.75,8.25/2016-05-12T08Z.json?appid=xyz'
        result = self.__instance.get_o3(params)
        self.assertEquals(expected_url, result)

        # case: 'day' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'day'}
        expected_url = 'http://api.openweathermap.org/pollution/v1/o3/43.75,8.25/2016-05-12Z.json?appid=xyz'
        result = self.__instance.get_o3(params)
        self.assertEquals(expected_url, result)

        # case: 'month' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'month'}
        expected_url = 'http://api.openweathermap.org/pollution/v1/o3/43.75,8.25/2016-05Z.json?appid=xyz'
        result = self.__instance.get_o3(params)
        self.assertEquals(expected_url, result)

        # case: 'year' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'year'}
        expected_url = 'http://api.openweathermap.org/pollution/v1/o3/43.75,8.25/2016Z.json?appid=xyz'
        result = self.__instance.get_o3(params)
        self.assertEquals(expected_url, result)

        self.__instance._lookup_cache_or_invoke_API = bkp