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
        """
        lib_version = self.__test_instance.get_version()
        API_version = self.__test_instance.get_API_version()
        self.assertIsInstance(lib_version, str, "")
        self.assertIsInstance(API_version, str, "")

    #def test_observation_for_name(self):
    #    """
    #    Test that owm.observation_for_name returns a Location, a Weather and a 
    #    reception time and the objects are as expected
    #    """

    #def test_observation_for_name(self):
    #    """
    #    Test that owm.observation_for_name returns a Location, a Weather and a 
    #    reception time and the objects are as expected
    #    """
    
if __name__ == "__main__":
    unittest.main()