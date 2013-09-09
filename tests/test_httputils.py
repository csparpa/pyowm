#!/usr/bin/env python

"""
Test case for httputils.py module
"""

import unittest
from pyowm.utils import httputils

class Test(unittest.TestCase):
    
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
        

if __name__ == "__main__":
    unittest.main()