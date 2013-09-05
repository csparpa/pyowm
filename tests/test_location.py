#!/usr/bin/env python

"""
Test case for location.py module
"""
import unittest
from pyowm import Location


class Test(unittest.TestCase):
    
    testName = 'London'
    testLon = 12.3
    testLat = 43.7
    testID = 1234
        
    def test_init_fails_when_name_is_not_string(self):
        """
        Test failure when providing: None, float, dict, list, tuple 
        """
        self.assertRaises(AssertionError, Location, None, 12.3, 43.7, 1234)
        self.assertRaises(AssertionError, Location, 1.0, 12.3, 43.7, 1234)
        self.assertRaises(AssertionError, Location, {'foo':'bar'}, 12.3, 43.7, 1234)
        self.assertRaises(AssertionError, Location, ['foo','bar'], 12.3, 43.7, 1234)
        self.assertRaises(AssertionError, Location, ('foo','bar'), 12.3, 43.7, 1234)

    def test_init_fails_when_lon_is_not_number(self):
        """
        Test failure when providing: None, string, dict, list, tuple 
        """
        self.assertRaises(AssertionError, Location, 'London', None, 43.7, 1234)
        self.assertRaises(AssertionError, Location, 'London', 'foo', 43.7, 1234)
        self.assertRaises(AssertionError, Location, 'London', {'foo':'bar'}, 43.7, 1234)
        self.assertRaises(AssertionError, Location, 'London', ['foo','bar'], 43.7, 1234)
        self.assertRaises(AssertionError, Location, 'London', ('foo','bar'), 43.7, 1234)        
        
    def test_init_fails_when_lat_is_not_number(self):
        """
        Test failure when providing: None, string, dict, list, tuple 
        """
        self.assertRaises(AssertionError, Location, 'London', 12.3, None, 1234)
        self.assertRaises(AssertionError, Location, 'London', 12.3, 'foo', 1234)
        self.assertRaises(AssertionError, Location, 'London', 12.3, {'foo':'bar'}, 1234)
        self.assertRaises(AssertionError, Location, 'London', 12.3, ['foo','bar'], 1234)
        self.assertRaises(AssertionError, Location, 'London', 12.3, ('foo','bar'), 1234)
        
    def test_init_fails_when_coordinates_are_out_of_bounds(self):
        """
        Test failure when providing: lon < -180, lon > 180, lat < -90, lat > 90
        """
        self.assertRaises(ValueError, Location, 'London', -200.0, 43.7, 1234)
        self.assertRaises(ValueError, Location, 'London', 200.0, 43.7, 1234)
        self.assertRaises(ValueError, Location, 'London', 12.3, -100.0, 1234)
        self.assertRaises(ValueError, Location, 'London', 12.3, 100.0, 1234)
        
    def test_init_succeeds_when_coordinates_are_int(self):
        """
        Test by first providing an integer lon, then an integer lat
        """ 
        intLon = 43
        intLat = 12
        instance1 = Location('London', intLon, float(intLat), 1234)
        self.assertEqual(instance1.getLon(), float(intLon), "")
        instance2 = Location('London', float(intLon), intLat, 1234)
        self.assertEqual(instance2.getLat(), float(intLat), "")
        
    def test_init_fails_when_ID_is_not_int(self):
        """
        Test failure when providing: None, string, dict, list, tuple 
        """
        self.assertRaises(AssertionError, Location, 'London', 12.3, 43.7, None)
        self.assertRaises(AssertionError, Location, 'London', 12.3, 43.7, 'foo')
        self.assertRaises(AssertionError, Location, 'London', 12.3, 43.7, {'foo':'bar'})
        self.assertRaises(AssertionError, Location, 'London', 12.3, 43.7, ['foo','bar'])
        self.assertRaises(AssertionError, Location, 'London', 12.3, 43.7, ('foo','bar'))
        
    def test_init_fails_when_ID_is_smaller_than_zero(self):
        self.assertRaises(ValueError, Location, 'London', 12.3, 43.7, -987)
        
    def test_getters_return_expected_data(self):
        instance = Location(self.testName, self.testLon, self.testLat, self.testID)
        self.assertEqual(instance.getName(), self.testName, "")
        self.assertEqual(instance.getLon(), self.testLon, "")
        self.assertEqual(instance.getLat(), self.testLat, "")
        self.assertEqual(instance.getID(), self.testID, "")
        

    def test_toXML(self):
        expectedOutput = """<Location><name>%s</name><coordinates><lon>%s</lon>
            <lat>%s</lat></coordinates><ID>%s</ID></Location>""" % (self.testName,
                                                                    self.testLon,
                                                                    self.testLat,
                                                                    self.testID)
        instance = Location(self.testName, self.testLon, self.testLat, self.testID)
        self.assertEqual(instance.toXML(), expectedOutput, "")
        
    def test_toJSON(self):
        expectedOutput = """{"name": "%s", "coordinates": {"lat": %s, "lon": %s}, "ID": %s}""" %  (self.testName, 
           self.testLat, self.testLon, self.testID)
        instance = Location(self.testName, self.testLon, self.testLat, self.testID)
        self.assertEqual(instance.toJSON(), expectedOutput, "")
        

if __name__ == "__main__":
    unittest.main()