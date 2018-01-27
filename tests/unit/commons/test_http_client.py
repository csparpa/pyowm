# -*- coding: utf-8 -*-

import unittest
import requests
import json
from pyowm.exceptions import api_call_error, unauthorized_error, not_found_error, \
    parse_response_error
from pyowm.commons.http_client import HttpClient


class MockResponse:
    def __init__(self, status, payload):
        self.status_code = status
        self.text = payload

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

        def monkey_patched_get(uri, params=None, headers=None, timeout=None):
            return MockResponse(200, expected_data)

        requests.get = monkey_patched_get
        status, data = HttpClient().get_json('http://anyurl.com')
        self.assertEqual(json.loads(expected_data), data)
        requests.get = self.requests_original_get

    def test_get_json_parse_error(self):

        def monkey_patched_get(uri, params=None, headers=None, timeout=None):
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

        def monkey_patched_get(uri, params=None, headers=None, timeout=None):
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
                                timeout=None):
            return MockResponse(201, expected_data)

        requests.post = monkey_patched_post
        status, data = HttpClient().post('http://anyurl.com', data=dict(key='value'))
        self.assertEqual(json.loads(expected_data), data)

        requests.post = self.requests_original_post

    def test_put(self):
        expected_data = '{"key": "value"}'

        def monkey_patched_put(uri, params=None, headers=None, json=None,
                               timeout=None):
            return MockResponse(200, expected_data)

        requests.put = monkey_patched_put
        status, data = HttpClient().put('http://anyurl.com', data=dict(key=7))
        self.assertEqual(json.loads(expected_data), data)

        requests.put = self.requests_original_put

    def test_delete(self):
        # in case an empty payload is returned
        def monkey_patched_delete(uri, params=None, headers=None, json=None,
                                  timeout=None):
            return MockResponse(204, None)

        requests.delete = monkey_patched_delete
        status, data = HttpClient().delete('http://anyurl.com')
        self.assertIsNone(data)

        # in case a non-empty payload is returned
        expected_data = '{"message": "deleted"}'

        def monkey_patched_delete_returning_payload(uri, params=None, headers=None,
                                                    json=None, timeout=None):
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
        with self.assertRaises(unauthorized_error.UnauthorizedError):
            HttpClient.check_status_code(401, msg)
        with self.assertRaises(not_found_error.NotFoundError):
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
        params = {'a': 1}
        API_key = 'test_API_key'
        api_subscription = 'free'
        result = HttpClient.to_url(API_endpoint, params, API_key, api_subscription)
        expected_1 = 'http://api.openweathermap.org/data/2.5/ep?a=1&APPID=test_API_key'
        expected_2 = 'http://api.openweathermap.org/data/2.5/ep?APPID=test_API_key&a=1'
        self.assertTrue(result == expected_1 or result == expected_2)

    def test_to_url_with_no_API_key(self):
        API_endpoint = 'http://%s.openweathermap.org/data/2.5/ep'
        params = {'a': 1, 'b': 2}
        api_subscription = 'pro'
        result = HttpClient.to_url(API_endpoint, params, None, api_subscription)
        expected_1 = 'http://pro.openweathermap.org/data/2.5/ep?a=1&b=2'
        expected_2 = 'http://pro.openweathermap.org/data/2.5/ep?b=2&a=1'
        self.assertTrue(result == expected_1 or result == expected_2)

    def test_to_url_with_unicode_chars_in_API_key(self):
        API_key = '£°test££'
        API_endpoint = 'http://%s.openweathermap.org/data/2.5/ep'
        params = {'a': 1}
        api_subscription = 'free'
        result = HttpClient.to_url(API_endpoint, params, API_key, api_subscription)
        expected_1 = 'http://api.openweathermap.org/data/2.5/ep?a=1&APPID=%C2%A3%C2%B0test%C2%A3%C2%A3'
        expected_2 = 'http://api.openweathermap.org/data/2.5/ep?APPID=%C2%A3%C2%B0test%C2%A3%C2%A3&a=1'
        self.assertTrue(result == expected_1 or result == expected_2)

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

        # no subdomain escaping
        API_endpoint = 'http://www.openweathermap.org/data/2.5/ep'
        api_subscription = 'free'
        expected = API_endpoint
        result = HttpClient._escape_subdomain(API_endpoint, api_subscription)
        self.assertEqual(expected, result)


    def test_timeouts(self):
        timeout = 0.5
        def monkey_patched_get_timeouting(uri, params=None, headers=None,
                                          timeout=timeout):
            raise requests.exceptions.Timeout()

        requests.get = monkey_patched_get_timeouting
        try:
            status, data = HttpClient(timeout=timeout).get_json('http://anyurl.com')
            self.fail()
        except api_call_error.APICallTimeoutError:
            requests.get = self.requests_original_get
