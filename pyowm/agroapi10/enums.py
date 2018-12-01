
class MetaImagePresetEnum:
    """
    Allowed presets for MetaImages on Agro API 1.0

    """
    TRUE_COLOR = 'truecolor'
    FALSE_COLOR = 'falsecolor'
    NDVI = 'ndvi'
    EVI = 'evi'

    @classmethod
    def items(cls):
        """
        All values for this enum
        :return: list of str

        """
        return [
            cls.TRUE_COLOR,
            cls.FALSE_COLOR,
            cls.NDVI,
            cls.EVI
        ]


class Satellite:
    """
    Databox class representing a satellite

    :param name: the satellite
    :type name: str
    :param symbol: the short name of the satellite
    :type symbol: str
    """
    def __init__(self, name, symbol):

        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return "<%s.%s - name=%s symbol=%s>" % (
            __name__, self.__class__.__name__, self.name, self.symbol)


class SatelliteEnum:
    """
    Allowed presets for satellite names on Agro API 1.0

    """
    LANDSAT_8 = Satellite('Landsat 8', 'l8')
    SENTINEL_2 = Satellite('Sentinel 2', 's2')

    @classmethod
    def items(cls):
        """
        All values for this enum
        :return: list of str

        """
        return [
            cls.LANDSAT_8,
            cls.SENTINEL_2
        ]
