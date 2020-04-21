#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from os import sep
from pyowm.commons.cityidregistry import CityIDRegistry
from pyowm.weatherapi25.location import Location


class TestCityIDRegistryReadsFS(unittest.TestCase):

    _prefix = 'cityids'+sep
    _instance = CityIDRegistry(_prefix+'%03d-%03d.txt.bz2')

    def test_assess_subfile_from(self):
        self.assertEqual(self._instance._assess_subfile_from('b-city'),
                         self._prefix+'097-102.txt.bz2')
        self.assertEqual(self._instance._assess_subfile_from('h-city'),
                         self._prefix+'103-108.txt.bz2')
        self.assertEqual(self._instance._assess_subfile_from('n-city'),
                         self._prefix+'109-114.txt.bz2')
        self.assertEqual(self._instance._assess_subfile_from('t-city'),
                         self._prefix+'115-122.txt.bz2')
        self.assertRaises(ValueError, CityIDRegistry._assess_subfile_from,
                          self._instance, '123abc')
        self.assertRaises(ValueError, CityIDRegistry._assess_subfile_from,
                          self._instance, '{abc')

    def test_lookup_line_by_city_name(self):
        expected = u'Dongen,2756723,51.626671,4.93889,NL'
        self.assertEqual(expected,
                          self._instance._lookup_line_by_city_name('dongen'))
        self.assertTrue(self._instance. \
                            _lookup_line_by_city_name('aaaaaaaa') is None)

    def test_ids_for(self):
        self.assertEqual([(2756723, 'Dongen', 'NL')], self._instance.ids_for('dongen'))
        self.assertEqual([], self._instance.ids_for('aaaaaaaaaa'))

    def test_ids_for_fails_with_malformed_inputs(self):
        self.assertRaises(ValueError, CityIDRegistry.ids_for, self._instance, '123abc')

    def test_locations_for(self):
        expected = Location('Dongen', 4.938890, 51.626671, 2756723, 'NL')
        result_list = self._instance.locations_for('dongen')
        self.assertEqual(1, len(result_list))
        result = result_list[0]
        self.assertEqual(result.name, expected.name)
        self.assertEqual(result.country, expected.country)
        self.assertEqual(result.id, expected.id)
        self.assertEqual(result.lat, expected.lat)
        self.assertEqual(result.lon, expected.lon)
        self.assertEqual([], self._instance.locations_for('aaaaaaaaaa'))

    def test_locations_for_fails_with_malformed_inputs(self):
        self.assertRaises(ValueError, CityIDRegistry.locations_for, self._instance, '123abc')

    def test_ids_for_more_cases(self):
        result = self._instance.ids_for("bologna", matching='exact')
        self.assertEqual(0, len(result))

        result = self._instance.ids_for("Abbans-Dessus")
        self.assertEqual(2, len(result))
        self.assertTrue((3038800, 'Abbans-Dessus', 'FR') in result)
        self.assertTrue((6452202, 'Abbans-Dessus', 'FR') in result)

        result = self._instance.ids_for("Dessus", matching='like')
        self.assertEqual(6, len(result))

    def test_locations_for_more_cases(self):
        expected1 = Location('Abbans-Dessus', 5.88188, 47.120548, 3038800, 'FR')
        expected2 = Location('Abbans-Dessus', 5.88333, 47.116669, 6452202, 'FR')
        result = self._instance.locations_for("Abbans-Dessus")
        self.assertEqual(2, len(result))
        for l in result:
            self.assertTrue(isinstance(l, Location))
            self.assertTrue(l.id in [expected1.id, expected2.id])


if __name__ == "__main__":
    unittest.main()
