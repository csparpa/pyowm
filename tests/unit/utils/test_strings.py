#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pyowm.utils import strings


class Placeholder:
    pass  # don't move!


class TestStringUtils(unittest.TestCase):

    def test_obfuscate_API_key(self):
        API_key = '22e28da2669c4283acdbd9cfa7dc0903'
        expected = '************************a7dc0903'

        self.assertEqual(expected, strings.obfuscate_API_key(API_key))
        self.assertIsNone(strings.obfuscate_API_key(None))

    def test_version_tuple_to_str(self):
        version_tuple = (1, 4, 6)
        expected = '1.4.6'
        result = strings.version_tuple_to_str(version_tuple)
        self.assertEqual(expected, result)
        version_tuple = (1, 4, 6, 9)
        separator = ';'
        expected = '1;4;6;9'
        result = strings.version_tuple_to_str(version_tuple, separator=separator)
        self.assertEqual(expected, result)

    def test_class_from_dotted_path(self):
        path = 'tests.unit.utils.test_strings.Placeholder'
        result = strings.class_from_dotted_path(path)
        assert result == Placeholder
