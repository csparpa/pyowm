"""
Module containing classes for HTTP client/server interactions
"""

# Python 2.x/3.x compatibility imports
try:
    from urllib.error import HTTPError, URLError
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import HTTPError, URLError
    from urllib import urlencode

import socket
from pyowm.exceptions import api_call_error
from pyowm.utils import timeformatutils
from pyowm.webapi25.configuration25 import ROOT_API_URL, ROOT_UV_API_URL, \
    UV_INDEX_URL


class OWMHTTPClient(object):

    API_SUBSCRIPTION_SUBDOMAINS = {
        'free': 'api',
        'pro': 'pro'
    }

    """
    An HTTP client class for the OWM web API. The class can leverage a
    caching mechanism

    :param API_key: a Unicode object representing the OWM web API key
    :type API_key: Unicode
    :param cache: an *OWMCache* concrete instance that will be used to
         cache OWM web API responses.
    :type cache: an *OWMCache* concrete instance
    :param subscription_type: the type of OWM web API subscription to be wrapped.
           The value is used to pick the proper API subdomain for HTTP calls.
           Defaults to: 'free'
    :type subscription_type: str
    """

    def __init__(self, API_key, cache, subscription_type='free'):
        self._API_key = API_key
        self._cache = cache
        self._API_root_URL = ROOT_API_URL % \
                     (self.API_SUBSCRIPTION_SUBDOMAINS[subscription_type],)

    def _lookup_cache_or_invoke_API(self, cache, API_full_url, timeout):
        cached = cache.get(API_full_url)
        if cached:
            return cached
        else:
            try:
                try:
                    from urllib.request import urlopen
                except ImportError:
                    from urllib2 import urlopen
                response = urlopen(API_full_url, None, timeout)
            except HTTPError as e:
                raise api_call_error.APICallError(str(e), e)
            except URLError as e:
                raise api_call_error.APICallError(str(e), e)
            else:
                data = response.read().decode('utf-8')
                cache.set(API_full_url, data)
                return data

    def call_API(self, API_endpoint_URL, params_dict,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT):

        """
        Invokes a specific OWM web API endpoint URL, returning raw JSON data.

        :param API_endpoint_URL: the API endpoint to be invoked
        :type API_endpoint_URL: str
        :param params_dict: a dictionary containing the query parameters to be
            used in the HTTP request (given as key-value couples in the dict)
        :type params_dict: dict
        :param timeout: how many seconds to wait for connection establishment
            (defaults to ``socket._GLOBAL_DEFAULT_TIMEOUT``)
        :type timeout: int
        :returns: a string containing raw JSON data
        :raises: *APICallError*

        """
        url = self._build_full_URL(API_endpoint_URL, params_dict)
        return self._lookup_cache_or_invoke_API(self._cache, url, timeout)

    def _build_full_URL(self, API_endpoint_URL, params_dict):
        """
        Adds the API key and the query parameters dictionary to the specified
        API endpoint URL, returning a complete HTTP request URL.

        :param API_endpoint_URL: the API endpoint base URL
        :type API_endpoint_URL: str
        :param params_dict: a dictionary containing the query parameters to be
            used in the HTTP request (given as key-value couples in the dict)
        :type params_dict: dict
        :param API_key: the OWM web API key
        :type API_key: str
        :returns: a full string HTTP request URL

        """
        url =self._API_root_URL + API_endpoint_URL
        params = params_dict.copy()
        if self._API_key is not None:
            params['APPID'] = self._API_key
        return self._build_query_parameters(url, params)

    def _build_query_parameters(self, base_URL, params_dict):
        """
        Turns dictionary items into query parameters and adds them to the base
        URL

        :param base_URL: the base URL whom the query parameters must be added
            to
        :type base_URL: str
        :param params_dict: a dictionary containing the query parameters to be
            used in the HTTP request (given as key-value couples in the dict)
        :type params_dict: dict
        :returns: a full string HTTP request URL

        """
        return base_URL + '?' + urlencode(params_dict)

    def __repr__(self):
        return "<%s.%s - cache=%s>" % \
            (__name__, self.__class__.__name__, repr(self._cache))


class OWMHttpUVClient(object):

    """
    An HTTP client class for the OWM UV web API. The class can leverage a
    caching mechanism

    :param API_key: a Unicode object representing the OWM UV web API key
    :type API_key: Unicode
    :param cache: an *OWMCache* concrete instance that will be used to
         cache OWM UV web API responses.
    :type cache: an *OWMCache* concrete instance
    """

    def __init__(self, API_key, cache):
        self._API_key = API_key
        self._cache = cache
        self._API_root_URL = ROOT_UV_API_URL

    def _trim_to_ISO8601(self, date_object, interval):
        if interval == 'minute':
            return date_object.strftime('%Y-%m-%dT%H:%MZ')
        elif interval == 'hour':
            return date_object.strftime('%Y-%m-%dT%HZ')
        elif interval == 'day':
            return date_object.strftime('%Y-%m-%dZ')
        elif interval == 'month':
            return date_object.strftime('%Y-%mZ')
        elif interval == 'year':
            return date_object.strftime('%YZ')
        else:
            raise ValueError("The interval provided for UVIndex search "
                             "window is invalid")

    def get_uvi(self, params_dict, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """
        Invokes the UV Index endpoint
        :param params_dict: dict of parameters
        :param timeout: how many seconds to wait for connection establishment
            (defaults to ``socket._GLOBAL_DEFAULT_TIMEOUT``)
        :type timeout: int
        :returns: a string containing raw JSON data
        :raises: *ValueError*, *APICallError*
        """
        lon = str(params_dict['lon'])
        lat = str(params_dict['lat'])
        start = params_dict['start']
        interval = params_dict['interval']

        # build request URL
        url_template = '%s%s/%s,%s/%s.json?appid=%s'
        if start is None:
            timeref = 'current'
        else:
            if interval is None:
                timeref = self._trim_to_ISO8601(
                    timeformatutils.to_UNIXtime(start), 'year')
            else:
                timeref = self._trim_to_ISO8601(
                    timeformatutils.to_date(start), interval)

        url = url_template % (ROOT_UV_API_URL, UV_INDEX_URL, lat, lon,
                              timeref, self._API_key)
        return lookup_cache_or_invoke_API(self._cache, url, timeout)

    def __repr__(self):
        return "<%s.%s - cache=%s>" % \
               (__name__, self.__class__.__name__, repr(self._cache))