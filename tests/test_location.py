#!/usr/bin/env python

"""
Test case for location.py module
"""
import unittest
from pyowm.location import Location


class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_init_fails_when_coordinates_is_not_dict(self):
        """
        Test failure when providing: None, integer, string, list, tuple 
        """
        self.assertRaises(AssertionError, Location, 'London', None, 1234)
        self.assertRaises(AssertionError, Location, 'London', 1, 1234)
        self.assertRaises(AssertionError, Location, 'London', "foo", 1234)
        self.assertRaises(AssertionError, Location, 'London', ["foo","bar"], 1234)
        self.assertRaises(AssertionError, Location, 'London', ("foo","bar"), 1234)


if __name__ == "__main__":
    unittest.main()