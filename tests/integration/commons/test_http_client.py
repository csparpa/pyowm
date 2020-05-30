#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import pyowm.commons.exceptions
from pyowm.commons.http_client import HttpClient
from pyowm.config import DEFAULT_CONFIG


class TestHTTPClient(unittest.TestCase):

    instance = HttpClient('fakeapikey', DEFAULT_CONFIG, 'httpbin.org', admits_subdomains=False)

    def test_get_json_against_httpbin_ok(self):
        # http://httpbin.org/ip
        status, data = self.instance.get_json('/ip')
        self.assertEqual(200, status)
        self.assertIsInstance(data, dict)

    def test_get_json_against_httpbin_status_code_ko(self):
        # http://httpbin.org/status/400
        expected_status = 400

        self.assertRaises(pyowm.commons.exceptions.APIRequestError, HttpClient.get_json,
                          self.instance, 'status/{}'.format(str(expected_status)))

    def test_get_json_against_httpbin_parse_error(self):
        # http://httpbin.org/xml
        try:
            status, data = self.instance.get_json('xml')
            self.fail()
        except pyowm.commons.exceptions.ParseAPIResponseError:
            pass

    def test_put_against_httpbin(self):
        # http://httpbin.org/put
        formdata = dict(a=1, b=2, c=3)
        status, data = self.instance.put('put', data=formdata)
        self.assertEqual(200, status)
        self.assertIsInstance(data, dict)
        self.assertEqual(formdata, data['json'])

    def test_delete_against_httpbin(self):
        # http://httpbin.org/delete
        formdata = dict(a=1, b=2, c=3)
        status, data = self.instance.delete('delete', data=formdata)
        self.assertEqual(200, status)
        self.assertIsInstance(data, dict)
        self.assertEqual(formdata, data['json'])

    def test_ssl_certs_verification_failure(self):
        # https://wrong.host.badssl.com does not have a valid SSL cert
        config = DEFAULT_CONFIG.copy()
        config['connection']['use_ssl'] = True
        config['connection']['verify_ssl_certs'] = True
        instance = HttpClient('fakeapikey', config, 'wrong.host.badssl.com', admits_subdomains=False)
        self.assertRaises(pyowm.commons.exceptions.InvalidSSLCertificateError, HttpClient.get_json, instance, '')

    def test_get_png(self):
        # http://httpbin.org/image/png
        status, data = self.instance.get_png('image/png')
        self.assertIsNotNone(data)
        self.assertIsInstance(data, bytes)

    def test_get_geotiff(self):
        # https://download.osgeo.org/geotiff/samples/made_up/bogota.tif
        config = DEFAULT_CONFIG.copy()
        config['connection']['use_ssl'] = True
        instance = HttpClient('fakeapikey', config, 'download.osgeo.org', admits_subdomains=False)
        status, data = instance.get_geotiff('geotiff/samples/made_up/bogota.tif')
        self.assertIsNotNone(data)
        self.assertIsInstance(data, bytes)

    def test_get_png(self):
        # http://httpbin.org/image/png
        status, data = self.instance.get_png('http://httpbin.org/image/png')
        self.assertIsNotNone(data)
        self.assertIsInstance(data, bytes)

    def test_get_geotiff(self):
        # https://download.osgeo.org/geotiff/samples/made_up/bogota.tif
        status, data = self.instance.get_geotiff('https://download.osgeo.org/geotiff/samples/made_up/bogota.tif')
        self.assertIsNotNone(data)
        self.assertIsInstance(data, bytes)


if __name__ == "__main__":
    unittest.main()

