#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from pyowm import owm
from pyowm.agroapi10.polygon import GeoPolygon
from pyowm.commons.enums import ImageTypeEnum
from pyowm.agroapi10.enums import SatelliteEnum, PresetEnum
from pyowm.agroapi10.imagery import MetaImage


class IntegrationTestsSatelliteImagerySearch(unittest.TestCase):

    __owm = owm.OWM(os.getenv('OWM_API_KEY', None))
    __polygon = None
    __acquired_from = 1500336000  # 18 July 2017
    __acquired_to = 1508976000  # 26 October 2017

    @classmethod
    def setUpClass(cls):
        # create a polygon
        mgr = cls.__owm.agro_manager()
        geopol = GeoPolygon([[
            [-121.1958, 37.6683],
            [-121.1779, 37.6687],
            [-121.1773, 37.6792],
            [-121.1958, 37.6792],
            [-121.1958, 37.6683]
        ]])
        cls.__polygon = mgr.create_polygon(geopol, 'search_test_polygon')

    @classmethod
    def tearDownClass(cls):
        # delete the polygon
        mgr = cls.__owm.agro_manager()
        mgr.delete_polygon(cls.__polygon)

    # Test methods

    def test_search_all(self):
        mgr = self.__owm.agro_manager()

        # search all images in the specified time frame
        result_set = mgr.search_satellite_imagery(self.__polygon.id, self.__acquired_from, self.__acquired_to)
        self.assertIsInstance(result_set, list)
        self.assertEqual(len(result_set), 360)
        self.assertTrue(all([isinstance(i, MetaImage) for i in result_set]))

    def test_search_for_one_satellite(self):
        mgr = self.__owm.agro_manager()

        # search all Landsat 8 images in the specified time frame
        result_set = mgr.search_satellite_imagery(self.__polygon.id, self.__acquired_from, self.__acquired_to, None,
                                                  None, None, None, SatelliteEnum.LANDSAT_8.symbol, None, None, None, None)
        self.assertIsInstance(result_set, list)
        self.assertEqual(len(result_set), 132)
        self.assertTrue(all([isinstance(i, MetaImage) and i.satellite_name == SatelliteEnum.LANDSAT_8.name for i in result_set]))

    def test_search_for_geotiff_type_only(self):
        mgr = self.__owm.agro_manager()

        # search all geotiff images in the specified time frame
        result_set = mgr.search_satellite_imagery(self.__polygon.id, self.__acquired_from, self.__acquired_to,
                                                  ImageTypeEnum.GEOTIFF, None, None, None, None, None, None, None, None)
        self.assertIsInstance(result_set, list)
        self.assertEqual(len(result_set), 120)
        self.assertTrue(all([isinstance(i, MetaImage) and i.image_type == ImageTypeEnum.GEOTIFF for i in result_set]))

    def test_search_for_ndvi_preset_only(self):
        mgr = self.__owm.agro_manager()

        # search all NDVI images in the specified time frame
        result_set = mgr.search_satellite_imagery(self.__polygon.id, self.__acquired_from, self.__acquired_to,
                                                  None, PresetEnum.NDVI, None, None, None, None, None, None, None)
        self.assertIsInstance(result_set, list)
        self.assertEqual(len(result_set), 90)
        self.assertTrue(all([isinstance(i, MetaImage) and i.preset == PresetEnum.NDVI for i in result_set]))

    def test_search_for_falsecolor_png_only(self):
        mgr = self.__owm.agro_manager()

        # search all PNG images in falsecolor in the specified time frame
        result_set = mgr.search_satellite_imagery(self.__polygon.id, self.__acquired_from, self.__acquired_to, ImageTypeEnum.PNG,
                                                  PresetEnum.FALSE_COLOR, None, None, None, None, None, None, None)
        self.assertIsInstance(result_set, list)
        self.assertEqual(len(result_set), 60)
        self.assertTrue(all([isinstance(i, MetaImage) and i.preset == PresetEnum.FALSE_COLOR and
                             i.image_type == ImageTypeEnum.PNG for i in result_set]))

    def test_detailed_search(self):
        mgr = self.__owm.agro_manager()

        # in the specified time frame, search all PNG images in truecolor acquired by Sentinel 2
        # and with a max cloud coverage of 5% and at least 90% of valid data coverage
        result_set = mgr.search_satellite_imagery(self.__polygon.id, self.__acquired_from, self.__acquired_to, ImageTypeEnum.PNG,
                                                  PresetEnum.TRUE_COLOR, None, None, SatelliteEnum.SENTINEL_2.symbol,
                                                  None, 5, 90, None)
        self.assertIsInstance(result_set, list)
        self.assertEqual(len(result_set), 30)
        self.assertTrue(all([isinstance(i, MetaImage) and
                             i.preset == PresetEnum.TRUE_COLOR and
                             i.image_type == ImageTypeEnum.PNG and
                             i.satellite_name == SatelliteEnum.SENTINEL_2.name and
                             i.cloud_coverage_percentage <= 5 and
                             i.valid_data_percentage >= 90 for i in result_set]))


if __name__ == "__main__":
    unittest.main()
