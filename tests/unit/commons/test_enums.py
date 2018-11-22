import unittest
from pyowm.commons.enums import ImageTypeEnum, ImageType


class TestImageTypeEnum(unittest.TestCase):

    def test_lookup_by_mime_typ(self):
        mime_not_found = 'unexistent/xyz'
        mime_found = 'image/png'
        result = ImageTypeEnum.lookup_by_mime_type(mime_found)
        self.assertTrue(isinstance(result, ImageType))
        result = ImageTypeEnum.lookup_by_mime_type(mime_not_found)
        self.assertIsNone(result)
