import unittest
from pyowm.tiles.tile_manager import TileManager
from pyowm.tiles.enums import MapLayerEnum


class TestTileManager(unittest.TestCase):

    def test_instantiation_fails_with_wrong_arguments(self):
        self.assertRaises(AssertionError, TileManager, None, MapLayerEnum.PRESSURE)
        self.assertRaises(AssertionError, TileManager, 'apikey', None)
        self.assertRaises(AssertionError, TileManager, 'apikey', 1234)
