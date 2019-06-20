#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from pyowm.config import DEFAULT_CONFIG
from pyowm.uvindexapi30 import uv_client, uvindex, uvindex_manager
from tests.unit.uvindexapi30.test_uvindex import UVINDEX_JSON, UVINDEX_LIST_JSON
from pyowm.constants import UVINDEX_API_VERSION


class TestUVIndexManager(unittest.TestCase):

    __test_instance = uvindex_manager.UVIndexManager('fakeapikey', DEFAULT_CONFIG)

    def mock_get_uvi_returning_uvindex_around_coords(self, params_dict):
        return json.loads(UVINDEX_JSON)

    def mock_get_uvi_forecast(self, params_dict):
        return json.loads(UVINDEX_LIST_JSON)

    def mock_get_uvi_history(self, params_dict):
        return json.loads(UVINDEX_LIST_JSON)

    def test_instantiation_with_wrong_params(self):
        with self.assertRaises(AssertionError):
            uvindex_manager.UVIndexManager(None, dict())
        with self.assertRaises(AssertionError):
            uvindex_manager.UVIndexManager('apikey', None)

    def test_get_uvindex_api_version(self):
        result = self.__test_instance.uvindex_api_version()
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, UVINDEX_API_VERSION)

    def test_uvindex_around_coords(self):
        ref_to_original = uv_client.UltraVioletHttpClient.get_uvi
        uv_client.UltraVioletHttpClient.get_uvi = \
            self.mock_get_uvi_returning_uvindex_around_coords
        result = self.__test_instance.uvindex_around_coords(45, 9)
        uv_client.UltraVioletHttpClient.get_uvi = ref_to_original
        self.assertTrue(isinstance(result, uvindex.UVIndex))
        self.assertIsNotNone(result.reference_time())
        self.assertIsNotNone(result.reception_time())
        loc = result.location
        self.assertIsNotNone(loc)
        self.assertIsNotNone(loc.lat)
        self.assertIsNotNone(loc.lon)
        self.assertIsNotNone(result.value)

    def test_uvindex_around_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, uvindex_manager.UVIndexManager.uvindex_around_coords, \
                          self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, uvindex_manager.UVIndexManager.uvindex_around_coords, \
                          self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, uvindex_manager.UVIndexManager.uvindex_around_coords, \
                          self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, uvindex_manager.UVIndexManager.uvindex_around_coords, \
                          self.__test_instance, 200, 2.5)

    def test_uvindex_forecast_around_coords(self):
        ref_to_original = uv_client.UltraVioletHttpClient.get_uvi_forecast
        uv_client.UltraVioletHttpClient.get_uvi_forecast = \
            self.mock_get_uvi_forecast
        result = self.__test_instance.uvindex_forecast_around_coords(45, 9)
        uv_client.UltraVioletHttpClient.get_uvi_forecast = ref_to_original
        self.assertTrue(isinstance(result, list))
        self.assertTrue(all([isinstance(i, uvindex.UVIndex) for i in result]))

    def test_uvindex_forecast_around_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, uvindex_manager.UVIndexManager.uvindex_forecast_around_coords, \
                          self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, uvindex_manager.UVIndexManager.uvindex_forecast_around_coords, \
                          self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, uvindex_manager.UVIndexManager.uvindex_forecast_around_coords, \
                          self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, uvindex_manager.UVIndexManager.uvindex_forecast_around_coords, \
                          self.__test_instance, 200, 2.5)

    def test_uvindex_history_around_coords(self):
        ref_to_original = uv_client.UltraVioletHttpClient.get_uvi_history
        uv_client.UltraVioletHttpClient.get_uvi_history = \
            self.mock_get_uvi_history
        result = self.__test_instance.uvindex_history_around_coords(
            45, 9, 1498049953, end=1498481991)
        uv_client.UltraVioletHttpClient.get_uvi_history = ref_to_original
        self.assertTrue(isinstance(result, list))
        self.assertTrue(all([isinstance(i, uvindex.UVIndex) for i in result]))

    def test_uvindex_history_around_coords_fails_with_wrong_parameters(self):
        # wrong lat/lon
        self.assertRaises(ValueError, uvindex_manager.UVIndexManager.uvindex_history_around_coords, \
                          self.__test_instance, 43.7, -200.0, 1498049953)
        self.assertRaises(ValueError, uvindex_manager.UVIndexManager.uvindex_history_around_coords, \
                          self.__test_instance, 43.7, 200.0, 1498049953)
        self.assertRaises(ValueError, uvindex_manager.UVIndexManager.uvindex_history_around_coords, \
                          self.__test_instance, -200, 2.5, 1498049953)
        self.assertRaises(ValueError, uvindex_manager.UVIndexManager.uvindex_history_around_coords, \
                          self.__test_instance, 200, 2.5, 1498049953)
        # wrong start of time period
        self.assertRaises(TypeError, uvindex_manager.UVIndexManager.uvindex_history_around_coords, \
                          self.__test_instance, 45, 9, dict(a=1, b=2))
        # wrong end of time period
        self.assertRaises(TypeError, uvindex_manager.UVIndexManager.uvindex_history_around_coords, \
                          self.__test_instance, 45, 9, 1498049953,
                          end=dict(a=1, b=2))

    def test_uvindex_history_around_coords_when_no_end_specified(self):
        ref_to_original = uv_client.UltraVioletHttpClient.get_uvi_history

        def mock_get_uvi_history_checking_end_parameter(instance, params_dict):
            self.assertIn('end', params_dict)
            self.assertIsNotNone(params_dict['end'])
            return json.loads(UVINDEX_LIST_JSON)

        uv_client.UltraVioletHttpClient.get_uvi_history = \
            mock_get_uvi_history_checking_end_parameter

        _ = self.__test_instance.uvindex_history_around_coords(
            45, 9, 1498049953)
        uv_client.UltraVioletHttpClient.get_uvi_history = ref_to_original

    def test_repr(self):
        print(self.__test_instance)
