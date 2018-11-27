from pyowm.utils import timeformatutils
from pyowm.commons.enums import ImageTypeEnum


class MetaImage:
    """
    A class representing metadata for a satellite-acquired image

    :param url: the public URL of the image
    :type url: str
    :param preset: the preset of the image (supported values are listed by `pyowm.agroapi10.enums.MetaImagePresetEnum`)
    :type preset: str
    :param satellite_name: the name of the satellite that acquired the image (supported values are listed
        by `pyowm.agroapi10.enums.SatelliteNameEnum`)
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
    :param http_client: an optional HTTP client to use for downloading
    :type http_client: a `pyowm.commons.http_client.HttpClient` instance
    :returns: an `MetaImage` object
    """

    image_type = None

    def __init__(self, url, preset, satellite_name, acquisition_time,
                 valid_data_percentage, cloud_coverage_percentage, sun_azimuth, sun_elevation,
                 http_client=None):
        assert isinstance(url, str)
        self.url = url
        self.preset = preset
        self.satellite_name = satellite_name
        assert isinstance(acquisition_time, int)
        assert acquisition_time >= 0, 'acquisition_time cannot be negative'
        self._acquisition_time = acquisition_time
        assert isinstance(valid_data_percentage, float)
        assert valid_data_percentage >= 0., 'valid_data_percentage cannot be negative'
        self.valid_data_percentage = valid_data_percentage
        assert isinstance(cloud_coverage_percentage, float)
        assert cloud_coverage_percentage >= 0., 'cloud_coverage_percentage cannot be negative'
        self.cloud_coverage_percentage = cloud_coverage_percentage
        assert isinstance(sun_azimuth, float)
        assert sun_azimuth >= 0. and sun_azimuth <= 360., 'sun_azimuth must be between 0 and 360 degrees'
        self.sun_azimuth  = sun_azimuth
        assert isinstance(sun_elevation, float)
        assert sun_elevation >= 0. and sun_elevation <= 90., 'sun_elevation must be between 0 and 90 degrees'
        self.sun_elevation = sun_elevation
        self.http_client = http_client

    def acquisition_time(self, timeformat='unix'):
        """Returns the UTC time telling when the image data was acquired by the satellite

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str

        """
        return timeformatutils.timeformat(self._acquisition_time, timeformat)

    def __repr__(self):
        return "<%s.%s - %s %s image acquired at %s by %s>" % (
            __name__, self.__class__.__name__,
            self.image_type if self.image_type is not None else '',
            self.preset, self.acquisition_time('iso'), self.satellite_name)


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


class MetaZonalStatistics(MetaImage):
    """
    Class representing metadata for NDVI & EVI indices of a polygon
    """
    pass
