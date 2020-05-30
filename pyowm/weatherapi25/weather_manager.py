#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone
from typing import Union

from pyowm.commons.http_client import HttpClient
from pyowm.constants import WEATHER_API_VERSION
from pyowm.utils import geo
from pyowm.weatherapi25 import forecaster, historian, observation, forecast, stationhistory, one_call
from pyowm.weatherapi25.uris import ROOT_WEATHER_API, OBSERVATION_URI, GROUP_OBSERVATIONS_URI, FIND_OBSERVATIONS_URI, \
    BBOX_CITY_URI, THREE_HOURS_FORECAST_URI, DAILY_FORECAST_URI, STATION_WEATHER_HISTORY_URI, ONE_CALL_URI, \
    ONE_CALL_HISTORICAL_URI


class WeatherManager:
    """
    A manager objects that provides a full interface to OWM Weather API.

    :param API_key: the OWM AirPollution API key
    :type API_key: str
    :param config: the configuration dictionary
    :type config: dict
    :returns: a *WeatherManager* instance
    :raises: *AssertionError* when no API Key is provided

    """

    def __init__(self, API_key, config):
        assert isinstance(API_key, str), 'You must provide a valid API Key'
        self.API_key = API_key
        assert isinstance(config, dict)
        self.http_client = HttpClient(API_key, config, ROOT_WEATHER_API)

    def weather_api_version(self):
        return WEATHER_API_VERSION

    def weather_at_place(self, name):
        """
        Queries the OWM Weather API for the currently observed weather at the
        specified toponym (eg: "London,uk")

        :param name: the location's toponym
        :type name: str
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed or *APICallException* when OWM Weather API can not be
            reached
        """

        assert isinstance(name, str), "Value must be a string"
        params = {'q': name}
        _, json_data = self.http_client.get_json(OBSERVATION_URI, params=params)
        return observation.Observation.from_dict(json_data)

    def weather_at_coords(self, lat, lon):
        """
        Queries the OWM Weather API for the currently observed weather at the
        specified geographic (eg: 51.503614, -0.107331).

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed or *APICallException* when OWM Weather API can not be
            reached
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        params = {'lon': lon, 'lat': lat}
        _, json_data = self.http_client.get_json(OBSERVATION_URI, params=params)
        return observation.Observation.from_dict(json_data)

    def weather_at_zip_code(self, zipcode, country):
        """
        Queries the OWM Weather API for the currently observed weather at the
        specified zip code and country code (eg: 2037, au).

        :param zip: the location's zip or postcode
        :type zip: string
        :param country: the location's country code
        :type country: string
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed or *APICallException* when OWM Weather API can not be
            reached
        """
        assert isinstance(zipcode, str), "Value must be a string"
        assert isinstance(country, str), "Value must be a string"
        zip_param = zipcode + ',' + country
        params = {'zip': zip_param}
        _, json_data = self.http_client.get_json(OBSERVATION_URI, params=params)
        return observation.Observation.from_dict(json_data)

    def weather_at_id(self, id):
        """
        Queries the OWM Weather API for the currently observed weather at the
        specified city ID (eg: 5128581)

        :param id: the location's city ID
        :type id: int
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed or *APICallException* when OWM Weather API can not be
            reached
        """
        assert type(id) is int, "'id' must be an int"
        if id < 0:
            raise ValueError("'id' value must be greater than 0")
        params = {'id': id}
        _, json_data = self.http_client.get_json(OBSERVATION_URI, params=params)
        return observation.Observation.from_dict(json_data)

    def weather_at_ids(self, ids_list):
        """
        Queries the OWM Weather API for the currently observed weathers at the
        specified city IDs (eg: [5128581,87182])

        :param ids_list: the list of city IDs
        :type ids_list: list of int
        :returns: a list of *Observation* instances or an empty list if no
            weather data is available
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed or *APICallException* when OWM Weather API can not be
            reached
        """
        assert type(ids_list) is list, "'ids_list' must be a list of integers"
        for id in ids_list:
            assert type(id) is int, "'ids_list' must be a list of integers"
            if id < 0:
                raise ValueError("id values in 'ids_list' must be greater "
                                 "than 0")
        params = {'id': ','.join(list(map(str, ids_list)))}
        _, json_data = self.http_client.get_json(GROUP_OBSERVATIONS_URI, params=params)
        return observation.Observation.from_dict_of_lists(json_data)

    def weather_at_places(self, pattern, searchtype, limit=None):
        """
        Queries the OWM Weather API for the currently observed weather in all the
        locations whose name is matching the specified text search parameters.
        A twofold search can be issued: *'accurate'* (exact matching) and
        *'like'* (matches names that are similar to the supplied pattern).

        :param pattern: the string pattern (not a regex) to be searched for the
            toponym
        :type pattern: str
        :param searchtype: the search mode to be used, must be *'accurate'* for
          an exact matching or *'like'* for a likelihood matching
        :type: searchtype: str
        :param limit: the maximum number of *Observation* items in the returned
            list (default is ``None``, which stands for any number of items)
        :param limit: int or ``None``
        :returns: a list of *Observation* objects or ``None`` if no weather
            data is available
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed, *APICallException* when OWM Weather API can not be
            reached, *ValueError* when bad value is supplied for the search
            type or the maximum number of items retrieved
        """
        assert isinstance(pattern, str), "'pattern' must be a str"
        assert isinstance(searchtype, str), "'searchtype' must be a str"
        if searchtype != "accurate" and searchtype != "like":
            raise ValueError("'searchtype' value must be 'accurate' or 'like'")
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        params = {'q': pattern, 'type': searchtype}
        if limit is not None:
            # fix for OWM 2.5 API bug!
            params['cnt'] = limit - 1
        _, json_data = self.http_client.get_json(FIND_OBSERVATIONS_URI, params=params)
        return observation.Observation.from_dict_of_lists(json_data)

    def weather_at_places_in_bbox(self, lon_left, lat_bottom, lon_right, lat_top,
                                  zoom=10, cluster=False):
        """
        Queries the OWM Weather API for the weather currently observed by
        meteostations inside the bounding box of latitude/longitude coords.

        :param lat_top: latitude for top margin of bounding box, must be
            between -90.0 and 90.0
        :type lat_top: int/float
        :param lon_left: longitude for left margin of bounding box
            must be between -180.0 and 180.0
        :type lon_left: int/float
        :param lat_bottom: latitude for the bottom margin of bounding box, must
            be between -90.0 and 90.0
        :type lat_bottom: int/float
        :param lon_right: longitude for the right margin of bounding box,
            must be between -180.0 and 180.0
        :type lon_right: int/float
        :param zoom: zoom level (defaults to: 10)
        :type zoom: int
        :param cluster: use server clustering of points
        :type cluster: bool
        :returns: a list of *Observation* objects or ``None`` if no weather
            data is available
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed, *APICallException* when OWM Weather API can not be
            reached, *ValueError* when coordinates values are out of bounds or
            negative values are provided for limit
        """
        geo.assert_is_lon(lon_left)
        geo.assert_is_lon(lon_right)
        geo.assert_is_lat(lat_bottom)
        geo.assert_is_lat(lat_top)
        assert type(zoom) is int, "'zoom' must be an int"
        if zoom <= 0:
            raise ValueError("'zoom' must greater than zero")
        assert type(cluster) is bool, "'cluster' must be a bool"
        params = {'bbox': ','.join([str(lon_left),
                                    str(lat_bottom),
                                    str(lon_right),
                                    str(lat_top),
                                    str(zoom)]),
                  'cluster': 'yes' if cluster else 'no'}
        _, json_data = self.http_client.get_json(BBOX_CITY_URI, params=params)
        return observation.Observation.from_dict_of_lists(json_data)

    def weather_around_coords(self, lat, lon, limit=None):
        """
        Queries the OWM Weather API for the currently observed weather in all the
        locations in the proximity of the specified coordinates.

        :param lat: location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param limit: the maximum number of *Observation* items in the returned
            list (default is ``None``, which stands for any number of items)
        :param limit: int or ``None``
        :returns: a list of *Observation* objects or ``None`` if no weather
            data is available
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed, *APICallException* when OWM Weather API can not be
            reached, *ValueError* when coordinates values are out of bounds or
            negative values are provided for limit
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        params = {'lon': lon, 'lat': lat}
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
            params['cnt'] = limit
        _, json_data = self.http_client.get_json(FIND_OBSERVATIONS_URI, params=params)
        return observation.Observation.from_dict_of_lists(json_data)

    def forecast_at_place(self, name, interval, limit=None):
        """
        Queries the OWM Weather API for weather forecast for the
        specified location (eg: "London,uk") with the given time granularity.
        A *Forecaster* object is returned, containing a *Forecast*: this instance
        encapsulates *Weather* objects corresponding to the provided granularity.

        :param name: the location's toponym
        :type name: str
        :param interval: the granularity of the forecast, among `3h` and 'daily'
        :type interval: str among `3h` and 'daily'
        :param limit: the maximum number of *Weather* items to be retrieved
            (default is ``None``, which stands for any number of items)
        :type limit: int or ``None``
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed, *APICallException* when OWM Weather API can not be
            reached
        """
        assert isinstance(name, str), "Value must be a string"
        assert isinstance(interval, str), "Interval must be a string"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        params = {'q': name}
        if limit is not None:
            params['cnt'] = limit
        if interval == '3h':
            uri = THREE_HOURS_FORECAST_URI
        elif interval == 'daily':
            uri = DAILY_FORECAST_URI
        else:
            raise ValueError("Unsupported time interval for forecast")
        _, json_data = self.http_client.get_json(uri, params=params)
        fc = forecast.Forecast.from_dict(json_data)
        if fc is not None:
            fc.interval = interval
            return forecaster.Forecaster(fc)
        else:
            return None

    def forecast_at_coords(self, lat, lon, interval, limit=None):
        """
        Queries the OWM Weather API for weather forecast for the
        specified geographic coordinates with the given time granularity.
        A *Forecaster* object is returned, containing a *Forecast*: this instance
        encapsulates *Weather* objects corresponding to the provided granularity.

        :param lat: location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param interval: the granularity of the forecast, among `3h` and 'daily'
        :type interval: str among `3h` and 'daily'
        :param limit: the maximum number of *Weather* items to be retrieved
            (default is ``None``, which stands for any number of items)
        :type limit: int or ``None``
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed, *APICallException* when OWM Weather API can not be
            reached
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        assert isinstance(interval, str), "Interval must be a string"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        params = {'lon': lon, 'lat': lat}
        if limit is not None:
            params['cnt'] = limit
        if interval == '3h':
            uri = THREE_HOURS_FORECAST_URI
        elif interval == 'daily':
            uri = DAILY_FORECAST_URI
        else:
            raise ValueError("Unsupported time interval for forecast")
        _, json_data = self.http_client.get_json(uri, params=params)
        fc = forecast.Forecast.from_dict(json_data)
        if fc is not None:
            fc.interval = interval
            return forecaster.Forecaster(fc)
        else:
            return None

    def forecast_at_id(self, id, interval, limit=None):
        """
        Queries the OWM Weather API for weather forecast for the
        specified city ID (eg: 5128581) with the given time granularity.
        A *Forecaster* object is returned, containing a *Forecast*: this instance
        encapsulates *Weather* objects corresponding to the provided granularity.

        :param id: the location's city ID
        :type id: int
        :param interval: the granularity of the forecast, among `3h` and 'daily'
        :type interval: str among `3h` and 'daily'
        :param limit: the maximum number of *Weather* items to be retrieved
            (default is ``None``, which stands for any number of items)
        :type limit: int or ``None``
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed, *APICallException* when OWM Weather API can not be
            reached
        """
        assert type(id) is int, "'id' must be an int"
        if id < 0:
            raise ValueError("'id' value must be greater than 0")
        assert isinstance(interval, str), "Interval must be a string"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        params = {'id': id}
        if limit is not None:
            params['cnt'] = limit
        if interval == '3h':
            uri = THREE_HOURS_FORECAST_URI
        elif interval == 'daily':
            uri = DAILY_FORECAST_URI
        else:
            raise ValueError("Unsupported time interval for forecast")
        _, json_data = self.http_client.get_json(uri, params=params)
        fc = forecast.Forecast.from_dict(json_data)
        if fc is not None:
            fc.interval = interval
            return forecaster.Forecaster(fc)
        else:
            return None

    def station_tick_history(self, station_ID, limit=None):
        """
        Queries the OWM Weather API for historic weather data measurements for the
        specified meteostation (eg: 2865), sampled once a minute (tick).
        A *StationHistory* object instance is returned, encapsulating the
        measurements: the total number of data points can be limited using the
        appropriate parameter

        :param station_ID: the numeric ID of the meteostation
        :type station_ID: int
        :param limit: the maximum number of data points the result shall
            contain (default is ``None``, which stands for any number of data
            points)
        :type limit: int or ``None``
        :returns: a *StationHistory* instance or ``None`` if data is not
            available for the specified meteostation
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed, *APICallException* when OWM Weather API can not be
            reached, *ValueError* if the limit value is negative

        """
        assert isinstance(station_ID, int), "'station_ID' must be int"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        station_history = self._retrieve_station_history(station_ID, limit, "tick")
        if station_history is not None:
            return historian.Historian(station_history)
        else:
            return None

    def station_hour_history(self, station_ID, limit=None):
        """
        Queries the OWM Weather API for historic weather data measurements for the
        specified meteostation (eg: 2865), sampled once a hour.
        A *Historian* object instance is returned, encapsulating a
        *StationHistory* objects which contains the measurements. The total
        number of retrieved data points can be limited using the appropriate
        parameter

        :param station_ID: the numeric ID of the meteostation
        :type station_ID: int
        :param limit: the maximum number of data points the result shall
            contain (default is ``None``, which stands for any number of data
            points)
        :type limit: int or ``None``
        :returns: a *Historian* instance or ``None`` if data is not
            available for the specified meteostation
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed, *APICallException* when OWM Weather API can not be
            reached, *ValueError* if the limit value is negative

        """
        assert isinstance(station_ID, int), "'station_ID' must be int"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        station_history = self._retrieve_station_history(station_ID, limit, "hour")
        if station_history is not None:
            return historian.Historian(station_history)
        else:
            return None

    def station_day_history(self, station_ID, limit=None):
        """
        Queries the OWM Weather API for historic weather data measurements for the
        specified meteostation (eg: 2865), sampled once a day.
        A *Historian* object instance is returned, encapsulating a
        *StationHistory* objects which contains the measurements. The total
        number of retrieved data points can be limited using the appropriate
        parameter

        :param station_ID: the numeric ID of the meteostation
        :type station_ID: int
        :param limit: the maximum number of data points the result shall
            contain (default is ``None``, which stands for any number of data
            points)
        :type limit: int or ``None``
        :returns: a *Historian* instance or ``None`` if data is not
            available for the specified meteostation
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed, *APICallException* when OWM Weather API can not be
            reached, *ValueError* if the limit value is negative

        """
        assert isinstance(station_ID, int), "'station_ID' must be int"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        station_history = self._retrieve_station_history(station_ID, limit, "day")
        if station_history is not None:
            return historian.Historian(station_history)
        else:
            return None

    def _retrieve_station_history(self, station_ID, limit, interval):
        """
        Helper method for station_X_history functions.
        """
        params = {'id': station_ID, 'type': interval}
        if limit is not None:
            params['cnt'] = limit
        _, json_data = self.http_client.get_json(STATION_WEATHER_HISTORY_URI, params=params)
        sh = stationhistory.StationHistory.from_dict(json_data)
        if sh is not None:
            sh.station_id = station_ID
            sh.interval = interval
        return sh

    def one_call(self, lat: Union[int, float], lon: Union[int, float]) -> one_call.OneCall:
        """
        Queries the OWM Weather API with one call for current weather information and forecast for the
        specified geographic coordinates.
        One Call API provides the following weather data for any geographical coordinate:
        - Current weather
        - Hourly forecast for 48 hours
        - Daily forecast for 7 days

        A *OneCall* object is returned with the current data and the two forecasts.

        :param lat: location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :returns: a *OneCall* instance or ``None`` if the data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed, *APICallException* when OWM Weather API can not be
            reached
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        params = {'lon': lon, 'lat': lat}

        _, json_data = self.http_client.get_json(ONE_CALL_URI, params=params)
        return one_call.OneCall.from_dict(json_data)

    def one_call_history(self, lat: Union[int, float], lon: Union[int, float], dt: int = None):
        """
        Queries the OWM Weather API with one call for historical weather information for the
        specified geographic coordinates.

        A *OneCall* object is returned with the current data and the two forecasts.

        :param lat: location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param dt: timestamp from when the historical data starts. Cannot be less then now - 5 days.
                    Default = None means now - 5 days
        :type dt: int
        :returns: a *OneCall* instance or ``None`` if the data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM Weather API responses' data
            cannot be parsed, *APICallException* when OWM Weather API can not be
            reached
        """
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        if dt is None:
            dt = int((datetime.now() - timedelta(days=5)).replace(tzinfo=timezone.utc).timestamp())
        else:
            if not isinstance(dt, int):
                raise ValueError("dt must be of type int")
            if dt < 0:
                raise ValueError("dt must be positive")

        params = {'lon': lon, 'lat': lat, 'dt': dt}

        _, json_data = self.http_client.get_json(ONE_CALL_HISTORICAL_URI, params=params)
        return one_call.OneCall.from_dict(json_data)

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)
