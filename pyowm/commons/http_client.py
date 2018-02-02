import requests
import json
from pyowm.caches import nullcache
from pyowm.exceptions import api_call_error, unauthorized_error, not_found_error, \
    parse_response_error
from pyowm.webapi25.configuration25 import API_AVAILABILITY_TIMEOUT, \
    API_SUBSCRIPTION_SUBDOMAINS


class HttpClient(object):

    def __init__(self, timeout=API_AVAILABILITY_TIMEOUT, cache=None):
        self.timeout = timeout
        if cache is None:
            self.cache = nullcache.NullCache()
        else:
            self.cache = cache

    def get_json(self, uri, params=None, headers=None):
        try:
            resp = requests.get(uri, params=params, headers=headers,
                                timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise api_call_error.APICallTimeoutError('API call timeouted')
        HttpClient.check_status_code(resp.status_code, resp.text)
        try:
            return resp.status_code, resp.json()
        except:
            raise parse_response_error.ParseResponseError('Impossible to parse'
                                                          'API response data')

    def cacheable_get_json(self, uri, params=None, headers=None):
        # check if already cached
        cached = self.cache.get(uri)
        if cached:
            return 200, cached
        status_code, data = self.get_json(uri, params=params, headers=headers)
        json_string = json.dumps(data)
        self.cache.set(uri, json_string)
        return status_code, json_string


    def post(self, uri, params=None, data=None, headers=None):
        try:
            resp = requests.post(uri, params=params, json=data, headers=headers,
                                 timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise api_call_error.APICallTimeoutError('API call timeouted')
        HttpClient.check_status_code(resp.status_code, resp.text)
        # this is a defense against OWM API responses containing an empty body!
        try:
            json_data = resp.json()
        except:
            json_data = {}
        return resp.status_code, json_data

    def put(self, uri, params=None, data=None, headers=None):
        try:
            resp = requests.put(uri, params=params, json=data, headers=headers,
                                timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise api_call_error.APICallTimeoutError('API call timeouted')
        HttpClient.check_status_code(resp.status_code, resp.text)
        # this is a defense against OWM API responses containing an empty body!
        try:
            json_data = resp.json()
        except:
            json_data = {}
        return resp.status_code, json_data

    def delete(self, uri, params=None, data=None, headers=None):
        try:
            resp = requests.delete(uri, params=params, json=data, headers=headers,
                                   timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise api_call_error.APICallTimeoutError('API call timeouted')
        HttpClient.check_status_code(resp.status_code, resp.text)
        # this is a defense against OWM API responses containing an empty body!
        try:
            json_data = resp.json()
        except:
            json_data = None
        return resp.status_code, json_data


    @classmethod
    def check_status_code(cls, status_code, payload):
        if status_code < 400:
            return
        if status_code == 400:
            raise api_call_error.APICallError(payload)
        elif status_code == 401:
            raise unauthorized_error.UnauthorizedError('Invalid API Key provided')
        elif status_code == 404:
            raise not_found_error.NotFoundError('Unable to find the resource')
        elif status_code == 502:
            raise api_call_error.BadGatewayError('Unable to contact the upstream server')
        else:
            raise api_call_error.APICallError(payload)

    @classmethod
    def is_success(cls, status_code):
        if 200 <= status_code < 300:
            return True
        return False

    @classmethod
    def to_url(cls, API_endpoint_URL, API_key, subscription_type):
        # Add API Key to query params
        params = dict()
        if API_key is not None:
            params['APPID'] = API_key
        # Escape subscription subdomain if needed
        escaped_url = HttpClient._escape_subdomain(API_endpoint_URL, subscription_type)
        r = requests.Request('GET', escaped_url, params=params).prepare()
        return r.url

    @classmethod
    def _escape_subdomain(cls, API_endpoint_URL, subscription_type):
        if subscription_type is None:
            return API_endpoint_URL
        try:
            return API_endpoint_URL % (API_SUBSCRIPTION_SUBDOMAINS[subscription_type],)
        except KeyError:
            raise ValueError('Unexistent API subscription type')
        except TypeError:  # API endpoint URL is not escapable
            return API_endpoint_URL

    def __repr__(self):
        return "<%s.%s - timeout=%s - cache=%s>" % \
               (__name__, self.__class__.__name__, repr(self.timeout),
                str(self.cache) if self.cache is not None else 'None')