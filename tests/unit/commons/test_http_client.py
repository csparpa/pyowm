# -*- coding: utf-8 -*-

import unittest
import requests
import json
from pyowm.exceptions import api_call_error, api_response_error, parse_response_error
from pyowm.commons.http_client import HttpClient


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

    def test_get_json(self):

        expected_data = '{"name": "james bond", "designation": "007"}'

        def monkey_patched_get(uri, params=None, headers=None, timeout=None,
                               verify=False):
            return MockResponse(200, expected_data)

        requests.get = monkey_patched_get
        status, data = HttpClient().get_json('http://anyurl.com')
        self.assertEqual(json.loads(expected_data), data)
        requests.get = self.requests_original_get

    def test_get_json_parse_error(self):

        def monkey_patched_get(uri, params=None, headers=None, timeout=None,
                               verify=False):
            return MockResponse(200, 123846237647236)

        requests.get = monkey_patched_get
        self.assertRaises(parse_response_error.ParseResponseError,
                          HttpClient().get_json,
                          'http://anyurl.com',
                          params=dict(a=1, b=2))
        requests.get = self.requests_original_get

    def cacheable_get_json(self):

        cached_data = '{"name": "james bond", "designation": "007"}'
        other_data = '{"name": "doctor no"}'

        def monkey_patched_get(uri, params=None, headers=None, timeout=None,
                               verify=False):
            return MockResponse(200, other_data)
        requests.get = monkey_patched_get

        # cache hit
        cache = MockCache(cached_data)
        instance = HttpClient(cache=cache)
        status, data = instance.cacheable_get_json('http://anyurl.com')
        self.assertEqual(200, status)
        self.assertEqual(cached_data, data)

        # cache miss
        cache = MockCache(None)
        instance = HttpClient(cache=cache)
        status, data = instance.cacheable_get_json('http://anyurl.com')
        self.assertEqual(200, status)
        self.assertEqual(other_data, data)

        requests.get = self.requests_original_get

    def test_post(self):
        expected_data = '{"key": "value"}'

        def monkey_patched_post(uri, params=None, headers=None, json=None,
                                timeout=None, verify=False):
            return MockResponse(201, expected_data)

        requests.post = monkey_patched_post
        status, data = HttpClient().post('http://anyurl.com', data=dict(key='value'))
        self.assertEqual(json.loads(expected_data), data)

        requests.post = self.requests_original_post

    def test_put(self):
        expected_data = '{"key": "value"}'

        def monkey_patched_put(uri, params=None, headers=None, json=None,
                               timeout=None, verify=False):
            return MockResponse(200, expected_data)

        requests.put = monkey_patched_put
        status, data = HttpClient().put('http://anyurl.com', data=dict(key=7))
        self.assertEqual(json.loads(expected_data), data)


        requests.put = self.requests_original_put

    def test_delete(self):
        # in case an empty payload is returned
        def monkey_patched_delete(uri, params=None, headers=None, json=None,
                                  timeout=None, verify=False):
            return MockResponse(204, None)

        requests.delete = monkey_patched_delete
        status, data = HttpClient().delete('http://anyurl.com')
        self.assertIsNone(data)

        # in case a non-empty payload is returned
        expected_data = '{"message": "deleted"}'

        def monkey_patched_delete_returning_payload(uri, params=None, headers=None,
                                                    json=None, timeout=None,
                                                    verify=False):
            return MockResponse(204, expected_data)

        requests.delete = monkey_patched_delete_returning_payload
        status, data = HttpClient().delete('http://anyurl.com')
        self.assertEqual(json.loads(expected_data), data)

        requests.delete = self.requests_original_delete

    def test_check_status_code(self):
        msg = 'Generic error'
        HttpClient.check_status_code(200, msg)
        with self.assertRaises(api_call_error.APICallError):
            HttpClient.check_status_code(400, msg)
        with self.assertRaises(api_response_error.UnauthorizedError):
            HttpClient.check_status_code(401, msg)
        with self.assertRaises(api_response_error.NotFoundError):
            HttpClient.check_status_code(404, msg)
        with self.assertRaises(api_call_error.BadGatewayError):
            HttpClient.check_status_code(502, msg)
        with self.assertRaises(api_call_error.APICallError):
            HttpClient.check_status_code(555, msg)

    def test_is_success(self):
        self.assertTrue(HttpClient.is_success(200))
        self.assertTrue(HttpClient.is_success(201))
        self.assertTrue(HttpClient.is_success(299))
        self.assertFalse(HttpClient.is_success(300))
        self.assertFalse(HttpClient.is_success(400))
        self.assertFalse(HttpClient.is_success(500))

    def test_to_url(self):
        API_endpoint = 'http://%s.openweathermap.org/data/2.5/ep'
        API_key = 'test_API_key'
        api_subscription = 'free'
        result = HttpClient.to_url(API_endpoint, API_key, api_subscription)
        expected = 'http://api.openweathermap.org/data/2.5/ep?APPID=test_API_key'
        self.assertEqual(expected, expected)

    def test_to_url_with_no_API_key(self):
        API_endpoint = 'http://%s.openweathermap.org/data/2.5/ep'
        params = {'a': 1, 'b': 2}
        api_subscription = 'pro'
        result = HttpClient.to_url(API_endpoint, None, api_subscription)
        expected = 'http://pro.openweathermap.org/data/2.5/ep'
        self.assertEqual(expected, result)

    def test_to_url_with_unicode_chars_in_API_key(self):
        API_key = '£°test££'
        API_endpoint = 'http://%s.openweathermap.org/data/2.5/ep'
        api_subscription = 'free'
        result = HttpClient.to_url(API_endpoint, API_key, api_subscription)
        expected = 'http://api.openweathermap.org/data/2.5/ep?APPID=%C2%A3%C2%B0test%C2%A3%C2%A3'
        self.assertEqual(expected, result)

    def test_fix_schema_to_http(self):
        API_endpoint = 'http://api.openweathermap.org/data/2.5/ep?APPID=%C2%A3%C2%B0test%C2%A3%C2%A3'
        result = HttpClient._fix_schema(API_endpoint, False)
        self.assertEqual(API_endpoint, result)

    def test_fix_schema_to_https(self):
        API_endpoint = 'http://api.openweathermap.org/data/2.5/ep?APPID=%C2%A3%C2%B0test%C2%A3%C2%A3'
        expected = 'https://api.openweathermap.org/data/2.5/ep?APPID=%C2%A3%C2%B0test%C2%A3%C2%A3'
        result = HttpClient._fix_schema(API_endpoint, True)
        self.assertEqual(expected, result)

    def test_escape_subdomain(self):
        # correct subscription type
        API_endpoint = 'http://%s.openweathermap.org/data/2.5/ep'
        api_subscription = 'free'
        expected = 'http://api.openweathermap.org/data/2.5/ep'
        result = HttpClient._escape_subdomain(API_endpoint, api_subscription)
        self.assertEqual(expected, result)

        # non-existing subscription type
        API_endpoint = 'http://%s.openweathermap.org/data/2.5/ep'
        try:
            HttpClient._escape_subdomain(API_endpoint, 'unexistent')
            self.fail()
        except ValueError:
            pass

        # no subdomains needed
        API_endpoint = 'http://test.com'
        result = HttpClient._escape_subdomain(API_endpoint, api_subscription)
        self.assertEqual(API_endpoint, result)

        # subscription type is None
        API_endpoint = 'http://test.com'
        result = HttpClient._escape_subdomain(API_endpoint, None)
        self.assertEqual(API_endpoint, result)

    def test_timeouts(self):
        timeout = 0.5
        def monkey_patched_get_timeouting(uri, params=None, headers=None,
                                          timeout=timeout, verify=False):
            raise requests.exceptions.Timeout()

        requests.get = monkey_patched_get_timeouting
        try:
            status, data = HttpClient(timeout=timeout).get_json('http://anyurl.com')
            self.fail()
        except api_call_error.APICallTimeoutError:
            requests.get = self.requests_original_get

    def test_get_png(self):
        expected_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x00\x00%\xdbV\xca\x00\x00\x00\x03PLTE\x00p\xff\xa5G\xab\xa1\x00\x00\x00\x01tRNS\xcc\xd24V\xfd\x00\x00\x00\nIDATx\x9ccb\x00\x00\x00\x06\x00\x0367|\xa8\x00\x00\x00\x00IEND\xaeB`\x82'

        def monkey_patched_get(uri, stream=True, params=None, headers=None, timeout=None,
                               verify=False):
            return MockResponse(200, expected_data)

        requests.get = monkey_patched_get
        status, data = HttpClient().get_png('http://anyurl.com')
        self.assertIsInstance(data, bytes)
        self.assertEqual(expected_data, data)
        requests.get = self.requests_original_get

    def test_get_geotiff(self):
        expected_data = b'II*\x00\x08\x00\x04\x00k{\x84s\x84\x84\x8c\x84\x84\x84k\x84k\x84\x84k{s\x9c\x94k\x84'

        def monkey_patched_get(uri, stream=True, params=None, headers=None, timeout=None,
                               verify=False):
            return MockResponse(200, expected_data)

        requests.get = monkey_patched_get
        status, data = HttpClient().get_geotiff('http://anyurl.com')
        self.assertIsInstance(data, bytes)
        self.assertEqual(expected_data, data)
        requests.get = self.requests_original_get
