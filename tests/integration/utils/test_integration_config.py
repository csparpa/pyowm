#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import unittest

import pyowm.commons.exceptions
from pyowm.utils import config
from pyowm.exceptions import config_error


class TesIntegrationConfig(unittest.TestCase):

    def test_get_config_from(self):
        config_file_name = 'test_config.json'
        path = (pathlib.Path() / config_file_name).absolute()
        result = config.get_config_from(path)
        self.assertIsInstance(result, dict)

        path = 'non_json'
        self.assertRaises(pyowm.commons.exceptions.ConfigurationParseError, config.get_config_from, path)


if __name__ == "__main__":
    unittest.main()
