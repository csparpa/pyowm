#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pathlib
import pyowm.commons.exceptions
from pyowm.commons.enums import SubscriptionTypeEnum
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

    def test_get_default_config_for_subscription_type(self):
        result = config.get_default_config_for_subscription_type('free')
        self.assertEqual(SubscriptionTypeEnum.FREE, result['subscription_type'])
        result = config.get_default_config_for_subscription_type('startup')
        self.assertEqual(SubscriptionTypeEnum.STARTUP, result['subscription_type'])
        result = config.get_default_config_for_subscription_type('developer')
        self.assertEqual(SubscriptionTypeEnum.DEVELOPER, result['subscription_type'])
        result = config.get_default_config_for_subscription_type('professional')
        self.assertEqual(SubscriptionTypeEnum.PROFESSIONAL, result['subscription_type'])
        result = config.get_default_config_for_subscription_type('enterprise')
        self.assertEqual(SubscriptionTypeEnum.ENTERPRISE, result['subscription_type'])
        with self.assertRaises(ValueError):
            config.get_default_config_for_subscription_type('non-existent')

    def test_get_default_config_for_proxy(self):
        test_url_1 = 'abc'
        test_url_2 = 'def'
        result = config.get_default_config_for_proxy(test_url_1, test_url_2)
        self.assertTrue(result['connection']['use_proxy'])
        self.assertEqual(result['proxies']['http'], test_url_1)
        self.assertEqual(result['proxies']['https'], test_url_2)
