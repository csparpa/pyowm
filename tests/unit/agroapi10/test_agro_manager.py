#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
import copy
from pyowm.config import DEFAULT_CONFIG
from pyowm.constants import AGRO_API_VERSION
from pyowm.commons.http_client import HttpClient
from pyowm.commons.enums import ImageTypeEnum
from pyowm.commons.image import Image
from pyowm.commons.tile import Tile
from pyowm.agroapi10.agro_manager import AgroManager
from pyowm.agroapi10.polygon import Polygon, GeoPolygon, GeoPoint
from pyowm.agroapi10.soil import Soil
from pyowm.agroapi10.imagery import SatelliteImage, MetaPNGImage, MetaGeoTiffImage, MetaTile
from pyowm.agroapi10.enums import PresetEnum, SatelliteEnum, PaletteEnum


class MockHttpClientPolygons(HttpClient):

    test_polygon_json = '''{
        "id":"5abb9fb82c8897000bde3e87",
        "geo_json":{
        "type":"Feature",
        "properties":{},
        "geometry":{
        "type":"Polygon",
        "coordinates":[
            [[-121.1958,37.6683],
            [-121.1779,37.6687],
            [-121.1773,37.6792],
            [-121.1958,37.6792],
            [-121.1958,37.6683]]
        ]}},
        "name":"Polygon Sample",
        "center":[-121.1867,37.6739],
        "area":190.6343,
        "user_id":"557066d0ee7b3e3897531d94"}'''

    def get_json(self, uri, params=None, headers=None):
        return 200, [json.loads(self.test_polygon_json)]


class MockHttpClientOnePolygon(HttpClient):
    test_polygon_json = '''{
        "id":"5abb9fb82c8897000bde3e87",
        "geo_json":{
        "type":"Feature",
        "properties":{},
        "geometry":{
        "type":"Polygon",
        "coordinates":[
            [[-121.1958,37.6683],
            [-121.1779,37.6687],
            [-121.1773,37.6792],
            [-121.1958,37.6792],
            [-121.1958,37.6683]]
        ]}},
        "name":"Polygon Sample",
        "center":[-121.1867,37.6739],
        "area":190.6343,
        "user_id":"557066d0ee7b3e3897531d94"}'''

    def get_json(self, uri, params=None, headers=None):
        return 200, json.loads(self.test_polygon_json)

    def post(self, uri, params=None, data=None, headers=None):
        return 200, json.loads(self.test_polygon_json)

    def put(self, uri, params=None, data=None, headers=None):
        return 200, self.test_polygon_json

    def delete(self, uri, params=None, data=None, headers=None):
        return 204, None


class MockHttpClientSoil(HttpClient):
    test_soil_json = '''{
       "dt":1522108800,
       "t10":281.96,
       "moisture":0.175,
       "t0":279.02}'''

    def get_json(self, uri, params=None, headers=None):
        return 200, json.loads(self.test_soil_json)


class MockHttpClientReturningImage(HttpClient):

    d = b'1234567890'

    def get_png(self, uri, params=None, headers=None):
        return 200, self.d

    def get_geotiff(self, uri, params=None, headers=None):
        return 200, self.d


class MockHttpClientStats(HttpClient):

    test_stats_json = '''{"std": 0.19696951630010479, "p25": 0.3090659340659341, "num": 57162, 
    "min": -0.2849250197316496, "max": 0.8658669574700109, "median": 0.45692992317131553, 
    "p75": 0.6432460461498574, "mean": 0.47631485576814037}'''

    def get_json(self, uri, params=None, headers=None):
        return 200, json.loads(self.test_stats_json)


class MockHttpClientImagerySearch(HttpClient):

    test_search_results_json = '''[{
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
       "evi":"http://api.agromonitoring.com/data/1.0/03259768a00/5ac22f004b1ae4000b5b97cf?appid=bb0664ed43c153aa072c760594d775a7"}}]'''

    def get_json(self, uri, params=None, headers=None):
        return 200, json.loads(self.test_search_results_json)


class TestAgroManager(unittest.TestCase):

    geopolygon = GeoPolygon([[
        [-121.1958, 37.6683],
        [-121.1779, 37.6687],
        [-121.1773, 37.6792],
        [-121.1958, 37.6792],
        [-121.1958, 37.6683]]])

    center = GeoPoint(-119.1779, 32.6687)

    polygon = Polygon('test-id', 'test-name', geopolygon, center=center, area=789.4, user_id='a-user')

    def factory(self, _kls):
        sm = AgroManager('APIKey', DEFAULT_CONFIG)
        sm.http_client = _kls('APIKey', DEFAULT_CONFIG, 'fake-root.com')
        return sm

    def test_instantiation_with_wrong_params(self):
        with self.assertRaises(AssertionError):
            AgroManager(None, dict())
        with self.assertRaises(AssertionError):
            AgroManager('apikey', None)

    def test_get_agro_api_version(self):
        instance = AgroManager('APIKey', DEFAULT_CONFIG)
        result = instance.agro_api_version()
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, AGRO_API_VERSION)

    # Test Polygons API subset

    def test_get_polygons(self):
        instance = self.factory(MockHttpClientPolygons)
        results = instance.get_polygons()
        self.assertEqual(1, len(results))
        p = results[0]
        self.assertIsInstance(p, Polygon)

    def test_get_polygon(self):
        instance = self.factory(MockHttpClientOnePolygon)
        result = instance.get_polygon('1234')
        self.assertIsInstance(result, Polygon)

    def test_create_polygon(self):
        instance = self.factory(MockHttpClientOnePolygon)
        result = instance.create_polygon(self.geopolygon, 'test name')
        self.assertIsInstance(result, Polygon)

        Polygon.name = None
        result = instance.create_polygon(self.geopolygon)
        self.assertIsInstance(result, Polygon)

    def test_create_polygons_fails_with_wrong_inputs(self):
        instance = self.factory(MockHttpClientOnePolygon)
        with self.assertRaises(AssertionError):
            instance.create_polygon(None, "test name")
        with self.assertRaises(AssertionError):
            instance.create_polygon(12345, "test name")

    def test_update_polygon(self):
        instance = self.factory(MockHttpClientOnePolygon)
        p = copy.deepcopy(self.polygon)
        p.name = 'a new name'
        result = instance.update_polygon(self.polygon)
        self.assertIsNone(result)
        p.id = None
        with self.assertRaises(AssertionError):
            instance.update_polygon(p)

    def test_delete_polygon(self):
        instance = self.factory(MockHttpClientOnePolygon)
        result = instance.delete_polygon(self.polygon)
        self.assertIsNone(result)
        p = copy.deepcopy(self.polygon)
        p.id = None
        with self.assertRaises(AssertionError):
            instance.delete_polygon(p)

    # Test Soil API subset

    def test_soil_data(self):
        instance = self.factory(MockHttpClientSoil)

        # failures
        with self.assertRaises(AssertionError):
            instance.soil_data(None)
        with self.assertRaises(AssertionError):
            instance.soil_data('not-a-polygon')

        # normal operativity
        result = instance.soil_data(self.polygon)
        self.assertIsInstance(result, Soil)
        self.assertEqual(self.polygon.id, result.polygon_id)

    # Test utilities
    def test_fill_url(self):
        instance = self.factory(MockHttpClientReturningImage)
        url_template = 'http://abc.com/{x}/{y}/{z}/json'
        expected = 'http://abc.com/1/2/3/json'
        result = instance._fill_url(url_template, 1, '2', 3)
        self.assertEqual(expected, result)

    # Test Satellite Imagery API subset

    def test_download_satellite_image_fails_with_wrong_metaimage_type(self):
        instance = self.factory(MockHttpClientReturningImage)
        with self.assertRaises(ValueError):
            instance.download_satellite_image("not-a-metaimage")

    def test_download_satellite_image_with_polygon_png(self):
        instance = self.factory(MockHttpClientReturningImage)
        metaimg = MetaPNGImage('http://a.com', PresetEnum.FALSE_COLOR,
                               SatelliteEnum.SENTINEL_2, 1378459200, 98.2, 0.3, 11.7, 7.89, 'a1b2c3d4')
        result = instance.download_satellite_image(metaimg, palette=PaletteEnum.BLACK_AND_WHITE)
        self.assertTrue(isinstance(result,SatelliteImage))
        self.assertTrue(isinstance(result.metadata, MetaPNGImage))
        self.assertTrue(isinstance(result.data, Image))
        self.assertEqual(result.data.image_type, ImageTypeEnum.PNG)
        self.assertEqual(result.palette, PaletteEnum.BLACK_AND_WHITE)

    def test_download_satellite_image_with_geotiff(self):
        instance = self.factory(MockHttpClientReturningImage)
        metaimg = MetaGeoTiffImage('http://a.com', PresetEnum.FALSE_COLOR,
                                   SatelliteEnum.SENTINEL_2.name, 1378459200, 98.2, 0.3, 11.7, 7.89, 'a1b2c3d4')
        result = instance.download_satellite_image(metaimg)
        self.assertTrue(isinstance(result,SatelliteImage))
        self.assertTrue(isinstance(result.metadata, MetaGeoTiffImage))
        self.assertTrue(isinstance(result.data, Image))
        self.assertEqual(result.data.image_type, ImageTypeEnum.GEOTIFF)
        self.assertEqual(result.palette, PaletteEnum.GREEN)

    def test_download_satellite_image_with_tile_png_fails_without_tile_coords(self):
        instance = self.factory(MockHttpClientReturningImage)
        metaimg = MetaTile('http://a.com', PresetEnum.FALSE_COLOR,
                           SatelliteEnum.SENTINEL_2.name, 1378459200, 98.2, 0.3, 11.7, 7.89, 'a1b2c3d4')
        with self.assertRaises(AssertionError):
            instance.download_satellite_image(metaimg)
        with self.assertRaises(AssertionError):
            instance.download_satellite_image(metaimg, x=1)
        with self.assertRaises(AssertionError):
            instance.download_satellite_image(metaimg, x=1, y=2)

    def test_download_satellite_image_with_tile_png(self):
        instance = self.factory(MockHttpClientReturningImage)
        metaimg = MetaTile('http://a.com', PresetEnum.FALSE_COLOR,
                           SatelliteEnum.SENTINEL_2.name, 1378459200, 98.2, 0.3, 11.7, 7.89, 'a1b2c3d4')
        result = instance.download_satellite_image(metaimg, x=1, y=2, zoom=4)
        self.assertTrue(isinstance(result,SatelliteImage))
        self.assertTrue(isinstance(result.metadata, MetaTile))
        self.assertTrue(isinstance(result.data, Tile))
        self.assertEqual(result.data.image.image_type, ImageTypeEnum.PNG)
        self.assertEqual(result.palette, PaletteEnum.GREEN)

    def test_stats_for_satellite_image_fails_with_wrong_arguments(self):
        instance = self.factory(MockHttpClientStats)
        with self.assertRaises(ValueError):
            metaimg = MetaTile('http://a.com', PresetEnum.FALSE_COLOR,
                               SatelliteEnum.SENTINEL_2.name, 1378459200, 98.2, 0.3, 11.7, 7.89, 'a1b2c3d4',
                               'http://b.com')
            instance.stats_for_satellite_image(metaimg)

        with self.assertRaises(ValueError):
            metaimg = MetaTile('http://a.com', PresetEnum.EVI,
                               SatelliteEnum.SENTINEL_2.name, 1378459200, 98.2, 0.3, 11.7, 7.89, 'a1b2c3d4',
                               None)
            instance.stats_for_satellite_image(metaimg)

    def test_stats_for_satellite_image(self):
        instance = self.factory(MockHttpClientStats)
        # stats retrieval currently only works for NDVI and EVI presets
        try:
            metaimg = MetaTile('http://a.com', PresetEnum.EVI,
                               SatelliteEnum.SENTINEL_2.name, 1378459200, 98.2, 0.3, 11.7, 7.89, 'a1b2c3d4',
                               'http://b.com')
            result = instance.stats_for_satellite_image(metaimg)
            self.assertIsInstance(result, dict)
        except:
            self.fail()
        try:
            metaimg = MetaTile('http://a.com', PresetEnum.NDVI,
                               SatelliteEnum.SENTINEL_2.name, 1378459200, 98.2, 0.3, 11.7, 7.89, 'a1b2c3d4',
                               'http://b.com')
            instance.stats_for_satellite_image(metaimg)
            self.assertIsInstance(result, dict)
        except:
            self.fail()

    def test_search_satellite_imagery_fails_with_wrong_arguments(self):
        instance = self.factory(MockHttpClientImagerySearch)
        self.assertRaises(AssertionError, instance.search_satellite_imagery,
                          None, 1480699083, 1480782083, ImageTypeEnum.PNG, PresetEnum.EVI, 10, 20,
                          SatelliteEnum.SENTINEL_2.symbol, 0, 10, 90, 100)
        self.assertRaises(AssertionError, instance.search_satellite_imagery,
                          'test_pol', None, 1480782083, ImageTypeEnum.PNG, PresetEnum.EVI, 10, 20,
                          SatelliteEnum.SENTINEL_2.symbol, 0, 10, 90, 100)
        self.assertRaises(AssertionError, instance.search_satellite_imagery,
                          'test_pol', 1480699083, None, ImageTypeEnum.PNG, PresetEnum.EVI, 10, 20,
                          SatelliteEnum.SENTINEL_2.symbol, 0, 10, 90, 100)
        self.assertRaises(AssertionError, instance.search_satellite_imagery,
                          'test_pol', 9999999, 1234, ImageTypeEnum.PNG, PresetEnum.EVI, 10, 20,
                          SatelliteEnum.SENTINEL_2.symbol, 0, 10, 90, 100)
        self.assertRaises(AssertionError, instance.search_satellite_imagery,
                          'test_pol', 1480699083, 1480782083, ImageTypeEnum.PNG, PresetEnum.EVI, -10, 20,
                          SatelliteEnum.SENTINEL_2.symbol, 0, 10, 90, 100)
        self.assertRaises(AssertionError, instance.search_satellite_imagery,
                          'test_pol', 1480699083, 1480782083, ImageTypeEnum.PNG, PresetEnum.EVI, 10, -20,
                          SatelliteEnum.SENTINEL_2.symbol, 0, 10, 90, 100)
        self.assertRaises(AssertionError, instance.search_satellite_imagery,
                          'test_pol', 1480699083, 1480782083, ImageTypeEnum.PNG, PresetEnum.EVI, 80, 20,
                          SatelliteEnum.SENTINEL_2.symbol, 0, 10, 90, 100)
        self.assertRaises(AssertionError, instance.search_satellite_imagery,
                          'test_pol', 1480699083, 1480782083, ImageTypeEnum.PNG, PresetEnum.EVI, 10, 20,
                          SatelliteEnum.SENTINEL_2.symbol, -10, 10, 90, 100)
        self.assertRaises(AssertionError, instance.search_satellite_imagery,
                          'test_pol', 1480699083, 1480782083, ImageTypeEnum.PNG, PresetEnum.EVI, 10, 20,
                          SatelliteEnum.SENTINEL_2.symbol, 0, -10, 90, 100)
        self.assertRaises(AssertionError, instance.search_satellite_imagery,
                          'test_pol', 1480699083, 1480782083, ImageTypeEnum.PNG, PresetEnum.EVI, 10, 20,
                          SatelliteEnum.SENTINEL_2.symbol, 90, 10, 90, 100)
        self.assertRaises(AssertionError, instance.search_satellite_imagery,
                          'test_pol', 1480699083, 1480782083, ImageTypeEnum.PNG, PresetEnum.EVI, 10, 20,
                          SatelliteEnum.SENTINEL_2.symbol, 0, 10, -90, 100)
        self.assertRaises(AssertionError, instance.search_satellite_imagery,
                          'test_pol', 1480699083, 1480782083, ImageTypeEnum.PNG, PresetEnum.EVI, 10, 20,
                          SatelliteEnum.SENTINEL_2.symbol, 0, 10, 90, -100)
        self.assertRaises(AssertionError, instance.search_satellite_imagery,
                          'test_pol', 1480699083, 1480782083, ImageTypeEnum.PNG, PresetEnum.EVI, 10, 20,
                          SatelliteEnum.SENTINEL_2.symbol, 0, 10, 100, 20)

        try:
            instance.search_satellite_imagery('test_pol', 1480699083, 1480782083, ImageTypeEnum.PNG,
                                              PresetEnum.EVI, 10, 20, SatelliteEnum.SENTINEL_2.symbol, 0, 10, 90, 100)
            instance.search_satellite_imagery('test_pol', 1480699083, 1480782083)
        except:
            self.fail()

    def test_search_satellite_imagery(self):
        instance = self.factory(MockHttpClientImagerySearch)

        # all images available for the polygon
        results = instance.search_satellite_imagery('test_pol', 1480699083, 1480782083)
        self.assertEqual(12, len(results))

        # all Landsat 8 images available for the polygon
        results = instance.search_satellite_imagery('test_pol', 1480699083, 1480782083, None, None, None, None,
                                                    SatelliteEnum.LANDSAT_8.symbol)
        self.assertEqual(12, len(results))

        # all Sentinel2 EVI PNG images available for the polygon, 10 < px/m < 20, cloud coverage < 10%, data doverage > 90 %
        results = instance.search_satellite_imagery('test_pol', 1480699083, 1480782083, ImageTypeEnum.PNG,
                                                    PresetEnum.EVI, 10, 20, SatelliteEnum.SENTINEL_2.symbol, 0,
                                                    10, 90, 100)
        self.assertEqual(2, len(results))
        self.assertTrue(all([i.image_type == ImageTypeEnum.PNG and i.preset == PresetEnum.EVI for i in results]))

        # all Sentinel2 EVI images available for the polygon, 10 < px/m < 20, cloud coverage < 10%, data doverage > 90 %
        results = instance.search_satellite_imagery('test_pol', 1480699083, 1480782083, None,
                                                    PresetEnum.EVI, 10, 20, SatelliteEnum.SENTINEL_2.symbol, 0,
                                                    10, 90, 100)
        self.assertEqual(3, len(results))
        self.assertTrue(all([i.preset == PresetEnum.EVI for i in results]))

        results = instance.search_satellite_imagery('test_pol', 1480699083, 1480782083, ImageTypeEnum.PNG,
                                                    None, 10, 20, SatelliteEnum.SENTINEL_2.symbol, 0,
                                                    10, 90, 100)
        self.assertEqual(8, len(results))

    def test_repr(self):
        print(AgroManager('APIKey', DEFAULT_CONFIG))
