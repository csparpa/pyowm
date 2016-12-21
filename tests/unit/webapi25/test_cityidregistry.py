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
    _test_file_contents_with_homonymies = """Abasolo,3533505,24.066669,-98.366669,MX
Abasolo,4019867,25.950001,-100.400002,MX
Abasolo,4019869,20.450001,-101.51667,MX
Abbans-Dessus,3038800,47.120548,5.88188,FR
Abbans-Dessus,6452202,47.116669,5.88333,FR
Abbeville,3038789,50.099998,1.83333,FR
Abbeville,4178992,31.992121,-83.306824,US
Abbeville,4314295,29.974649,-92.134293,US
Abbeville,4568985,34.178169,-82.379013,US
Abbeville,4829449,31.57184,-85.250488,US
Bologna,2829449,30.57184,-83.250488,IT"""
    _test_file_contents_with_commas_in_names = """Thalassery,1254780,11.75,75.533333,IN
Thale, Stadt,6550950,51.7528,11.058,DE"""

    test_filelines = [
        'Londinieres,2997784,49.831871,1.40232,FR\n',
        'Londoko,2020707,49.033329,131.983337,RU\n',
        'London Borough of Harrow,7535661,51.566669,-0.33333,GB\n',
        'London Village,4030939,1.98487,-157.475021,KI\n',
        'London,2643743,51.50853,-0.12574,GB\n',
        'London,4119617,35.328972,-93.25296,US\n']

    # mocked functions and helpers

    def _mock_get_lines(self, filename):
        return StringIO(self._test_file_contents).readlines()

    def _mock_get_lines_with_homonymies(self, filename):
        return StringIO(self._test_file_contents_with_homonymies).readlines()

    def _mock_get_all_lines(self):
        return StringIO(self._test_file_contents_with_homonymies).readlines()

    def _mock_test_file_contents_with_commas_in_names(self, filename):
        return StringIO(self._test_file_contents_with_commas_in_names).readlines()

    def _assertLocationsEqual(self, loc1, loc2):
        self.assertEquals(loc1.get_ID(), loc2.get_ID())
        self.assertEquals(loc1.get_name(), loc2.get_name())
        self.assertEquals(loc1.get_lat(), loc2.get_lat())
        self.assertEquals(loc1.get_lon(), loc2.get_lon())
        self.assertEquals(loc1.get_country(), loc2.get_country())

    # tests for helper functions

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

    def test_city_name_matches(self):
        self.assertTrue(self._instance._city_name_matches(
            'test', 'test', 'exact'))
        self.assertFalse(self._instance._city_name_matches(
            'Test', 'test', 'exact'))
        self.assertFalse(self._instance._city_name_matches(
            'foo', 'bar', 'exact'))
        self.assertTrue(self._instance._city_name_matches(
            'tEsT mE', 'teST ME', 'nocase'))
        self.assertFalse(self._instance._city_name_matches(
            'foo', 'bar', 'nocase'))
        self.assertTrue(self._instance._city_name_matches(
            'test', 'test me', 'like'))
        self.assertFalse(self._instance._city_name_matches(
            'foo', 'bar', 'like'))

    # tests for IDs retrieval

    def test_id_for(self):
        ref_to_original = CityIDRegistry._get_lines
        CityIDRegistry._get_lines = self._mock_get_lines
        result_1 = self._instance.id_for('dongen')
        result_2 = self._instance.id_for('aaaaaaaaaa')
        CityIDRegistry._get_lines = ref_to_original
        self.assertEqual(result_1, 2756723)
        self.assertTrue(result_2 is None)

    def test_id_for_when_multiple_matches(self):
        ref_to_original = CityIDRegistry._get_lines
        CityIDRegistry._get_lines = self._mock_get_lines_with_homonymies
        result = self._instance.id_for('Abbeville')
        CityIDRegistry._get_lines = ref_to_original
        # only the ID of the first matching location name is returned
        self.assertEqual(result, 3038789)

    def test_id_for_fails_with_malformed_inputs(self):
        self.assertRaises(ValueError, CityIDRegistry.id_for, self._instance,
                          '123abc')

    def test_location_for(self):
        ref_to_original = CityIDRegistry._get_lines
        CityIDRegistry._get_lines = self._mock_get_lines
        expected = Location('dongdu', 117.699997, 35.849998, 1812597, 'CN')
        result_1 = self._instance.location_for('dongdu')
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

    def test_match_line(self):
        instance = CityIDRegistry('test')

        # no matches
        result = instance._match_line('blabla', self.test_filelines)
        self.assertIsNone(result)

        # single exact matches
        result = instance._match_line('Londoko', self.test_filelines)
        self.assertEqual('Londoko,2020707,49.033329,131.983337,RU', result)
        result = instance._match_line('London Borough of Harrow', self.test_filelines)
        self.assertEqual('London Borough of Harrow,7535661,51.566669,-0.33333,GB',
                         result)

        # single match with different casing
        result1 = instance._match_line('LONDOKO', self.test_filelines)
        result2 = instance._match_line('londoko', self.test_filelines)
        self.assertEquals(result1, result2)
        self.assertEqual('Londoko,2020707,49.033329,131.983337,RU', result1)
        result3 = instance._match_line('London borough of harrow', self.test_filelines)
        result4 = instance._match_line('london BOROUGH of Harrow', self.test_filelines)
        self.assertEquals(result3, result4)
        self.assertEquals('London Borough of Harrow,7535661,51.566669,-0.33333,GB',
                          result3)
        # homonymies
        result = instance._match_line('London', self.test_filelines)
        self.assertEquals('London,2643743,51.50853,-0.12574,GB', result)

    def test_ids_for(self):
        ref_to_original = CityIDRegistry._get_lines
        CityIDRegistry._get_lines = self._mock_get_lines_with_homonymies

        # No matches
        result = self._instance.ids_for('aaaaaaaaaa')
        self.assertEquals(0, len(result))

        # One match
        result = self._instance.ids_for("Bologna")
        self.assertEquals(1, len(result))
        self.assertEquals((2829449, 'Bologna', 'IT'), result[0])

        # Multiple matches
        result = self._instance.ids_for("Abbans-Dessus")
        self.assertEquals(2, len(result))
        self.assertTrue((3038800, 'Abbans-Dessus', 'FR') in result)
        self.assertTrue((6452202, 'Abbans-Dessus', 'FR') in result)

        CityIDRegistry._get_lines = ref_to_original

    def test_ids_for_with_wrong_input_values(self):
        self.assertRaises(ValueError,
                          CityIDRegistry.ids_for, self._instance,
                          "bologna", matching='xyz')
        self.assertRaises(ValueError,
                          CityIDRegistry.ids_for, self._instance,
                          "bologna", country='superlongcountry')

    def test_ids_for_matching_criteria(self):
        original_get_lines = CityIDRegistry._get_lines
        original_get_all_lines = CityIDRegistry._get_all_lines
        CityIDRegistry._get_lines = self._mock_get_lines_with_homonymies
        CityIDRegistry._get_all_lines = self._mock_get_all_lines

        # look for an empty name
        result = self._instance.ids_for("")
        self.assertEquals(0, len(result))

        # case sensitive
        result = self._instance.ids_for("bologna", matching='exact')
        self.assertEquals(0, len(result))

        result = self._instance.ids_for("Bologna", matching='exact')
        self.assertEquals(1, len(result))
        self.assertEquals((2829449, 'Bologna', 'IT'), result[0])

        # case insensitive
        result = self._instance.ids_for("bologna", matching='nocase')
        self.assertEquals(1, len(result))
        self.assertEquals((2829449, 'Bologna', 'IT'), result[0])

        result = self._instance.ids_for("Bologna", matching='nocase')
        self.assertEquals(1, len(result))
        self.assertEquals((2829449, 'Bologna', 'IT'), result[0])

        # like
        result = self._instance.ids_for("abbans", matching='like')
        self.assertEquals(2, len(result))
        self.assertTrue((3038800, 'Abbans-Dessus', 'FR') in result)
        self.assertTrue((6452202, 'Abbans-Dessus', 'FR') in result)

        result = self._instance.ids_for("Dessus", matching='like')
        self.assertEquals(2, len(result))
        self.assertTrue((3038800, 'Abbans-Dessus', 'FR') in result)
        self.assertTrue((6452202, 'Abbans-Dessus', 'FR') in result)

        CityIDRegistry._get_lines = original_get_lines
        CityIDRegistry._get_all_lines = original_get_all_lines

    def test_ids_for_restricted_to_country(self):
        ref_to_original = CityIDRegistry._get_lines
        CityIDRegistry._get_lines = self._mock_get_lines_with_homonymies

        result = self._instance.ids_for("Abbeville", country='JP')
        self.assertEquals(0, len(result))

        result = self._instance.ids_for("Abbeville", country='US')
        self.assertEquals(4, len(result))
        self.assertTrue((4178992, 'Abbeville', 'US') in result)
        self.assertTrue((4314295, 'Abbeville', 'US') in result)
        self.assertTrue((4568985, 'Abbeville', 'US') in result)
        self.assertTrue((4829449, 'Abbeville', 'US') in result)

        result = self._instance.ids_for("Abbeville", country='FR')
        self.assertEquals(1, len(result))
        self.assertTrue((3038789, 'Abbeville', 'FR') in result)

        CityIDRegistry._get_lines = ref_to_original

    def test_ids_for_with_commas_in_city_names(self):
        ref_to_original = CityIDRegistry._get_lines
        CityIDRegistry._get_lines = self._mock_test_file_contents_with_commas_in_names

        result = self._instance.ids_for("Thale, Stadt")
        self.assertEquals(1, len(result))
        self.assertTrue((6550950, 'Thale, Stadt', 'DE') in result)

        CityIDRegistry._get_lines = ref_to_original

    # tests for locations retrieval

    def test_locations_for(self):
        ref_to_original = CityIDRegistry._get_lines
        CityIDRegistry._get_lines = self._mock_get_lines_with_homonymies

        # No matches
        result = self._instance.locations_for('aaaaaaaaaa')
        self.assertEquals(0, len(result))

        # One match
        expected = Location('Bologna', -83.250488, 30.57184, 2829449, 'IT')
        result = self._instance.locations_for("Bologna")
        self.assertEquals(1, len(result))
        self._assertLocationsEqual(expected, result[0])

        # Multiple matches
        expected1 = Location('Abbans-Dessus', 5.88188, 47.120548, 3038800, 'FR')
        expected2 = Location('Abbans-Dessus', 5.88333, 47.116669, 6452202, 'FR')
        result = self._instance.locations_for("Abbans-Dessus")
        self.assertEquals(2, len(result))
        self._assertLocationsEqual(expected1, result[0])
        self._assertLocationsEqual(expected2, result[1])

        CityIDRegistry._get_lines = ref_to_original

    def test_locations_for_matching_criteria(self):
        original_get_lines = CityIDRegistry._get_lines
        original_get_all_lines = CityIDRegistry._get_all_lines
        CityIDRegistry._get_lines = self._mock_get_lines_with_homonymies
        CityIDRegistry._get_all_lines = self._mock_get_all_lines

        # look for an empty name
        result = self._instance.locations_for("")
        self.assertEquals(0, len(result))

        expected = Location('Bologna', -83.250488, 30.57184, 2829449, 'IT')

        # case sensitive
        result = self._instance.locations_for("bologna", matching='exact')
        self.assertEquals(0, len(result))

        result = self._instance.locations_for("Bologna", matching='exact')
        self.assertEquals(1, len(result))
        self._assertLocationsEqual(expected, result[0])

        # case insensitive
        result = self._instance.locations_for("bologna", matching='nocase')
        self.assertEquals(1, len(result))
        self._assertLocationsEqual(expected, result[0])

        result = self._instance.locations_for("Bologna", matching='nocase')
        self.assertEquals(1, len(result))
        self._assertLocationsEqual(expected, result[0])

        # like
        expected1 = Location('Abbans-Dessus', 5.88188, 47.120548, 3038800, 'FR')
        expected2 = Location('Abbans-Dessus', 5.88333, 47.116669, 6452202, 'FR')

        result = self._instance.locations_for("abbans", matching='like')
        self.assertEquals(2, len(result))
        self._assertLocationsEqual(expected1, result[0])
        self._assertLocationsEqual(expected2, result[1])

        result = self._instance.locations_for("Dessus", matching='like')
        self.assertEquals(2, len(result))
        self._assertLocationsEqual(expected1, result[0])
        self._assertLocationsEqual(expected2, result[1])

        CityIDRegistry._get_lines = original_get_lines
        CityIDRegistry._get_all_lines = original_get_all_lines

    def test_locations_for_restricted_to_country(self):
        ref_to_original = CityIDRegistry._get_lines
        CityIDRegistry._get_lines = self._mock_get_lines_with_homonymies

        result = self._instance.locations_for("Abbeville", country='JP')
        self.assertEquals(0, len(result))

        result = self._instance.locations_for("Abbeville", country='US')
        self.assertEquals(4, len(result))
        self._assertLocationsEqual(
            Location('Abbeville', -83.306824, 31.992121, 4178992, 'US'),
            result[0])
        self._assertLocationsEqual(
            Location('Abbeville', -92.134293, 29.974649, 4314295, 'US'),
            result[1])
        self._assertLocationsEqual(
            Location('Abbeville', -82.379013, 34.178169, 4568985, 'US'),
            result[2])
        self._assertLocationsEqual(
            Location('Abbeville', -85.250488, 31.57184, 4829449, 'US'),
            result[3])

        result = self._instance.locations_for("Abbeville", country='FR')
        self.assertEquals(1, len(result))
        self._assertLocationsEqual(
            Location("Abbeville", 1.83333, 50.099998, 3038789, 'FR'),
            result[0])

        CityIDRegistry._get_lines = ref_to_original

    def test_locations_for_with_commas_in_city_names(self):
        ref_to_original = CityIDRegistry._get_lines
        CityIDRegistry._get_lines = self._mock_test_file_contents_with_commas_in_names

        result = self._instance.locations_for("Thale, Stadt")
        self.assertEquals(1, len(result))
        self._assertLocationsEqual(
            Location('Thale, Stadt', 11.058, 51.7528, 6550950, 'DE'),
            result[0])

        CityIDRegistry._get_lines = ref_to_original