#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.commons.enums import ImageTypeEnum
from pyowm.commons.http_client import HttpClient
from pyowm.commons.image import Image
from pyowm.commons.tile import Tile
from pyowm.tiles.uris import ROOT_TILE_URL, NAMED_MAP_LAYER_URL


class TileManager:

    """
    A manager objects that reads OWM map layers tile images .

    :param API_key: the OWM Weather API key
    :type API_key: str
    :param map_layer: the layer for which you want tiles fetched. Allowed map layers are specified by
        the `pyowm.tiles.enum.MapLayerEnum` enumerator class.
    :type map_layer: str
    :param config: the configuration dictionary
    :type config: dict
    :returns: a *TileManager* instance
    :raises: *AssertionError* when no API Key or no map layer is provided, or map layer name is not a string

    """

    def __init__(self, API_key, map_layer, config):
        assert API_key is not None, 'You must provide a valid API Key'
        self.API_key = API_key
        assert map_layer is not None, 'You must provide a valid map layer name'
        assert isinstance(map_layer, str), 'Map layer name must be a string'
        self.map_layer = map_layer
        assert isinstance(config, dict)
        self.http_client = HttpClient(API_key, config, ROOT_TILE_URL, admits_subdomains=False)

    def get_tile(self, x, y, zoom):
        """
        Retrieves the tile having the specified coordinates and zoom level

        :param x: horizontal tile number in OWM tile reference system
        :type x: int
        :param y: vertical tile number in OWM tile reference system
        :type y: int
        :param zoom: zoom level for the tile
        :type zoom: int
        :returns: a `pyowm.tiles.Tile` instance

        """
        status, data = self.http_client.get_png(
            NAMED_MAP_LAYER_URL % self.map_layer + '/%s/%s/%s.png' % (zoom, x, y),
            params={'appid': self.API_key})
        img = Image(data, ImageTypeEnum.PNG)
        return Tile(x, y, zoom, self.map_layer, img)

    def __repr__(self):
        return "<%s.%s - layer_name=%s>" % (__name__, self.__class__.__name__, self.map_layer)
