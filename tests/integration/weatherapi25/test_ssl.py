# -*- coding: utf-8 -*-

import unittest
import os
from pyowm.constants import DEFAULT_API_KEY
from pyowm.weatherapi25.configuration25 import parsers
from pyowm.weatherapi25.owm25 import OWM25


class TestSecureAPICalls(unittest.TestCase):

    __API_key = os.getenv('OWM_API_KEY', DEFAULT_API_KEY)

    def test_ssl(self):

        # Try to call the OWM API using SSL and certificate validation
        owm = OWM25(parsers, API_key=self.__API_key, use_ssl=True)
        try:
            # weather API
            owm.weather_at_place('London,GB')

            # pollution API
            owm.uvindex_around_coords(-22.57, -43.12)

            # stations API
            mgr = owm.stations_manager()
            mgr.get_stations()

        except Exception as e:
            self.fail(str(e))


if __name__ == '__main__':
    unittest.main()
