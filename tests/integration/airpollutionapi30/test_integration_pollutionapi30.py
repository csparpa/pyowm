#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from pyowm import owm


class IntegrationTestsPollutionAPI30(unittest.TestCase):

    __owm = owm.OWM(os.getenv('OWM_API_KEY', None)).airpollution_manager()

    def test_air_quality_at_coords(self):
        """
        Test feature: get all air quality data around geo-coordinates.
        """
        airstatus = self.__owm.air_quality_at_coords(45, 9)
        self.assertIsNotNone(airstatus)
        self.assertIsNotNone(airstatus.air_quality_data)
        self.assertIsNotNone(airstatus.reception_time())
        self.assertIsNotNone(airstatus.reference_time())
        self.assertIsNotNone(airstatus.location)

    def test_air_quality_forecast_at_coords(self):
        """
        Test feature: get all forecasted air quality data around geo-coordinates.
        """
        list_of_airstatuses = self.__owm.air_quality_forecast_at_coords(45, 9)
        self.assertTrue(list_of_airstatuses)
        for airstatus in list_of_airstatuses:
            self.assertIsNotNone(airstatus.air_quality_data)
            self.assertIsNotNone(airstatus.reception_time())
            self.assertIsNotNone(airstatus.reference_time())
            self.assertIsNotNone(airstatus.location)


if __name__ == "__main__":
    unittest.main()
