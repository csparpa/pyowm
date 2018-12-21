import unittest
from pyowm.commons.http_client import HttpClient
from pyowm.tiles.tile_manager import TileManager
from pyowm.commons.tile import Tile
from pyowm.tiles.enums import MapLayerEnum


class MockHttpClientReturningTile(HttpClient):

    d = b'1234567890'

    def get_png(self, uri, params=None, headers=None):
        return 200, self.d


class TestTileManager(unittest.TestCase):

    def test_instantiation_fails_with_wrong_arguments(self):
        self.assertRaises(AssertionError, TileManager, None, MapLayerEnum.PRESSURE)
        self.assertRaises(AssertionError, TileManager, 'apikey', None)
        self.assertRaises(AssertionError, TileManager, 'apikey', 1234)

    def test_get_tile(self):
        mocked = MockHttpClientReturningTile()
        instance = TileManager('Api_key', 'a_layer')
        instance.http_client = mocked
        result = instance.get_tile(1, 2, 3)
        self.assertIsInstance(result, Tile)
        self.assertEqual(mocked.d, result.image.data)
