# -*- coding: utf-8 -*-

import unittest
from pyowm.exceptions import api_call_error, unauthorized_error, not_found_error
from pyowm.commons.http_client import HttpClient


class TestHTTPClient(unittest.TestCase):

    def test_check_status_code(self):
        msg = 'Generic error'
        HttpClient.check_status_code(200, msg)
        with self.assertRaises(unauthorized_error.UnauthorizedError):
            HttpClient.check_status_code(401, msg)
        with self.assertRaises(not_found_error.NotFoundError):
            HttpClient.check_status_code(404, msg)
        with self.assertRaises(api_call_error.BadGatewayError):
            HttpClient.check_status_code(502, msg)
        with self.assertRaises(api_call_error.APICallError):
            HttpClient.check_status_code(555, msg)