#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from pyowm import owm


class IntegrationTestsPollutionAPI30(unittest.TestCase):

    __owm = owm.OWM(os.getenv('OWM_API_KEY', None)).airpollution_manager()

    def test_coindex_around_coords(self):
        """
        Test feature: get CO index around geo-coordinates.
        """
        u = self.__owm.coindex_around_coords(45, 9)
        self.assertIsNotNone(u)
        self.assertIsNotNone(u.co_samples)
        self.assertIsNotNone(u.reception_time())
        self.assertIsNotNone(u.reference_time())
        self.assertIsNone(u.interval)
        self.assertIsNotNone(u.location)

    def test_ozone_around_coords(self):
        """
        Test feature: get ozone around geo-coordinates.
        """
        u = self.__owm.ozone_around_coords(0.0, 10.0, start='2016-12-31 12:55:55+00:00')
        self.assertIsNotNone(u)
        self.assertIsNotNone(u.du_value)
        self.assertIsNotNone(u.reception_time())
        self.assertIsNotNone(u.reference_time())
        self.assertIsNone(u.interval)
        self.assertIsNotNone(u.location)

    def test_no2index_around_coords(self):
        """
        Test feature: get NO2 index around geo-coordinates.
        """
        u = self.__owm.no2index_around_coords(0.0, 10.0, start='2016-12-31 12:55:55+00:00')
        self.assertIsNotNone(u)
        self.assertIsNotNone(u.no2_samples)
        self.assertIsNotNone(u.reception_time())
        self.assertIsNotNone(u.reference_time())
        self.assertIsNone(u.interval)
        self.assertIsNotNone(u.location)

    def test_so2index_around_coords(self):
        """
        Test feature: get SO2 index around geo-coordinates.
        """
        u = self.__owm.so2index_around_coords(0.0, 10.0, start='2016-12-31 12:55:55+00:00')
        self.assertIsNotNone(u)
        self.assertIsNotNone(u.so2_samples)
        self.assertIsNotNone(u.reception_time())
        self.assertIsNotNone(u.reference_time())
        self.assertIsNone(u.interval)
        self.assertIsNotNone(u.location)


if __name__ == "__main__":
    unittest.main()
