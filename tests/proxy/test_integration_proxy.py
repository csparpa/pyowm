#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib
import unittest
from pyowm import OWM
from pyowm.weatherapi25.observation import Observation
from pyowm.utils import config


class TesIntegrationProxy(unittest.TestCase):

    _api_key = os.getenv('OWM_API_KEY', None)

    def test_call_api_behind_http_proxy(self):
        # fetch config and overwrite API Key as per env variable
        config_file_name = 'proxy_http.json'
        path = (pathlib.Path() / config_file_name).absolute()
        cfg = config.get_config_from(path)
        cfg['api_key'] = self._api_key

        # go
        owm = OWM(cfg['api_key'], cfg)
        wm = owm.weather_manager()
        result = wm.weather_at_place('London,GB')
        self.assertIsInstance(result, Observation)

    def test_call_api_behind_socks_proxy(self):
        # fetch config and overwrite API Key as per env variable
        config_file_name = 'proxy_socks.json'
        path = (pathlib.Path() / config_file_name).absolute()
        cfg = config.get_config_from(path)
        cfg['api_key'] = self._api_key

        # go
        owm = OWM(cfg['api_key'], cfg)
        wm = owm.weather_manager()
        result = wm.weather_at_place('London,GB')
        self.assertIsInstance(result, Observation)


if __name__ == "__main__":
    unittest.main()
