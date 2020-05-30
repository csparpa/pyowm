#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from unittest.mock import patch

from pyowm.commons.image import Image, ImageTypeEnum
from pyowm.agroapi10.enums import PresetEnum, SatelliteEnum
from pyowm.agroapi10.imagery import MetaImage, SatelliteImage
from pyowm.utils.formatting import UTC


class TestMetaImage(unittest.TestCase):

    test_acquisition_time = 1378459200
    test_iso_acquisition_time = "2013-09-06 09:20:00+00"
    test_date_acquisition_time = datetime.strptime(test_iso_acquisition_time, '%Y-%m-%d %H:%M:%S+00').replace(
        tzinfo=UTC())

    test_instance = MetaImage('http://a.com', PresetEnum.FALSE_COLOR,
                              SatelliteEnum.SENTINEL_2.name, test_acquisition_time, 98.2, 0.3, 11.7, 7.89,
                              polygon_id='my_polygon', stats_url='http://stats.com')

    def test_init_fails_with_wrong_parameters(self):
        self.assertRaises(AssertionError, MetaImage, None, PresetEnum.FALSE_COLOR,
                          SatelliteEnum.SENTINEL_2.name, self.test_acquisition_time, 98.2, 0.3, 11.7, 7.89)
        self.assertRaises(AssertionError, MetaImage, 'http://a.com', PresetEnum.FALSE_COLOR,
                          SatelliteEnum.SENTINEL_2.name, 'a_string', 98.2, 0.3, 11.7, 7.89)
        self.assertRaises(AssertionError, MetaImage, 'http://a.com', PresetEnum.FALSE_COLOR,
                          SatelliteEnum.SENTINEL_2.name, -567, 98.2, 0.3, 11.7, 7.89)
        self.assertRaises(AssertionError, MetaImage, 'http://a.com', PresetEnum.FALSE_COLOR,
                          SatelliteEnum.SENTINEL_2.name, self.test_acquisition_time, 'a_string', 0.3, 11.7, 7.89)
        self.assertRaises(AssertionError, MetaImage, 'http://a.com', PresetEnum.FALSE_COLOR,
                          SatelliteEnum.SENTINEL_2.name, self.test_acquisition_time, -32.1, 0.3, 11.7, 7.89)

        self.assertRaises(AssertionError, MetaImage, 'http://a.com', PresetEnum.FALSE_COLOR,
                          SatelliteEnum.SENTINEL_2.name, self.test_acquisition_time, 98.2, 'a_string', 11.7, 7.89)
        self.assertRaises(AssertionError, MetaImage, 'http://a.com', PresetEnum.FALSE_COLOR,
                          SatelliteEnum.SENTINEL_2.name, self.test_acquisition_time, 98.2, -21.1, 11.7, 7.89)
        # sun azimuth
        self.assertRaises(AssertionError, MetaImage, 'http://a.com', PresetEnum.FALSE_COLOR,
                          SatelliteEnum.SENTINEL_2.name, self.test_acquisition_time, 98.2, 21.1, 'a_string', 7.89)
        self.assertRaises(AssertionError, MetaImage, 'http://a.com', PresetEnum.FALSE_COLOR,
                          SatelliteEnum.SENTINEL_2, self.test_acquisition_time, 98.2, 21.1, -54.4, 7.89)
        self.assertRaises(AssertionError, MetaImage, 'http://a.com', PresetEnum.FALSE_COLOR,
                          SatelliteEnum.SENTINEL_2.name, self.test_acquisition_time, 98.2, 21.1, 368.4, 7.89)
        # sun elevation
        self.assertRaises(AssertionError, MetaImage, 'http://a.com', PresetEnum.FALSE_COLOR,
                          SatelliteEnum.SENTINEL_2.name, self.test_acquisition_time, 98.2, 21.1, 54.4, 'a_string')
        self.assertRaises(AssertionError, MetaImage, 'http://a.com', PresetEnum.FALSE_COLOR,
                          SatelliteEnum.SENTINEL_2.name, self.test_acquisition_time, 98.2, 21.1, 54.4, -32.2)
        self.assertRaises(AssertionError, MetaImage, 'http://a.com', PresetEnum.FALSE_COLOR,
                          SatelliteEnum.SENTINEL_2.name, self.test_acquisition_time, 98.2, 21.1, 54.4, 100.3)

    def test_acquisition_time_returning_different_formats(self):

        self.assertEqual(self.test_instance.acquisition_time(timeformat='unix'),
                         self.test_acquisition_time)
        self.assertEqual(self.test_instance.acquisition_time(timeformat='iso'),
                         self.test_iso_acquisition_time)
        self.assertEqual(self.test_instance.acquisition_time(timeformat='date'),
                         self.test_date_acquisition_time)

    def test_acquisition_time_fails_with_unknown_timeformat(self):
        self.assertRaises(ValueError, MetaImage.acquisition_time, self.test_instance, 'xyz')

    def test_repr(self):
        repr(self.test_instance)


class TestSatelliteImage(unittest.TestCase):

        test_image = Image(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x00\x00\x00\x01', ImageTypeEnum.PNG)
        test_instance = SatelliteImage(TestMetaImage.test_instance, test_image,
                                       downloaded_on=TestMetaImage.test_acquisition_time)

        def test_init_fails_with_wrong_parameters(self):
            with self.assertRaises(AssertionError):
                SatelliteImage(None, self.test_image)
            with self.assertRaises(AssertionError):
                SatelliteImage(TestMetaImage.test_instance, None)
            with self.assertRaises(AssertionError):
                SatelliteImage(TestMetaImage.test_instance, self.test_image, downloaded_on='not_an_int')
            with self.assertRaises(AssertionError):
                SatelliteImage(TestMetaImage.test_instance, self.test_image, downloaded_on=1234567, palette=888)

        def test_downloaded_on_returning_different_formats(self):
            self.assertEqual(self.test_instance.downloaded_on(timeformat='unix'),
                             TestMetaImage.test_acquisition_time)
            self.assertEqual(self.test_instance.downloaded_on(timeformat='iso'),
                             TestMetaImage.test_iso_acquisition_time)
            self.assertEqual(self.test_instance.downloaded_on(timeformat='date'),
                             TestMetaImage.test_date_acquisition_time)

        def test_downloaded_on_fails_with_unknown_timeformat(self):
            self.assertRaises(ValueError, SatelliteImage.downloaded_on, self.test_instance, 'xyz')

        def test_repr(self):
            repr(self.test_instance)

        def test_init(self):
            test_instance = SatelliteImage(TestMetaImage.test_instance, self.test_image)

            self.assertFalse(hasattr(test_instance, '_downloaded_on'))

        def test_persist(self):
            with patch('builtins.open', unittest.mock.mock_open()) as mocked_open:
                persists = self.test_instance.persist('filename')
                assert persists is None

            mocked_open.assert_called_once_with('filename', 'wb')
