import unittest
from pyowm.tiles.tile import Tile
from pyowm.utils.geo import Polygon
from pyowm.commons.image import Image


class TestTile(unittest.TestCase):

    def test_instantiation_fails_with_wrong_arguments(self):
        i = Image(b'x/1')
        self.assertRaises(AssertionError, Tile, -1, 2, 3, 'layer', i)
        self.assertRaises(AssertionError, Tile, 1, -2, 3, 'layer', i)
        self.assertRaises(AssertionError, Tile, 1, 2, -3, 'layer', i)
        self.assertRaises(AssertionError, Tile, 1, 2, 3, 'layer', 'not-an-image')

    def test_bounding_box(self):
        instance = Tile(0, 0, 18, 'temperature', Image(b'x/1'))
        result = instance.bounding_polygon()
        self.assertIsInstance(result, Polygon)
        print(result.geojson())