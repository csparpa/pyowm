# -*- coding: utf-8 -*-

"""
Test case for httputils.py module.
Here we don't use mock objects because we don't want to rely on external
mocking libraries; we use monkey patching instead.
Monkey patching pattern:
  1. Keep a reference to the original function to be patched
  2. Replace the original function with the mock version
  3. Call function and get results
  4. Restore the original function (if possible, before unittest assertions
     because they might fail)
"""

import unittest

# Python 2.x/3.x compatibility imports
try:
    from urllib.error import HTTPError, URLError
    import urllib.request
except ImportError:
    from urllib2 import HTTPError, URLError
    import urllib2

from pyowm.commons.weather_client import WeatherHttpClient
from pyowm.exceptions.api_call_error import APICallError
from pyowm.exceptions import not_found_error
from pyowm.caches.nullcache import NullCache

context = locals()  # Local context


class TestOWMHTTPClient(unittest.TestCase):

    __test_cache = NullCache()
    __instance = WeatherHttpClient(None, __test_cache)
    __test_output = b"this is a test HTTP response payload"

    def mock_urlopen(self, url, data, timeout):
        """
        Mock implementation of urllib2.urlopen method for testing
        purposes
        """

        class Mock_Response(object):
            def __init__(self, output_msg):
                self.__output_msg = output_msg

            def read(self):
                return self.__output_msg

        return Mock_Response(self.__test_output)

    def mock_urlopen_raising_HTTPError(self, url, data, timeout):
        """Mock implementation of urllib2.urlopen raising HTTPError"""
        raise HTTPError(None, 404, "Failure", None, None)

    def mock_urlopen_raising_URLError(self, url, data, timeout):
        """Mock implementation of urllib2.urlopen raising URLError"""
        raise URLError("Failure")

    def test_build_query_parameters(self):
        root = "http://test.com"
        params_dict = {"a": 1, "b": 2}
        result = self.__instance._build_query_parameters(root, params_dict)
        expected_1 = "http://test.com?a=1&b=2"
        expected_2 = "http://test.com?b=2&a=1"
        self.assertTrue(result == expected_1 or result == expected_2)

    def test_build_full_URL(self):
        instance = WeatherHttpClient('test_API_key', self.__test_cache)
        API_subset_URL = '/subset'
        params = {'a': 1}
        result = instance._build_full_URL(API_subset_URL, params)
        expected_1 = 'http://api.openweathermap.org/data/2.5/subset?a=1&APPID=test_API_key'
        expected_2 = 'http://api.openweathermap.org/data/2.5/subset?APPID=test_API_key&a=1'
        self.assertTrue(result == expected_1 or result == expected_2)

    def test_build_full_URL_with_no_API_key(self):
        API_subset_URL = '/subset'
        params = {'a': 1, 'b': 2}
        result = self.__instance._build_full_URL(API_subset_URL, params)
        expected_1 = 'http://api.openweathermap.org/data/2.5/subset?a=1&b=2'
        expected_2 = 'http://api.openweathermap.org/data/2.5/subset?b=2&a=1'
        self.assertTrue(result == expected_1 or result == expected_2)

    def test_build_full_URL_with_unicode_chars_in_API_key(self):
        instance = WeatherHttpClient('£°test££', self.__test_cache)
        API_subset_URL = '/subset'
        params = {'a': 1}
        result = instance._build_full_URL(API_subset_URL, params)
        expected_1 = 'http://api.openweathermap.org/data/2.5/subset?a=1&APPID=%C2%A3%C2%B0test%C2%A3%C2%A3'
        expected_2 = 'http://api.openweathermap.org/data/2.5/subset?APPID=%C2%A3%C2%B0test%C2%A3%C2%A3&a=1'
        self.assertTrue(result == expected_1 or result == expected_2)

    def test_call_API(self):
        # Setup monkey patching
        if 'urllib2' in context:  # Python 2.x
            ref_to_original_urlopen = urllib2.urlopen
            urllib2.urlopen = self.mock_urlopen
        else:  # Python 3.x
            ref_to_original_urlopen = urllib.request.urlopen
            urllib.request.urlopen = self.mock_urlopen
        result_output = \
            self.__instance.call_API('http://tests.com/api', {'a': 1, 'b': 2})
        # Tear down monkey patching
        if 'urllib2' in context:  # Python 2.x
            urllib2.urlopen = ref_to_original_urlopen
        else:   # Python 3.x
            urllib.request.urlopen = ref_to_original_urlopen
        self.assertEqual(self.__test_output.decode('utf-8'), result_output)

    def test_call_API_raises_exception(self):
        # Setup monkey patching
        if 'urllib2' in context:  # Python 2.x
            ref_to_original_urlopen = urllib2.urlopen
        else:  # Python 3.x
            ref_to_original_urlopen = urllib.request.urlopen

        # Test raising HTTPrror
        if 'urllib2' in context:  # Python 2.x
            urllib2.urlopen = self.mock_urlopen_raising_HTTPError
        else:  # Python 3.x
            urllib.request.urlopen = \
                self.mock_urlopen_raising_HTTPError
        self.assertRaises(not_found_error.NotFoundError,
                          self.__instance.call_API,
                          'http://tests.com/api', {'a': 1, 'b': 2})

        # Test raising URLError
        if 'urllib2' in context:  # Python 2.x
            urllib2.urlopen = self.mock_urlopen_raising_URLError
        else:  # Python 3.x
            urllib.request.urlopen = self.mock_urlopen_raising_URLError
        self.assertRaises(APICallError, self.__instance.call_API,
                          'http://tests.com/api', {'a': 1, 'b': 2})

        # Tear down monkey patching
        if 'urllib2' in context:  # Python 2.x
            urllib2.urlopen = ref_to_original_urlopen
        else:  # Python 3.x
            urllib.request.urlopen = ref_to_original_urlopen
