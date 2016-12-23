"""
Integration test case for cityidregistry.py module
"""

import unittest
from os import sep
from pyowm.webapi25.cityidregistry import CityIDRegistry
from pyowm.webapi25.location import Location


class TestCityIDRegistryReadsFS(unittest.TestCase):

    _prefix = 'cityids'+sep
    _instance = CityIDRegistry(_prefix+'%03d-%03d.txt')

    def test_assess_subfile_from(self):
        self.assertEqual(self._instance._assess_subfile_from('b-city'),
                         self._prefix+'097-102.txt')
        self.assertEqual(self._instance._assess_subfile_from('h-city'),
                         self._prefix+'103-108.txt')
        self.assertEqual(self._instance._assess_subfile_from('n-city'),
                         self._prefix+'109-114.txt')
        self.assertEqual(self._instance._assess_subfile_from('t-city'),
                         self._prefix+'115-122.txt')
        self.assertRaises(ValueError, CityIDRegistry._assess_subfile_from,
                          self._instance, '123abc')
        self.assertRaises(ValueError, CityIDRegistry._assess_subfile_from,
                          self._instance, '{abc')

    def test_lookup_line_by_city_name(self):
        expected = u'Dongen,2756723,51.626671,4.93889,NL'
        self.assertEquals(expected,
                          self._instance._lookup_line_by_city_name('dongen'))
        self.assertTrue(self._instance. \
                            _lookup_line_by_city_name('aaaaaaaa') is None)

    def test_id_for(self):
        self.assertEqual(self._instance.id_for('dongen'), 2756723)
        self.assertTrue(self._instance.id_for('aaaaaaaaaa') is None)

    def test_id_for_fails_with_malformed_inputs(self):
        self.assertRaises(ValueError, CityIDRegistry.id_for, self._instance,
                          '123abc')

    def test_location_for(self):
        expected = Location('Dongen', 4.938890, 51.626671, 2756723, 'NL')
        result = self._instance.location_for('dongen')
        self.assertEqual(result.get_name(), expected.get_name())
        self.assertEqual(result.get_country(), expected.get_country())
        self.assertEqual(result.get_ID(), expected.get_ID())
        self.assertEqual(result.get_lat(), expected.get_lat())
        self.assertEqual(result.get_lon(), expected.get_lon())
        self.assertTrue(self._instance.location_for('aaaaaaaaaa') is None)

    def test_location_for_fails_with_malformed_inputs(self):
        self.assertRaises(ValueError, CityIDRegistry.location_for,
                          self._instance, '123abc')

    def test_ids_for(self):
        result = self._instance.ids_for("bologna", matching='exact')
        self.assertEquals(0, len(result))

        result = self._instance.ids_for("Abbans-Dessus")
        self.assertEquals(2, len(result))
        self.assertTrue((3038800, 'Abbans-Dessus', 'FR') in result)
        self.assertTrue((6452202, 'Abbans-Dessus', 'FR') in result)

        result = self._instance.ids_for("Dessus", matching='like')
        self.assertEquals(6, len(result))

    def test_locations_for(self):
        expected1 = Location('Abbans-Dessus', 5.88188, 47.120548, 3038800, 'FR')
        expected2 = Location('Abbans-Dessus', 5.88333, 47.116669, 6452202, 'FR')
        result = self._instance.locations_for("Abbans-Dessus")
        self.assertEquals(2, len(result))
        for l in result:
            self.assertTrue(isinstance(l, Location))
            self.assertTrue(l.get_ID() in [expected1.get_ID(), expected2.get_ID()])

if __name__ == "__main__":
    unittest.main()
