from pyowm.commons.http_client import HttpClient
from pyowm.commons.uris import ROOT_GEOCODING_API_URL, DIRECT_GEOCODING_URI, REVERSE_GEOCODING_URI
from pyowm.constants import GEOCODING_API_VERSION
from pyowm.utils import geo
from pyowm.weatherapi25.location import Location


class GeocodingManager:

    """
    A manager objects that provides a full interface to OWM Geocoding API.

    :param API_key: the OWM API key
    :type API_key: str
    :param config: the configuration dictionary
    :type config: dict
    :returns: an *GeocodingManager* instance
    :raises: *AssertionError* when no API Key is provided

    """

    def __init__(self, API_key, config):
        assert API_key is not None, 'You must provide a valid API Key'
        self.API_key = API_key
        assert isinstance(config, dict)
        self.http_client = HttpClient(API_key, config, ROOT_GEOCODING_API_URL)

    def geocoding_api_version(self):
        return GEOCODING_API_VERSION

    def geocode(self, toponym, country=None, state_code=None, limit=None):
        """
        Invokes the direct geocoding API endpoint

        :param toponym: the name of the location
        :type toponym: `str`
        :param country: the 2-chars ISO symbol of the country
        :type country: `str` or `None`
        :param state_code: the 2-chars ISO symbol of state (only useful in case the country is US)
        :type state_code: `str` or `None`
        :param limit: the max number of results to be returned in case of multiple matchings (no limits by default)
        :type limit: `int` or `None`
        :returns: a list of *Location* instances
        :raises: *AssertionError*, *ValueError*, *APIRequestError*

        """
        assert toponym, 'Toponym must be specified'
        if country is not None and len(country) != 2:
            raise ValueError("Country must be a 2-char string")
        if state_code is not None and len(state_code) != 2:
            raise ValueError("State Code must be a 2-char string")
        if limit is not None:
            assert isinstance(limit, int)
            assert limit > 0

        query = toponym
        if state_code is not None:
            query += ',' + state_code
        if country is not None:
            query += ',' + country

        params = {'q': query}

        if limit is not None:
            params['limit'] = limit

        _, json_data = self.http_client.get_json(DIRECT_GEOCODING_URI, params=params)
        return [Location.from_dict(item) for item in json_data]

    def reverse_geocode(self, lat, lon, limit=None):
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        if limit is not None:
            assert isinstance(limit, int)
            assert limit > 0

        params = {'lat': lat, 'lon': lon}
        if limit is not None:
            params['limit'] = limit

        _, json_data = self.http_client.get_json(REVERSE_GEOCODING_URI, params=params)
        return [Location.from_dict(item) for item in json_data]

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)