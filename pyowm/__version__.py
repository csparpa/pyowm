#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm import constants
from pyowm.utils.strings import version_tuple_to_str

__title__ = 'pyowm'
__description__ = 'A Python wrapper around OpenWeatherMap web APIs'
__url__ = 'https://github.com/csparpa/pyowm'
__version__ = version_tuple_to_str(constants.PYOWM_VERSION)
__author__ = 'Claudio Sparpaglione'
__author_email__ = 'csparpa@gmail.com'
__license__ = 'MIT'
