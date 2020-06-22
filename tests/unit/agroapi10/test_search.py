#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
from datetime import datetime
from pyowm.commons.enums import ImageTypeEnum
from pyowm.agroapi10.search import SatelliteImagerySearchResultSet
from pyowm.agroapi10.enums import PresetEnum


class TestSatelliteImagerySearchResultSet(unittest.TestCase):

    test_data = json.loads('''[{
    "dt":1500940800,
    "type":"Landsat 8",
    "dc":100,
    "cl":1.56,
    "sun":{  
       "azimuth":126.742,
       "elevation":63.572},
    "image":{  
       "truecolor":"http://api.agromonitoring.com/image/1.0/00059768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7",
       "falsecolor":"http://api.agromonitoring.com/image/1.0/01059768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7",
       "ndvi":"http://api.agromonitoring.com/image/1.0/02059768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7",
       "evi":"http://api.agromonitoring.com/image/1.0/03059768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7"},
    "tile":{  
       "truecolor":"http://api.agromonitoring.com/tile/1.0/{z}/{x}/{y}/00059768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7",
       "falsecolor":"http://api.agromonitoring.com/tile/1.0/{z}/{x}/{y}/01059768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7",
       "ndvi":"http://api.agromonitoring.com/tile/1.0/{z}/{x}/{y}/02059768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7",
       "evi":"http://api.agromonitoring.com/tile/1.0/{z}/{x}/{y}/03059768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7"},
    "stats":{  
       "ndvi":"http://api.agromonitoring.com/stats/1.0/02359768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7",
       "evi":"http://api.agromonitoring.com/stats/1.0/03359768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7"},
    "data":{  
       "truecolor":"http://api.agromonitoring.com/data/1.0/00159768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7",
       "falsecolor":"http://api.agromonitoring.com/data/1.0/01159768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7",
       "ndvi":"http://api.agromonitoring.com/data/1.0/02259768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7",
       "evi":"http://api.agromonitoring.com/data/1.0/03259768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7"}}]''')
    test_issuing_time = 1378459200
    test_iso_issuing_time = "2013-09-06 09:20:00+00:00"
    test_date_issuing_time = datetime.fromisoformat(test_iso_issuing_time)

    test_instance = SatelliteImagerySearchResultSet('my_polygon', test_data, test_issuing_time)

    def test_instantiation_fails_with_wrong_arguments(self):
        self.assertRaises(AssertionError, SatelliteImagerySearchResultSet, None, [], 1234567)
        self.assertRaises(AssertionError, SatelliteImagerySearchResultSet, 'my_polygon', None, 1234567)
        self.assertRaises(AssertionError, SatelliteImagerySearchResultSet, 'my_polygon', [], None)

    def test_instantiation(self):
        self.assertEqual(12, self.test_instance.__len__())
        self.assertTrue(all([mi.stats_url is not None for mi in self.test_instance.metaimages if mi.preset in
                             [PresetEnum.EVI, PresetEnum.NDVI]]))

    def test_empty_metaimages_init(self):
        test_data = self.test_data[0]
        for dictionary in ['image', 'stats', 'tile', 'data']:
            for key in test_data[dictionary].keys():
                test_data[dictionary][key] = None

        test_data = [test_data]
        test_instance = SatelliteImagerySearchResultSet('my_polygon', test_data, self.test_issuing_time)
        self.assertFalse(len(test_instance.metaimages))

    def test_issued_on_returning_different_formats(self):
        self.assertEqual(self.test_instance.issued_on(timeformat='unix'),
                         self.test_issuing_time)
        self.assertEqual(self.test_instance.issued_on(timeformat='iso'),
                         self.test_iso_issuing_time)
        self.assertEqual(self.test_instance.issued_on(timeformat='date'),
                         self.test_date_issuing_time)

    def test_issued_on_fails_with_unknown_timeformat(self):
        self.assertRaises(ValueError, SatelliteImagerySearchResultSet.issued_on, self.test_instance, 'xyz')

    def test_all(self):
        result = self.test_instance.all()
        self.assertEqual(result, self.test_instance.metaimages)

    def test_with_img_type(self):
        # failure
        with self.assertRaises(AssertionError):
            self.test_instance.with_img_type(1234)

        # success
        result = self.test_instance.with_img_type(ImageTypeEnum.PNG)
        self.assertEqual(8, len(result))
        result = self.test_instance.with_img_type(ImageTypeEnum.GEOTIFF)
        self.assertEqual(4, len(result))

    def test_with_preset(self):
        # failure
        with self.assertRaises(AssertionError):
            self.test_instance.with_preset(1234)

        # success
        result = self.test_instance.with_preset(PresetEnum.TRUE_COLOR)
        self.assertEqual(3, len(result))
        result = self.test_instance.with_preset(PresetEnum.FALSE_COLOR)
        self.assertEqual(3, len(result))
        result = self.test_instance.with_preset(PresetEnum.NDVI)
        self.assertEqual(3, len(result))
        result = self.test_instance.with_preset(PresetEnum.EVI)
        self.assertEqual(3, len(result))

    def test_with_img_type_and_preset(self):
        # failure
        with self.assertRaises(AssertionError):
            self.test_instance.with_img_type_and_preset(1234, 1234)
        with self.assertRaises(AssertionError):
            self.test_instance.with_img_type_and_preset(1234, PresetEnum.TRUE_COLOR)
        with self.assertRaises(AssertionError):
            self.test_instance.with_img_type_and_preset(ImageTypeEnum.PNG, 1234)

        # success
        result = self.test_instance.with_img_type_and_preset(ImageTypeEnum.PNG, PresetEnum.TRUE_COLOR)
        self.assertEqual(2, len(result))
        result = self.test_instance.with_img_type_and_preset(ImageTypeEnum.GEOTIFF, PresetEnum.EVI)
        self.assertEqual(1, len(result))
        result = self.test_instance.with_img_type_and_preset(ImageTypeEnum.GEOTIFF, PresetEnum.FALSE_COLOR)
        self.assertEqual(1, len(result))

    def test_repr(self):
        self.assertEqual('<pyowm.agroapi10.search.SatelliteImagerySearchResultSet'
                ' - 12 results for query issued on polygon_id=my_polygon at 2013-09-06 09:20:00+00:00>',
                         self.test_instance.__repr__())
