#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.agroapi10.enums import PresetEnum
from pyowm.agroapi10.imagery import MetaPNGImage, MetaTile, MetaGeoTiffImage
from pyowm.commons.databoxes import ImageType
from pyowm.utils import formatting


class SatelliteImagerySearchResultSet:
    """
    Class representing a filterable result set by a satellite imagery search against the Agro API 1.0. Each result
    is a `pyowm.agroapi10.imagery.MetaImage` subtype instance

    """

    def __init__(self, polygon_id, list_of_dict, query_timestamp):
        """
        Parses raw data dict into a list of `pyowm.agroapi10.imagery.MetaImage` subtypes instances and stores that
        list internally for further filtering

        :param polygon_id: the ID of the polygon that has been searched for images
        :type polygon_id: str
        :param list_of_dict: the input data dictionary
        :type list_of_dict: list
        :param query_timestamp: UNIX timestamp of the query
        :type query_timestamp: int
        :returns: a `pyowm.agroapi10.imagery.SatelliteImagerySearchResultSet` instance or an exception is parsing fails

        """
        assert isinstance(polygon_id, str)
        self.polygon_id = polygon_id

        assert isinstance(list_of_dict, list)

        assert isinstance(query_timestamp, int)
        self.query_timestamp = query_timestamp

        # parse raw data
        result = []
        for the_dict in list_of_dict:
            # common metadata
            acquisition_time = the_dict.get('dt', None)
            satellite_name = the_dict.get('type', None)
            valid_data_percentage = the_dict.get('dc', None)
            cloud_coverage_percentage = the_dict.get('cl', None)
            sun = the_dict.get('sun', dict())
            sun_azimuth = sun.get('azimuth', None)
            sun_elevation = sun.get('elevation', None)

            # Stats for the images
            stats_dict = the_dict.get('stats', dict())
            stats_url_for_ndvi = stats_dict.get('ndvi', None)
            stats_url_for_evi = stats_dict.get('evi', None)

            # PNG images for the polygon
            png_dict = the_dict.get('image', dict())
            true_color_png_url = png_dict.get('truecolor', None)
            false_color_png_url = png_dict.get('falsecolor', None)
            ndvi_png_url = png_dict.get('ndvi', None)
            evi_png_url = png_dict.get('evi', None)
            if true_color_png_url is not None:
                result.append(
                    MetaPNGImage(true_color_png_url, PresetEnum.TRUE_COLOR, satellite_name, acquisition_time,
                                 valid_data_percentage, cloud_coverage_percentage, sun_azimuth, sun_elevation,
                                 polygon_id=polygon_id))
            if false_color_png_url is not None:
                result.append(
                    MetaPNGImage(false_color_png_url, PresetEnum.FALSE_COLOR, satellite_name, acquisition_time,
                                 valid_data_percentage, cloud_coverage_percentage, sun_azimuth, sun_elevation,
                                 polygon_id=polygon_id))
            if ndvi_png_url is not None:
                result.append(
                    MetaPNGImage(ndvi_png_url, PresetEnum.NDVI, satellite_name, acquisition_time,
                                 valid_data_percentage, cloud_coverage_percentage, sun_azimuth, sun_elevation,
                                 polygon_id=polygon_id, stats_url=stats_url_for_ndvi))
            if evi_png_url is not None:
                result.append(
                    MetaPNGImage(evi_png_url, PresetEnum.EVI, satellite_name, acquisition_time,
                                 valid_data_percentage, cloud_coverage_percentage, sun_azimuth, sun_elevation,
                                 polygon_id=polygon_id, stats_url=stats_url_for_evi))

            # Tiles for the polygon
            tiles_dict = the_dict.get('tile', dict())
            true_color_tile_url = tiles_dict.get('truecolor', None)
            false_color_tile_url = tiles_dict.get('falsecolor', None)
            ndvi_tile_url = tiles_dict.get('ndvi', None)
            evi_tile_url = tiles_dict.get('evi', None)
            if true_color_tile_url is not None:
                result.append(
                    MetaTile(true_color_tile_url, PresetEnum.TRUE_COLOR, satellite_name, acquisition_time,
                             valid_data_percentage, cloud_coverage_percentage, sun_azimuth, sun_elevation,
                             polygon_id=polygon_id))
            if false_color_tile_url is not None:
                result.append(
                    MetaTile(false_color_tile_url, PresetEnum.FALSE_COLOR, satellite_name, acquisition_time,
                             valid_data_percentage, cloud_coverage_percentage, sun_azimuth, sun_elevation,
                             polygon_id=polygon_id))
            if ndvi_tile_url is not None:
                result.append(
                    MetaTile(ndvi_tile_url, PresetEnum.NDVI, satellite_name, acquisition_time,
                             valid_data_percentage, cloud_coverage_percentage, sun_azimuth, sun_elevation,
                             polygon_id=polygon_id, stats_url=stats_url_for_ndvi))
            if evi_tile_url is not None:
                result.append(
                    MetaTile(evi_tile_url, PresetEnum.EVI, satellite_name, acquisition_time,
                             valid_data_percentage, cloud_coverage_percentage, sun_azimuth, sun_elevation,
                             polygon_id=polygon_id, stats_url=stats_url_for_evi))

            # geoTiff images for the polygon
            geotiff_dict = the_dict.get('data', dict())
            true_color_geotiff_url = geotiff_dict.get('truecolor', None)
            false_color_geotiff_url = geotiff_dict.get('falsecolor', None)
            ndvi_geotiff_url = geotiff_dict.get('ndvi', None)
            evi_geotiff_url = geotiff_dict.get('evi', None)
            if true_color_geotiff_url is not None:
                result.append(
                    MetaGeoTiffImage(true_color_geotiff_url, PresetEnum.TRUE_COLOR, satellite_name,
                                     acquisition_time, valid_data_percentage, cloud_coverage_percentage,
                                     sun_azimuth, sun_elevation, polygon_id=polygon_id))
            if false_color_geotiff_url is not None:
                result.append(
                    MetaGeoTiffImage(false_color_geotiff_url, PresetEnum.FALSE_COLOR, satellite_name,
                                     acquisition_time, valid_data_percentage, cloud_coverage_percentage,
                                     sun_azimuth, sun_elevation, polygon_id=polygon_id))
            if ndvi_geotiff_url is not None:
                result.append(
                    MetaGeoTiffImage(ndvi_geotiff_url, PresetEnum.NDVI, satellite_name,
                                     acquisition_time, valid_data_percentage, cloud_coverage_percentage,
                                     sun_azimuth, sun_elevation, polygon_id=polygon_id, stats_url=stats_url_for_ndvi))
            if evi_geotiff_url is not None:
                result.append(
                    MetaGeoTiffImage(evi_geotiff_url, PresetEnum.EVI, satellite_name,
                                     acquisition_time, valid_data_percentage, cloud_coverage_percentage,
                                     sun_azimuth, sun_elevation, polygon_id=polygon_id, stats_url=stats_url_for_evi))
        self.metaimages = result

    def issued_on(self, timeformat='unix'):
        """Returns the UTC time telling when the query was performed against the OWM Agro API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str

        """
        return formatting.timeformat(self.query_timestamp, timeformat)

    def __len__(self):
        return len(self.metaimages)

    def __repr__(self):
        return '<%s.%s - %s results for query issued on polygon_id=%s at %s>' % (
            __name__, self.__class__.__name__,
            len(self), self.polygon_id, self.issued_on(timeformat='iso'))

    def all(self):
        """
        Returns all search results

        :returns: a list of `pyowm.agroapi10.imagery.MetaImage` instances

        """
        return self.metaimages

    def with_img_type(self, image_type):
        """
        Returns the search results having the specified image type

        :param image_type: the desired image type (valid values are provided by the
            `pyowm.commons.enums.ImageTypeEnum` enum)
        :type image_type: `pyowm.commons.databoxes.ImageType` instance
        :returns: a list of `pyowm.agroapi10.imagery.MetaImage` instances

        """
        assert isinstance(image_type, ImageType)
        return list(filter(lambda x: x.image_type == image_type, self.metaimages))

    def with_preset(self, preset):
        """
        Returns the search results having the specified preset

        :param preset: the desired image preset (valid values are provided by the
            `pyowm.agroapi10.enums.PresetEnum` enum)
        :type preset: str
        :returns: a list of `pyowm.agroapi10.imagery.MetaImage` instances

        """
        assert isinstance(preset, str)
        return list(filter(lambda x: x.preset == preset, self.metaimages))

    def with_img_type_and_preset(self, image_type, preset):
        """
        Returns the search results having both the specified image type and preset

        :param image_type: the desired image type (valid values are provided by the
            `pyowm.commons.enums.ImageTypeEnum` enum)
        :type image_type: `pyowm.commons.databoxes.ImageType` instance
        :param preset: the desired image preset (valid values are provided by the
            `pyowm.agroapi10.enums.PresetEnum` enum)
        :type preset: str
        :returns: a list of `pyowm.agroapi10.imagery.MetaImage` instances

        """
        assert isinstance(image_type, ImageType)
        assert isinstance(preset, str)
        return list(filter(lambda x: x.image_type == image_type and x.preset == preset, self.metaimages))
