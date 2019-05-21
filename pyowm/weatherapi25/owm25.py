#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm import constants
from pyowm.agroapi10 import agro_manager
from pyowm.alertapi30 import alert_manager
from pyowm.commons import http_client, cityidregistry
from pyowm.airpollutionapi30 import airpollution_client
from pyowm.stationsapi30 import stations_manager
from pyowm.tiles import tile_manager
from pyowm.utils import strings


class OWM25:

    """
    OWM subclass providing methods for each OWM Weather API 2.5 endpoint and ad-hoc API clients for the other
    OWM web APis. The class is instantiated with *jsonparser* subclasses, each one parsing the response
    payload of a specific API endpoint

    :param parsers: the dictionary containing *jsonparser* concrete instances
        to be used as parsers for OWM Weather API 2.5 responses
    :type parsers: dict
    :param API_key: the OWM Weather API key (defaults to ``None``)
    :type API_key: str
    :param cache: a concrete implementation of class *OWMCache* serving as the cache provider
    :type cache: an *OWMCache* concrete instance
    :param language: the language in which you want text results to be returned.
          It's a two-characters string, eg: "en", "ru", "it". Defaults to: "en"
    :type language: str
    :param subscription_type: the type of OWM Weather API subscription to be wrapped.
           Can be 'free' (free subscription) or 'pro' (paid subscription),
           Defaults to: 'free'
    :type subscription_type: str
    :param use_ssl: whether API calls should be made via SSL or not.
           Defaults to: False
    :type use_ssl: bool
    :returns: an *OWM25* instance

    """
    def __init__(self, API_key=None, cache=None,
                 language="en", subscription_type='free', use_ssl=False):
        if API_key is not None:
            assert isinstance(API_key, str), "Value must be a string"
        self._API_key = API_key
        self._city_id_reg = cityidregistry.CityIDRegistry.get_instance()
        self._wapi = http_client.HttpClient(cache=cache)
        self._pollapi = airpollution_client.AirPollutionHttpClient(API_key, self._wapi)
        self._language = language
        if API_key is None and subscription_type == 'pro':
            raise AssertionError('You must provide an API Key for paid subscriptions')
        self._subscription_type = subscription_type
        self._use_ssl = use_ssl

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

    def get_API_version(self):
        """
        Returns the currently supported OWM Weather API version

        :returns: str

        """
        return constants.WEATHER_API_VERSION

    def get_version(self):
        """
        Returns the current version of the PyOWM library

        :returns: `tuple`

        """
        return constants.PYOWM_VERSION

    def get_language(self):
        """
        Returns the language in which the OWM Weather API shall return text results

        :returns: the language

        """
        return self._language

    def set_language(self, language):
        """
        Sets the language in which the OWM Weather API shall return text results

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
        return self._city_id_reg

    def stations_manager(self):
        """
        Gives a *StationsManager* instance that can be used to read/write
        meteostations data.
        :returns: a *StationsManager* instance
        """
        return stations_manager.StationsManager(self._API_key)

    def alert_manager(self):
        """
        Gives an *AlertManager* instance that can be used to read/write weather triggers and alerts data.
        :return: an *AlertManager* instance
        """
        return alert_manager.AlertManager(self._API_key)

    def tile_manager(self, layer_name):
        """
        Gives a `pyowm.tiles.tile_manager.TileManager` instance that can be used to fetch tile images.
        :param layer_name: the layer name for the tiles (values can be looked up on `pyowm.tiles.enums.MapLayerEnum`)
        :return: a `pyowm.tiles.tile_manager.TileManager` instance
        """
        return tile_manager.TileManager(self._API_key, map_layer=layer_name)

    def agro_manager(self):
        """
        Gives a `pyowm.agro10.agro_manager.AgroManager` instance that can be used to read/write data from the
        Agricultural API.
        :return: a `pyowm.agro10.agro_manager.AgroManager` instance
        """
        return agro_manager.AgroManager(self._API_key)



    def __repr__(self):
        return "<%s.%s - API key=%s, OWM Weather API version=%s, " \
               "subscription type=%s, PyOWM version=%s, language=%s>" % \
                    (__name__,
                     self.__class__.__name__,
                     strings.obfuscate_API_key(self._API_key) if self._API_key is not None else 'None',
                     self.get_API_version(),
                     self._subscription_type,
                     self.get_version(),
                     self._language)
