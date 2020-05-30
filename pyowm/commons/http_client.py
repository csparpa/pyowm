#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

from pyowm.commons import exceptions
from pyowm.commons.enums import ImageTypeEnum


class HttpRequestBuilder:

    URL_TEMPLATE_WITH_SUBDOMAINS = '{}://{}.{}/{}'
    URL_TEMPLATE_WITHOUT_SUBDOMAINS = '{}://{}/{}'

    """
    A stateful HTTP URL, params and headers builder with a fluent interface
    """
    def __init__(self, root_uri_token, api_key, config, has_subdomains=True):
        assert isinstance(root_uri_token, str)
        self.root = root_uri_token
        assert isinstance(api_key, str)
        self.api_key = api_key
        assert isinstance(config, dict)
        self.config = config
        assert isinstance(has_subdomains, bool)
        self.has_subdomains = has_subdomains
        self.schema = None
        self.subdomain = None
        self.proxies = None
        self.path = None
        self.params = dict()
        self.headers = dict()
        self._set_schema()
        self._set_subdomain()
        self._set_proxies()

    def _set_schema(self):
        use_ssl = self.config['connection']['use_ssl']
        if use_ssl:
            self.schema = 'https'
        else:
            self.schema = 'http'

    def _set_subdomain(self):
        if self.has_subdomains:
            st = self.config['subscription_type']
            self.subdomain = st.subdomain

    def _set_proxies(self):
        if self.config['connection']['use_proxy']:
            self.proxies = self.config['proxies']
        else:
            self.proxies = dict()

    def with_path(self, path_uri_token):
        assert isinstance(path_uri_token, str)
        self.path = path_uri_token
        return self

    def with_headers(self, headers):
        assert isinstance(headers, dict)
        self.headers.update(headers)
        return self

    def with_header(self, key, value):
        assert isinstance(key, str)
        try:
            json.dumps(value)
        except TypeError:
            raise ValueError('Header value is not JSON serializable')
        self.headers.update({key: value})
        return self

    def with_query_params(self, query_params):
        assert isinstance(query_params, dict)
        self.params.update(query_params)
        return self

    def with_api_key(self):
        self.params['APPID'] = self.api_key
        return self

    def with_language(self):
        self.params['lang'] = self.config['language']
        return self

    def build(self):
        if self.has_subdomains:
            return self.URL_TEMPLATE_WITH_SUBDOMAINS.format(self.schema, self.subdomain, self.root, self.path), \
                   self.params, self.headers, self.proxies
        else:
            return self.URL_TEMPLATE_WITHOUT_SUBDOMAINS.format(self.schema, self.root, self.path), \
                   self.params, self.headers, self.proxies

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)


class HttpClient:

    """
    An HTTP client encapsulating some config data and abstarcting away data raw retrieval

    :param api_key: the OWM API key
    :type api_key: str
    :param config: the configuration dictionary (if not provided, a default one will be used)
    :type config: dict
    :param root_uri: the root URI of the API endpoint
    :type root_uri: str
    :param admits_subdomains: if the root URI of the API endpoint admits subdomains based on the subcription type (default: True)
    :type admits_subdomains: bool
    """

    def __init__(self, api_key, config, root_uri, admits_subdomains=True):
        assert isinstance(api_key, str)
        self.api_key = api_key
        assert isinstance(config, dict)
        self.config = config
        assert isinstance(root_uri, str)
        self.root_uri = root_uri
        assert isinstance(admits_subdomains, bool)
        self.admits_subdomains = admits_subdomains

    def get_json(self, path, params=None, headers=None):
        builder = HttpRequestBuilder(self.root_uri, self.api_key, self.config, has_subdomains=self.admits_subdomains)\
            .with_path(path)\
            .with_api_key()\
            .with_language()\
            .with_query_params(params if params is not None else dict())\
            .with_headers(headers if headers is not None else dict())
        url, params, headers, proxies = builder.build()
        try:
            resp = requests.get(url, params=params, headers=headers, proxies=proxies,
                                timeout=self.config['connection']['timeout_secs'],
                                verify=self.config['connection']['verify_ssl_certs'])
        except requests.exceptions.SSLError as e:
            raise exceptions.InvalidSSLCertificateError(str(e))
        except requests.exceptions.ConnectionError as e:
            raise exceptions.InvalidSSLCertificateError(str(e))
        except requests.exceptions.Timeout:
            raise exceptions.TimeoutError('API call timeouted')
        HttpClient.check_status_code(resp.status_code, resp.text)
        try:
            return resp.status_code, resp.json()
        except:
            raise exceptions.ParseAPIResponseError('Impossible to parse API response data')

    def get_png(self, path, params=None, headers=None):
        builder = HttpRequestBuilder(self.root_uri, self.api_key, self.config, has_subdomains=self.admits_subdomains)\
            .with_path(path)\
            .with_api_key()\
            .with_language()\
            .with_query_params(params if params is not None else dict())\
            .with_headers(headers if headers is not None else dict())\
            .with_header('Accept', ImageTypeEnum.PNG.mime_type)
        url, params, headers, proxies = builder.build()
        try:
            resp = requests.get(url, stream=True, params=params, headers=headers, proxies=proxies,
                                timeout=self.config['connection']['timeout_secs'],
                                verify=self.config['connection']['verify_ssl_certs'])
        except requests.exceptions.SSLError as e:
            raise exceptions.InvalidSSLCertificateError(str(e))
        except requests.exceptions.ConnectionError as e:
            raise exceptions.InvalidSSLCertificateError(str(e))
        except requests.exceptions.Timeout:
            raise exceptions.TimeoutError('API call timeouted')
        HttpClient.check_status_code(resp.status_code, resp.text)
        try:
            return resp.status_code, resp.content
        except:
            raise exceptions.ParseAPIResponseError('Impossible to parse'
                                                          'API response data')

    def get_geotiff(self, path, params=None, headers=None):
        builder = HttpRequestBuilder(self.root_uri, self.api_key, self.config, has_subdomains=self.admits_subdomains)\
            .with_path(path)\
            .with_api_key()\
            .with_language()\
            .with_query_params(params if params is not None else dict())\
            .with_headers(headers if headers is not None else dict())\
            .with_header('Accept', ImageTypeEnum.GEOTIFF.mime_type)
        url, params, headers, proxies = builder.build()
        try:
            resp = requests.get(url, stream=True, params=params, headers=headers, proxies=proxies,
                                timeout=self.config['connection']['timeout_secs'],
                                verify=self.config['connection']['verify_ssl_certs'])
        except requests.exceptions.SSLError as e:
            raise exceptions.InvalidSSLCertificateError(str(e))
        except requests.exceptions.ConnectionError as e:
            raise exceptions.InvalidSSLCertificateError(str(e))
        except requests.exceptions.Timeout:
            raise exceptions.TimeoutError('API call timeouted')
        HttpClient.check_status_code(resp.status_code, resp.text)
        try:
            return resp.status_code, resp.content
        except:
            raise exceptions.ParseAPIResponseError('Impossible to parse'
                                                          'API response data')

    def post(self, path, params=None, data=None, headers=None):
        builder = HttpRequestBuilder(self.root_uri, self.api_key, self.config, has_subdomains=self.admits_subdomains)\
            .with_path(path)\
            .with_api_key()\
            .with_language()\
            .with_query_params(params if params is not None else dict())\
            .with_headers(headers if headers is not None else dict())
        url, params, headers, proxies = builder.build()
        try:
            resp = requests.post(url, params=params, json=data, headers=headers, proxies=proxies,
                                 timeout=self.config['connection']['timeout_secs'],
                                 verify=self.config['connection']['verify_ssl_certs'])
        except requests.exceptions.SSLError as e:
            raise exceptions.InvalidSSLCertificateError(str(e))
        except requests.exceptions.ConnectionError as e:
            raise exceptions.InvalidSSLCertificateError(str(e))
        except requests.exceptions.Timeout:
            raise exceptions.TimeoutError('API call timeouted')
        HttpClient.check_status_code(resp.status_code, resp.text)
        # this is a defense against OWM API responses containing an empty body!
        try:
            json_data = resp.json()
        except:
            json_data = {}
        return resp.status_code, json_data

    def put(self, path, params=None, data=None, headers=None):
        builder = HttpRequestBuilder(self.root_uri, self.api_key, self.config, has_subdomains=self.admits_subdomains)\
            .with_path(path)\
            .with_api_key()\
            .with_language()\
            .with_query_params(params if params is not None else dict())\
            .with_headers(headers if headers is not None else dict())
        url, params, headers, proxies = builder.build()
        try:
            resp = requests.put(url, params=params, json=data, headers=headers, proxies=proxies,
                                timeout=self.config['connection']['timeout_secs'],
                                verify=self.config['connection']['verify_ssl_certs'])
        except requests.exceptions.SSLError as e:
            raise exceptions.InvalidSSLCertificateError(str(e))
        except requests.exceptions.ConnectionError as e:
            raise exceptions.InvalidSSLCertificateError(str(e))
        except requests.exceptions.Timeout:
            raise exceptions.TimeoutError('API call timeouted')
        HttpClient.check_status_code(resp.status_code, resp.text)
        # this is a defense against OWM API responses containing an empty body!
        try:
            json_data = resp.json()
        except:
            json_data = {}
        return resp.status_code, json_data

    def delete(self, path, params=None, data=None, headers=None):
        builder = HttpRequestBuilder(self.root_uri, self.api_key, self.config, has_subdomains=self.admits_subdomains)\
            .with_path(path)\
            .with_api_key()\
            .with_language()\
            .with_query_params(params if params is not None else dict())\
            .with_headers(headers if headers is not None else dict())
        url, params, headers, proxies = builder.build()
        try:
            resp = requests.delete(url, params=params, json=data, headers=headers, proxies=proxies,
                                   timeout=self.config['connection']['timeout_secs'],
                                   verify=self.config['connection']['verify_ssl_certs'])
        except requests.exceptions.SSLError as e:
            raise exceptions.InvalidSSLCertificateError(str(e))
        except requests.exceptions.ConnectionError as e:
            raise exceptions.InvalidSSLCertificateError(str(e))
        except requests.exceptions.Timeout:
            raise exceptions.TimeoutError('API call timeouted')
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
            raise exceptions.APIRequestError(payload)
        elif status_code == 401:
            raise exceptions.UnauthorizedError('Invalid API Key provided')
        elif status_code == 404:
            raise exceptions.NotFoundError('Unable to find the resource')
        elif status_code == 502:
            raise exceptions.BadGatewayError('Unable to contact the upstream server')
        else:
            raise exceptions.APIRequestError(payload)

    def __repr__(self):
        return "<%s.%s - root: %s>" % (__name__, self.__class__.__name__, self.root_uri)
