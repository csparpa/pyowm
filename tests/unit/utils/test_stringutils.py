import unittest
import sys
from pyowm.utils import stringutils


class TestStringUtils(unittest.TestCase):

    def test_obfuscate_API_key(self):
        API_key = '22e28da2669c4283acdbd9cfa7dc0903'
        expected = '************************a7dc0903'

        self.assertEqual(expected, stringutils.obfuscate_API_key(API_key))
        self.assertIsNone(stringutils.obfuscate_API_key(None))

    def test_encode_to_utf8(self):
        name = 'testname'
        if sys.version_info > (3, 0):
            result = stringutils.encode_to_utf8(name)
            self.assertEqual(result, name)
        else:  # Python 2
            result = stringutils.encode_to_utf8(name)
            try:
                result.decode('ascii')
            except:
                self.fail()

    def test_assert_is_string(self):
        a_string = 'test'
        a_non_string = 123
        stringutils.assert_is_string(a_string)
        self.assertRaises(AssertionError, stringutils.assert_is_string,
                          a_non_string)

    def test_assert_is_string_or_unicode(self):
        a_string = 'test'
        a_non_string = 123
        stringutils.assert_is_string_or_unicode(a_string)
        self.assertRaises(AssertionError,
                          stringutils.assert_is_string_or_unicode,
                          a_non_string)

        try:  # only for Python 2
            unicode_value = unicode('test')
            stringutils.assert_is_string_or_unicode(unicode_value)
        except:
            pass