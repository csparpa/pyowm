#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from pyowm.airpollutionapi30 import airpollution_client, airpollution_manager, coindex, so2index, ozone, no2index, airstatus
from pyowm.config import DEFAULT_CONFIG
from pyowm.constants import AIRPOLLUTION_API_VERSION
from pyowm.utils import timestamps
from tests.unit.airpollutionapi30.test_ozone import OZONE_JSON
from tests.unit.airpollutionapi30.test_coindex import COINDEX_JSON
from tests.unit.airpollutionapi30.test_no2index import NO2INDEX_JSON
from tests.unit.airpollutionapi30.test_so2index import SO2INDEX_JSON
from tests.unit.airpollutionapi30.test_airstatus import AIRSTATUS_JSON, AIRSTATUS_MULTIPLE_JSON


class TestAirPollutionManager(unittest.TestCase):

    __test_instance = airpollution_manager.AirPollutionManager('fakeapikey', DEFAULT_CONFIG)

    def mock_get_coi_returning_coindex_around_coords(self, params_dict):
        return json.loads(COINDEX_JSON)

    def mock_get_o3_returning_ozone_around_coords(self, params_dict):
        return json.loads(OZONE_JSON)

    def mock_get_no2_returning_no2index_around_coords(self, params_dict):
        return json.loads(NO2INDEX_JSON)

    def mock_get_air_pollution(self, params_dict):
        return json.loads(AIRSTATUS_JSON)

    def mock_get_forecast_air_pollution(self, params_dict):
        return json.loads(AIRSTATUS_MULTIPLE_JSON)

    def mock_get_historical_air_pollution(self, params_dict):
        return json.loads(AIRSTATUS_MULTIPLE_JSON)

    def mock_get_so2_returning_so2index_around_coords(self, params_dict):
        return json.loads(SO2INDEX_JSON)

    def test_instantiation_with_wrong_params(self):
        self.assertRaises(AssertionError, airpollution_manager.AirPollutionManager, None, dict())
        self.assertRaises(AssertionError, airpollution_manager.AirPollutionManager, 'apikey', None)

    def test_get_uvindex_api_version(self):
        result = self.__test_instance.airpollution_api_version()
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, AIRPOLLUTION_API_VERSION)

    def test_coindex_around_coords(self):
        ref_to_original = airpollution_client.AirPollutionHttpClient.get_coi
        airpollution_client.AirPollutionHttpClient.get_coi = \
            self.mock_get_coi_returning_coindex_around_coords
        result = self.__test_instance.coindex_around_coords(45, 9, interval='day')
        airpollution_client.AirPollutionHttpClient.coi = ref_to_original
        self.assertTrue(isinstance(result, coindex.COIndex))
        self.assertIsNotNone(result.reference_time)
        self.assertIsNotNone(result.reception_time())
        loc = result.location
        self.assertIsNotNone(loc)
        self.assertIsNotNone(loc.lat)
        self.assertIsNotNone(loc.lon)
        self.assertIsNotNone(result.co_samples)

        ref_to_original = airpollution_client.AirPollutionHttpClient.get_coi
        airpollution_client.AirPollutionHttpClient.get_coi = \
            self.mock_get_coi_returning_coindex_around_coords
        result = self.__test_instance.coindex_around_coords(45, 9, interval=None)
        airpollution_client.AirPollutionHttpClient.coi = ref_to_original
        self.assertTrue(isinstance(result, coindex.COIndex))
        self.assertEqual('year', result.interval)

    def test_coindex_around_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.coindex_around_coords, \
                          self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.coindex_around_coords, \
                          self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.coindex_around_coords, \
                          self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.coindex_around_coords, \
                          self.__test_instance, 200, 2.5)

    def test_ozone_around_coords(self):
        ref_to_original = airpollution_client.AirPollutionHttpClient.get_o3
        airpollution_client.AirPollutionHttpClient.get_o3 = \
            self.mock_get_o3_returning_ozone_around_coords
        result = self.__test_instance.ozone_around_coords(45, 9, interval='day')
        airpollution_client.AirPollutionHttpClient.o3 = ref_to_original
        self.assertTrue(isinstance(result, ozone.Ozone))
        self.assertIsNotNone(result.reference_time)
        self.assertIsNotNone(result.reception_time())
        loc = result.location
        self.assertIsNotNone(loc)
        self.assertIsNotNone(loc.lat)
        self.assertIsNotNone(loc.lon)
        self.assertIsNotNone(result.du_value)

        ref_to_original = airpollution_client.AirPollutionHttpClient.get_o3
        airpollution_client.AirPollutionHttpClient.get_o3 = \
            self.mock_get_o3_returning_ozone_around_coords
        result = self.__test_instance.ozone_around_coords(45, 9, interval=None)
        airpollution_client.AirPollutionHttpClient.o3 = ref_to_original
        self.assertTrue(isinstance(result, ozone.Ozone))
        self.assertEqual('year', result.interval)

    def test_ozone_around_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.ozone_around_coords, \
                          self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.ozone_around_coords, \
                          self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.ozone_around_coords, \
                          self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.ozone_around_coords, \
                          self.__test_instance, 200, 2.5)

    def test_no2index_around_coords(self):
        ref_to_original = airpollution_client.AirPollutionHttpClient.get_no2
        airpollution_client.AirPollutionHttpClient.get_no2 = \
            self.mock_get_no2_returning_no2index_around_coords
        result = self.__test_instance.no2index_around_coords(45, 9, interval='day')
        airpollution_client.AirPollutionHttpClient.get_no2 = ref_to_original
        self.assertTrue(isinstance(result, no2index.NO2Index))
        self.assertIsNotNone(result.reference_time)
        self.assertIsNotNone(result.reception_time())
        loc = result.location
        self.assertIsNotNone(loc)
        self.assertIsNotNone(loc.lat)
        self.assertIsNotNone(loc.lon)
        self.assertIsNotNone(result.no2_samples)

        ref_to_original = airpollution_client.AirPollutionHttpClient.get_no2
        airpollution_client.AirPollutionHttpClient.get_no2 = \
            self.mock_get_no2_returning_no2index_around_coords
        result = self.__test_instance.no2index_around_coords(45, 9, interval=None)
        airpollution_client.AirPollutionHttpClient.get_no2 = ref_to_original
        self.assertTrue(isinstance(result, no2index.NO2Index))
        self.assertEqual('year', result.interval)

    def test_no2index_around_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.no2index_around_coords, \
                          self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.no2index_around_coords, \
                          self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.no2index_around_coords, \
                          self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.no2index_around_coords, \
                          self.__test_instance, 200, 2.5)

    def test_so2index_around_coords(self):
        ref_to_original = airpollution_client.AirPollutionHttpClient.get_so2
        airpollution_client.AirPollutionHttpClient.get_so2 = \
            self.mock_get_so2_returning_so2index_around_coords
        result = self.__test_instance.so2index_around_coords(45, 9, interval='day')
        airpollution_client.AirPollutionHttpClient.get_so2 = ref_to_original
        self.assertTrue(isinstance(result, so2index.SO2Index))
        self.assertIsNotNone(result.reference_time())
        self.assertIsNotNone(result.reception_time())
        loc = result.location
        self.assertIsNotNone(loc)
        self.assertIsNotNone(loc.lat)
        self.assertIsNotNone(loc.lon)
        self.assertIsNotNone(result.so2_samples)
        self.assertIsNotNone(result.interval)

        ref_to_original = airpollution_client.AirPollutionHttpClient.get_so2
        airpollution_client.AirPollutionHttpClient.get_so2 = \
            self.mock_get_so2_returning_so2index_around_coords
        result = self.__test_instance.so2index_around_coords(45, 9, interval=None)
        airpollution_client.AirPollutionHttpClient.get_so2 = ref_to_original
        self.assertTrue(isinstance(result, so2index.SO2Index))
        self.assertEqual('year', result.interval)

    def test_so2index_around_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.so2index_around_coords, \
                          self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.so2index_around_coords, \
                          self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.so2index_around_coords, \
                          self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.so2index_around_coords, \
                          self.__test_instance, 200, 2.5)

    def test_air_quality_at_coords(self):
        ref_to_original = airpollution_client.AirPollutionHttpClient.get_air_pollution
        airpollution_client.AirPollutionHttpClient.get_air_pollution = \
            self.mock_get_air_pollution
        result = self.__test_instance.air_quality_at_coords(45, 9)
        airpollution_client.AirPollutionHttpClient.get_air_pollution = ref_to_original
        self.assertTrue(isinstance(result, airstatus.AirStatus))
        self.assertIsNotNone(result.reference_time)
        self.assertIsNotNone(result.reception_time())
        loc = result.location
        self.assertIsNotNone(loc)
        self.assertIsNotNone(loc.lat)
        self.assertIsNotNone(loc.lon)
        self.assertIsNotNone(result.air_quality_data)

    def test_air_quality_at_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_at_coords, \
                          self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_at_coords, \
                          self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_at_coords, \
                          self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_at_coords, \
                          self.__test_instance, 200, 2.5)

    def test_air_quality_forecast_at_coords(self):
        ref_to_original = airpollution_client.AirPollutionHttpClient.get_forecast_air_pollution
        airpollution_client.AirPollutionHttpClient.get_forecast_air_pollution = \
            self.mock_get_forecast_air_pollution
        result = self.__test_instance.air_quality_forecast_at_coords(45, 9)
        airpollution_client.AirPollutionHttpClient.get_forecast_air_pollution = ref_to_original
        self.assertTrue(isinstance(result, list))
        for item in result:
            self.assertIsInstance(item, airstatus.AirStatus)
            self.assertIsNotNone(item.reference_time)
            self.assertIsNotNone(item.reception_time())
            loc = item.location
            self.assertIsNotNone(loc)
            self.assertIsNotNone(loc.lat)
            self.assertIsNotNone(loc.lon)
            self.assertIsNotNone(item.air_quality_data)

    def test_air_quality_forecast_at_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_forecast_at_coords, \
                          self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_forecast_at_coords, \
                          self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_forecast_at_coords, \
                          self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_forecast_at_coords, \
                          self.__test_instance, 200, 2.5)

    def test_air_quality_history_at_coords(self):
        ref_to_original = airpollution_client.AirPollutionHttpClient.get_historical_air_pollution
        airpollution_client.AirPollutionHttpClient.get_historical_air_pollution = \
            self.mock_get_historical_air_pollution
        result = self.__test_instance.air_quality_history_at_coords(45, 9, 12345678)
        airpollution_client.AirPollutionHttpClient.get_historical_air_pollution = ref_to_original
        self.assertTrue(isinstance(result, list))
        for item in result:
            self.assertIsInstance(item, airstatus.AirStatus)
            self.assertIsNotNone(item.reference_time)
            self.assertIsNotNone(item.reception_time())
            loc = item.location
            self.assertIsNotNone(loc)
            self.assertIsNotNone(loc.lat)
            self.assertIsNotNone(loc.lon)
            self.assertIsNotNone(item.air_quality_data)

    def test_air_quality_history_at_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_history_at_coords, \
                          self.__test_instance, 43.7, -200.0, 12345678, 12349999)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_history_at_coords, \
                          self.__test_instance, 43.7, 200.0, 12345678, 12349999)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_history_at_coords, \
                          self.__test_instance, -200, 2.5, 12345678, 12349999)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_history_at_coords, \
                          self.__test_instance, 200, 2.5, 12345678, 12349999)
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_history_at_coords, \
                          self.__test_instance, 200, 2.5, 'test')
        self.assertRaises(ValueError, airpollution_manager.AirPollutionManager.air_quality_history_at_coords, \
                          self.__test_instance, 200, 2.5, 'test', 'test2')

    def test_air_quality_history_at_coords_clips_end_param_to_current_timestamp(self):
        now = timestamps.now(timeformat='unix')
        end = now + 99999999999

        def assert_clipped(obj, params_dict):
            self.assertEqual(params_dict['end'], now)

        airpollution_client.AirPollutionHttpClient.get_historical_air_pollution = assert_clipped
        _ = self.__test_instance.air_quality_history_at_coords(45, 9, 12345678, end=end)

    def test_repr(self):
        print(self.__test_instance)
