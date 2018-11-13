"""
Programmatic interface to OWM Agro API endpoints
"""

from pyowm.commons.http_client import HttpClient
from pyowm.constants import AGRO_API_VERSION


class AgroManager(object):

    """
    A manager objects that provides a full interface to OWM Agro API.

    :param API_key: the OWM Weather API key
    :type API_key: str
    :returns: an `AgroManager` instance
    :raises: `AssertionError` when no API Key is provided

    """

    def __init__(self, API_key):
        assert API_key is not None, 'You must provide a valid API Key'
        self.API_key = API_key
        self.http_client = HttpClient()

    def agro_api_version(self):
        return AGRO_API_VERSION

    def create_polygon(self):
        raise NotImplementedError()

    def get_polygons(self):
        raise NotImplementedError()

    def get_polygon(self, polygon_id):
        raise NotImplementedError()

    def update_polygon(self, polygon):
        raise NotImplementedError()

    def delete_polygon(self, polygon):
        raise NotImplementedError()
