"""
Test case for cityidregistry.py module
"""

import unittest
from os import path, sep
from pyowm.webapi25.cityidregistry import CityIDRegistry
from pyowm.webapi25.location import Location

class TestCityIDRegistryReadsFS(unittest.TestCase):

    if path.isfile(path.abspath(path.dirname(__name__))+sep+'097-102.txt'):
        _current_folder = path.abspath(path.dirname(__name__))
    elif path.isfile(path.abspath(path.dirname(__name__) + 
            path.join('tests', 'functional', 'webapi25', '097-102.txt'))):
        _current_folder = path.join('..','..','tests','functional','webapi25')
    else:
        _current_folder = path.abspath(path.dirname(__name__))+sep+ \
                          sep.join(["functional","webapi25"])

    _prefix = _current_folder+sep
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
        expected = u'dongen,2756723,51.626671,4.938890,NL'
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
        expected = Location('dongen', 4.938890, 51.626671, 2756723, 'NL')
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

if __name__ == "__main__":
    unittest.main()