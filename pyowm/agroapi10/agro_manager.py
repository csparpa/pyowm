"""
Programmatic interface to OWM Agro API endpoints
"""

from pyowm.constants import AGRO_API_VERSION
from pyowm.commons.http_client import HttpClient
from pyowm.commons.image import Image
from pyowm.commons.tile import Tile
from pyowm.agroapi10.uris import POLYGONS_URI, NAMED_POLYGON_URI, SOIL_URI
from pyowm.agroapi10.enums import MetaImagePresetEnum
from pyowm.agroapi10.polygon import Polygon, GeoPolygon
from pyowm.agroapi10.soil import Soil
from pyowm.agroapi10.imagery import MetaTile, MetaGeoTiffImage, MetaPNGImage, SatelliteImage


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

    # POLYGON API subset methods

    def create_polygon(self, geopolygon, name=None):
        """
        Create a new polygon on the Agro API with the given parameters

        :param geopolygon: the geopolygon representing the new polygon
        :type geopolygon: `pyowm.utils.geo.Polygon` instance
        :param name: optional mnemonic name for the new polygon
        :type name: str
        :return: a `pyowm.agro10.polygon.Polygon` instance
        """
        assert geopolygon is not None
        assert isinstance(geopolygon, GeoPolygon)
        data = dict()
        data['geo_json'] = {
            "type": "Feature",
            "properties": {},
            "geometry": geopolygon.as_dict()
        }
        if name is not None:
            data['name'] = name
        status, payload = self.http_client.post(
            POLYGONS_URI,
            params={'appid': self.API_key},
            data=data,
            headers={'Content-Type': 'application/json'})
        return Polygon.from_dict(payload)

    def get_polygons(self):
        """
        Retrieves all of the user's polygons registered on the Agro API.

        :returns: list of `pyowm.agro10.polygon.Polygon` objects

        """

        status, data = self.http_client.get_json(
            POLYGONS_URI,
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})
        return [Polygon.from_dict(item) for item in data]

    def get_polygon(self, polygon_id):
        """
        Retrieves a named polygon registered on the Agro API.

        :param id: the ID of the polygon
        :type id: str
        :returns: a `pyowm.agro10.polygon.Polygon` object

        """
        status, data = self.http_client.get_json(
            NAMED_POLYGON_URI % str(polygon_id),
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})
        return Polygon.from_dict(data)

    def update_polygon(self, polygon):
        """
        Updates on the Agro API the Polygon identified by the ID of the provided polygon object.
        Currently this only changes the mnemonic name of the remote polygon

        :param polygon: the `pyowm.agro10.polygon.Polygon` object to be updated
        :type polygon: `pyowm.agro10.polygon.Polygon` instance
        :returns: `None` if update is successful, an exception otherwise
        """
        assert polygon.id is not None
        status, _ = self.http_client.put(
            NAMED_POLYGON_URI % str(polygon.id),
            params={'appid': self.API_key},
            data=dict(name=polygon.name),
            headers={'Content-Type': 'application/json'})

    def delete_polygon(self, polygon):
        """
        Deletes on the Agro API the Polygon identified by the ID of the provided polygon object.

        :param polygon: the `pyowm.agro10.polygon.Polygon` object to be deleted
        :type polygon: `pyowm.agro10.polygon.Polygon` instance
        :returns: `None` if deletion is successful, an exception otherwise
        """
        assert polygon.id is not None
        status, _ = self.http_client.delete(
            NAMED_POLYGON_URI % str(polygon.id),
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})

    # SOIL API subset methods

    def soil_data(self, polygon):
        """
        Retrieves the latest soil data on the specified polygon

        :param polygon: the reference polygon you want soil data for
        :type polygon: `pyowm.agro10.polygon.Polygon` instance
        :returns: a `pyowm.agro10.soil.Soil` instance

        """
        assert polygon is not None
        assert isinstance(polygon, Polygon)
        polyd = polygon.id
        status, data = self.http_client.get_json(
            SOIL_URI,
            params={'appid': self.API_key,
                    'polyid': polyd},
            headers={'Content-Type': 'application/json'})
        the_dict = dict()
        the_dict['reference_time'] = data['dt']
        the_dict['surface_temp'] = data['t0']
        the_dict['ten_cm_temp'] = data['t10']
        the_dict['moisture'] = data['moisture']
        the_dict['polygon_id'] = polyd
        return Soil.from_dict(the_dict)

    # Satellite Imagery subset methods

    def search_satellite_imagery(self, polygon_id, img_type, preset):
        raise NotImplementedError()

    def download_satellite_image(self, metaimage, x=None, y=None, zoom=None):
        """
        Downloads the satellite image described by the provided metadata. In case the satellite image is a tile, then
        tile coordinates and zoom must be provided

        :param metaimage: the satellite image's metadata, in the form of a `MetaImage` subtype instance
        :type metaimage: a `pyowm.agroapi10.imagery.MetaImage` subtype
        :param x: x tile coordinate (only needed in case you are downloading a tile image)
        :type x: int or `None`
        :param y: y tile coordinate (only needed in case you are downloading a tile image)
        :type y: int or `None`
        :param zoom: zoom level (only needed in case you are downloading a tile image)
        :type zoom: int or `None`
        :return: a `pyowm.agroapi10.imagery.SatelliteImage` instance containing both image's metadata and data
        """
        # polygon PNG
        if isinstance(metaimage, MetaPNGImage):
            prepared_url = metaimage.url
            status, data = self.http_client.get_png(
                prepared_url,
                params={'appid': self.API_key})
            img = Image(data, metaimage.image_type)
            return SatelliteImage(metaimage, img)
        # GeoTIF
        elif isinstance(metaimage, MetaGeoTiffImage):
            prepared_url = metaimage.url
            status, data = self.http_client.get_geotiff(
                prepared_url,
                params={'appid': self.API_key})
            img = Image(data, metaimage.image_type)
            return SatelliteImage(metaimage, img)
        # tile PNG
        elif isinstance(metaimage, MetaTile):
            assert x is not None
            assert y is not None
            assert zoom is not None
            prepared_url = self._fill_url(metaimage.url, x, y, zoom)
            status, data = self.http_client.get_png(
                prepared_url,
                params={'appid': self.API_key})
            img = Image(data, metaimage.image_type)
            tile = Tile(x, y, zoom, None, img)
            return SatelliteImage(metaimage, tile)
        else:
            raise ValueError("Cannot download: unsupported MetaImage subtype")

    def stats_for_satellite_image(self, metaimage):
        """
        Retrieves statistics for the satellite image described by the provided metadata.
        This is currently only supported 'EVI' and 'NDVI' presets

        :param metaimage: the satellite image's metadata, in the form of a `MetaImage` subtype instance
        :type metaimage: a `pyowm.agroapi10.imagery.MetaImage` subtype
        :return: dict
        """
        if metaimage.preset != MetaImagePresetEnum.EVI and metaimage.preset != MetaImagePresetEnum.NDVI:
            raise ValueError("Unsupported image preset: should be EVI or NDVI")
        if metaimage.stats_url is None:
            raise ValueError("URL for image statistics is not defined")
        status, data = self.http_client.get_json(
            metaimage.stats_url,
            params={'appid': self.API_key})
        return data

    # Utilities
    def _fill_url(self, url_template, x, y, zoom):
        return url_template.replace('{x}', str(x)).replace('{y}', str(y)).replace('{z}', str(zoom))
