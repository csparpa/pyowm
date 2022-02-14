#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.commons.enums import SubscriptionTypeEnum

DEFAULT_CONFIG = {
    'subscription_type': SubscriptionTypeEnum.FREE,
    'language': 'en',
    'connection': {
        'use_ssl': True,
        'verify_ssl_certs': True,
        'use_proxy': False,
        'timeout_secs': 5,
        'max_retries': None
    },
    'proxies': {
        'http': 'http://user:pass@host:port',
        'https': 'socks5://user:pass@host:port'
    }
}
