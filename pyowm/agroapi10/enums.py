
class MetaImagePresetEnum:
    """
    Allowed presets for MetaImages on Agro API 1.0

    """
    TRUE_COLOR = 'truecolor'
    FALSE_COLOR = 'falsecolor'
    NDVI = 'ndvi'
    EVI = 'evi'

    def items(self):
        """
        All values for this enum
        :return: list of tuples

        """
        return [
            ('truecolor', self.TRUE_COLOR),
            ('falsecolor', self.FALSE_COLOR),
            ('ndvi', self.NDVI),
            ('evi', self.EVI)
        ]


class SatelliteNameEnum:
    """
    Allowed presets for satellite names on Agro API 1.0

    """
    LANDSAT_8 = 'Landsat 8'
    SENTINEL_2 = 'Sentinel 2'

    def items(self):
        """
        All values for this enum
        :return: list of tuples

        """
        return [
            ('Landsat 8', self.LANDSAT_8),
            ('Sentinel 2', self.SENTINEL_2)
        ]
