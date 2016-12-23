# -*- coding: utf-8 -*-

"""
Integration tests for the README.md code snippets
These are "live" executions, that of course need the OWM web API to be up
and running
"""

import unittest
import os
from pyowm.constants import DEFAULT_API_KEY
from pyowm import timeutils
from pyowm.webapi25.configuration25 import parsers
from pyowm.webapi25.owm25 import OWM25
from pyowm.webapi25.weather import Weather
from pyowm.webapi25.observation import Observation
from pyowm.webapi25.forecaster import Forecaster


class IntegrationTestsREADMESnippets(unittest.TestCase):

    __owm = OWM25(parsers, os.getenv('OWM_API_KEY', DEFAULT_API_KEY))

    def test_snippets(self):

        # Will it be sunny tomorrow at this time in Milan (Italy) ?
        f_milan = self.__owm.daily_forecast("Milan,it")
        self.assertIsNotNone(f_milan)
        self.assertTrue(isinstance(f_milan, Forecaster))
        tomorrow = timeutils.tomorrow()
        willbesunny = f_milan.will_be_sunny_at(tomorrow)
        self.assertTrue(isinstance(willbesunny, bool))

        # Search for current weather in London (UK)
        o_london = self.__owm.weather_at_place('London,uk')
        self.assertTrue(isinstance(o_london, Observation))
        w_london = o_london.get_weather()
        self.assertTrue(isinstance(w_london, Weather))

        # Weather details
        self.assertIsNotNone(w_london.get_wind())
        self.assertIsNotNone(w_london.get_humidity())
        self.assertIsNotNone(w_london.get_temperature('celsius'))

        # Search current weather observations in the surroundings of
        # lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
        os_rio = self.__owm.weather_around_coords(-22.57, -43.12)
        self.assertIsNotNone(os_rio)
        self.assertTrue(len(os_rio) > 0)
        for o in os_rio:
            self.assertTrue(isinstance(o, Observation))
