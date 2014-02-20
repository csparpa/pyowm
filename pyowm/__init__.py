#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The PyOWM init file

**Author**: Claudio Sparpaglione, @csparpa <csparpa@gmail.com>

**Platform**: platform independent

"""

from pyowm import constants
from pyowm.utils import timeutils  # Convenience import


def OWM(API_key=None, version=constants.LATEST_OWM_API_VERSION):
    """
    A parametrized factory method returning a global OWM instance that
    represents the desired OWM web API version (or the currently supported one
    if no version number is specified

    :param API_key: the OWM web API key (``None`` by default)
    :type API_key: str
    :param version: the OWM web API version. Defaults to ``None``, which means
        use the latest web API version
    :type version: str
    :returns: an instance of a proper *OWM* subclass
    :raises: *ValueError* when unsupported OWM API versions are provided
    """
    if version == "2.5":
        from webapi25.configuration25 import parsers
        from webapi25.configuration25 import cache
        from webapi25.owm25 import OWM25
        return OWM25(parsers, API_key, cache)
    raise ValueError("Unsupported OWM web API version")
