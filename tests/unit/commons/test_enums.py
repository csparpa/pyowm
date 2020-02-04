#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pyowm.commons.enums import ImageTypeEnum, SubscriptionTypeEnum
from pyowm.commons.databoxes import ImageType


class TestSubscriptionTypeEnum(unittest.TestCase):

    def test_lookup_by_name(self):
        name_not_found = 'non-existent'
        with self.assertRaises(ValueError):
            SubscriptionTypeEnum.lookup_by_name(name_not_found)


class TestImageTypeEnum(unittest.TestCase):

    def test_lookup_by_mime_type(self):
        mime_not_found = 'unexistent/xyz'
        mime_found = 'image/png'
        result = ImageTypeEnum.lookup_by_mime_type(mime_found)
        self.assertTrue(isinstance(result, ImageType))
        result = ImageTypeEnum.lookup_by_mime_type(mime_not_found)
        self.assertIsNone(result)

    def test_lookup_by_name(self):
        name_not_found = 'ZOOMOOO'
        name_found = 'GEOTIFF'
        result = ImageTypeEnum.lookup_by_name(name_found)
        self.assertTrue(isinstance(result, ImageType))
        result = ImageTypeEnum.lookup_by_name(name_not_found)
        self.assertIsNone(result)

