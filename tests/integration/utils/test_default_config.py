#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pyowm.config import DEFAULT_CONFIG


class TesDefaultConfig(unittest.TestCase):

    def test_default_config_is_complete(self):

        # default fake API key
        self.assertTrue('api_key' in DEFAULT_CONFIG)

        # subscription type is free
        self.assertTrue('subscription_type' in DEFAULT_CONFIG)
        self.assertEqual('free', DEFAULT_CONFIG['subscription_type'])

        # language is English
        self.assertTrue('language' in DEFAULT_CONFIG)
        self.assertEqual('en', DEFAULT_CONFIG['language'])

        # connection is a sub-dict, check its keys
        self.assertTrue('connection' in DEFAULT_CONFIG)
        connection = DEFAULT_CONFIG['connection']
        self.assertIsInstance(connection, dict)

        self.assertTrue('use_ssl' in connection)
        self.assertEqual(False, connection['use_ssl'])

        self.assertTrue('verify_ssl_certs' in connection)
        self.assertEqual(True, connection['verify_ssl_certs'])

        self.assertTrue('timeout_secs' in connection)
        self.assertEqual(2, connection['timeout_secs'])

