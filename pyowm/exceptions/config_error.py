#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.exceptions import OWMError


class ConfigurationNotFoundError(OWMError):
    """Raised when configuration source file is not available"""
    pass


class ConfigurationParseError(OWMError):
    """Raised on failures in parsing configuration data"""
    pass
