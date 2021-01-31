#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm import constants
from pyowm.agroapi10 import agro_manager
from pyowm.airpollutionapi30 import airpollution_manager
from pyowm.alertapi30 import alert_manager
from pyowm.geocodingapi10 import geocoding_manager
from pyowm.stationsapi30 import stations_manager
from pyowm.tiles import tile_manager
from pyowm.utils import strings
from pyowm.uvindexapi30 import uvindex_manager
from pyowm.utils import config as cfg
from pyowm.commons import cityidregistry
from pyowm.weatherapi25 import weather_manager


class OWM:

    """
    Entry point class providing ad-hoc API clients for each OWM web API.

    :param api_key: the OWM API key
    :type api_key: str
    :param config: the configuration dictionary (if not provided, a default one will be used)
    :type config: dict
    """
    def __init__(self, api_key, config=None):
        assert api_key is not None, 'API Key must be set'
        self.api_key = api_key
        if config is None:
            self.config = cfg.get_default_config()
        else:
            assert isinstance(config, dict)
            self.config = config

    @property
    def configuration(self):
        """
        Returns the configuration dict for the PyOWM

        :returns: `dict`

        """
        return self.config

    @property
    def version(self):
        """
        Returns the current version of the PyOWM library

        :returns: `tuple`

        """
        return constants.PYOWM_VERSION

    @property
    def supported_languages(self):
        """
        Returns the languages that the OWM API supports

        :return: `list` of `str`

        """
        return constants.LANGUAGES

    def agro_manager(self):
        """
        Gives a `pyowm.agro10.agro_manager.AgroManager` instance that can be used to read/write data from the
        Agricultural API.
        :return: a `pyowm.agro10.agro_manager.AgroManager` instance
        """
        return agro_manager.AgroManager(self.api_key, self.config)

    def airpollution_manager(self):
        """
        Gives a `pyowm.airpollutionapi30.airpollution_manager.AirPollutionManager` instance that can be used to fetch air
        pollution data.
        :return: a `pyowm.airpollutionapi30.airpollution_manager.AirPollutionManager` instance
        """
        return airpollution_manager.AirPollutionManager(self.api_key, self.config)

    def alert_manager(self):
        """
        Gives an *AlertManager* instance that can be used to read/write weather triggers and alerts data.
        :return: an *AlertManager* instance
        """
        return alert_manager.AlertManager(self.api_key, self.config)

    def city_id_registry(self):
        """
        Gives the *CityIDRegistry* singleton instance that can be used to lookup for city IDs.

        :returns: a *CityIDRegistry* instance
        """
        return cityidregistry.CityIDRegistry.get_instance()

    def stations_manager(self):
        """
        Gives a *StationsManager* instance that can be used to read/write
        meteostations data.
        :returns: a *StationsManager* instance
        """
        return stations_manager.StationsManager(self.api_key, self.config)

    def tile_manager(self, layer_name):
        """
        Gives a `pyowm.tiles.tile_manager.TileManager` instance that can be used to fetch tile images.
        :param layer_name: the layer name for the tiles (values can be looked up on `pyowm.tiles.enums.MapLayerEnum`)
        :return: a `pyowm.tiles.tile_manager.TileManager` instance
        """
        return tile_manager.TileManager(self.api_key, layer_name, self.config)

    def uvindex_manager(self):
        """
        Gives a `pyowm.uvindexapi30.uvindex_manager.UVIndexManager` instance that can be used to fetch UV data.
        :return: a `pyowm.uvindexapi30.uvindex_manager.UVIndexManager` instance
        """
        return uvindex_manager.UVIndexManager(self.api_key, self.config)

    def weather_manager(self):
        """
        Gives a `pyowm.weatherapi25.weather_manager.WeatherManager` instance that can be used to fetch air
        pollution data.
        :return: a `pyowm.weatherapi25.weather_manager.WeatherManager` instance
        """
        return weather_manager.WeatherManager(self.api_key, self.config)

    def geocoding_manager(self):
        """
        Gives a `pyowm.geocoding10.geocoding_manager.GeocodingManager` instance that can be used to perform direct
        and reverse geocoding
        :return: a `pyowm.geocoding10.geocoding_manager.GeocodingManager` instance
        """
        return geocoding_manager.GeocodingManager(self.api_key, self.config)

    def __repr__(self):
        return "<%s.%s - API key=%s, subscription type=%s, PyOWM version=%s>" % \
                    (__name__,
                     self.__class__.__name__,
                     strings.obfuscate_API_key(self.api_key) if self.api_key is not None else 'None',
                     self.config['subscription_type'].name, self.version)
