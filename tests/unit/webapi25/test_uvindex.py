"""
Test case for uvindex.py module
"""

import unittest
from datetime import datetime
from pyowm.webapi25.location import Location
from pyowm.webapi25.uvindex import UVIndex, uv_intensity_to_exposure_risk
from pyowm.utils.timeformatutils import UTC, _datetime_to_UNIXtime
from tests.unit.webapi25.json_test_dumps import UVINDEX_JSON_DUMP
from tests.unit.webapi25.xml_test_dumps import UVINDEX_XML_DUMP


class TestUVIndex(unittest.TestCase):

    __test_reception_time = 1234567
    __test_iso_reception_time = "1970-01-15 06:56:07+00"
    __test_date_reception_time = datetime.strptime(__test_iso_reception_time,
                               '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
    __test_location = Location('test', 12.3, 43.7, 987, 'UK')
    __test_uv_intensity = 6.8
    __test_exposure_risk = 'high'
    __test_instance = UVIndex(
        __test_reception_time, __test_location, __test_uv_intensity)

    def test_init_fails_when_reception_time_is_negative(self):
        self.assertRaises(ValueError, UVIndex, -1234567,
                          self.__test_location, self.__test_uv_intensity)

    def test_init_fails_when_uv_intensity_is_negative(self):
        self.assertRaises(ValueError, UVIndex, self.__test_reception_time,
                          self.__test_location, -8.9)

    def test_getters_return_expected_data(self):
        self.assertEqual(self.__test_instance.get_reception_time(),
                         self.__test_reception_time)
        self.assertEqual(self.__test_instance.get_location(),
                         self.__test_location)
        self.assertEqual(self.__test_instance.get_value(),
                         self.__test_uv_intensity)
        self.assertEqual(self.__test_instance.get_exposure_risk(),
                         self.__test_exposure_risk)

    def test_returning_different_formats_for_reception_time(self):
        self.assertEqual(self.__test_instance.get_reception_time(timeformat='iso'), \
                         self.__test_iso_reception_time)
        self.assertEqual(self.__test_instance.get_reception_time(timeformat='unix'), \
                         self.__test_reception_time)
        self.assertEqual(self.__test_instance.get_reception_time(timeformat='date'), \
                         self.__test_date_reception_time)

    def test_is_forecast(self):
        self.assertFalse(self.__test_instance.is_forecast())
        in_a_year = _datetime_to_UNIXtime(datetime.utcnow()) + 31536000
        uvindex = UVIndex(in_a_year,
                          self.__test_location,
                          self.__test_uv_intensity)
        self.assertTrue(uvindex.is_forecast())

    def test_uv_intensity_to_exposure_risk(self):
        self.assertEqual(uv_intensity_to_exposure_risk(0.5), 'low')
        self.assertEqual(uv_intensity_to_exposure_risk(3.5), 'moderate')
        self.assertEqual(uv_intensity_to_exposure_risk(6.5), 'high')
        self.assertEqual(uv_intensity_to_exposure_risk(8.5), 'very high')
        self.assertEqual(uv_intensity_to_exposure_risk(30.5), 'extreme')

    # Test JSON and XML comparisons by ordering strings (this overcomes
    # interpeter-dependant serialization of XML/JSON objects)

    def test_to_JSON(self):
        ordered_base_json = ''.join(sorted(UVINDEX_JSON_DUMP))
        ordered_actual_json = ''.join(sorted(self.__test_instance.to_JSON()))
        self.assertEqual(ordered_base_json, ordered_actual_json)

    def test_to_XML(self):
        ordered_base_xml = ''.join(sorted(UVINDEX_XML_DUMP))
        ordered_actual_xml = ''.join(sorted(self.__test_instance.to_XML()))
        self.assertEqual(ordered_base_xml, ordered_actual_xml)