#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from pyowm.weatherapi25.owm25 import OWM25
from pyowm.tiles.enums import MapLayerEnum
from pyowm.commons.tile import Tile
from pyowm.config import DEFAULT_CONFIG


class TesIntegrationTileManager(unittest.TestCase):

    __owm = OWM25(os.getenv('OWM_API_KEY', DEFAULT_CONFIG['api_key']))

    def test_tiles_fetch(self):
        mgr = self.__owm.tile_manager(MapLayerEnum.PRECIPITATION)
        tile = mgr.get_tile(3, 6, 7)
        self.assertIsInstance(tile, Tile)


if __name__ == "__main__":
    unittest.main()

