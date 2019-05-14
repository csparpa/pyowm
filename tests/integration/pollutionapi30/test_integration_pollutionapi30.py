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
        self.assertIsNotNone(u.get_co_samples())
        self.assertIsNotNone(u.get_reception_time())
        self.assertIsNotNone(u.get_reference_time())
        self.assertIsNotNone(u.get_interval())
        self.assertIsNotNone(u.get_location())

    def test_ozone_around_coords(self):
        """
        Test feature: get ozone around geo-coordinates.
        """
        u = self.__owm.ozone_around_coords(0.0, 10.0, start='2016-12-31 12:55:55+00')
        self.assertIsNotNone(u)
        self.assertIsNotNone(u.get_du_value())
        self.assertIsNotNone(u.get_reception_time())
        self.assertIsNotNone(u.get_reference_time())
        self.assertIsNotNone(u.get_interval())
        self.assertIsNotNone(u.get_location())

    def test_no2index_around_coords(self):
        """
        Test feature: get NO2 index around geo-coordinates.
        """
        u = self.__owm.no2index_around_coords(0.0, 10.0, start='2016-12-31 12:55:55+00')
        self.assertIsNotNone(u)
        self.assertIsNotNone(u.get_no2_samples())
        self.assertIsNotNone(u.get_reception_time())
        self.assertIsNotNone(u.get_reference_time())
        self.assertIsNotNone(u.get_interval())
        self.assertIsNotNone(u.get_location())

    def test_so2index_around_coords(self):
        """
        Test feature: get SO2 index around geo-coordinates.
        """
        u = self.__owm.so2index_around_coords(0.0, 10.0, start='2016-12-31 12:55:55+00')
        self.assertIsNotNone(u)
        self.assertIsNotNone(u.get_so2_samples())
        self.assertIsNotNone(u.get_reception_time())
        self.assertIsNotNone(u.get_reference_time())
        self.assertIsNotNone(u.get_interval())
        self.assertIsNotNone(u.get_location())


if __name__ == "__main__":
    unittest.main()