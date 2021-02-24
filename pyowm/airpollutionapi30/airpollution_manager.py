#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.airpollutionapi30 import airpollution_client, coindex, no2index, ozone, so2index, airstatus
from pyowm.airpollutionapi30.uris import ROOT_POLLUTION_API_URL, NEW_ROOT_POLLUTION_API_URL
from pyowm.commons.http_client import HttpClient
from pyowm.constants import AIRPOLLUTION_API_VERSION
from pyowm.utils import geo, decorators, formatting, timestamps


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
        self.new_ap_client = airpollution_client.AirPollutionHttpClient(
            API_key,
            HttpClient(API_key, config, NEW_ROOT_POLLUTION_API_URL))

    def airpollution_api_version(self):
        return AIRPOLLUTION_API_VERSION

    @decorators.deprecated('removed', '4', 'coindex_around_coords')
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

    @decorators.deprecated('removed', '4', 'ozone_around_coords')
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

    @decorators.deprecated('removed', '4', 'no2index_around_coords')
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

    @decorators.deprecated('removed', '4', 'so2index_around_coords')
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

    def air_quality_at_coords(self, lat, lon):
        """
        Queries the OWM AirPollution API for available air quality indicators around the specified coordinates.

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :return: a *AirStatus* instance or ``None`` if data is not available
        :raises: *ParseResponseException* when OWM AirPollution API responses' data
            cannot be parsed, *APICallException* when OWM AirPollution API can not be
            reached, *ValueError* for wrong input values
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        params = {'lon': lon, 'lat': lat}
        json_data = self.new_ap_client.get_air_pollution(params)
        try:
            return airstatus.AirStatus.from_dict(json_data)
        except:
            return None

    def air_quality_forecast_at_coords(self, lat, lon):
        """
        Queries the OWM AirPollution API for available forecasted air quality indicators around the specified coordinates.

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :return: a `list` of *AirStatus* instances or an empty `list` if data is not available
        :raises: *ParseResponseException* when OWM AirPollution API responses' data
            cannot be parsed, *APICallException* when OWM AirPollution API can not be
            reached, *ValueError* for wrong input values
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        params = {'lon': lon, 'lat': lat}
        json_data = self.new_ap_client.get_forecast_air_pollution(params)
        try:
            return airstatus.AirStatus.from_dict(json_data)
        except:
            return []

    def air_quality_history_at_coords(self, lat, lon, start, end=None):
        """
        Queries the OWM AirPollution API for available forecasted air quality indicators around the specified coordinates.

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param start: the object conveying the start value of the search time window
        :type start: int, ``datetime.datetime`` or ISO8601-formatted string
        :param end: the object conveying the end value of the search time window. Values in the future will be clipped
           to the current timestamp. Defaults to the current UNIX timestamp.
        :type end: int, ``datetime.datetime`` or ISO8601-formatted string
        :return: a `list` of *AirStatus* instances or an empty `list` if data is not available
        :raises: *ParseResponseException* when OWM AirPollution API responses' data
            cannot be parsed, *APICallException* when OWM AirPollution API can not be
            reached, *ValueError* for wrong input values
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        now = timestamps.now(timeformat='unix')
        assert start is not None
        start = formatting.timeformat(start, 'unix')
        if end is None:
            end = now
        else:
            end = formatting.timeformat(end, 'unix')
            if end > now:
                end = now

        params = {'lon': lon, 'lat': lat, 'start': start, 'end': end}
        json_data = self.new_ap_client.get_historical_air_pollution(params)
        try:
            return airstatus.AirStatus.from_dict(json_data)
        except:
            return []

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)
