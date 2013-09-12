#!/usr/bin/env python

"""
Test case for owm.py module.
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
from json_test_responses import OBSERVATION_JSON
from pyowm import OWM
from pyowm.utils import httputils

class Test(unittest.TestCase):
    
    __test_instance = OWM('test_API_key')
    
    def mock_httputils_call_API(self, API_subset_URL, params_dict, API_key):
        """Mock implementation of httputils.call_API"""
        return OBSERVATION_JSON

    def test_API_key_accessors(self):
        test_API_key = 'G097IueS-9xN712E'
        owm = OWM()
        self.assertEqual(owm.get_API_key(), None, "")
        owm.set_API_key(test_API_key)
        self.assertEqual(owm.get_API_key(), test_API_key, "")
        
    def test_version_print_methods(self):
        lib_version = self.__test_instance.get_version()
        API_version = self.__test_instance.get_API_version()
        self.assertIsInstance(lib_version, str, "")
        self.assertIsInstance(API_version, str, "")

    def test_observation_at_place(self):
        """
        Test that owm.observation_at_place returns a valid Observation object.
        We need to monkey patch the inner call to httputils.call_API function
        """
        ref_to_original_call_API = httputils.call_API
        httputils.call_API = self.mock_httputils_call_API
        result = self.__test_instance.observation_at_place("London,uk")
        httputils.call_API = ref_to_original_call_API
        self.assertFalse(result is None, "")
        self.assertFalse(result.get_reception_time() is None, "")
        self.assertFalse(result.get_location() is None, "")
        self.assertNotIn(None, result.get_location().__dict__.values(), "")
        self.assertFalse(result.get_weather() is None, "")
        self.assertNotIn(None, result.get_weather().__dict__.values(), "")
    
    def test_observation_at_coords(self):
        """
        Test that owm.observation_at_coords returns a valid Observation object.
        We need to monkey patch the inner call to httputils.call_API function
        """
        ref_to_original_call_API = httputils.call_API
        httputils.call_API = self.mock_httputils_call_API
        result = self.__test_instance.observation_at_coords(-2.15,57.0)
        httputils.call_API = ref_to_original_call_API
        self.assertFalse(result is None, "")
        self.assertFalse(result.get_reception_time() is None, "")
        self.assertFalse(result.get_location() is None, "")
        self.assertNotIn(None, result.get_location().__dict__.values(), "")
        self.assertFalse(result.get_weather() is None, "")
        self.assertNotIn(None, result.get_weather().__dict__.values(), "")
        
    def test_find_observations_by_name_fails_with_wrong_params(self):
        """
        Test method failure providing: a bad value for 'searchtype' and a
        negative value for 'limit'
        """
        self.assertRaises(ValueError, OWM.find_observations_by_name, self.__test_instance, "London", "x")
        self.assertRaises(ValueError, OWM.find_observations_by_name, self.__test_instance, "London", "accurate", -5)
if __name__ == "__main__":
    unittest.main()