import unittest
import json
import copy
from pyowm.constants import AGRO_API_VERSION
from pyowm.commons.http_client import HttpClient
from pyowm.agroapi10.agro_manager import AgroManager
from pyowm.agroapi10.polygon import Polygon, GeoPolygon, GeoPoint
from pyowm.agroapi10.soil import Soil


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
