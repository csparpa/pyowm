#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.weatherapi25 import weathercoderegistry, cityidregistry


"""
Configuration for the PyOWM library specific to OWM Weather API version 2.5
"""

# Subdomains mapping
API_SUBSCRIPTION_SUBDOMAINS = {
    'free': 'api',
    'pro': 'pro'
}

# Default usage of SSL on OWM API calls
USE_SSL = False
VERIFY_SSL_CERTS = True


# Parser objects injection for OWM Weather API responses parsing
parsers = {}

# City ID registry
city_id_registry = cityidregistry.CityIDRegistry('cityids/%03d-%03d.txt.gz')

# Cache provider to be used
cache = None

# Default language for OWM Weather API queries text results
language = 'en'

# Default API subscription type ('free' or 'pro')
API_SUBSCRIPTION_TYPE = 'free'

# OWM Weather API availability timeout in seconds
API_AVAILABILITY_TIMEOUT = 5
