#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from pyowm import owm
from pyowm.tiles.enums import MapLayerEnum
from pyowm.commons.tile import Tile


class TesIntegrationTileManager(unittest.TestCase):

    __owm = owm.OWM(os.getenv('OWM_API_KEY', None))

    def test_tiles_fetch(self):
        mgr = self.__owm.tile_manager(MapLayerEnum.PRECIPITATION)
        tile = mgr.get_tile(3, 6, 7)
        self.assertIsInstance(tile, Tile)


if __name__ == "__main__":
    unittest.main()

