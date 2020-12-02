#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.agroapi10.enums import PresetEnum, PaletteEnum
from pyowm.agroapi10.imagery import MetaTile, MetaGeoTiffImage, MetaPNGImage, SatelliteImage
from pyowm.agroapi10.polygon import Polygon, GeoPolygon
from pyowm.agroapi10.search import SatelliteImagerySearchResultSet
from pyowm.agroapi10.soil import Soil
from pyowm.agroapi10.uris import ROOT_AGRO_API, POLYGONS_URI, NAMED_POLYGON_URI, SOIL_URI, SATELLITE_IMAGERY_SEARCH_URI
from pyowm.commons.http_client import HttpClient
from pyowm.commons.image import Image
from pyowm.commons.tile import Tile
from pyowm.constants import AGRO_API_VERSION
from pyowm.utils import timestamps


class AgroManager:

    """
    A manager objects that provides a full interface to OWM Agro API.

    :param API_key: the OWM Weather API key
    :type API_key: str
    :param config: the configuration dictionary
    :type config: dict
    :returns: an `AgroManager` instance
    :raises: `AssertionError` when no API Key is provided

    """

    def __init__(self, API_key, config):
        assert isinstance(API_key, str), 'You must provide a valid API Key'
        self.API_key = API_key
        assert isinstance(config, dict)
        self.http_client = HttpClient(API_key, config, ROOT_AGRO_API)

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
        data = {
            'geo_json': {
                "type": "Feature",
                "properties": {},
                "geometry": geopolygon.to_dict(),
            }
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
        the_dict = {
            'reference_time': data['dt'],
            'surface_temp': data['t0'],
            'ten_cm_temp': data['t10'],
            'moisture': data['moisture'],
            'polygon_id': polyd,
        }

        return Soil.from_dict(the_dict)

    # Satellite Imagery subset methods

    def search_satellite_imagery(self, polygon_id, acquired_from, acquired_to, img_type=None, preset=None,
                                 min_resolution=None, max_resolution=None, acquired_by=None, min_cloud_coverage=None,
                                 max_cloud_coverage=None, min_valid_data_coverage=None, max_valid_data_coverage=None):
        """
        Searches on the Agro API the metadata for all available satellite images that contain the specified polygon and
        acquired during the specified time interval; and optionally matching the specified set of filters:
        - image type (eg. GeoTIF)
        - image preset (eg. false color, NDVI, ...)
        - min/max acquisition resolution
        - acquiring satellite
        - min/max cloud coverage on acquired scene
        - min/max valid data coverage on acquired scene

        :param polygon_id: the ID of the reference polygon
        :type polygon_id: str
        :param acquired_from: lower edge of acquisition interval, UNIX timestamp
        :type acquired_from: int
        :param acquired_to: upper edge of acquisition interval, UNIX timestamp
        :type acquired_to: int
        :param img_type: the desired file format type of the images. Allowed values are given by `pyowm.commons.enums.ImageTypeEnum`
        :type img_type: `pyowm.commons.databoxes.ImageType`
        :param preset: the desired preset of the images. Allowed values are given by `pyowm.agroapi10.enums.PresetEnum`
        :type preset: str
        :param min_resolution: minimum resolution for images, px/meters
        :type min_resolution: int
        :param max_resolution: maximum resolution for images, px/meters
        :type max_resolution: int
        :param acquired_by: short symbol of the satellite that acquired the image (eg. "l8")
        :type acquired_by: str
        :param min_cloud_coverage: minimum cloud coverage percentage on acquired images
        :type min_cloud_coverage: int
        :param max_cloud_coverage: maximum cloud coverage percentage on acquired images
        :type max_cloud_coverage: int
        :param min_valid_data_coverage: minimum valid data coverage percentage on acquired images
        :type min_valid_data_coverage: int
        :param max_valid_data_coverage: maximum valid data coverage percentage on acquired images
        :type max_valid_data_coverage: int
        :return: a list of `pyowm.agro10.imagery.MetaImage` subtypes instances
        """
        assert polygon_id is not None
        assert acquired_from is not None
        assert acquired_to is not None
        assert acquired_from <= acquired_to, 'Start timestamp of acquisition window must come before its end'
        if min_resolution is not None:
            assert min_resolution > 0, 'Minimum resolution must be positive'
        if max_resolution is not None:
            assert max_resolution > 0, 'Maximum resolution must be positive'
        if min_resolution is not None and max_resolution is not None:
            assert min_resolution <= max_resolution, 'Mininum resolution must be lower than maximum resolution'
        if min_cloud_coverage is not None:
            assert min_cloud_coverage >= 0, 'Minimum cloud coverage must be non negative'
        if max_cloud_coverage is not None:
            assert max_cloud_coverage >= 0, 'Maximum cloud coverage must be non negative'
        if min_cloud_coverage is not None and max_cloud_coverage is not None:
            assert min_cloud_coverage <= max_cloud_coverage, 'Minimum cloud coverage must be lower than maximum cloud coverage'
        if min_valid_data_coverage is not None:
            assert min_valid_data_coverage >= 0, 'Minimum valid data coverage must be non negative'
        if max_valid_data_coverage is not None:
            assert max_valid_data_coverage >= 0, 'Maximum valid data coverage must be non negative'
        if min_valid_data_coverage is not None and max_valid_data_coverage is not None:
            assert min_valid_data_coverage <= max_valid_data_coverage, 'Minimum valid data coverage must be lower than maximum valid data coverage'

        # prepare params
        params = dict(appid=self.API_key, polyid=polygon_id, start=acquired_from, end=acquired_to)
        if min_resolution is not None:
            params['resolution_min'] = min_resolution
        if max_resolution is not None:
            params['resolution_max'] = max_resolution
        if acquired_by is not None:
            params['type'] = acquired_by
        if min_cloud_coverage is not None:
            params['clouds_min'] = min_cloud_coverage
        if max_cloud_coverage is not None:
            params['clouds_max'] = max_cloud_coverage
        if min_valid_data_coverage is not None:
            params['coverage_min'] = min_valid_data_coverage
        if max_valid_data_coverage is not None:
            params['coverage_max'] = max_valid_data_coverage

        # call API
        status, data = self.http_client.get_json(SATELLITE_IMAGERY_SEARCH_URI, params=params)

        result_set = SatelliteImagerySearchResultSet(polygon_id, data, timestamps.now(timeformat='unix'))

        # further filter by img_type and/or preset (if specified)
        if img_type is not None and preset is not None:
            return result_set.with_img_type_and_preset(img_type, preset)
        elif img_type is not None:
            return result_set.with_img_type(img_type)
        elif preset is not None:
            return result_set.with_preset(preset)
        else:
            return result_set.all()

    def download_satellite_image(self, metaimage, x=None, y=None, zoom=None, palette=None):
        """
        Downloads the satellite image described by the provided metadata. In case the satellite image is a tile, then
        tile coordinates and zoom must be provided. An optional palette ID can be provided, if supported by the
        downloaded preset (currently only NDVI is supported)

        :param metaimage: the satellite image's metadata, in the form of a `MetaImage` subtype instance
        :type metaimage: a `pyowm.agroapi10.imagery.MetaImage` subtype
        :param x: x tile coordinate (only needed in case you are downloading a tile image)
        :type x: int or `None`
        :param y: y tile coordinate (only needed in case you are downloading a tile image)
        :type y: int or `None`
        :param zoom: zoom level (only needed in case you are downloading a tile image)
        :type zoom: int or `None`
        :param palette: ID of the color palette of the downloaded images. Values are provided by `pyowm.agroapi10.enums.PaletteEnum`
        :type palette: str or `None`
        :return: a `pyowm.agroapi10.imagery.SatelliteImage` instance containing both image's metadata and data
        """
        if palette is not None:
            assert isinstance(palette, str)
            params = dict(paletteid=palette)
        else:
            palette = PaletteEnum.GREEN
            params = {}
        # polygon PNG
        if isinstance(metaimage, MetaPNGImage):
            prepared_url = metaimage.url
            status, data = self.http_client.get_png(
                prepared_url, params=params)
            img = Image(data, metaimage.image_type)
            return SatelliteImage(metaimage, img, downloaded_on=timestamps.now(timeformat='unix'), palette=palette)
        # GeoTIF
        elif isinstance(metaimage, MetaGeoTiffImage):
            prepared_url = metaimage.url
            status, data = self.http_client.get_geotiff(
                prepared_url, params=params)
            img = Image(data, metaimage.image_type)
            return SatelliteImage(metaimage, img, downloaded_on=timestamps.now(timeformat='unix'), palette=palette)
        # tile PNG
        elif isinstance(metaimage, MetaTile):
            assert x is not None
            assert y is not None
            assert zoom is not None
            prepared_url = self._fill_url(metaimage.url, x, y, zoom)
            status, data = self.http_client.get_png(
                prepared_url, params=params)
            img = Image(data, metaimage.image_type)
            tile = Tile(x, y, zoom, None, img)
            return SatelliteImage(metaimage, tile, downloaded_on=timestamps.now(timeformat='unix'), palette=palette)
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
        if metaimage.preset not in [PresetEnum.EVI, PresetEnum.NDVI]:
            raise ValueError("Unsupported image preset: should be EVI or NDVI")
        if metaimage.stats_url is None:
            raise ValueError("URL for image statistics is not defined")
        status, data = self.http_client.get_json(metaimage.stats_url, params={})
        return data

    # Utilities
    def _fill_url(self, url_template, x, y, zoom):
        return url_template.replace('{x}', str(x)).replace('{y}', str(y)).replace('{z}', str(zoom))

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)
