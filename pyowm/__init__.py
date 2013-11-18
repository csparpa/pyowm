#!/usr/bin/env python

"""
The PyOWM init file

**Author**: Claudio Sparpaglione, @csparpa <claspock@hotmail.com>

**Platform**: platform independent

"""

from location import Location
from weather import Weather
from observation import Observation
from forecast import Forecast
from forecaster import Forecaster
from stationhistory import StationHistory
from utils import timeutils
from owm25 import OWM25

#Factory
def OWM(API_key=None, version=None):
    if version is None:  # return the latest version
        return OWM25(API_key)
    if version == "2.5":
        return OWM25(API_key)