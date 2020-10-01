#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import requests
import json
import pyowm.commons.exceptions
from pyowm.config import DEFAULT_CONFIG
from pyowm.commons.enums import SubscriptionTypeEnum
from pyowm.commons.http_client import HttpClient, HttpRequestBuilder


class MockResponse:
    def __init__(self, status, payload):
        self.status_code = status
        self.text = payload
        self.content = payload

    def json(self):
        return json.loads(self.text)


class MockCache:
    def __init__(self, expected_back):
        self.expected_back = expected_back

    def get(self, url):
        return self.expected_back

    def set(self, url, json_str):
        pass


class TestHTTPClient(unittest.TestCase):

    requests_original_get = requests.get
    requests_original_post = requests.post
    requests_original_put= requests.put
    requests_original_delete = requests.delete

    def test_instantiation(self):
        self.assertRaises(AssertionError, HttpClient, None, DEFAULT_CONFIG, 'test.com', True)
        self.assertRaises(AssertionError, HttpClient, 'apikey', None, 'test.com', True)
        self.assertRaises(AssertionError, HttpClient, 'apikey', DEFAULT_CONFIG, None, True)
        self.assertRaises(AssertionError, HttpClient, 'apikey', DEFAULT_CONFIG, 'test.com', None)

    def test_get_json(self):

        expected_data = '{"name": "james bond", "designation": "007"}'

        def monkey_patched_get(uri, params=None, headers=None, proxies=None, timeout=None, verify=False):
            return MockResponse(200, expected_data)

        requests.get = monkey_patched_get
        status, data = HttpClient('apikey', DEFAULT_CONFIG, 'anyurl.com').get_json('/resource')
        self.assertEqual(json.loads(expected_data), data)
        requests.get = self.requests_original_get

    def test_get_json_parse_error(self):

        def monkey_patched_get(uri, params=None, headers=None, proxies=None, timeout=None, verify=False):
            return MockResponse(200, 123846237647236)

        requests.get = monkey_patched_get
        self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError,
                          HttpClient('apikey', DEFAULT_CONFIG, 'anyurl.com').get_json, '/resource', params=dict(a=1, b=2))
        requests.get = self.requests_original_get

    def test_post(self):
        expected_data = '{"key": "value"}'

        def monkey_patched_post(uri, params=None, headers=None, proxies=None, json=None, timeout=None, verify=False):
            return MockResponse(201, expected_data)

        requests.post = monkey_patched_post
        status, data = HttpClient('apikey', DEFAULT_CONFIG, 'anyurl.com').post('/resource', data=dict(key='value'))
        self.assertEqual(json.loads(expected_data), data)
        requests.post = self.requests_original_post

    def test_put(self):
        expected_data = '{"key": "value"}'

        def monkey_patched_put(uri, params=None, headers=None, proxies=None, json=None, timeout=None, verify=False):
            return MockResponse(200, expected_data)

        requests.put = monkey_patched_put
        status, data = HttpClient('apikey', DEFAULT_CONFIG, 'anyurl.com').put('/resource', data=dict(key=7))
        self.assertEqual(json.loads(expected_data), data)
        requests.put = self.requests_original_put

    def test_delete(self):
        # in case an empty payload is returned
        def monkey_patched_delete(uri, params=None, headers=None, proxies=None, json=None, timeout=None, verify=False):
            return MockResponse(204, None)

        requests.delete = monkey_patched_delete
        status, data = HttpClient('apikey', DEFAULT_CONFIG, 'anyurl.com').delete('/resource')
        self.assertIsNone(data)

        # in case a non-empty payload is returned
        expected_data = '{"message": "deleted"}'

        def monkey_patched_delete_returning_payload(uri, params=None, headers=None, proxies=None,  json=None, timeout=None, verify=False):
            return MockResponse(204, expected_data)

        requests.delete = monkey_patched_delete_returning_payload
        status, data = HttpClient('apikey', DEFAULT_CONFIG, 'anyurl.com').delete('/resource')
        self.assertEqual(json.loads(expected_data), data)

        requests.delete = self.requests_original_delete

    def test_check_status_code(self):
        msg = 'Generic error'
        HttpClient.check_status_code(200, msg)
        with self.assertRaises(pyowm.commons.exceptions.APIRequestError):
            HttpClient.check_status_code(400, msg)
        with self.assertRaises(pyowm.commons.exceptions.UnauthorizedError):
            HttpClient.check_status_code(401, msg)
        with self.assertRaises(pyowm.commons.exceptions.NotFoundError):
            HttpClient.check_status_code(404, msg)
        with self.assertRaises(pyowm.commons.exceptions.BadGatewayError):
            HttpClient.check_status_code(502, msg)
        with self.assertRaises(pyowm.commons.exceptions.APIRequestError):
            HttpClient.check_status_code(555, msg)

    def test_timeouts(self):
        timeout = 0.5

        def monkey_patched_get_timeouting(uri, params=None, headers=None, proxies=None, timeout=timeout, verify=False):
            raise requests.exceptions.Timeout()

        requests.get = monkey_patched_get_timeouting
        config = DEFAULT_CONFIG.copy()
        config['connection']['timeout_secs'] = timeout
        try:
            status, data = HttpClient('apikey', config, 'anyurl.com').get_json('/resource')
            self.fail()
        except pyowm.commons.exceptions.TimeoutError:
            requests.get = self.requests_original_get

    def test_get_png(self):
        expected_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x00\x00%\xdbV\xca\x00\x00\x00\x03PLTE\x00p\xff\xa5G\xab\xa1\x00\x00\x00\x01tRNS\xcc\xd24V\xfd\x00\x00\x00\nIDATx\x9ccb\x00\x00\x00\x06\x00\x0367|\xa8\x00\x00\x00\x00IEND\xaeB`\x82'

        def monkey_patched_get(uri, stream=True, params=None, headers=None, proxies=None, timeout=None, verify=False):
            return MockResponse(200, expected_data)

        requests.get = monkey_patched_get
        status, data = HttpClient('apikey', DEFAULT_CONFIG, 'anyurl.com').get_png('/resource')
        self.assertIsInstance(data, bytes)
        self.assertEqual(expected_data, data)
        requests.get = self.requests_original_get

    def test_get_geotiff(self):
        expected_data = b'II*\x00\x08\x00\x04\x00k{\x84s\x84\x84\x8c\x84\x84\x84k\x84k\x84\x84k{s\x9c\x94k\x84'

        def monkey_patched_get(uri, stream=True, params=None, headers=None, proxies=None, timeout=None, verify=False):
            return MockResponse(200, expected_data)

        requests.get = monkey_patched_get
        status, data = HttpClient('apikey', DEFAULT_CONFIG, 'anyurl.com').get_geotiff('/resource')
        self.assertIsInstance(data, bytes)
        self.assertEqual(expected_data, data)
        requests.get = self.requests_original_get

    def test_repr(self):
        print(HttpClient('apikey', DEFAULT_CONFIG, 'anyurl.com'))


class TestHttpRequestBuilder(unittest.TestCase):

    test_config = {
        'subscription_type': SubscriptionTypeEnum.FREE,
        'language': 'jp',
        'connection': {
            'use_ssl': False,
            'use_proxy': True
        },
        'proxies': {
            'http': 'http://my:secret@proxy:3128',
        }
    }

    def test_instantiation_with_wrong_params(self):
        with self.assertRaises(AssertionError):
            HttpRequestBuilder(None, 'apikey', self.test_config)
        with self.assertRaises(AssertionError):
            HttpRequestBuilder('test.com', None, self.test_config)
        with self.assertRaises(AssertionError):
            HttpRequestBuilder('test.com', 'apikey', None)
        with self.assertRaises(AssertionError):
            HttpRequestBuilder('test.com', 'apikey', self.test_config, has_subdomains=1234)

    def test__set_schema(self):
        with_ssl = self.test_config.copy()
        with_ssl['connection']['use_ssl'] = True
        instance = HttpRequestBuilder('test.com', 'apikey', with_ssl)
        self.assertEqual('https', instance.schema)
        without_ssl = self.test_config.copy()
        without_ssl['connection']['use_ssl'] = False
        instance = HttpRequestBuilder('test.com', 'apikey', without_ssl)
        self.assertEqual('http', instance.schema)

    def test__set_subdomain(self):
        # in case of a root URL with subdomains
        for st in SubscriptionTypeEnum.items():
            config = self.test_config.copy()
            config['subscription_type'] = st
            instance = HttpRequestBuilder('test.com', 'apikey', config)
            self.assertEqual(st.subdomain, instance.subdomain)

        # in case of a root URL without subdomains
        instance = HttpRequestBuilder('nosubdomains.com', 'apikey', self.test_config, has_subdomains=False)
        self.assertIsNone(instance.subdomain)
        instance._set_subdomain()
        self.assertIsNone(instance.subdomain)

    def test__set_proxies(self):
        with_proxies = self.test_config.copy()
        with_proxies['connection']['use_proxy'] = True
        instance = HttpRequestBuilder('test.com', 'apikey', with_proxies)
        self.assertEqual(with_proxies['proxies'], instance.proxies)
        without_proxies = self.test_config.copy()
        without_proxies['connection']['use_proxy'] = False
        instance = HttpRequestBuilder('test.com', 'apikey', without_proxies)
        self.assertEqual(dict(), instance.proxies)

    def test_with_path(self):
        instance = HttpRequestBuilder('test.com', 'apikey', self.test_config)
        self.assertEqual(None, instance.path)
        path = 'test/path'
        instance.with_path(path)
        self.assertEqual(path, instance.path)
        with self.assertRaises(AssertionError):
            instance.with_path(1234)

    def test_with_api_key(self):
        apikey = 'xyz'
        instance = HttpRequestBuilder('test.com', apikey, self.test_config)
        self.assertIsNotNone(instance.api_key)
        self.assertEqual(dict(), instance.params)
        instance.with_api_key()
        self.assertTrue('APPID' in instance.params.keys())
        self.assertEqual(apikey, instance.params.get('APPID'))

    def test_with_language(self):
        lang = 'fr'
        config = self.test_config.copy()
        config['language'] = lang
        instance = HttpRequestBuilder('test.com', 'apikey', config)
        self.assertEqual(dict(), instance.params)
        instance.with_language()
        self.assertTrue('lang' in instance.params.keys())
        self.assertEqual(lang, instance.params.get('lang'))

    def test_with_query_params(self):
        params = dict(a=1, b=2)
        instance = HttpRequestBuilder('test.com', 'apikey', self.test_config)
        self.assertEqual(dict(), instance.params)
        instance.with_query_params(params)
        self.assertEqual(params, instance.params)
        more_params = dict(c=3, d=4)
        params.update(more_params)
        instance.with_query_params(more_params)
        self.assertEqual(params, instance.params)
        with self.assertRaises(AssertionError):
            instance.with_query_params('not-a-dict')

    def test_with_headers(self):
        headers = dict(a=1, b=2)
        instance = HttpRequestBuilder('test.com', 'apikey', self.test_config)
        self.assertEqual(dict(), instance.headers)
        instance.with_headers(headers)
        self.assertEqual(headers, instance.headers)
        more_headers = dict(c=3, d=4)
        headers.update(more_headers)
        instance.with_headers(more_headers)
        self.assertEqual(headers, instance.headers)
        with self.assertRaises(AssertionError):
            instance.with_headers('not-a-dict')

    def test_with_header(self):
        instance = HttpRequestBuilder('test.com', 'apikey', self.test_config)
        self.assertEqual(dict(), instance.headers)
        hkey = 'key'
        hvalue = 'value'
        instance.with_header(hkey, hvalue)
        self.assertEqual({hkey: hvalue}, instance.headers)
        with self.assertRaises(AssertionError):
            instance.with_header(123, 'value')
        with self.assertRaises(ValueError):
            instance.with_header('key', bytes()) # any non-serializable value is OK here

    def test_build_with_subdomains(self):
        apikey = 'apikey'
        lang = 'ru'
        proxies = {'https': 'https://my:secret@proxy:3128'}
        config = {
            'subscription_type': SubscriptionTypeEnum.PROFESSIONAL,
            'language': lang,
            'connection': {
                'use_ssl': True,
                'use_proxy': True
            },
            'proxies': proxies
        }
        expected_url = 'https://api.test.com/root/path-to-resource.json'
        expected_params = {
            'q': 'my-query',
            'APPID': apikey,
            'lang': lang
        }
        expected_headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'it,en;q=0.9',
            'cache-control': 'no-cache'
        }
        expected_proxies = proxies
        instance = HttpRequestBuilder('test.com/root', apikey, config)
        instance\
            .with_api_key()\
            .with_language()\
            .with_path('path-to-resource.json')\
            .with_query_params({'q': 'my-query'})\
            .with_headers({
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'it,en;q=0.9'
            })\
            .with_header('cache-control', 'no-cache')
        result_url, result_params, result_headers, result_proxies = instance.build()
        self.assertEqual(expected_url, result_url)
        self.assertEqual(expected_params, result_params)
        self.assertEqual(expected_headers, result_headers)
        self.assertEqual(expected_proxies, result_proxies)

    def test_build_without_subdomains(self):
        apikey = 'apikey'
        lang = 'ru'
        proxies = {'https': 'https://my:secret@proxy:3128'}
        config = {
            'subscription_type': SubscriptionTypeEnum.PROFESSIONAL,
            'language': lang,
            'connection': {
                'use_ssl': True,
                'use_proxy': True
            },
            'proxies': proxies
        }
        expected_url = 'https://test.com/root/path-to-resource.json'
        expected_params = {
            'q': 'my-query',
            'APPID': apikey,
            'lang': lang
        }
        expected_headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'it,en;q=0.9',
            'cache-control': 'no-cache'
        }
        expected_proxies = proxies
        instance = HttpRequestBuilder('test.com/root', apikey, config, has_subdomains=False)
        instance\
            .with_api_key()\
            .with_language()\
            .with_path('path-to-resource.json')\
            .with_query_params({'q': 'my-query'})\
            .with_headers({
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'it,en;q=0.9'
            })\
            .with_header('cache-control', 'no-cache')
        result_url, result_params, result_headers, result_proxies = instance.build()
        self.assertEqual(expected_url, result_url)
        self.assertEqual(expected_params, result_params)
        self.assertEqual(expected_headers, result_headers)
        self.assertEqual(expected_proxies, result_proxies)

    def test_fluidity_of_interface(self):
        instance = HttpRequestBuilder('test.com/root', 'apikey', self.test_config)
        self.assertTrue(isinstance(instance.with_path('/path'), HttpRequestBuilder))
        self.assertTrue(isinstance(instance.with_headers({}), HttpRequestBuilder))
        self.assertTrue(isinstance(instance.with_query_params({}), HttpRequestBuilder))
        self.assertTrue(isinstance(instance.with_header('key', 'value'), HttpRequestBuilder))
        self.assertTrue(isinstance(instance.with_api_key(), HttpRequestBuilder))
        self.assertTrue(isinstance(instance.with_language(), HttpRequestBuilder))

    def test_repr(self):
        print(HttpRequestBuilder('/test', 'apikey', self.test_config))