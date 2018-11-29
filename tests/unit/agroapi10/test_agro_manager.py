import unittest
import json
import copy
from pyowm.constants import AGRO_API_VERSION
from pyowm.commons.http_client import HttpClient
from pyowm.commons.enums import ImageTypeEnum
from pyowm.commons.image import Image
from pyowm.commons.tile import Tile
from pyowm.agroapi10.agro_manager import AgroManager
from pyowm.agroapi10.polygon import Polygon, GeoPolygon, GeoPoint
from pyowm.agroapi10.soil import Soil
from pyowm.agroapi10.imagery import SatelliteImage, MetaPNGImage, MetaGeoTiffImage, MetaTile
from pyowm.agroapi10.enums import MetaImagePresetEnum, SatelliteNameEnum


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
        sm = AgroManager('APIKey')
        sm.http_client = _kls()
        return sm

    def test_instantiation_fails_without_api_key(self):
        self.assertRaises(AssertionError, AgroManager, None)

    def test_get_agro_api_version(self):
        instance = AgroManager('APIKey')
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
        result = instance.update_polygon(self.polygon)
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
        metaimg = MetaPNGImage('http://a.com', MetaImagePresetEnum.FALSE_COLOR,
                               SatelliteNameEnum.SENTINEL_2, 1378459200, 98.2, 0.3, 11.7, 7.89, 'a1b2c3d4')
        result = instance.download_satellite_image(metaimg)
        self.assertTrue(isinstance(result,SatelliteImage))
        self.assertTrue(isinstance(result.metadata, MetaPNGImage))
        self.assertTrue(isinstance(result.data, Image))
        self.assertTrue(result.data.image_type, ImageTypeEnum.PNG)

    def test_download_satellite_image_with_geotiff(self):
        instance = self.factory(MockHttpClientReturningImage)
        metaimg = MetaGeoTiffImage('http://a.com', MetaImagePresetEnum.FALSE_COLOR,
                                   SatelliteNameEnum.SENTINEL_2, 1378459200, 98.2, 0.3, 11.7, 7.89, 'a1b2c3d4')
        result = instance.download_satellite_image(metaimg)
        self.assertTrue(isinstance(result,SatelliteImage))
        self.assertTrue(isinstance(result.metadata, MetaGeoTiffImage))
        self.assertTrue(isinstance(result.data, Image))
        self.assertTrue(result.data.image_type, ImageTypeEnum.GEOTIFF)

    def test_download_satellite_image_with_tile_png_fails_without_tile_coords(self):
        instance = self.factory(MockHttpClientReturningImage)
        metaimg = MetaTile('http://a.com', MetaImagePresetEnum.FALSE_COLOR,
                           SatelliteNameEnum.SENTINEL_2, 1378459200, 98.2, 0.3, 11.7, 7.89, 'a1b2c3d4')
        with self.assertRaises(AssertionError):
            instance.download_satellite_image(metaimg)
        with self.assertRaises(AssertionError):
            instance.download_satellite_image(metaimg, x=1)
        with self.assertRaises(AssertionError):
            instance.download_satellite_image(metaimg, x=1, y=2)

    def test_download_satellite_image_with_tile_png(self):
        instance = self.factory(MockHttpClientReturningImage)
        metaimg = MetaTile('http://a.com', MetaImagePresetEnum.FALSE_COLOR,
                           SatelliteNameEnum.SENTINEL_2, 1378459200, 98.2, 0.3, 11.7, 7.89, 'a1b2c3d4')
        result = instance.download_satellite_image(metaimg, x=1, y=2, zoom=4)
        self.assertTrue(isinstance(result,SatelliteImage))
        self.assertTrue(isinstance(result.metadata, MetaTile))
        self.assertTrue(isinstance(result.data, Tile))
        self.assertTrue(result.data.image.image_type, ImageTypeEnum.PNG)
