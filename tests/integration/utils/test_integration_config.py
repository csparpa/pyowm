#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import unittest

import pyowm.commons.exceptions
from pyowm.utils import config


class TesIntegrationConfig(unittest.TestCase):

    def test_get_config_from(self):
        config_file_name = 'test_config.json'
        path = (pathlib.Path(__file__).parent / config_file_name).absolute()
        result = config.get_config_from(path)
        self.assertIsInstance(result, dict)

        config_file_name = 'non_json'
        path = (pathlib.Path(__file__).parent / config_file_name).absolute()
        self.assertRaises(pyowm.commons.exceptions.ConfigurationParseError, config.get_config_from, path)


if __name__ == "__main__":
    unittest.main()
