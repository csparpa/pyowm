#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging as lg
import unittest
from pyowm.utils import logging


class TestLoggingUtils(unittest.TestCase):

    def test_get_default_logger(self):
        result = logging.get_default_logger()
        result.warning('primo')
        result.error('due')
        result.critical('tre')
        result.debug('non ce')
        self.assertIsInstance(result, lg.Logger)
        self.assertEqual(result.level, lg.WARNING)
