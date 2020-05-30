#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import uuid
from pyowm import owm
from pyowm.agroapi10.polygon import GeoPolygon
from pyowm.commons.enums import ImageTypeEnum
from pyowm.commons.image import Image
from pyowm.agroapi10.enums import SatelliteEnum, PresetEnum, PaletteEnum
from pyowm.agroapi10.imagery import MetaPNGImage, MetaTile, MetaGeoTiffImage, SatelliteImage


class IntegrationTestsSatelliteImageryDownload(unittest.TestCase):

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

    def test_download_png(self):
        mgr = self.__owm.agro_manager()

        # search PNG, truecolor, non-tile images acquired by Landsat 8
        result_set = mgr.search_satellite_imagery(self.__polygon.id, self.__acquired_from, self.__acquired_to,
                                                  ImageTypeEnum.PNG, PresetEnum.TRUE_COLOR, None, None,
                                                  SatelliteEnum.LANDSAT_8.symbol, None, None, None, None)
        self.assertIsInstance(result_set, list)
        self.assertEqual(len(result_set), 22)

        # just keep the non-tile images
        non_tile_pngs = [mimg for mimg in result_set if isinstance(mimg, MetaPNGImage)]
        self.assertEqual(len(non_tile_pngs), 11)

        # download one
        result = mgr.download_satellite_image(non_tile_pngs[0])

        self.assertIsInstance(result, SatelliteImage)
        self.assertIsInstance(result.metadata, MetaPNGImage)
        img = result.data
        self.assertIsInstance(img, Image)
        self.assertEqual(img.image_type, ImageTypeEnum.PNG)
        self.assertNotEqual(len(img.data), 0)

    def test_download_geotiff(self):
        mgr = self.__owm.agro_manager()

        # search GeoTiff, EVIimages acquired by Landsat 8
        result_set = mgr.search_satellite_imagery(self.__polygon.id, self.__acquired_from, self.__acquired_to,
                                                  ImageTypeEnum.GEOTIFF, PresetEnum.EVI, None, None,
                                                  SatelliteEnum.LANDSAT_8.symbol, None, None, None, None)
        self.assertIsInstance(result_set, list)
        self.assertEqual(len(result_set), 11)

        # download one
        result = mgr.download_satellite_image(result_set[0], palette=PaletteEnum.CONTRAST_SHIFTED)

        self.assertIsInstance(result, SatelliteImage)
        self.assertIsInstance(result.metadata, MetaGeoTiffImage)
        img = result.data
        self.assertIsInstance(img, Image)
        self.assertEqual(img.image_type, ImageTypeEnum.GEOTIFF)
        self.assertNotEqual(len(img.data), 0)

    def test_download_tile(self):
        mgr = self.__owm.agro_manager()

        # search PNG, truecolor, tile images acquired by Landsat 8
        result_set = mgr.search_satellite_imagery(self.__polygon.id, self.__acquired_from, self.__acquired_to,
                                                  ImageTypeEnum.PNG, PresetEnum.TRUE_COLOR, None, None,
                                                  SatelliteEnum.LANDSAT_8.symbol, None, None, None, None)
        self.assertIsInstance(result_set, list)
        self.assertEqual(len(result_set), 22)

        # just keep the tiles
        tile_pngs = [mimg for mimg in result_set if isinstance(mimg, MetaTile)]
        self.assertEqual(len(tile_pngs), 11)

        # try to download one without specifying x, y and zoom
        with self.assertRaises(AssertionError):
            mgr.download_satellite_image(tile_pngs[0])
        with self.assertRaises(AssertionError):
            mgr.download_satellite_image(tile_pngs[0], x=1)
        with self.assertRaises(AssertionError):
            mgr.download_satellite_image(tile_pngs[0], x=1, y=2)

        # download one
        result = mgr.download_satellite_image(tile_pngs[1], x=1, y=2, zoom=5)

        self.assertIsInstance(result, SatelliteImage)
        self.assertIsInstance(result.metadata, MetaTile)
        img = result.data
        self.assertIsInstance(img, Image)
        self.assertEqual(img.image_type, ImageTypeEnum.PNG)
        self.assertNotEqual(len(img.data), 0)

    def test_persisting_to_disk(self):
        path = '%s.tif' % uuid.uuid4()
        mgr = self.__owm.agro_manager()

        # search GeoTiff, EVIimages acquired by Landsat 8
        result_set = mgr.search_satellite_imagery(self.__polygon.id, self.__acquired_from, self.__acquired_to,
                                                  ImageTypeEnum.GEOTIFF, PresetEnum.EVI, None, None,
                                                  SatelliteEnum.LANDSAT_8.symbol, None, None, None, None)
        self.assertTrue(len(result_set) > 1)
        metaimg = result_set[0]
        sat_img = mgr.download_satellite_image(metaimg)
        try:
            self.assertFalse(os.path.isfile(path))
            sat_img.persist(path)
            self.assertTrue(os.path.isfile(path))
        except:
            self.fail()
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
