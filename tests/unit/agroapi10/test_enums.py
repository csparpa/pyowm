import unittest

from pyowm.agroapi10.enums import PresetEnum, PaletteEnum, SatelliteEnum


class TestPresetEnum(unittest.TestCase):

    def test_items(self):
        preset_enum = PresetEnum()
        items = preset_enum.items()

        self.assertEqual(4, len(items))
        self.assertEqual(sorted([preset_enum.TRUE_COLOR,
                                preset_enum.FALSE_COLOR,
                                preset_enum.NDVI,
                                preset_enum.EVI]),
                         sorted(items))


class TestSatelliteEnum(unittest.TestCase):

    def test_items(self):
        satellite_enum = SatelliteEnum()
        items = satellite_enum.items()

        self.assertEqual(2, len(items))
        self.assertEqual([satellite_enum.LANDSAT_8, satellite_enum.SENTINEL_2],
                         items)


class TestPaletteEnum(unittest.TestCase):

    def test_items(self):
        palette_enum = PaletteEnum()
        items = palette_enum.items()

        self.assertEqual(4, len(items))
        self.assertEqual(sorted([palette_enum.GREEN,
                                palette_enum.BLACK_AND_WHITE,
                                palette_enum.CONTRAST_SHIFTED,
                                palette_enum.CONTRAST_CONTINUOUS]),
                         sorted(items))
