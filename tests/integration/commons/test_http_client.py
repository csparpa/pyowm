# -*- coding: utf-8 -*-

import unittest
from pyowm.exceptions import parse_response_error
from pyowm.commons.http_client import HttpClient


class TestHTTPClient(unittest.TestCase):

    instance = HttpClient()

    def test_get_json_against_httpbin_ok(self):
        # https://httpbin.org/ip
        status, data = self.instance.get_json('http://httpbin.org/ip')
        self.assertEqual(200, status)
        self.assertIsInstance(data, dict)

    def test_get_json_against_httpbin_status_code_ko(self):
        # https://httpbin.org/status/400
        expected_status = 400
        status, data = self.instance.get_json('https://httpbin.org/status/' +
                                              str(expected_status))
        self.assertEqual(expected_status, status)
        self.assertIsInstance(data, dict)

    def test_get_json_against_httpbin_parse_error(self):
        # https://httpbin.org/xml
        try:
            status, data = self.instance.get_json('http://httpbin.org/xml')
            self.fail()
        except parse_response_error.ParseResponseError:
            pass

    def test_put_against_httpbin(self):
        # https://httpbin.org/put
        formdata = dict(a=1, b=2, c=3)
        status, data = self.instance.put('http://httpbin.org/put', data=formdata)
        self.assertEqual(200, status)
        self.assertIsInstance(data, dict)