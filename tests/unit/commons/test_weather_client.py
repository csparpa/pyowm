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

    def mock_urlopen_raising_unusual_HTTPError(self, url, data, timeout):
        """Mock implementation of urllib2.urlopen raising an uncharted HTTPError"""
        raise HTTPError(None, 579, "Uncharted failure", None, None)

    def mock_urlopen_raising_URLError(self, url, data, timeout):
        """Mock implementation of urllib2.urlopen raising URLError"""
        raise URLError("Failure")

    def test_call_API(self):
        # Setup monkey patching
        if 'urllib2' in context:  # Python 2.x
            ref_to_original_urlopen = urllib2.urlopen
            urllib2.urlopen = self.mock_urlopen
        else:  # Python 3.x
            ref_to_original_urlopen = urllib.request.urlopen
            urllib.request.urlopen = self.mock_urlopen
        result_output = \
            self.__instance.call_API('http://%s.tests.com/api', {'a': 1, 'b': 2})
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
                          'http://%s.tests.com/api', {'a': 1, 'b': 2})

        # Test raising URLError
        if 'urllib2' in context:  # Python 2.x
            urllib2.urlopen = self.mock_urlopen_raising_URLError
        else:  # Python 3.x
            urllib.request.urlopen = self.mock_urlopen_raising_URLError
        self.assertRaises(APICallError, self.__instance.call_API,
                          'http://%s.tests.com/api', {'a': 1, 'b': 2})

        # Test raising URLError upon unusual (eg. non 401, 404, 502) HTTP errors
        if 'urllib2' in context:  # Python 2.x
            urllib2.urlopen = self.mock_urlopen_raising_unusual_HTTPError
        else:  # Python 3.x
            urllib.request.urlopen = self.mock_urlopen_raising_unusual_HTTPError
        self.assertRaises(APICallError, self.__instance.call_API,
                          'http://%s.tests.com/api', {'a': 1, 'b': 2})

        # Tear down monkey patching
        if 'urllib2' in context:  # Python 2.x
            urllib2.urlopen = ref_to_original_urlopen
        else:  # Python 3.x
            urllib.request.urlopen = ref_to_original_urlopen
