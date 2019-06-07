#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
from pyowm.weatherapi25.location import Location
from pyowm.utils.geo import Point
from tests.unit.weatherapi25.json_test_dumps import LOCATION_JSON_DUMP


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
        result1 = Location.from_dict(dict1)
        result2 = Location.from_dict(dict2)
        result3 = Location.from_dict(dict3)
        self.assertTrue(isinstance(result1, Location))
        self.assertTrue(isinstance(result2, Location))
        self.assertFalse(result1.country is not None)
        self.assertTrue(result1.id is not None)
        self.assertTrue(result1.lat is not None)
        self.assertTrue(result1.lon is not None)
        self.assertTrue(result1.name is not None)
        self.assertTrue(result2.country is not None)
        self.assertTrue(result2.id is not None)
        self.assertTrue(result2.lat is not None)
        self.assertTrue(result2.lon is not None)
        self.assertTrue(result2.name is not None)
        self.assertTrue(result3.lat is not None)
        self.assertTrue(result3.lon is not None)
        self.assertTrue(result3.country is None)
        self.assertTrue(result3.name is None)
        self.assertTrue(result3.id is None)

    def test_from_dictionary_holds_the_lack_of_geocoords(self):
        dict1 = {"station":{"coord":{}}}
        dict2 = {"coord":{}}
        result1 = Location.from_dict(dict1)
        self.assertTrue(isinstance(result1, Location))
        self.assertEqual(result1.lat, 0.0)
        self.assertEqual(result1.lon, 0.0)
        self.assertTrue(result1.country is None)
        self.assertTrue(result1.name is None)
        self.assertTrue(result1.id is None)
        result2 = Location.from_dict(dict2)
        self.assertTrue(isinstance(result2, Location))
        self.assertEqual(result2.lat, 0.0)
        self.assertEqual(result2.lon, 0.0)
        self.assertTrue(result2.country is None)
        self.assertTrue(result2.name is None)
        self.assertTrue(result2.id is None)

    def test_to_dict(self):
        expected = json.loads(LOCATION_JSON_DUMP)
        result = self.__test_instance.to_dict()
        self.assertEqual(expected, result)

    def to_geopoint(self):
        loc_1 = Location(self.__test_name, None, self.__test_lat,
                         self.__test_ID, self.__test_country)
        loc_2 = Location(self.__test_name, self.__test_lon, None,
                         self.__test_ID, self.__test_country)
        loc_3 = Location(self.__test_name, self.__test_lon, self.__test_lat,
                         self.__test_ID, self.__test_country)
        self.assertIsNone(loc_1.to_geopoint())
        self.assertIsNone(loc_2.to_geopoint())
        result = loc_3.to_geopoint()
        self.assertTrue(isinstance(result, Point))
        expected_geojson = json.dumps({
            "coordinates": [12.3, 43.7],
            "type": "Point"
        })
        self.assertEqual(sorted(expected_geojson),
                         sorted(result.geojson()))

