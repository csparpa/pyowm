#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from pyowm import owm
from pyowm.weatherapi30.location import Location


class IntegrationTestsGeocodingAPI(unittest.TestCase):

    __owm = owm.OWM(os.getenv('OWM_API_KEY', None))

    def test_geocode(self):
        mgr = self.__owm.geocoding_manager()

        # Geocode all Paris in the United States
        locations = mgr.geocode('Paris', 'US')
        self.assertTrue(isinstance(locations, list))
        self.assertTrue(all([isinstance(l, Location) for l in locations]))
        self.assertTrue(all([l.name == 'Paris' and l.country == 'US' for l in locations]))

    def test_reverse_geocode(self):
        mgr = self.__owm.geocoding_manager()

        # Reverse geocode the geocoords for Florence (Italy)
        locations = mgr.reverse_geocode(43.783731, 11.246603)
        self.assertTrue(isinstance(locations, list))
        self.assertTrue(all([isinstance(l, Location) for l in locations]))
        self.assertTrue(all([l.name == 'Firenze' and l.country == 'IT' for l in locations]))

