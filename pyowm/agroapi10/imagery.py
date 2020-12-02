#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.commons.enums import ImageTypeEnum
from pyowm.commons.image import Image
from pyowm.commons.tile import Tile
from pyowm.utils import formatting


class MetaImage:
    """
    A class representing metadata for a satellite-acquired image

    :param url: the public URL of the image
    :type url: str
    :param preset: the preset of the image (supported values are listed by `pyowm.agroapi10.enums.PresetEnum`)
    :type preset: str
    :param satellite_name: the name of the satellite that acquired the image (supported values are listed
        by `pyowm.agroapi10.enums.SatelliteEnum`)
    :type satellite_name: str
    :param acquisition_time: the UTC Unix epoch when the image was acquired
    :type acquisition_time: int
    :param valid_data_percentage: approximate percentage of valid data coverage
    :type valid_data_percentage: float
    :param cloud_coverage_percentage: approximate percentage of cloud coverage on the scene
    :type cloud_coverage_percentage: float
    :param sun_azimuth: sun azimuth angle at scene acquisition time
    :type sun_azimuth: float
    :param sun_elevation: sun zenith angle at scene acquisition time
    :type sun_elevation: float
    :param polygon_id: optional id of the polygon the image refers to
    :type polygon_id: str
    :param stats_url: the public URL of the image statistics, if available
    :type stats_url: str or `None`
    :returns: an `MetaImage` object
    """

    image_type = None

    def __init__(self, url, preset, satellite_name, acquisition_time,
                 valid_data_percentage, cloud_coverage_percentage, sun_azimuth, sun_elevation, polygon_id=None,
                 stats_url=None):
        assert isinstance(url, str)
        self.url = url
        self.preset = preset
        self.satellite_name = satellite_name
        assert isinstance(acquisition_time, int)
        assert acquisition_time >= 0, 'acquisition_time cannot be negative'
        self._acquisition_time = acquisition_time
        assert isinstance(valid_data_percentage, (float, int))
        assert valid_data_percentage >= 0., 'valid_data_percentage cannot be negative'
        self.valid_data_percentage = valid_data_percentage
        assert isinstance(cloud_coverage_percentage, (float, int))
        assert cloud_coverage_percentage >= 0., 'cloud_coverage_percentage cannot be negative'
        self.cloud_coverage_percentage = cloud_coverage_percentage
        assert isinstance(sun_azimuth, (float, int))
        assert sun_azimuth >= 0. and sun_azimuth <= 360., 'sun_azimuth must be between 0 and 360 degrees'
        self.sun_azimuth  = sun_azimuth
        assert isinstance(sun_elevation, (float, int))
        assert sun_elevation >= 0. and sun_elevation <= 90., 'sun_elevation must be between 0 and 90 degrees'
        self.sun_elevation = sun_elevation
        self.polygon_id = polygon_id
        self.stats_url = stats_url

    def acquisition_time(self, timeformat='unix'):
        """Returns the UTC time telling when the image data was acquired by the satellite

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str

        """
        return formatting.timeformat(self._acquisition_time, timeformat)

    def __repr__(self):
        return "<%s.%s - %s %s image acquired at %s by %s on polygon with id=%s>" % (
            __name__, self.__class__.__name__,
            self.image_type.name if self.image_type is not None else '',
            self.preset, self.acquisition_time('iso'), self.satellite_name,
            self.polygon_id if self.polygon_id is not None else 'None')


class MetaPNGImage(MetaImage):
    """
    Class representing metadata for a satellite image of a polygon in PNG format
    """
    image_type = ImageTypeEnum.PNG


class MetaTile(MetaImage):
    """
    Class representing metadata for a tile in PNG format
    """
    image_type = ImageTypeEnum.PNG


class MetaGeoTiffImage(MetaImage):
    """
    Class representing metadata for a satellite image of a polygon in GeoTiff format
    """
    image_type = ImageTypeEnum.GEOTIFF


class SatelliteImage:
    """
    Class representing a downloaded satellite image, featuring both metadata and data

    :param metadata: the metadata for this satellite image
    :type metadata: a `pyowm.agro10.imagery.MetaImage` subtype instance
    :param data: the actual data for this satellite image
    :type data: either `pyowm.commons.image.Image` or `pyowm.commons.tile.Tile` object
    :param downloaded_on: the UNIX epoch this satellite image was downloaded at
    :type downloaded_on: int or `None`
    :param palette: ID of the color palette of the downloaded images. Values are provided by `pyowm.agroapi10.enums.PaletteEnum`
    :type palette: str or `None`
    :returns: a `pyowm.agroapi10.imagery.SatelliteImage` instance
    """

    def __init__(self, metadata, data, downloaded_on=None, palette=None):
        assert isinstance(metadata, MetaImage)
        self.metadata = metadata
        assert isinstance(data, (Image, Tile))
        self.data = data
        if downloaded_on is not None:
            assert isinstance(downloaded_on, int)
            self._downloaded_on = downloaded_on
        if palette is not None:
            assert isinstance(palette, str)
            self.palette = palette

    def downloaded_on(self, timeformat='unix'):
        """Returns the UTC time telling when the satellite image was downloaded from the OWM Agro API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str

        """
        return formatting.timeformat(self._downloaded_on, timeformat)

    def persist(self, path_to_file):
        """
        Saves the satellite image to disk on a file

        :param path_to_file: path to the target file
        :type path_to_file: str
        :return: `None`
        """
        self.data.persist(path_to_file)

    def __repr__(self):
        return "<%s.%s - %s %s satellite image downloaded on: %s>" % (
            __name__, self.__class__.__name__,
            self.metadata.preset, self.metadata.satellite_name,
            self.downloaded_on('iso') if self._downloaded_on is not None else 'None')
