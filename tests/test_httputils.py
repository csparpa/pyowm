#!/usr/bin/env python

"""
Test case for httputils.py module. 
Here we don't use mock objects because we don't want to rely on exeternal 
mocking libraries; we use monkey patching instead.
Monkey patching pattern:
  1. Keep a reference to the original function to be patched
  2. Replace the original function with the mock version
  3. Call function and get results
  4. Restore the original function (if possible, before unittest assertions 
     because they might fail)
"""

import unittest
from pyowm.utils import httputils
from pyowm.exceptions.api_call_exception import APICallException

class Test(unittest.TestCase):
    
    __test_output = "this is a test HTTP response payload"
    
    def mock_urllib2_urlopen(self, url):
        """Mock implementation of urllib2.urlopen method for testing purposes"""
        
        class Mock_Response(object):
            def __init__(self, output_msg):
                self.__output_msg = output_msg
            def read(self):
                return self.__output_msg
        
        return Mock_Response(self.__test_output)
    
    def mock_urllib2_urlopen_raising_HTTPError(self, url):
        """Mock implementation of urllib2.urlopen raising HTTPError"""
        raise httputils.urllib2.HTTPError(None, 404, "Failure", None, None)
    
    def mock_urllib2_urlopen_raising_URLError(self, url):
        """Mock implementation of urllib2.urlopen raising URLError"""
        raise httputils.urllib2.URLError("Failure")
    
    def test_build_query_parameters(self):
        root = "http://test.com"
        params_dict = {"a": 1, "b": 2, "c": 3}
        expected = "http://test.com?a=1&c=3&b=2"
        self.assertEqual(httputils.build_query_parameters(root, params_dict), expected, "")

    def test_build_full_URL(self):
        API_subset_URL = 'http://test.com/api'
        API_key = 'test_API_key'
        params = {'a': 1, 'b': 2}
        expected1 = 'http://test.com/api?a=1&b=2&APPID=test_API_key'
        expected2 = 'http://test.com/api?a=1&b=2'
        self.assertEqual(httputils.build_full_URL(API_subset_URL, params, API_key), expected1, "")
        self.assertEqual(httputils.build_full_URL(API_subset_URL, params, None), expected2, "")
        
    def test_call_API(self):
        ref_to_original_urlopen = httputils.urllib2.urlopen
        httputils.urllib2.urlopen = self.mock_urllib2_urlopen
        result_output = httputils.call_API('http://tests.com/api', {'a': 1, 'b': 2}, 'test_API_key')
        httputils.urllib2.urlopen = ref_to_original_urlopen
        self.assertEqual(self.__test_output, result_output, "")

    def test_call_API_raises_OWM_API_call_exception(self):
        ref_to_original_urlopen = httputils.urllib2.urlopen
        httputils.urllib2.urlopen = self.mock_urllib2_urlopen_raising_HTTPError
        self.assertRaises(APICallException, httputils.call_API, 'http://tests.com/api', {'a': 1, 'b': 2}, 'test_API_key')
        httputils.urllib2.urlopen = self.mock_urllib2_urlopen_raising_URLError
        self.assertRaises(APICallException, httputils.call_API, 'http://tests.com/api', {'a': 1, 'b': 2}, 'test_API_key')
        httputils.urllib2.urlopen = ref_to_original_urlopen
        
if __name__ == "__main__":
    unittest.main()