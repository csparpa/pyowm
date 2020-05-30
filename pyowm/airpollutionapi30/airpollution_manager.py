#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.airpollutionapi30 import airpollution_client, coindex, no2index, ozone, so2index
from pyowm.airpollutionapi30.uris import ROOT_POLLUTION_API_URL
from pyowm.commons.http_client import HttpClient
from pyowm.constants import AIRPOLLUTION_API_VERSION
from pyowm.utils import geo


class AirPollutionManager:

    """
    A manager objects that provides a full interface to OWM Air Pollution API.

    :param API_key: the OWM AirPollution API key
    :type API_key: str
    :param config: the configuration dictionary
    :type config: dict
    :returns: an *AirPollutionManager* instance
    :raises: *AssertionError* when no API Key is provided

    """

    def __init__(self, API_key, config):
        assert API_key is not None, 'You must provide a valid API Key'
        self.API_key = API_key
        assert isinstance(config, dict)
        self.ap_client = airpollution_client.AirPollutionHttpClient(
            API_key,
            HttpClient(API_key, config, ROOT_POLLUTION_API_URL))

    def airpollution_api_version(self):
        return AIRPOLLUTION_API_VERSION

    def coindex_around_coords(self, lat, lon, start=None, interval=None):
        """
        Queries the OWM AirPollution API for Carbon Monoxide values sampled in the
        surroundings of the provided geocoordinates and in the specified time
        interval.
        A *COIndex* object instance is returned, encapsulating a
        *Location* object and the list of CO samples
        If `start` is not provided, the latest available CO samples are
        retrieved
        If `start` is provided but `interval` is not, then `interval` defaults
        to the maximum extent, which is: `year`

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param start: the object conveying the start value of the search time
            window start (defaults to ``None``). If not provided, the latest
            available CO samples value are retrieved
        :type start: int, ``datetime.datetime`` or ISO8601-formatted
            string
        :param interval: the length of the search time window starting at
           `start` (defaults to ``None``). If not provided, 'year' is used
        :type interval: str among: 'minute', 'hour', 'day', 'month, 'year'
        :return: a *COIndex* instance or ``None`` if data is not available
        :raises: *ParseResponseException* when OWM AirPollution API responses' data
            cannot be parsed, *APICallException* when OWM AirPollution API can not be
            reached, *ValueError* for wrong input values
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        params = {'lon': lon, 'lat': lat, 'start': start, 'interval': interval}
        json_data = self.ap_client.get_coi(params)
        coi = coindex.COIndex.from_dict(json_data)
        if interval is None:
            interval = 'year'
        coi.interval = interval
        return coi

    def ozone_around_coords(self, lat, lon, start=None, interval=None):
        """
        Queries the OWM AirPollution API for Ozone (O3) value in Dobson Units sampled in
        the surroundings of the provided geocoordinates and in the specified
        time interval. An *Ozone* object instance is returned, encapsulating a
        *Location* object and the UV intensity value.
        If `start` is not provided, the latest available ozone value is
        retrieved.
        If `start` is provided but `interval` is not, then `interval` defaults
        to the maximum extent, which is: `year`

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param start: the object conveying the start value of the search time
            window start (defaults to ``None``). If not provided, the latest
            available Ozone value is retrieved
        :type start: int, ``datetime.datetime`` or ISO8601-formatted
            string
        :param interval: the length of the search time window starting at
           `start` (defaults to ``None``). If not provided, 'year' is used
        :type interval: str among: 'minute', 'hour', 'day', 'month, 'year'
        :return: an *Ozone* instance or ``None`` if data is not available
        :raises: *ParseResponseException* when OWM AirPollution API responses' data
            cannot be parsed, *APICallException* when OWM AirPollution API can not be
            reached, *ValueError* for wrong input values
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        params = {'lon': lon, 'lat': lat, 'start': start, 'interval': interval}
        json_data = self.ap_client.get_o3(params)
        oz = ozone.Ozone.from_dict(json_data)
        if interval is None:
            interval = 'year'
        oz.interval = interval
        return oz

    def no2index_around_coords(self, lat, lon, start=None, interval=None):
        """
        Queries the OWM AirPollution API for Nitrogen Dioxide values sampled in the
        surroundings of the provided geocoordinates and in the specified time
        interval.
        A *NO2Index* object instance is returned, encapsulating a
        *Location* object and the list of NO2 samples
        If `start` is not provided, the latest available NO2 samples are
        retrieved
        If `start` is provided but `interval` is not, then `interval` defaults
        to the maximum extent, which is: `year`

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param start: the object conveying the start value of the search time
            window start (defaults to ``None``). If not provided, the latest
            available NO2 samples value are retrieved
        :type start: int, ``datetime.datetime`` or ISO8601-formatted
            string
        :param interval: the length of the search time window starting at
           `start` (defaults to ``None``). If not provided, 'year' is used
        :type interval: str among: 'minute', 'hour', 'day', 'month, 'year'
        :return: a *NO2Index* instance or ``None`` if data is not available
        :raises: *ParseResponseException* when OWM AirPollution API responses' data
            cannot be parsed, *APICallException* when OWM AirPollution API can not be
            reached, *ValueError* for wrong input values
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        params = {'lon': lon, 'lat': lat, 'start': start, 'interval': interval}
        json_data = self.ap_client.get_no2(params)
        no2 = no2index.NO2Index.from_dict(json_data)
        if interval is None:
            interval = 'year'
        no2.interval = interval
        return no2

    def so2index_around_coords(self, lat, lon, start=None, interval=None):
        """
        Queries the OWM AirPollution API for Sulphur Dioxide values sampled in the
        surroundings of the provided geocoordinates and in the specified time
        interval.
        A *SO2Index* object instance is returned, encapsulating a
        *Location* object and the list of SO2 samples
        If `start` is not provided, the latest available SO2 samples are
        retrieved
        If `start` is provided but `interval` is not, then `interval` defaults
        to the maximum extent, which is: `year`

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param start: the object conveying the start value of the search time
            window start (defaults to ``None``). If not provided, the latest
            available SO2 samples value are retrieved
        :type start: int, ``datetime.datetime`` or ISO8601-formatted
            string
        :param interval: the length of the search time window starting at
           `start` (defaults to ``None``). If not provided, 'year' is used
        :type interval: str among: 'minute', 'hour', 'day', 'month, 'year'
        :return: a *SO2Index* instance or ``None`` if data is not available
        :raises: *ParseResponseException* when OWM AirPollution API responses' data
            cannot be parsed, *APICallException* when OWM AirPollution API can not be
            reached, *ValueError* for wrong input values
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        params = {'lon': lon, 'lat': lat, 'start': start, 'interval': interval}
        json_data = self.ap_client.get_so2(params)
        so2 = so2index.SO2Index.from_dict(json_data)
        if interval is None:
            interval = 'year'
        so2.interval = interval
        return so2

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)
