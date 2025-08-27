#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import unittest
import os
from pyowm import owm


class IntegrationTestsPollutionAPI30(unittest.TestCase):

    __owm = owm.OWM(os.getenv('OWM_API_KEY', None)).airpollution_manager()

    def test_air_quality_at_coords(self, lat=45, lon=9):
        """
        Test feature: get all air quality data around geo-coordinates.
        """
        airstatus = self.__owm.air_quality_at_coords(lat, lon)
        self.assertIsNotNone(airstatus)
        self.assertIsNotNone(airstatus.air_quality_data)
        self.assertIsNotNone(airstatus.reception_time())
        self.assertIsNotNone(airstatus.reference_time())
        self.assertIsNotNone(airstatus.location)

    def test_air_quality_at_range_of_coords(self):
        """
        Test feature: tests air quality data around a range of geo-coordinates
        """

        # Cities chosen based on extreme locations in longitude and latitude as well
        # as being major hubs that measure and return air quality data
        geocoords = [
            {'lat': -43.951 , 'lon': -176.561 }, # Waitangi
            {'lat': 21.3294 , 'lon': -157.846 }, # Honolulu
            {'lat': 45.6366 , 'lon': -122.5967}, # Vancouver
            {'lat': 37.7562 , 'lon': -122.443 }, # San Francisco
            {'lat': 64.7333 , 'lon': 177.7    }, # Ugol'nyye Kopi
            {'lat': -77.6554, 'lon': 168.2227 }, # McMurdo Station, Antarctica
            {'lat': -38.6625, 'lon': 178.0178 }, # Gisborne
            {'lat': -18.1333, 'lon': 178.4333 }, # Suva
        ]

        for location in geocoords:
            self.test_air_quality_at_coords(lat=location['lat'], lon=location['lon'])


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

    def test_air_quality_history_at_coords(self):
        """
        Test feature: get historical air quality data around geo-coordinates.
        """
        start = datetime.datetime(2020, 11, 28, tzinfo=datetime.timezone.utc)
        end = datetime.datetime(2020, 12, 31, tzinfo=datetime.timezone.utc)

        list_of_airstatuses = self.__owm.air_quality_history_at_coords(45, 9, start, end)
        self.assertIsInstance(list_of_airstatuses, list)
        for airstatus in list_of_airstatuses:
            self.assertIsNotNone(airstatus.air_quality_data)
            self.assertIsNotNone(airstatus.reception_time())
            self.assertIsNotNone(airstatus.reference_time())
            self.assertIsNotNone(airstatus.location)


if __name__ == "__main__":
    unittest.main()
