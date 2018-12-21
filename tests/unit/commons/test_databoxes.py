import unittest
from pyowm.commons.databoxes import ImageType, Satellite


class TestImageType(unittest.TestCase):

    def test_repr(self):
        instance = ImageType('PDF', 'application/pdf')
        repr(instance)


class TestSatellite(unittest.TestCase):

    def test_repr(self):
        instance = Satellite('Terrasat', 'tst')
        repr(instance)

