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
        wm = self.__owm.weather_manager()
        try:
            # weather API
            wm.weather_at_place('London,GB')

            # pollution API
            wm.uvindex_around_coords(-22.57, -43.12)

            # stations API
            mgr = self.__owm.stations_manager()
            mgr.get_stations()

        except Exception as e:
            self.fail(str(e))


if __name__ == '__main__':
    unittest.main()
