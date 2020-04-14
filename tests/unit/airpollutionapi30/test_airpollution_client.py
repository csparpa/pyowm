#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pyowm.airpollutionapi30.airpollution_client import AirPollutionHttpClient
from pyowm.commons.http_client import HttpClient
from pyowm.config import DEFAULT_CONFIG
from pyowm.utils import formatting


class TestAirPollutionHttpClient(unittest.TestCase):

    __instance = AirPollutionHttpClient('xyz', HttpClient('apikey', DEFAULT_CONFIG, '/anyurl.com'))

    def test_trim_to(self):
        ts = formatting.to_date(1463041620)  # 2016-05-12T08:27:00Z
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

    def test_get_coi(self):

        # case: current CO index
        params = {'lon': 8.25, 'lat': 43.75, 'start': None, 'interval': None}

        def mock_func(uri, params=None, headers=None):
            return 200, uri

        self.__instance._client.get_json = mock_func

        expected_url = 'co/43.75,8.25/current.json'
        result = self.__instance.get_coi(params)
        self.assertEqual(expected_url, result)

        ts = formatting.to_date(1463041620)  # 2016-05-12T08:27:00Z

        # case: no interval specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': None}
        expected_url = 'co/43.75,8.25/2016Z.json'
        result = self.__instance.get_coi(params)
        self.assertEqual(expected_url, result)

        # case: 'minute' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'minute'}
        expected_url = 'co/43.75,8.25/2016-05-12T08:27Z.json'
        result = self.__instance.get_coi(params)
        self.assertEqual(expected_url, result)

        # case: 'hour' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'hour'}
        expected_url = 'co/43.75,8.25/2016-05-12T08Z.json'
        result = self.__instance.get_coi(params)
        self.assertEqual(expected_url, result)

        # case: 'day' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'day'}
        expected_url = 'co/43.75,8.25/2016-05-12Z.json'
        result = self.__instance.get_coi(params)
        self.assertEqual(expected_url, result)

        # case: 'month' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'month'}
        expected_url = 'co/43.75,8.25/2016-05Z.json'
        result = self.__instance.get_coi(params)
        self.assertEqual(expected_url, result)

        # case: 'year' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'year'}
        expected_url = 'co/43.75,8.25/2016Z.json'
        result = self.__instance.get_coi(params)
        self.assertEqual(expected_url, result)

    def test_get_o3(self):
        # case: current O3 index
        params = {'lon': 8.25, 'lat': 43.75, 'start': None, 'interval': None}

        def mock_func(uri, params=None, headers=None):
            return 200, uri

        self.__instance._client.get_json = mock_func

        expected_url = 'o3/43.75,8.25/current.json'
        result = self.__instance.get_o3(params)
        self.assertEqual(expected_url, result)

        ts = formatting.to_date(1463041620)  # 2016-05-12T08:27:00Z

        # case: no interval specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': None}
        expected_url = 'o3/43.75,8.25/2016Z.json'
        result = self.__instance.get_o3(params)
        self.assertEqual(expected_url, result)

        # case: 'minute' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'minute'}
        expected_url = 'o3/43.75,8.25/2016-05-12T08:27Z.json'
        result = self.__instance.get_o3(params)
        self.assertEqual(expected_url, result)

        # case: 'hour' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'hour'}
        expected_url = 'o3/43.75,8.25/2016-05-12T08Z.json'
        result = self.__instance.get_o3(params)
        self.assertEqual(expected_url, result)

        # case: 'day' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'day'}
        expected_url = 'o3/43.75,8.25/2016-05-12Z.json'
        result = self.__instance.get_o3(params)
        self.assertEqual(expected_url, result)

        # case: 'month' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'month'}
        expected_url = 'o3/43.75,8.25/2016-05Z.json'
        result = self.__instance.get_o3(params)
        self.assertEqual(expected_url, result)

        # case: 'year' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'year'}
        expected_url = 'o3/43.75,8.25/2016Z.json'
        result = self.__instance.get_o3(params)
        self.assertEqual(expected_url, result)

    def test_get_no2(self):

        # case: current NO2 index
        params = {'lon': 8.25, 'lat': 43.75, 'start': None, 'interval': None}

        def mock_func(uri, params=None, headers=None):
            return 200, uri

        self.__instance._client.get_json = mock_func

        expected_url = 'no2/43.75,8.25/current.json'
        result = self.__instance.get_no2(params)
        self.assertEqual(expected_url, result)

        ts = formatting.to_date(1463041620)  # 2016-05-12T08:27:00Z

        # case: no interval specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': None}
        expected_url = 'no2/43.75,8.25/2016Z.json'
        result = self.__instance.get_no2(params)
        self.assertEqual(expected_url, result)

        # case: 'minute' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'minute'}
        expected_url = 'no2/43.75,8.25/2016-05-12T08:27Z.json'
        result = self.__instance.get_no2(params)
        self.assertEqual(expected_url, result)

        # case: 'hour' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'hour'}
        expected_url = 'no2/43.75,8.25/2016-05-12T08Z.json'
        result = self.__instance.get_no2(params)
        self.assertEqual(expected_url, result)

        # case: 'day' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'day'}
        expected_url = 'no2/43.75,8.25/2016-05-12Z.json'
        result = self.__instance.get_no2(params)
        self.assertEqual(expected_url, result)

        # case: 'month' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'month'}
        expected_url = 'no2/43.75,8.25/2016-05Z.json'
        result = self.__instance.get_no2(params)
        self.assertEqual(expected_url, result)

        # case: 'year' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'year'}
        expected_url = 'no2/43.75,8.25/2016Z.json'
        result = self.__instance.get_no2(params)
        self.assertEqual(expected_url, result)

    def test_get_so2(self):

        # case: current SO2 index
        params = {'lon': 8.25, 'lat': 43.75, 'start': None, 'interval': None}

        def mock_func(uri, params=None, headers=None):
            return 200, uri

        self.__instance._client.get_json = mock_func

        expected_url = 'so2/43.75,8.25/current.json'
        result = self.__instance.get_so2(params)
        self.assertEqual(expected_url, result)

        ts = formatting.to_date(1463041620)  # 2016-05-12T08:27:00Z

        # case: no interval specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': None}
        expected_url = 'so2/43.75,8.25/2016Z.json'
        result = self.__instance.get_so2(params)
        self.assertEqual(expected_url, result)

        # case: 'minute' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'minute'}
        expected_url = 'so2/43.75,8.25/2016-05-12T08:27Z.json'
        result = self.__instance.get_so2(params)
        self.assertEqual(expected_url, result)

        # case: 'hour' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'hour'}
        expected_url = 'so2/43.75,8.25/2016-05-12T08Z.json'
        result = self.__instance.get_so2(params)
        self.assertEqual(expected_url, result)

        # case: 'day' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'day'}
        expected_url = 'so2/43.75,8.25/2016-05-12Z.json'
        result = self.__instance.get_so2(params)
        self.assertEqual(expected_url, result)

        # case: 'month' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'month'}
        expected_url = 'so2/43.75,8.25/2016-05Z.json'
        result = self.__instance.get_so2(params)
        self.assertEqual(expected_url, result)

        # case: 'year' specified
        params = {'lon': 8.25, 'lat': 43.75, 'start': ts, 'interval': 'year'}
        expected_url = 'so2/43.75,8.25/2016Z.json'
        result = self.__instance.get_so2(params)
        self.assertEqual(expected_url, result)

    def test_repr(self):
        print(self.__instance)
