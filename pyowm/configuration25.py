#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Subdomains mapping
API_SUBSCRIPTION_SUBDOMAINS = {
    'free': 'api',
    'pro': 'pro'
}

# Default usage of SSL on OWM API calls
USE_SSL = False
VERIFY_SSL_CERTS = True

# Default language for OWM Weather API queries text results
language = 'en'

# Default API subscription type ('free' or 'pro')
API_SUBSCRIPTION_TYPE = 'free'

# OWM Weather API availability timeout in seconds
API_AVAILABILITY_TIMEOUT = 5
