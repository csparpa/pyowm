#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from pyowm import owm
from pyowm.agroapi10.polygon import GeoPolygon
from pyowm.agroapi10.enums import SatelliteEnum, PresetEnum
from pyowm.agroapi10.imagery import MetaImage


class IntegrationTestsSatelliteImageryStats(unittest.TestCase):

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
        cls.__polygon = mgr.create_polygon(geopol, 'stats_test_polygon')

    @classmethod
    def tearDownClass(cls):
        # delete the polygon
        mgr = cls.__owm.agro_manager()
        mgr.delete_polygon(cls.__polygon)

    def test_stats_for_satellite_image(self):
        mgr = self.__owm.agro_manager()

        # search all Landsat 8 images in the specified time frame and with high valid data percentage
        result_set = mgr.search_satellite_imagery(self.__polygon.id, self.__acquired_from, self.__acquired_to, None, None,
                                                  None, None, SatelliteEnum.LANDSAT_8.symbol, None, 0.5, 99.5, None)
        self.assertIsInstance(result_set, list)
        self.assertTrue(all([isinstance(i, MetaImage) and i.satellite_name == SatelliteEnum.LANDSAT_8.name for i in result_set]))

        # only keep EVI and NDVI ones
        ndvi_only = [mimg for mimg in result_set if mimg.preset == PresetEnum.NDVI]
        evi_only = [mimg for mimg in result_set if mimg.preset == PresetEnum.EVI]

        self.assertTrue(len(ndvi_only) > 1)
        self.assertTrue(len(evi_only) > 1)

        # now search for stats for both types
        stats_ndvi = mgr.stats_for_satellite_image(ndvi_only[0])
        stats_evi = mgr.stats_for_satellite_image(evi_only[0])
        self.assertIsInstance(stats_ndvi, dict)
        self.assertIsInstance(stats_evi, dict)

        # try to search for stats of a non NDVI or EVI image
        falsecolor_only = [mimg for mimg in result_set if mimg.preset == PresetEnum.FALSE_COLOR]
        with self.assertRaises(ValueError):
            mgr.stats_for_satellite_image(falsecolor_only[0])


if __name__ == "__main__":
    unittest.main()
