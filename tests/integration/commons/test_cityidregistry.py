#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from pyowm.commons.cityidregistry import CityIDRegistry
from pyowm.utils.geo import Point
from pyowm.weatherapi30.location import Location


class TestCityIDRegistryReadsFS(unittest.TestCase):

    _instance = CityIDRegistry.get_instance()

    def _assertLocationsEqual(self, loc1, loc2):
        self.assertEqual(loc1.id, loc2.id)
        self.assertEqual(loc1.name, loc2.name)
        self.assertEqual(loc1.lat, loc2.lat)
        self.assertEqual(loc1.lon, loc2.lon)
        self.assertEqual(loc1.country, loc2.country)

    def _assertGeopointsEqual(self, point1, point2):
        self.assertIsInstance(point1, Point)
        self.assertIsInstance(point2, Point)
        self.assertEqual(point1.to_dict(), point2.to_dict())

    def test_ids_for(self):
        # No matches
        self.assertEqual([], self._instance.ids_for('aaaaaaaaaa', matching="exact"))

        # One match
        result = self._instance.ids_for("Milano", country="IT", matching="exact")
        self.assertEqual(1, len(result))

        # Multiple matches
        result = self._instance.ids_for("Bologna",  country="IT", matching="exact")
        self.assertEqual(3, len(result))

    def test_ids_for_fails_with_malformed_inputs(self):
        self.assertEqual([], self._instance.ids_for(None))
        self.assertRaises(ValueError, CityIDRegistry.ids_for, self._instance, 'name', 'country', None, '123abc')
        self.assertRaises(ValueError, CityIDRegistry.ids_for, self._instance, 'name', 'US', 'state', '123abc')
        self.assertRaises(ValueError, CityIDRegistry.ids_for, self._instance, 'name', None, 'CA', '123abc')
        self.assertRaises(ValueError, CityIDRegistry.ids_for, self._instance, 'name', 'US', 'CA', '123abc')

    def test_ids_for_matching_criteria(self):
        # look for an empty name
        result = self._instance.ids_for("")
        self.assertEqual(0, len(result))

        # exact
        result = self._instance.ids_for("gollar", matching='exact')
        self.assertEqual(0, len(result))

        result = self._instance.ids_for("Gollar", matching='exact')
        self.assertEqual(1, len(result))
        self.assertEqual((18007, 'Gollar', 'IR', None, 37.383331, 46.25), result[0])

        # like
        result = self._instance.ids_for("abbans", matching='like')
        self.assertEqual(2, len(result))
        self.assertEqual((3038800, 'Abbans-Dessus', 'FR', None, 47.120548, 5.88188), result[0])
        self.assertEqual((6452202, 'Abbans-Dessus', 'FR', None, 47.116669, 5.88333), result[1])

        result = self._instance.ids_for("Abbans", matching='like')
        self.assertEqual(2, len(result))

    def test_ids_for_same_name_different_countries(self):
        result = self._instance.ids_for("Ontario", matching='exact')
        self.assertEqual(6, len(result))

        result = self._instance.ids_for("Ontario", country="US", matching='exact')
        self.assertEqual(5, len(result))

        result = self._instance.ids_for("Ontario", country="CA", matching='exact')
        self.assertEqual(1, len(result))

        result = self._instance.ids_for("Ontario", country="US", state="NY", matching='exact')
        self.assertEqual(1, len(result))

    def test_ids_for_with_commas_in_city_names(self):
        result = self._instance.ids_for("Pitcairn, Henderson, Ducie and Oeno Islands", matching='exact')
        self.assertEqual(1, len(result))
        self.assertEqual((4030699, 'Pitcairn, Henderson, Ducie and Oeno Islands', 'PN', None, -25.066669, -130.100006), result[0])

    def test_locations_for(self):
        # No matches
        self.assertEqual([], self._instance.locations_for('aaaaaaaaaa'))

        # One match
        expected = Location('Milano', 9.19199, 45.464161, 6542283, country='IT')
        result = self._instance.locations_for("Milano", country="IT", matching="exact")
        self.assertEqual(1, len(result))
        self._assertLocationsEqual(expected, result[0])

        # Multiple matches
        expected1 = Location('Bologna', 11.43333, 44.466671, 3181927, country='IT')
        expected2 = Location('Bologna', 11.33875, 44.493809, 3181928, country='IT')
        expected3 = Location('Bologna', 11.35041, 44.506569, 6541998, country='IT')
        result = self._instance.locations_for("Bologna",  country="IT", matching="exact")
        self.assertEqual(3, len(result))
        self._assertLocationsEqual(expected1, result[0])
        self._assertLocationsEqual(expected2, result[1])
        self._assertLocationsEqual(expected3, result[2])

    def test_locations_for_fails_with_malformed_inputs(self):
        self.assertEqual([], self._instance.locations_for(None))
        self.assertRaises(ValueError, CityIDRegistry.locations_for, self._instance, 'name', 'country', None, '123abc')
        self.assertRaises(ValueError, CityIDRegistry.locations_for, self._instance, 'name', 'US', 'state', '123abc')
        self.assertRaises(ValueError, CityIDRegistry.locations_for, self._instance, 'name', None, 'CA', '123abc')
        self.assertRaises(ValueError, CityIDRegistry.locations_for, self._instance, 'name', 'US', 'CA', '123abc')

    def test_geopoints_for(self):
        # No matches
        self.assertEqual([], self._instance.geopoints_for('aaaaaaaaaa'))

        # One match
        expected = Location('Milano', 9.19199, 45.464161, 6542283, country='IT').to_geopoint()
        result = self._instance.geopoints_for("Milano", country="IT", matching="exact")
        self.assertEqual(1, len(result))
        self._assertGeopointsEqual(expected, result[0])

        # Multiple matches
        expected1 = Location('Bologna', 11.43333, 44.466671, 3181927, country='IT').to_geopoint()
        expected2 = Location('Bologna', 11.33875, 44.493809, 3181928, country='IT').to_geopoint()
        expected3 = Location('Bologna', 11.35041, 44.506569, 6541998, country='IT').to_geopoint()
        result = self._instance.geopoints_for("Bologna",  country="IT", matching="exact")
        self.assertEqual(3, len(result))
        self._assertGeopointsEqual(expected1, result[0])
        self._assertGeopointsEqual(expected2, result[1])
        self._assertGeopointsEqual(expected3, result[2])

    def test_repr(self):
        print(self._instance)


if __name__ == "__main__":
    unittest.main()
