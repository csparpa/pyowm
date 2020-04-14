import unittest
from pyowm.config import DEFAULT_CONFIG
from pyowm.commons.http_client import HttpClient
from pyowm.tiles.tile_manager import TileManager
from pyowm.commons.tile import Tile
from pyowm.tiles.enums import MapLayerEnum


class MockHttpClientReturningTile(HttpClient):

    d = b'1234567890'

    def get_png(self, uri, params=None, headers=None):
        return 200, self.d


class TestTileManager(unittest.TestCase):

    def test_instantiation_with_wrong_params(self):
        self.assertRaises(AssertionError, TileManager, None, MapLayerEnum.PRESSURE, dict())
        self.assertRaises(AssertionError, TileManager, 'apikey', None, dict())
        self.assertRaises(AssertionError, TileManager, 'apikey', MapLayerEnum.PRESSURE, None)

    def test_get_tile(self):
        mocked = MockHttpClientReturningTile('apikey', DEFAULT_CONFIG, 'anyurl.com')
        instance = TileManager('apikey', 'a_layer', DEFAULT_CONFIG)
        instance.http_client = mocked
        result = instance.get_tile(1, 2, 3)
        self.assertIsInstance(result, Tile)
        self.assertEqual(mocked.d, result.image.data)

    def test_repr(self):
        print(TileManager('apikey', 'a_layer', DEFAULT_CONFIG))
