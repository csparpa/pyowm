#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pyowm.commons.enums import SubscriptionTypeEnum
from pyowm.config import DEFAULT_CONFIG


class TesDefaultConfig(unittest.TestCase):

    def test_default_config_is_complete(self):

        # subscription type is free
        self.assertTrue('subscription_type' in DEFAULT_CONFIG)
        self.assertEqual(SubscriptionTypeEnum.FREE, DEFAULT_CONFIG['subscription_type'])

        # language is English
        self.assertTrue('language' in DEFAULT_CONFIG)
        self.assertEqual('en', DEFAULT_CONFIG['language'])

        # connection is a sub-dict, check its keys
        self.assertTrue('connection' in DEFAULT_CONFIG)
        connection = DEFAULT_CONFIG['connection']
        self.assertIsInstance(connection, dict)

        self.assertTrue('use_ssl' in connection)
        self.assertTrue(connection['use_ssl'])

        self.assertTrue('verify_ssl_certs' in connection)
        self.assertTrue(connection['verify_ssl_certs'])

        self.assertTrue('use_proxy' in connection)
        self.assertFalse(connection['use_proxy'])

        self.assertTrue('timeout_secs' in connection)
        self.assertEqual(5, connection['timeout_secs'])

        # proxies is a sub-dict, check its keys
        self.assertTrue('proxies' in DEFAULT_CONFIG)
        proxies = DEFAULT_CONFIG['proxies']
        self.assertIsInstance(proxies, dict)

        self.assertTrue('http' in  proxies)
        self.assertTrue('https' in  proxies)

