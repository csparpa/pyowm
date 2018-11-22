from pyowm.utils import timeformatutils


class MetaImage:
    def __init__(self, url, img_type, preset, satellite_name, acquisition_time,
                 valid_data_percentage, cloud_coverage_percentage, sun_azimuth, sun_elevation,
                 http_client=None):
        assert isinstance(url, str)
        self.url = url
        self.img_type = img_type
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
        """Returns the UTC time telling when the image data was acquired by the satellit

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
            self.img_type, self.preset, self.acquisition_time('iso'), self.satellite_name)


class MetaSatelliteImage:
    pass


class MetaTile:
    pass
