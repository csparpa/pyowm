#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from pyowm import owm


class TestSecureAPICalls(unittest.TestCase):

    __owm = owm.OWM(os.getenv('OWM_API_KEY', None))

    def test_ssl(self):

        # Try to call the OWM API using SSL and certificate validation
        self.__owm.config['connection']['use_ssl'] = True

        # weather API
        wm = self.__owm.weather_manager()
        wm.weather_at_place('London,GB')

        # pollution API
        um = self.__owm.uvindex_manager()
        um.uvindex_around_coords(-22.57, -43.12)

        # stations API
        mgr = self.__owm.stations_manager()
        mgr.get_stations()


if __name__ == '__main__':
    unittest.main()
