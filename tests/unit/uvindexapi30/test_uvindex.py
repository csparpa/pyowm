#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from datetime import datetime
import pyowm.commons.exceptions
from pyowm.utils.formatting import UTC
from pyowm.uvindexapi30 import uvindex
from pyowm.weatherapi25.location import Location
from unittest.mock import patch


UVINDEX_JSON_DUMP = '{"reference_time": 1234567, "location": {"country": "UK", ' \
                   '"name": "test", "coordinates": {"lat": 43.7, "lon": 12.3}, ' \
                   '"ID": 987}, "value": 6.8, ' \
                    '"reception_time": 1475283600}'

UVINDEX_XML_DUMP = """<?xml version='1.0' encoding='utf8'?>
<uvindex xmlns:u="http://github.com/csparpa/pyowm/tree/master/pyowm/uvindexapi30/xsd/uvindex.xsd"><u:reception_time>1234567</u:reception_time><u:reference_time>1475283600</u:reference_time><u:value>6.8</u:value><u:location><u:name>test</u:name><u:coordinates><u:lon>12.3</u:lon><u:lat>43.7</u:lat></u:coordinates><u:ID>987</u:ID><u:country>UK</u:country></u:location></uvindex>"""

UVINDEX_JSON = '{"lat":43.75,"lon":8.25,"date_iso":"2016-09-27T12:00:00Z",' \
               '"date":1474977600,"value":4.58}'
UVINDEX_MALFORMED_JSON = '{"lat":43.75,"lon":8.25,"zzz":"2016-09-27T12:00:00Z",' \
               '"date":1474977600,"test":4.58}'


UVINDEX_LIST_JSON = '[{"lat":37.75,"lon":-122.37,"date_iso":"2017-06-22T12:00:00Z",' \
                    '"date":1498132800,"value":9.92},{"lat":37.75,"lon":-122.37,' \
                    '"date_iso":"2017-06-23T12:00:00Z","date":1498219200,' \
                    '"value":10.09},{"lat":37.75,"lon":-122.37,"date_iso":' \
                    '"2017-06-24T12:00:00Z","date":1498305600,"value":10.95},' \
                    '{"lat":37.75,"lon":-122.37,"date_iso":"2017-06-25T12:00:00Z",' \
                    '"date":1498392000,"value":11.03},{"lat":37.75,"lon":-122.37,' \
                    '"date_iso":"2017-06-26T12:00:00Z","date":1498478400,"value":10.06}]'


class TestUVIndex(unittest.TestCase):

    __test_reception_time = 1475283600
    __test_iso_reception_time = "2016-10-01 01:00:00+00"
    __test_date_reception_time = datetime.strptime(__test_iso_reception_time,
                               '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())

    __test_reference_time = 1234567
    __test_iso_reference_time = "1970-01-15 06:56:07+00"
    __test_date_reference_time = datetime.strptime(__test_iso_reference_time,
                               '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())

    __test_location = Location('test', 12.3, 43.7, 987, 'UK')
    __test_uv_intensity = 6.8
    __test_exposure_risk = 'high'
    __test_instance = uvindex.UVIndex(
        __test_reference_time, __test_location, __test_uv_intensity,
        __test_reception_time)

    def test_init_fails_when_reference_time_is_negative(self):
        self.assertRaises(ValueError, uvindex.UVIndex, -1234567,
                          self.__test_location,
                          self.__test_uv_intensity,
                          self.__test_reception_time)

    def test_init_fails_when_reception_time_is_negative(self):
        self.assertRaises(ValueError, uvindex.UVIndex,
                            self.__test_reference_time,
                            self.__test_location,
                            self.__test_uv_intensity,
                            -1234567)

    def test_init_fails_when_uv_intensity_is_negative(self):
        self.assertRaises(ValueError, uvindex.UVIndex, self.__test_reference_time,
                          self.__test_location, -8.9,
                          self.__test_reception_time)

    def test_returning_different_formats_for_reception_time(self):
        self.assertEqual(self.__test_instance.reception_time(timeformat='iso'), \
                         self.__test_iso_reception_time)
        self.assertEqual(self.__test_instance.reception_time(timeformat='unix'), \
                         self.__test_reception_time)
        self.assertEqual(self.__test_instance.reception_time(timeformat='date'), \
                         self.__test_date_reception_time)

    def test_returning_different_formats_for_reference_time(self):
        self.assertEqual(self.__test_instance.reference_time(timeformat='iso'), \
                         self.__test_iso_reference_time)
        self.assertEqual(self.__test_instance.reference_time(timeformat='unix'), \
                         self.__test_reference_time)
        self.assertEqual(self.__test_instance.reference_time(timeformat='date'), \
                         self.__test_date_reference_time)

    def test_uv_intensity_to_exposure_risk(self):
        self.assertEqual(uvindex.uv_intensity_to_exposure_risk(0.5), 'low')
        self.assertEqual(uvindex.uv_intensity_to_exposure_risk(3.5), 'moderate')
        self.assertEqual(uvindex.uv_intensity_to_exposure_risk(6.5), 'high')
        self.assertEqual(uvindex.uv_intensity_to_exposure_risk(8.5), 'very high')
        self.assertEqual(uvindex.uv_intensity_to_exposure_risk(30.5), 'extreme')

    def test_to_dict(self):
        expected = json.loads(UVINDEX_JSON_DUMP)
        result = self.__test_instance.to_dict()
        self.assertEqual(expected, result)

    def test_from_dict(self):
        result = uvindex.UVIndex.from_dict(json.loads(UVINDEX_JSON))
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.reference_time())
        self.assertIsNotNone(result.reception_time())
        loc = result.location
        self.assertIsNotNone(loc)
        self.assertIsNone(loc.name)
        self.assertIsNone(loc.id)
        self.assertIsNotNone(loc.lon)
        self.assertIsNotNone(loc.lat)
        self.assertIsNotNone(result.value)

    def test_from_dict_fails_when_JSON_data_is_None(self):
        self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError, uvindex.UVIndex.from_dict, None)

    def test_from_dict_fails_with_malformed_JSON_data(self):
        self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError,uvindex. UVIndex.from_dict,
                          json.loads(UVINDEX_MALFORMED_JSON))

    def test_get_exposure_risk(self):
        with patch.object(uvindex, 'uv_intensity_to_exposure_risk') as mock:
            self.__test_instance.get_exposure_risk()

        mock.assert_called_once_with(self.__test_uv_intensity)

    def test_repr(self):
        print(self.__test_instance)
