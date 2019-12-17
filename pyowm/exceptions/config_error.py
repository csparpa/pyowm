#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.exceptions import PyOWMError


class ConfigurationNotFoundError(PyOWMError):
    """Raised when configuration source file is not available"""
    pass


class ConfigurationParseError(PyOWMError):
    """Raised on failures in parsing configuration data"""
    pass
