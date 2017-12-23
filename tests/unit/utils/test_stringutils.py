import unittest
from pyowm.utils import stringutils


class TestStringUtils(unittest.TestCase):

    def test_obfuscate_API_key(self):
        API_key = '22e28da2669c4283acdbd9cfa7dc0903'
        expected = '************************a7dc0903'

        self.assertEqual(expected, stringutils.obfuscate_API_key(API_key))
        self.assertIsNone(stringutils.obfuscate_API_key(None))
