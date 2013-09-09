#!/usr/bin/env python

"""
Test case for owm.py module
"""

import unittest
from pyowm import OWM


class Test(unittest.TestCase):
    
    __test_instance = OWM('test_API_key')

    def test_API_key_accessors(self):
        """
        Test getter and setter for the API_key propery
        """
        test_API_key = 'G097IueS-9xN712E'
        owm = OWM()
        self.assertEqual(owm.get_API_key(), None, "")
        owm.set_API_key(test_API_key)
        self.assertEqual(owm.get_API_key(), test_API_key, "")
        
    def test_version_print_methods(self):
        """
        Test methods that print out API and library versions
        """
        lib_version = self.__test_instance.get_version()
        API_version = self.__test_instance.get_API_version()
        self.assertIsInstance(lib_version, str, "")
        self.assertIsInstance(API_version, str, "")

if __name__ == "__main__":
    unittest.main()