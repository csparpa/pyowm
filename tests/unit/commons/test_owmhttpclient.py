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
import urllib2
from pyowm.commons.owmhttpclient import OWMHTTPClient
from pyowm.exceptions.api_call_error import APICallError 

class TestHTTPUtils(unittest.TestCase):
    
    __instance = OWMHTTPClient()
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
        raise urllib2.HTTPError(None, 404, "Failure", None, None)
    
    def mock_urllib2_urlopen_raising_URLError(self, url):
        """Mock implementation of urllib2.urlopen raising URLError"""
        raise urllib2.URLError("Failure")
    
    def test_build_query_parameters(self):
        root = "http://test.com"
        params_dict = {"a": 1, "b": 2, "c": 3}
        expected = "http://test.com?a=1&c=3&b=2"
        self.assertEqual(self.__instance._build_query_parameters(root, params_dict),
                         expected)

    def test_build_full_URL(self):
        instance = OWMHTTPClient('test_API_key')
        API_subset_URL = 'http://test.com/api'
        params = {'a': 1, 'b': 2}
        self.assertEqual('http://test.com/api?a=1&b=2&APPID=test_API_key', 
                         instance._build_full_URL(API_subset_URL, params))
        
    def test_build_full_URL_with_no_API_key(self):
        API_subset_URL = 'http://test.com/api'
        params = {'a': 1, 'b': 2}
        self.assertEqual('http://test.com/api?a=1&b=2', 
                         self.__instance._build_full_URL(API_subset_URL, params))
        
    def test_call_API(self):
        ref_to_original_urlopen = urllib2.urlopen
        urllib2.urlopen = self.mock_urllib2_urlopen
        result_output = \
            self.__instance.call_API('http://tests.com/api', {'a': 1, 'b': 2})
        urllib2.urlopen = ref_to_original_urlopen
        self.assertEqual(self.__test_output, result_output)

    def test_call_API_raises_OWM_API_call_exception(self):
        ref_to_original_urlopen = urllib2.urlopen
        urllib2.urlopen = self.mock_urllib2_urlopen_raising_HTTPError
        self.assertRaises(APICallError, self.__instance.call_API, 
                          'http://tests.com/api', {'a': 1, 'b': 2})
        urllib2.urlopen = self.mock_urllib2_urlopen_raising_URLError
        self.assertRaises(APICallError, self.__instance.call_API, 
                          'http://tests.com/api', {'a': 1, 'b': 2})
        urllib2.urlopen = ref_to_original_urlopen
        
if __name__ == "__main__":
    unittest.main()