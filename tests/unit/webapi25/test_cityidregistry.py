"""
Test case for cityidregistry.py module
"""

import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from pyowm.webapi25.cityidregistry import CityIDRegistry
from pyowm.webapi25.location import Location


class TestCityIDRegistry(unittest.TestCase):

    _instance = CityIDRegistry('%03d-%03d.txt')
    _test_file_contents = """dongditou,1812600,39.261391,117.368332,CN
dongdu,1812597,35.849998,117.699997,CN
dongel,747912,40.693600,29.941540,TR
dongen,2756723,51.626671,4.938890,NL
dongerying,1812594,39.957500,117.279167,CN
donges,3021093,47.318241,-2.075380,FR"""

    def _mock_get_lines(self, filename):
        return StringIO(self._test_file_contents).readlines()

    def test_assess_subfile_from(self):
        self.assertEqual(self._instance._assess_subfile_from('b-city'),
                         '097-102.txt')
        self.assertEqual(self._instance._assess_subfile_from('h-city'),
                         '103-108.txt')
        self.assertEqual(self._instance._assess_subfile_from('n-city'),
                         '109-114.txt')
        self.assertEqual(self._instance._assess_subfile_from('t-city'),
                         '115-122.txt')
        self.assertRaises(ValueError, CityIDRegistry._assess_subfile_from,
                          self._instance, '123abc')
        self.assertRaises(ValueError, CityIDRegistry._assess_subfile_from,
                          self._instance, '{abc')

    def test_lookup_line_by_city_name(self):
        ref_to_original = CityIDRegistry._get_lines
        CityIDRegistry._get_lines = self._mock_get_lines
        expected = 'dongen,2756723,51.626671,4.938890,NL'
        result_1 = self._instance._lookup_line_by_city_name('dongen')
        result_2 = self._instance._lookup_line_by_city_name('aaaaaaaa')
        CityIDRegistry._get_lines = ref_to_original
        self.assertEqual(expected, result_1)
        self.assertTrue(result_2 is None)

    def test_id_for(self):
        ref_to_original = CityIDRegistry._get_lines
        CityIDRegistry._get_lines = self._mock_get_lines
        result_1 = self._instance.id_for('dongen')
        result_2 = self._instance.id_for('aaaaaaaaaa')
        CityIDRegistry._get_lines = ref_to_original
        self.assertEqual(result_1, 2756723)
        self.assertTrue(result_2 is None)

    def test_id_for_fails_with_malformed_inputs(self):
        self.assertRaises(ValueError, CityIDRegistry.id_for, self._instance,
                          '123abc')

    def test_location_for(self):
        ref_to_original = CityIDRegistry._get_lines
        CityIDRegistry._get_lines = self._mock_get_lines
        expected = Location('dongen', 4.938890, 51.626671, 2756723, 'NL')
        result_1 = self._instance.location_for('dongen')
        result_2 = self._instance.location_for('aaaaaaaaaa')
        CityIDRegistry._get_lines = ref_to_original        
        self.assertEqual(result_1.get_name(), expected.get_name())
        self.assertEqual(result_1.get_country(), expected.get_country())
        self.assertEqual(result_1.get_ID(), expected.get_ID())
        self.assertEqual(result_1.get_lat(), expected.get_lat())
        self.assertEqual(result_1.get_lon(), expected.get_lon())
        self.assertTrue(result_2 is None)

    def test_location_for_fails_with_malformed_inputs(self):
        self.assertRaises(ValueError, CityIDRegistry.location_for,
                          self._instance, '123abc')