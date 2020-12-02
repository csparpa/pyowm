#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.commons.http_client import HttpClient
from pyowm.constants import UVINDEX_API_VERSION
from pyowm.utils import formatting, geo, timestamps
from pyowm.uvindexapi30 import uv_client, uvindex
from pyowm.uvindexapi30.uris import ROOT_UV_API_URL


class UVIndexManager:

    """
    A manager objects that provides a full interface to OWM UV Index API.

    :param API_key: the OWM UV Index API key
    :type API_key: str
    :param config: the configuration dictionary
    :type config: dict
    :returns: a *UVIndexManager* instance
    :raises: *AssertionError* when no API Key is provided

    """

    def __init__(self, API_key, config):
        assert API_key is not None, 'You must provide a valid API Key'
        self.API_key = API_key
        assert isinstance(config, dict)
        self.uv_client = uv_client.UltraVioletHttpClient(
            API_key, HttpClient(API_key, config, ROOT_UV_API_URL))

    def uvindex_api_version(self):
        return UVINDEX_API_VERSION

    def uvindex_around_coords(self, lat, lon):
        """
        Queries for Ultra Violet value sampled in the
        surroundings of the provided geocoordinates and in the specified time
        interval. A *UVIndex* object instance is returned, encapsulating a
        *Location* object and the UV intensity value.

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :return: a *UVIndex* instance or ``None`` if data is not available
        :raises: *ParseResponseException* when OWM UV Index API responses' data
            cannot be parsed, *APICallException* when OWM UV Index API can not be
            reached, *ValueError* for wrong input values
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        params = {'lon': lon, 'lat': lat}
        json_data = self.uv_client.get_uvi(params)
        return uvindex.UVIndex.from_dict(json_data)

    def uvindex_forecast_around_coords(self, lat, lon):
        """
        Queries for forecast Ultra Violet values in the next 8
        days in the surroundings of the provided geocoordinates.

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :return: a list of *UVIndex* instances or empty list if data is not available
        :raises: *ParseResponseException* when OWM UV Index API responses' data
            cannot be parsed, *APICallException* when OWM UV Index API can not be
            reached, *ValueError* for wrong input values
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        params = {'lon': lon, 'lat': lat}
        json_data = self.uv_client.get_uvi_forecast(params)
        return [uvindex.UVIndex.from_dict(item) for item in json_data]

    def uvindex_history_around_coords(self, lat, lon, start, end=None):
        """
        Queries for UV index historical values in the
        surroundings of the provided geocoordinates and in the specified
        time frame. If the end of the time frame is not provided, that is
        intended to be the current datetime.

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param start: the object conveying the time value for the start query boundary
        :type start: int, ``datetime.datetime`` or ISO8601-formatted string
        :param end: the object conveying the time value for the end query
            boundary (defaults to ``None``, in which case the current datetime
            will be used)
        :type end: int, ``datetime.datetime`` or ISO8601-formatted string
        :return: a list of *UVIndex* instances or empty list if data is not available
        :raises: *ParseResponseException* when OWM UV Index API responses' data
            cannot be parsed, *APICallException* when OWM UV Index API can not be
            reached, *ValueError* for wrong input values
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        assert start is not None
        start = formatting.timeformat(start, 'unix')
        if end is None:
            end = timestamps.now(timeformat='unix')
        else:
            end = formatting.timeformat(end, 'unix')
        params = {'lon': lon, 'lat': lat, 'start': start, 'end': end}
        json_data = self.uv_client.get_uvi_history(params)
        return [uvindex.UVIndex.from_dict(item) for item in json_data]

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)