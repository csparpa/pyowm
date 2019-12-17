#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pathlib
import pyowm.commons.exceptions
from pyowm.config import DEFAULT_CONFIG
from pyowm.utils import config


class TestConfig(unittest.TestCase):

    def test_get_default_config(self):
        result = config.get_default_config()
        self.assertEqual(result, DEFAULT_CONFIG)

    def test_get_config_from_failing(self):
        self.assertRaises(AssertionError, config.get_config_from, None)
        self.assertRaises(pyowm.commons.exceptions.ConfigurationNotFoundError, config.get_config_from,
                          str(pathlib.Path('.').absolute()))
