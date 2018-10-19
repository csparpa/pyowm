"""
Object that can download tile images at various zoom levels
"""

from pyowm.commons.http_client import HttpClient
from pyowm.tiles.uris import ROOT_TILE_URL


class TileManager(object):

    """
    A manager objects that reads OWM map layers tile images .

    :param API_key: the OWM Weather API key
    :type API_key: str
    :param map_layer: the layer for which you want tiles fetced. Allowed map layers are specified by the
    `pyowm.tiles.enum.MapLayerEnum` enumerator class.
    :type map_layer: str
    :returns: a *TileManager* instance
    :raises: *AssertionError* when no API Key or no map layer is provided, or map layer name is not a string

    """

    def __init__(self, API_key, map_layer):
        assert API_key is not None, 'You must provide a valid API Key'
        self.API_key = API_key
        assert map_layer is not None, 'You must provide a valid map layer name'
        assert isinstance(map_layer, str), 'Map layer name must be a string'
        self.map_layer = map_layer
        self.http_client = HttpClient()

    def get_tile(self, x, y, zoom):
        raise NotImplementedError()
