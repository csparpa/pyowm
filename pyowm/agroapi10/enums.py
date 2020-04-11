from pyowm.commons.databoxes import Satellite


class PresetEnum:
    """
    Allowed presets for satellite images on Agro API 1.0

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


class SatelliteEnum:
    """
    Allowed presets for satellite names on Agro API 1.0

    """
    LANDSAT_8 = Satellite('Landsat 8', 'l8')
    SENTINEL_2 = Satellite('Sentinel-2', 's2')

    @classmethod
    def items(cls):
        """
        All values for this enum
        :return: list of Satellite databoxes

        """
        return [
            cls.LANDSAT_8,
            cls.SENTINEL_2
        ]


class PaletteEnum:
    """
    Allowed color palettes for satellite images on Agro API 1.0

    """
    GREEN = '1'   # default Agro API 1.0 palette
    BLACK_AND_WHITE = '2'
    CONTRAST_SHIFTED = '3'
    CONTRAST_CONTINUOUS = '4'

    @classmethod
    def items(cls):
        """
        All values for this enum
        :return: list of str

        """
        return [
            cls.GREEN,
            cls.BLACK_AND_WHITE,
            cls.CONTRAST_SHIFTED,
            cls.CONTRAST_CONTINUOUS
        ]
