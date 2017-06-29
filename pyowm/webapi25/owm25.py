"""
Module containing the PyOWM library main entry point
"""

from time import time
from pyowm import constants
from pyowm.webapi25.configuration25 import (
    OBSERVATION_URL, GROUP_OBSERVATIONS_URL,
    FIND_OBSERVATIONS_URL, THREE_HOURS_FORECAST_URL,
    DAILY_FORECAST_URL, CITY_WEATHER_HISTORY_URL, STATION_WEATHER_HISTORY_URL,
    FIND_STATION_URL, STATION_URL, BBOX_STATION_URL, API_AVAILABILITY_TIMEOUT)
from pyowm.webapi25.configuration25 import city_id_registry as reg
from pyowm.abstractions import owm
from pyowm.abstractions.decorators import deprecated
from pyowm.caches import nullcache
from pyowm.commons import weather_client, uv_client, airpollution_client
from pyowm.utils import timeformatutils
from pyowm.webapi25 import forecaster
from pyowm.webapi25 import historian


class OWM25(owm.OWM):

    OWM_API_VERSION = '2.5'

    """
    OWM subclass providing methods for each OWM web API 2.5 endpoint. The class
    is instantiated with *jsonparser* subclasses, each one parsing the response
    payload of a specific API endpoint

    :param parsers: the dictionary containing *jsonparser* concrete instances
        to be used as parsers for OWM web API 2.5 responses
    :type parsers: dict
    :param API_key: the OWM web API key (defaults to ``None``)
    :type API_key: str
    :param cache: a concrete implementation of class *OWMCache* serving as the
        cache provider (defaults to a *NullCache* instance)
    :type cache: an *OWMCache* concrete instance
    :param language: the language in which you want text results to be returned.
          It's a two-characters string, eg: "en", "ru", "it". Defaults to: "en"
    :type language: str
    :param subscription_type: the type of OWM web API subscription to be wrapped.
           Can be 'free' (free subscription) or 'pro' (paid subscription),
           Defaults to: 'free'
    :type subscription_type: str
    :returns: an *OWM25* instance

    """
    def __init__(self, parsers, API_key=None, cache=nullcache.NullCache(),
                 language="en", subscription_type='free'):
        self._parsers = parsers
        if API_key is not None:
            OWM25._assert_is_string(API_key)
        self._API_key = API_key
        self._api = weather_client.WeatherHttpClient(API_key, cache, subscription_type)
        self._uvapi = uv_client.UltraVioletHttpClient(API_key, cache)
        self._pollapi = \
            airpollution_client.AirPollutionHttpClient(API_key, cache)
        self._language = language
        if API_key is None and subscription_type == 'pro':
            raise AssertionError('You must provide an API Key for paid subscriptions')
        self._subscription_type = subscription_type

    @staticmethod
    def _assert_is_string(value):
        """
        Checks if the provided value is a valid string instance

        :param value: value to be checked
        :return: None
        """
        try:  # Python 2.x
            assert isinstance(value, basestring), "Value must be a string or unicode"
        except NameError:  # Python 3.x
            assert isinstance(value, str), "Value must be a string"


    @staticmethod
    def _assert_is_string_or_unicode(value):
        """
        Checks if the provided value is a valid string or unicode instance
        On Python 3.x it just checks that the value is a string instance.
        :param value: value to be checked
        :return: None
        """
        try:
            assert isinstance(value, basestring) or isinstance(value, unicode), \
                "Value must be a string or unicode"
        except NameError:
            assert isinstance(value, str), "Value must be a string"

    @staticmethod
    def _encode_string(value):
        """
        Turns the provided value to UTF-8 encoding

        :param value: input value
        :return: UTF-8 encoded value
        """
        try:  # The OWM API expects UTF-8 encoding
            if not isinstance(value, unicode):
                return value.encode('utf8')
            return value
        except NameError:
            return value

    def _obfuscate_API_key(self):
        """
        Return a mostly obfuscated version of the API Key

        :return: str
        """
        if self._API_key is not None:
            return (len(self._API_key)-8)*'*'+self._API_key[-8:]

    def get_API_key(self):
        """
        Returns the str OWM API key

        :returns: a str

        """
        return self._API_key

    def set_API_key(self, API_key):
        """
        Updates the str OWM API key

        :param API_key: the new str API key
        :type API_key: str

        """
        self._API_key = API_key

    @deprecated(will_be='modified', on_version=(3, 0, 0))
    def get_API_version(self):
        """
        Returns the currently supported OWM web API version

        .. deprecated:: 3.0.0
           Will return a tuple instead of a str

        :returns: str

        """
        return self.OWM_API_VERSION

    @deprecated(will_be='modified', on_version=(3, 0, 0))
    def get_version(self):
        """
        Returns the current version of the PyOWM library

        .. deprecated:: 3.0.0
           Will return a tuple instead of a str

        :returns: str

        """
        return constants.PYOWM_VERSION

    def get_language(self):
        """
        Returns the language in which the OWM web API shall return text results

        :returns: the language

        """
        return self._language

    def set_language(self, language):
        """
        Sets the language in which the OWM web API shall return text results

        :param language: the new two-characters language (eg: "ru")
        :type API_key: str

        """
        self._language = language

    def get_subscription_type(self):
        """
        Returns the OWM API subscription type

        :returns: the subscription type

        """
        return self._subscription_type

    def city_id_registry(self):
        """
        Gives the *CityIDRegistry* singleton instance that can be used to lookup
        for city IDs.

        :returns: a *CityIDRegistry* instance
        """
        return reg

    def is_API_online(self):
        """
        Returns True if the OWM web API is currently online. A short timeout
        is used to determine API service availability.

        :returns: bool

        """
        data = self._api.call_API(OBSERVATION_URL,
                                  {'q': 'London,UK'},
                                  API_AVAILABILITY_TIMEOUT)
        if data is not None:
            return True
        return False

    def weather_at_place(self, name):
        """
        Queries the OWM web API for the currently observed weather at the
        specified toponym (eg: "London,uk")

        :param name: the location's toponym
        :type name: str or unicode
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed or *APICallException* when OWM web API can not be
            reached
        """

        OWM25._assert_is_string_or_unicode(name)
        encoded_name = OWM25._encode_string(name)
        json_data = self._api.call_API(OBSERVATION_URL,
                                       {'q': encoded_name,
                                        'lang': self._language})
        return self._parsers['observation'].parse_JSON(json_data)

    def weather_at_coords(self, lat, lon):
        """
        Queries the OWM web API for the currently observed weather at the
        specified geographic (eg: 51.503614, -0.107331).

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed or *APICallException* when OWM web API can not be
            reached
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        json_data = self._api.call_API(OBSERVATION_URL,
                                       {'lon': lon, 'lat': lat,
                                        'lang': self._language})
        return self._parsers['observation'].parse_JSON(json_data)

    def weather_at_zip_code(self, zipcode, country):
        """
        Queries the OWM web API for the currently observed weather at the
        specified zip code and country code (eg: 2037, au).
        
        :param zip: the location's zip or postcode
        :type zip: string
        :param country: the location's country code
        :type country: string
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed or *APICallException* when OWM web API can not be
            reached
        """
        OWM25._assert_is_string_or_unicode(zipcode)
        OWM25._assert_is_string_or_unicode(country)
        encoded_zip = OWM25._encode_string(zipcode)
        encoded_country = OWM25._encode_string(country)
        zip_param = encoded_zip + ',' + encoded_country
        json_data = self._api.call_API(OBSERVATION_URL,
                                       {'zip': zip_param,
                                        'lang': self._language})
        return self._parsers['observation'].parse_JSON(json_data)

    def weather_at_id(self, id):
        """
        Queries the OWM web API for the currently observed weather at the
        specified city ID (eg: 5128581)

        :param id: the location's city ID
        :type id: int
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed or *APICallException* when OWM web API can not be
            reached
        """
        assert type(id) is int, "'id' must be an int"
        if id < 0:
            raise ValueError("'id' value must be greater than 0")
        json_data = self._api.call_API(OBSERVATION_URL,
                                       {'id': id,
                                        'lang': self._language})
        return self._parsers['observation'].parse_JSON(json_data)

    def weather_at_ids(self, ids_list):
        """
        Queries the OWM web API for the currently observed weathers at the
        specified city IDs (eg: [5128581,87182])

        :param ids_list: the list of city IDs
        :type ids_list: list of int
        :returns: a list of *Observation* instances or an empty list if no
            weather data is available
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed or *APICallException* when OWM web API can not be
            reached
        """
        assert type(ids_list) is list, "'ids_list' must be a list of integers"
        for id in ids_list:
            assert type(id) is int, "'ids_list' must be a list of integers"
            if id < 0:
                raise ValueError("id values in 'ids_list' must be greater "
                                 "than 0")
        json_data = self._api.call_API(GROUP_OBSERVATIONS_URL,
                                       {'id': ','.join(list(map(str, ids_list))),
                                       'lang': self._language})
        return self._parsers['observation_list'].parse_JSON(json_data)

    def weather_at_places(self, pattern, searchtype, limit=None):
        """
        Queries the OWM web API for the currently observed weather in all the
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
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
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
        params = {'q': pattern, 'type': searchtype, 'lang': self._language}
        if limit is not None:
            # fix for OWM 2.5 API bug!
            params['cnt'] = limit - 1
        json_data = self._api.call_API(FIND_OBSERVATIONS_URL, params)
        return self._parsers['observation_list'].parse_JSON(json_data)

    def weather_at_station(self, station_id):
        """
        Queries the OWM web API for the weather currently observed by a specific
        meteostation (eg: 29584)

        :param station_id: the meteostation ID
        :type station_id: int
        :returns: an *Observation* instance or ``None`` if no weather data is
            available
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed or *APICallException* when OWM web API can not be
            reached
        """
        assert type(station_id) is int, "'station_id' must be an int"
        if station_id < 0:
            raise ValueError("'station_id' value must be greater than 0")
        json_data = self._api.call_API(STATION_URL,
                                      {'id': station_id,
                                       'lang': self._language})
        return self._parsers['observation'].parse_JSON(json_data)

    def weather_at_stations_in_bbox(self, lat_top_left, lon_top_left,
                                    lat_bottom_right, lon_bottom_right,
                                    cluster=False, limit=None):
        """
        Queries the OWM web API for the weather currently observed by
        meteostations inside the bounding box of latitude/longitude coords.

        :param lat_top_left: latitude for top-left of bounding box, must be
            between -90.0 and 90.0
        :type lat_top_left: int/float
        :param lon_top_left: longitude for top-left of bounding box
            must be between -180.0 and 180.0
        :type lon_top_left: int/float
        :param lat_bottom_right: latitude for bottom-right of bounding box, must
            be between -90.0 and 90.0
        :type lat_bottom_right: int/float
        :param lon_bottom_right: longitude for bottom-right of bounding box,
            must be between -180.0 and 180.0
        :type lon_bottom_right: int/float
        :param cluster: use server clustering of points
        :type cluster: bool
        :param limit: the maximum number of *Observation* items in the returned
            list (default is ``None``, which stands for any number of items)
        :param limit: int or ``None``
        :returns: a list of *Observation* objects or ``None`` if no weather
            data is available
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* when coordinates values are out of bounds or
            negative values are provided for limit
        """
        assert type(lat_top_left) in (float, int), \
                "'lat_top_left' must be a float"
        assert type(lon_top_left) in (float, int), \
                "'lon_top_left' must be a float"
        assert type(lat_bottom_right) in (float, int), \
                "'lat_bottom_right' must be a float"
        assert type(lon_bottom_right) in (float, int), \
                "'lon_bottom_right' must be a float"
        assert type(cluster) is bool, "'cluster' must be a bool"
        assert type(limit) in (int, type(None)), \
                "'limit' must be an int or None"
        if lat_top_left < -90.0 or lat_top_left > 90.0:
            raise ValueError("'lat_top_left' value must be between -90 and 90")
        if lon_top_left < -180.0 or lon_top_left > 180.0:
            raise ValueError("'lon_top_left' value must be between -180 and" \
                             +" 180")
        if lat_bottom_right < -90.0 or lat_bottom_right > 90.0:
            raise ValueError("'lat_bottom_right' value must be between -90" \
                             +" and 90")
        if lon_bottom_right < -180.0 or lon_bottom_right > 180.0:
            raise ValueError("'lon_bottom_right' value must be between -180 "\
                             +"and 180")
        if limit is not None and limit < 1:
            raise ValueError("'limit' must be None or greater than zero")
        params = {'bbox': ','.join([str(lon_top_left),
                                    str(lat_top_left),
                                    str(lon_bottom_right),
                                    str(lat_bottom_right)]),
                  'cluster': 'yes' if cluster else 'no',}
        if limit is not None:
            params['cnt'] = limit

        json_data = self._api.call_API(BBOX_STATION_URL, params)
        return self._parsers['observation_list'].parse_JSON(json_data)

    def weather_around_coords(self, lat, lon, limit=None):
        """
        Queries the OWM web API for the currently observed weather in all the
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
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* when coordinates values are out of bounds or
            negative values are provided for limit
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        params = {'lon': lon, 'lat': lat, 'lang': self._language}
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
            params['cnt'] = limit
        json_data = self._api.call_API(FIND_OBSERVATIONS_URL, params)
        return self._parsers['observation_list'].parse_JSON(json_data)

    def three_hours_forecast(self, name):
        """
        Queries the OWM web API for three hours weather forecast for the
        specified location (eg: "London,uk"). A *Forecaster* object is
        returned, containing a *Forecast* instance covering a global streak of
        five days: this instance encapsulates *Weather* objects, with a time
        interval of three hours one from each other

        :param name: the location's toponym
        :type name: str or unicode
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached
        """
        OWM25._assert_is_string_or_unicode(name)
        encoded_name = OWM25._encode_string(name)
        json_data = self._api.call_API(THREE_HOURS_FORECAST_URL,
                                       {'q': encoded_name,
                                        'lang': self._language})
        forecast = self._parsers['forecast'].parse_JSON(json_data)
        if forecast is not None:
            forecast.set_interval("3h")
            return forecaster.Forecaster(forecast)
        else:
            return None

    def three_hours_forecast_at_coords(self, lat, lon):
        """
        Queries the OWM web API for three hours weather forecast for the
        specified geographic coordinate (eg: latitude: 51.5073509,
        longitude: -0.1277583). A *Forecaster* object is returned,
        containing a *Forecast* instance covering a global streak of
        five days: this instance encapsulates *Weather* objects, with a time
        interval of three hours one from each other

        :param lat: location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        params = {'lon': lon, 'lat': lat, 'lang': self._language}
        json_data = self._api.call_API(THREE_HOURS_FORECAST_URL, params)
        forecast = self._parsers['forecast'].parse_JSON(json_data)
        if forecast is not None:
            forecast.set_interval("3h")
            return forecaster.Forecaster(forecast)
        else:
            return None

    def three_hours_forecast_at_id(self, id):
        """
        Queries the OWM web API for three hours weather forecast for the
        specified city ID (eg: 5128581). A *Forecaster* object is returned,
        containing a *Forecast* instance covering a global streak of
        five days: this instance encapsulates *Weather* objects, with a time
        interval of three hours one from each other

        :param id: the location's city ID
        :type id: int
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached
        """
        assert type(id) is int, "'id' must be an int"
        if id < 0:
            raise ValueError("'id' value must be greater than 0")
        json_data = self._api.call_API(THREE_HOURS_FORECAST_URL,
                                       {'id': id,
                                        'lang': self._language})
        forecast = self._parsers['forecast'].parse_JSON(json_data)
        if forecast is not None:
            forecast.set_interval("3h")
            return forecaster.Forecaster(forecast)
        else:
            return None

    def daily_forecast(self, name, limit=None):
        """
        Queries the OWM web API for daily weather forecast for the specified
        location (eg: "London,uk"). A *Forecaster* object is returned,
        containing a *Forecast* instance covering a global streak of fourteen
        days by default: this instance encapsulates *Weather* objects, with a
        time interval of one day one from each other

        :param name: the location's toponym
        :type name: str or unicode
        :param limit: the maximum number of daily *Weather* items to be
            retrieved (default is ``None``, which stands for any number of
            items)
        :type limit: int or ``None``
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if negative values are supplied for limit
        """
        OWM25._assert_is_string_or_unicode(name)
        encoded_name = OWM25._encode_string(name)
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        params = {'q': encoded_name, 'lang': self._language}
        if limit is not None:
            params['cnt'] = limit
        json_data = self._api.call_API(DAILY_FORECAST_URL, params)
        forecast = self._parsers['forecast'].parse_JSON(json_data)
        if forecast is not None:
            forecast.set_interval("daily")
            return forecaster.Forecaster(forecast)
        else:
            return None

    def daily_forecast_at_coords(self, lat, lon, limit=None):
        """
        Queries the OWM web API for daily weather forecast for the specified
        geographic coordinate (eg: latitude: 51.5073509, longitude: -0.1277583).
        A *Forecaster* object is returned, containing a *Forecast* instance
        covering a global streak of fourteen days by default: this instance
        encapsulates *Weather* objects, with a time interval of one day one
        from each other

        :param lat: location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param limit: the maximum number of daily *Weather* items to be
            retrieved (default is ``None``, which stands for any number of
            items)
        :type limit: int or ``None``
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if negative values are supplied for limit
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        params = {'lon': lon, 'lat': lat, 'lang': self._language}
        if limit is not None:
            params['cnt'] = limit
        json_data = self._api.call_API(DAILY_FORECAST_URL, params)
        forecast = self._parsers['forecast'].parse_JSON(json_data)
        if forecast is not None:
            forecast.set_interval("daily")
            return forecaster.Forecaster(forecast)
        else:
            return None

    def daily_forecast_at_id(self, id, limit=None):
        """
        Queries the OWM web API for daily weather forecast for the specified
        city ID (eg: 5128581). A *Forecaster* object is returned, containing
        a *Forecast* instance covering a global streak of fourteen days by
        default: this instance encapsulates *Weather* objects, with a time
        interval of one day one from each other

        :param id: the location's city ID
        :type id: int
        :param limit: the maximum number of daily *Weather* items to be
            retrieved (default is ``None``, which stands for any number of
            items)
        :type limit: int or ``None``
        :returns: a *Forecaster* instance or ``None`` if forecast data is not
            available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if negative values are supplied for limit
        """
        assert type(id) is int, "'id' must be an int"
        if id < 0:
            raise ValueError("'id' value must be greater than 0")
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")

        params = {'id': id, 'lang': self._language}
        if limit is not None:
            params['cnt'] = limit
        json_data = self._api.call_API(DAILY_FORECAST_URL, params)
        forecast = self._parsers['forecast'].parse_JSON(json_data)
        if forecast is not None:
            forecast.set_interval("daily")
            return forecaster.Forecaster(forecast)
        else:
            return None

    def weather_history_at_place(self, name, start=None, end=None):
        """
        Queries the OWM web API for weather history for the specified location
        (eg: "London,uk"). A list of *Weather* objects is returned. It is
        possible to query for weather history in a closed time period, whose
        boundaries can be passed as optional parameters.

        :param name: the location's toponym
        :type name: str or unicode
        :param start: the object conveying the time value for the start query
            boundary (defaults to ``None``)
        :type start: int, ``datetime.datetime`` or ISO8601-formatted
            string
        :param end: the object conveying the time value for the end query
            boundary (defaults to ``None``)
        :type end: int, ``datetime.datetime`` or ISO8601-formatted string
        :returns: a list of *Weather* instances or ``None`` if history data is
            not available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if the time boundaries are not in the correct
            chronological order, if one of the time boundaries is not ``None``
            and the other is or if one or both of the time boundaries are after
            the current time

        """
        OWM25._assert_is_string_or_unicode(name)
        encoded_name = OWM25._encode_string(name)
        params = {'q': encoded_name, 'lang': self._language}
        if start is None and end is None:
            pass
        elif start is not None and end is not None:
            unix_start = timeformatutils.to_UNIXtime(start)
            unix_end = timeformatutils.to_UNIXtime(end)
            if unix_start >= unix_end:
                raise ValueError("Error: the start time boundary must " \
                                 "precede the end time!")
            current_time = time()
            if unix_start > current_time:
                raise ValueError("Error: the start time boundary must " \
                                 "precede the current time!")
            params['start'] = str(unix_start)
            params['end'] = str(unix_end)
        else:
            raise ValueError("Error: one of the time boundaries is None, " \
                             "while the other is not!")
        json_data = self._api.call_API(CITY_WEATHER_HISTORY_URL,
                                             params)
        return self._parsers['weather_history'].parse_JSON(json_data)

    def weather_history_at_coords(self, lat, lon, start=None, end=None):
        """
        Queries the OWM web API for weather history for the specified at the
        specified geographic (eg: 51.503614, -0.107331). A list of *Weather*
        objects is returned. It is possible to query for weather history in a
        closed time period, whose boundaries can be passed as optional
        parameters.

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param start: the object conveying the time value for the start query
            boundary (defaults to ``None``)
        :type start: int, ``datetime.datetime`` or ISO8601-formatted
            string
        :param end: the object conveying the time value for the end query
            boundary (defaults to ``None``)
        :type end: int, ``datetime.datetime`` or ISO8601-formatted string
        :returns: a list of *Weather* instances or ``None`` if history data is
            not available for the specified location

        """
        pass
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")

        params = {'lon': lon, 'lat': lat, 'lang': self._language}

        if start is not None:
            unix_start = timeformatutils.to_UNIXtime(start)

            current_time = time()
            if unix_start > current_time:
                raise ValueError("Error: the start time boundary must "
                                 "precede the current time!")
            params['start'] = str(unix_start)
        else:
            unix_start = None

        if end is not None:
            unix_end = timeformatutils.to_UNIXtime(end)
            params['end'] = str(unix_end)
        else:
            unix_end = None

        if unix_start is not None and unix_end is not None:
            if unix_start >= unix_end:
                raise ValueError("Error: the start time boundary must "
                                 "precede the end time!")

        json_data = self._api.call_API(CITY_WEATHER_HISTORY_URL, params)
        return self._parsers['weather_history'].parse_JSON(json_data)

    def weather_history_at_id(self, id, start=None, end=None):
        """
        Queries the OWM web API for weather history for the specified city ID.
        A list of *Weather* objects is returned. It is possible to query for
        weather history in a closed time period, whose boundaries can be passed
        as optional parameters.

        :param id: the city ID
        :type id: int
        :param start: the object conveying the time value for the start query
            boundary (defaults to ``None``)
        :type start: int, ``datetime.datetime`` or ISO8601-formatted
            string
        :param end: the object conveying the time value for the end query
            boundary (defaults to ``None``)
        :type end: int, ``datetime.datetime`` or ISO8601-formatted string
        :returns: a list of *Weather* instances or ``None`` if history data is
            not available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if the time boundaries are not in the correct
            chronological order, if one of the time boundaries is not ``None``
            and the other is or if one or both of the time boundaries are after
            the current time

        """
        assert type(id) is int, "'id' must be an int"
        if id < 0:
            raise ValueError("'id' value must be greater than 0")
        params = {'id': id, 'lang': self._language}
        if start is None and end is None:
            pass
        elif start is not None and end is not None:
            unix_start = timeformatutils.to_UNIXtime(start)
            unix_end = timeformatutils.to_UNIXtime(end)
            if unix_start >= unix_end:
                raise ValueError("Error: the start time boundary must " \
                                 "precede the end time!")
            current_time = time()
            if unix_start > current_time:
                raise ValueError("Error: the start time boundary must " \
                                 "precede the current time!")
            params['start'] = str(unix_start)
            params['end'] = str(unix_end)
        else:
            raise ValueError("Error: one of the time boundaries is None, " \
                             "while the other is not!")
        json_data = self._api.call_API(CITY_WEATHER_HISTORY_URL,
                                             params)
        return self._parsers['weather_history'].parse_JSON(json_data)

    def station_at_coords(self, lat, lon, limit=None):
        """
        Queries the OWM web API for weather stations nearest to the
        specified geographic coordinates (eg: latitude: 51.5073509,
        longitude: -0.1277583). A list of *Station* objects is returned,
        this instance encapsulates a last reported *Weather* object.

        :param lat: location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :param cnt: the maximum number of *Station* items to be retrieved
            (default is ``None``, which stands for any number of items)
        :type cnt: int or ``None``

        :returns: a list of *Station* objects or ``None`` if station data is
            not available for the specified location
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        params = {'lat': lat, 'lon': lon}
        if limit is not None:
            params['cnt'] = limit
        json_data = self._api.call_API(FIND_STATION_URL, params)
        return self._parsers['station_list'].parse_JSON(json_data)

    def station_tick_history(self, station_ID, limit=None):
        """
        Queries the OWM web API for historic weather data measurements for the
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
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if the limit value is negative

        """
        assert isinstance(station_ID, int), "'station_ID' must be int"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        station_history = self._retrieve_station_history(station_ID, limit,
                                                         "tick")
        if station_history is not None:
            return historian.Historian(station_history)
        else:
            return None

    def station_hour_history(self, station_ID, limit=None):
        """
        Queries the OWM web API for historic weather data measurements for the
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
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if the limit value is negative

        """
        assert isinstance(station_ID, int), "'station_ID' must be int"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        station_history = self._retrieve_station_history(station_ID, limit,
                                                         "hour")
        if station_history is not None:
            return historian.Historian(station_history)
        else:
            return None

    def station_day_history(self, station_ID, limit=None):
        """
        Queries the OWM web API for historic weather data measurements for the
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
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* if the limit value is negative

        """
        assert isinstance(station_ID, int), "'station_ID' must be int"
        if limit is not None:
            assert isinstance(limit, int), "'limit' must be an int or None"
            if limit < 1:
                raise ValueError("'limit' must be None or greater than zero")
        station_history = self._retrieve_station_history(station_ID, limit,
                                                         "day")
        if station_history is not None:
            return historian.Historian(station_history)
        else:
            return None

    def _retrieve_station_history(self, station_ID, limit, interval):
        """
        Helper method for station_X_history functions.
        """
        params = {'id': station_ID, 'type': interval, 'lang': self._language}
        if limit is not None:
            params['cnt'] = limit
        json_data = self._api.call_API(STATION_WEATHER_HISTORY_URL,
                                             params)
        station_history = \
            self._parsers['station_history'].parse_JSON(json_data)
        if station_history is not None:
            station_history.set_station_ID(station_ID)
            station_history.set_interval(interval)
        return station_history

    def uvindex_around_coords(self, lat, lon):
        """
        Queries the OWM web API for Ultra Violet value sampled in the
        surroundings of the provided geocoordinates and in the specified time
        interval. A *UVIndex* object instance is returned, encapsulating a
        *Location* object and the UV intensity value.
        If `start` is not provided, the latest available UVIndex value is
        retrieved.
        If `start` is provided but `interval` is not, then `interval` defaults
        to the maximum extent, which is: `year`

        :param lat: the location's latitude, must be between -90.0 and 90.0
        :type lat: int/float
        :param lon: the location's longitude, must be between -180.0 and 180.0
        :type lon: int/float
        :return: a *UVIndex* instance or ``None`` if data is not available
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* for wrong input values
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")

        params = {'lon': lon, 'lat': lat}
        json_data = self._uvapi.get_uvi(params)
        uvindex = self._parsers['uvindex'].parse_JSON(json_data)
        return uvindex

    def coindex_around_coords(self, lat, lon, start=None, interval=None):
        """
        Queries the OWM web API for Carbon Monoxide values sampled in the
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
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* for wrong input values
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")

        params = {'lon': lon, 'lat': lat, 'start': start, 'interval': interval}
        json_data = self._pollapi.get_coi(params)
        coindex = self._parsers['coindex'].parse_JSON(json_data)
        if interval is None:
            interval = 'year'
        coindex._interval = interval
        return coindex

    def ozone_around_coords(self, lat, lon, start=None, interval=None):
        """
        Queries the OWM web API for Ozone (O3) value in Dobson Units sampled in
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
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* for wrong input values
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")

        params = {'lon': lon, 'lat': lat, 'start': start, 'interval': interval}
        json_data = self._pollapi.get_o3(params)
        ozone = self._parsers['ozone'].parse_JSON(json_data)
        if interval is None:
            interval = 'year'
            ozone._interval = interval
        return ozone

    def no2index_around_coords(self, lat, lon, start=None, interval=None):
        """
        Queries the OWM web API for Nitrogen Dioxide values sampled in the
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
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* for wrong input values
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")

        params = {'lon': lon, 'lat': lat, 'start': start, 'interval': interval}
        json_data = self._pollapi.get_no2(params)
        no2index = self._parsers['no2index'].parse_JSON(json_data)
        if interval is None:
            interval = 'year'
        no2index._interval = interval
        return no2index

    def so2index_around_coords(self, lat, lon, start=None, interval=None):
        """
        Queries the OWM web API for Sulphur Dioxide values sampled in the
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
        :raises: *ParseResponseException* when OWM web API responses' data
            cannot be parsed, *APICallException* when OWM web API can not be
            reached, *ValueError* for wrong input values
        """
        assert type(lon) is float or type(lon) is int, "'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        assert type(lat) is float or type(lat) is int, "'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")

        params = {'lon': lon, 'lat': lat, 'start': start, 'interval': interval}
        json_data = self._pollapi.get_so2(params)
        so2index = self._parsers['so2index'].parse_JSON(json_data)
        if interval is None:
            interval = 'year'
        so2index._interval = interval
        return so2index

    def __repr__(self):
        return "<%s.%s - API key=%s, OWM web API version=%s, " \
               "subscription type=%s, PyOWM version=%s, language=%s>" % \
                    (__name__,
                      self.__class__.__name__,
                      self._obfuscate_API_key() if self._API_key is not None else 'None',
                      self.get_API_version(),
                      self._subscription_type,
                      self.get_version(),
                      self._language)
