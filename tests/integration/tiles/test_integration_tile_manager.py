import unittest
import os
from pyowm.constants import DEFAULT_API_KEY
from pyowm.weatherapi25.configuration25 import parsers
from pyowm.weatherapi25.owm25 import OWM25
from pyowm.tiles.enums import MapLayerEnum
from pyowm.commons.tile import Tile


class TesIntegrationTileManager(unittest.TestCase):

    __owm = OWM25(parsers, os.getenv('OWM_API_KEY', DEFAULT_API_KEY))

    def test_tiles_fetch(self):
        mgr = self.__owm.tile_manager(MapLayerEnum.PRECIPITATION)
        tile = mgr.get_tile(3, 6, 7)
        self.assertIsInstance(tile, Tile)


if __name__ == "__main__":
    unittest.main()

