"""
Test case for location.py module
"""

import unittest
from pyowm.webapi25.location import Location, location_from_dictionary
from tests.unit.webapi25.json_test_dumps import LOCATION_JSON_DUMP
from tests.unit.webapi25.xml_test_dumps import LOCATION_XML_DUMP


class TestLocation(unittest.TestCase):

    __test_name = 'London'
    __test_lon = 12.3
    __test_lat = 43.7
    __test_ID = 1234
    __test_country = 'UK'
    __test_instance = Location(__test_name, __test_lon, __test_lat, __test_ID,
                               __test_country)

    def test_init_fails_when_lat_or_lon_are_none(self):
        self.assertRaises(ValueError, Location, 'London', None, 43.7, 1234)
        self.assertRaises(ValueError, Location, 'London', 200.0, None, 1234)

    def test_init_fails_when_coordinates_are_out_of_bounds(self):
        """
        Test failure when providing: lon < -180, lon > 180, lat < -90, lat > 90
        """
        self.assertRaises(ValueError, Location, 'London', -200.0, 43.7, 1234)
        self.assertRaises(ValueError, Location, 'London', 200.0, 43.7, 1234)
        self.assertRaises(ValueError, Location, 'London', 12.3, -100.0, 1234)
        self.assertRaises(ValueError, Location, 'London', 12.3, 100.0, 1234)

    def test_from_dictionary(self):
        dict1 = {"coord": {"lon": -0.12574, "lat": 51.50853}, "id": 2643743,
                 "name": "London", "cnt": 9}
        dict2 = {"city": {"coord": {"lat": 51.50853, "lon": -0.125739},
                 "country": "GB", "id": 2643743, "name": "London",
                 "population": 1000000}
                }
        dict3 = {"station":{"coord":{"lon":-90.47,"lat":39.38}}}
        result1 = location_from_dictionary(dict1)
        result2 = location_from_dictionary(dict2)
        result3 = location_from_dictionary(dict3)
        self.assertTrue(isinstance(result1, Location))
        self.assertTrue(isinstance(result2, Location))
        self.assertFalse(result1.get_country() is not None)
        self.assertTrue(result1.get_ID() is not None)
        self.assertTrue(result1.get_lat() is not None)
        self.assertTrue(result1.get_lon() is not None)
        self.assertTrue(result1.get_name() is not None)
        self.assertTrue(result2.get_country() is not None)
        self.assertTrue(result2.get_ID() is not None)
        self.assertTrue(result2.get_lat() is not None)
        self.assertTrue(result2.get_lon() is not None)
        self.assertTrue(result2.get_name() is not None)
        self.assertTrue(result3.get_lat() is not None)
        self.assertTrue(result3.get_lon() is not None)
        self.assertTrue(result3.get_country() is None)
        self.assertTrue(result3.get_name() is None)
        self.assertTrue(result3.get_ID() is None)

    def test_getters_return_expected_data(self):
        instance = Location(self.__test_name, self.__test_lon, self.__test_lat,
                            self.__test_ID, self.__test_country)
        self.assertEqual(instance.get_name(), self.__test_name)
        self.assertEqual(instance.get_lon(), self.__test_lon)
        self.assertEqual(instance.get_lat(), self.__test_lat)
        self.assertEqual(instance.get_ID(), self.__test_ID)
        self.assertEqual(instance.get_country(), self.__test_country)

    # Test JSON and XML comparisons by ordering strings (this overcomes
    # interpeter-dependant serialization of XML/JSON objects

    def test_to_JSON(self):
        ordered_base_json = ''.join(sorted(LOCATION_JSON_DUMP))
        ordered_actual_json = ''.join(sorted(self.__test_instance.to_JSON()))
        self.assertEqual(ordered_base_json, ordered_actual_json)

    def test_to_XML(self):
        ordered_base_xml = ''.join(sorted(LOCATION_XML_DUMP))
        ordered_actual_xml = ''.join(sorted(self.__test_instance.to_XML()))
        self.assertEqual(ordered_base_xml, ordered_actual_xml)
