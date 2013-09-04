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
        
    def test_init_fails_when_name_is_not_string(self):
        """
        Test failure when providing: None, integer, dict, list, tuple 
        """
        self.assertRaises(AssertionError, Location, None, {'lon':12.3,'lat':43.7}, 1234)
        self.assertRaises(AssertionError, Location, 1, {'lon':12.3,'lat':43.7}, 1234)
        self.assertRaises(AssertionError, Location, {'foo':'bar'}, {'lon':12.3,'lat':43.7}, 1234)
        self.assertRaises(AssertionError, Location, ['foo','bar'], {'lon':12.3,'lat':43.7}, 1234)
        self.assertRaises(AssertionError, Location, ('foo','bar'), {'lon':12.3,'lat':43.7}, 1234)

    def test_init_fails_when_coordinates_is_not_dict(self):
        """
        Test failure when providing: None, integer, string, list, tuple 
        """
        self.assertRaises(AssertionError, Location, 'London', None, 1234)
        self.assertRaises(AssertionError, Location, 'London', 1, 1234)
        self.assertRaises(AssertionError, Location, 'London', 'foo', 1234)
        self.assertRaises(AssertionError, Location, 'London', ['foo','bar'], 1234)
        self.assertRaises(AssertionError, Location, 'London', ('foo','bar'), 1234)
        
    def test_init_fails_when_ID_is_not_int(self):
        """
        Test failure when providing: None, string, dict, list, tuple 
        """
        self.assertRaises(AssertionError, Location, 'London', {'lon':12.3,'lat':43.7}, None)
        self.assertRaises(AssertionError, Location, 'London', {'lon':12.3,'lat':43.7}, 'foo')
        self.assertRaises(AssertionError, Location, 'London', {'lon':12.3,'lat':43.7}, {'foo':'bar'})
        self.assertRaises(AssertionError, Location, 'London', {'lon':12.3,'lat':43.7}, ['foo','bar'])
        self.assertRaises(AssertionError, Location, 'London', {'lon':12.3,'lat':43.7}, ('foo','bar'))

if __name__ == "__main__":
    unittest.main()