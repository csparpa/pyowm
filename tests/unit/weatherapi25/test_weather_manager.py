#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from pyowm.weatherapi25.weather_manager import WeatherManager
from pyowm.commons.http_client import HttpClient
from pyowm.constants import WEATHER_API_VERSION
from pyowm.config import DEFAULT_CONFIG
from pyowm.weatherapi25.historian import Historian
from pyowm.weatherapi25.forecast import Forecast
from pyowm.weatherapi25.forecaster import Forecaster
from pyowm.weatherapi25.location import Location
from pyowm.weatherapi25.observation import Observation
from pyowm.weatherapi25.one_call import OneCall
from pyowm.weatherapi25.stationhistory import StationHistory
from pyowm.weatherapi25.weather import Weather
from tests.unit.weatherapi25.json_test_responses import (
    OBSERVATION_JSON, SEARCH_RESULTS_JSON, THREE_HOURS_FORECAST_JSON, DAILY_FORECAST_JSON,
    THREE_HOURS_FORECAST_AT_COORDS_JSON, DAILY_FORECAST_AT_COORDS_JSON,
    THREE_HOURS_FORECAST_AT_ID_JSON, DAILY_FORECAST_AT_ID_JSON,
    CITY_WEATHER_HISTORY_JSON, STATION_TICK_WEATHER_HISTORY_JSON,
    STATION_WEATHER_HISTORY_JSON, THREE_HOURS_FORECAST_NOT_FOUND_JSON,
    DAILY_FORECAST_NOT_FOUND_JSON, STATION_HISTORY_NO_ITEMS_JSON,
    WEATHER_AT_PLACES_IN_BBOX_JSON, ONE_CALL_JSON, ONE_CALL_HISTORY_JSON)


class TestWeatherManager(unittest.TestCase):

    __test_instance = WeatherManager('fakeapikey', DEFAULT_CONFIG)

    # --- MOCKS ---

    def mock_api_call_returning_single_obs(self, uri, params=None, headers=None):
        return 200, json.loads(OBSERVATION_JSON)

    def mock_api_call_ping(self, uri, params=None, headers=None):
        return 200, json.loads(OBSERVATION_JSON)

    def mock_api_call_returning_multiple_obs(self, uri, params=None, headers=None):
        return 200, json.loads(SEARCH_RESULTS_JSON)

    def mock_api_call_returning_3h_forecast(self, uri, params=None, headers=None):
        return 200, json.loads(THREE_HOURS_FORECAST_JSON)

    def mock_api_call_returning_empty_3h_forecast(self, uri, params=None, headers=None):
        return 200, json.loads(THREE_HOURS_FORECAST_NOT_FOUND_JSON)

    def mock_api_call_returning_empty_daily_forecast(self, uri, params=None, headers=None):
        return 200, json.loads(DAILY_FORECAST_NOT_FOUND_JSON)

    def mock_api_call_returning_3h_forecast_at_coords(self,uri, params=None, headers=None):
        return 200, json.loads(THREE_HOURS_FORECAST_AT_COORDS_JSON)

    def mock_api_call_returning_3h_forecast_at_id(self, uri, params=None, headers=None):
        return 200, json.loads(THREE_HOURS_FORECAST_AT_ID_JSON)

    def mock_api_call_returning_daily_forecast(self, uri, params=None, headers=None):
        return 200, json.loads(DAILY_FORECAST_JSON)

    def mock_api_call_returning_daily_forecast_at_coords(self, uri, params=None, headers=None):
        return 200, json.loads(DAILY_FORECAST_AT_COORDS_JSON)

    def mock_api_call_returning_daily_forecast_at_id(self, uri, params=None, headers=None):
        return 200, json.loads(DAILY_FORECAST_AT_ID_JSON)

    def mock_api_call_returning_city_weather_history(self, uri, params=None, headers=None):
        return 200, json.loads(CITY_WEATHER_HISTORY_JSON)

    def mock_api_call_returning_station_tick_weather_history(self, uri, params=None, headers=None):
        return 200, json.loads(STATION_TICK_WEATHER_HISTORY_JSON)

    def mock_api_call_returning_station_hour_weather_history(self, uri, params=None, headers=None):
        return 200, json.loads(STATION_WEATHER_HISTORY_JSON)

    def mock_call_api_returning_station_day_weather_history(self, uri, params=None, headers=None):
        return 200, json.loads(STATION_WEATHER_HISTORY_JSON)

    def mock_call_api_returning_station_history_with_no_items(self, uri, params=None, headers=None):
        return 200, json.loads(STATION_HISTORY_NO_ITEMS_JSON)

    def mock_api_call_returning_weather_at_places_in_bbox(self, uri, params=None, headers=None):
        return 200, json.loads(WEATHER_AT_PLACES_IN_BBOX_JSON)

    def mock_api_call_returning_weather_history_at_coords(self, uri, params=None, headers=None):
        return 200, json.loads(CITY_WEATHER_HISTORY_JSON)

    def mock_api_call_returning_onecall_data(self, uri, params=None, headers=None):
        return 200, json.loads(ONE_CALL_JSON)

    def mock_api_call_returning_onecall_history_data(self, uri, params=None, headers=None):
        return 200, json.loads(ONE_CALL_HISTORY_JSON)

    def mock__retrieve_station_history(self, station_ID, limit, interval):
        return None

    # -- TESTS --

    def test_get_weather_api_version(self):
        result = self.__test_instance.weather_api_version()
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, WEATHER_API_VERSION)

    def test_repr(self):
        print(self.__test_instance)

    def test_instantiation_with_wrong_params(self):
        with self.assertRaises(AssertionError):
            WeatherManager(None, dict())
        with self.assertRaises(AssertionError):
            WeatherManager('apikey', None)

    def test_weather_at_place(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_single_obs
        result = self.__test_instance.weather_at_place("London,uk")
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Observation))
        self.assertTrue(result.reception_time() is not None)
        loc = result.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = result.weather
        self.assertTrue(weat is not None)

    def test_weather_at_place_fails_with_wrong_parameters(self):
        self.assertRaises(AssertionError,  WeatherManager.weather_at_place, self.__test_instance, 3)

    def test_weather_at_coords(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_single_obs
        result = self.__test_instance.weather_at_coords(57.0, -2.15)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Observation))
        self.assertTrue(result.reception_time() is not None)
        loc = result.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = result.weather
        self.assertTrue(weat is not None)

    def test_weather_at_zip_code(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_single_obs
        result = self.__test_instance.weather_at_zip_code("2000", "AU")
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Observation))
        self.assertTrue(result.reception_time() is not None)
        loc = result.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = result.weather
        self.assertTrue(weat is not None)

    def test_weather_at_coords_fails_when_coordinates_out_of_bounds(self):
        """
        Test failure when providing: lon < -180, lon > 180, lat < -90, lat > 90
        """
        self.assertRaises(ValueError, WeatherManager.weather_at_coords,  self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, WeatherManager.weather_at_coords, self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, WeatherManager.weather_at_coords, self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, WeatherManager.weather_at_coords, self.__test_instance, 200, 2.5)

    def test_weather_at_id(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_single_obs
        result = self.__test_instance.weather_at_id(5128581)  # New York city, US
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Observation))
        self.assertTrue(result.reception_time() is not None)
        loc = result.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = result.weather
        self.assertTrue(weat is not None)

    def test_weather_at_id_fails_when_id_negative(self):
        self.assertRaises(ValueError, WeatherManager.weather_at_id,  self.__test_instance, -156667)

    def test_weather_at_ids(self):
        ref_to_original_call_API = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_multiple_obs
        result = self.__test_instance.weather_at_ids([5128581, 15647, 78654])
        HttpClient.get_json = ref_to_original_call_API
        self.assertTrue(isinstance(result, list))
        for obs in result:
            self.assertTrue(obs is not None)
            self.assertTrue(isinstance(obs, Observation))
            weat = obs.weather
            self.assertTrue(weat is not None)

    def test_weather_at_ids_fails_when_wrong_parameters(self):
        self.assertRaises(AssertionError, WeatherManager.weather_at_ids, self.__test_instance, "test")
        self.assertRaises(ValueError, WeatherManager.weather_at_ids, self.__test_instance, [-1, 2, 3])

    def test_weather_at_places_without_limits(self):
        original_func = HttpClient.get_json
        HttpClient.get_json= \
            self.mock_api_call_returning_multiple_obs
        result = \
            self.__test_instance.weather_at_places("London", "accurate")
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, list))
        self.assertEqual(2, len(result))
        for item in result:
            self.assertTrue(item is not None)
            self.assertTrue(item.reception_time())
            loc = item.location
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.weather
            self.assertTrue(weat is not None)

    def test_weather_at_places_with_limits(self):
        original_func = HttpClient.get_json
        HttpClient.get_json= \
            self.mock_api_call_returning_multiple_obs
        result = \
            self.__test_instance.weather_at_places("London", "accurate", limit=2)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, list))
        self.assertEqual(2, len(result))
        for item in result:
            self.assertTrue(item is not None)
            self.assertTrue(item.reception_time())
            loc = item.location
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.weather
            self.assertTrue(weat is not None)

    def test_weather_at_places_fails_with_wrong_params(self):
        self.assertRaises(ValueError, WeatherManager.weather_at_places, self.__test_instance, "London", "x")
        self.assertRaises(ValueError, WeatherManager.weather_at_places, self.__test_instance, "London", "accurate", -5)

    def test_weather_around_coords_without_limits(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_multiple_obs
        result = self.__test_instance.weather_around_coords(57.0, -2.15)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, list))
        for item in result:
            self.assertTrue(item is not None)
            self.assertTrue(item.reception_time() is not None)
            loc = item.location
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.weather
            self.assertTrue(weat is not None)

    def test_weather_around_coords_with_limits(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_multiple_obs
        result = self.__test_instance.weather_around_coords(57.0, -2.15, limit=2)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, list))
        for item in result:
            self.assertTrue(item is not None)
            self.assertTrue(item.reception_time() is not None)
            loc = item.location
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.weather
            self.assertTrue(weat is not None)

    def test_weather_around_coords_fails_when_coordinates_out_of_bounds(self):
        """
        Test failure when providing: lon < -180, lon > 180, lat < -90, lat > 90
        """
        self.assertRaises(ValueError, WeatherManager.weather_around_coords, self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, WeatherManager.weather_around_coords, self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, WeatherManager.weather_around_coords, self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, WeatherManager.weather_around_coords, self.__test_instance, 200, 2.5)

    def test_weather_around_coords_fails_with_wrong_params(self):
        self.assertRaises(ValueError, WeatherManager.weather_around_coords, self.__test_instance, 43.7, 20.0, -3)

    def test_forecast_at_place_fails_with_wrong_params(self):
        self.assertRaises(AssertionError, WeatherManager.forecast_at_place,
                          self.__test_instance, None, "daily", 3)
        self.assertRaises(AssertionError, WeatherManager.forecast_at_place,
                          self.__test_instance, "London,uk", None, -3)
        self.assertRaises(ValueError, WeatherManager.forecast_at_place,
                          self.__test_instance, "London,uk", "wrong", 3)
        self.assertRaises(ValueError, WeatherManager.forecast_at_place,
                          self.__test_instance, "London,uk", "daily", -3)

    def test_forecast_at_place_on_3h(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_3h_forecast
        result = self.__test_instance.forecast_at_place("London,uk", "3h")
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Forecaster))
        forecast = result.forecast
        self.assertTrue(isinstance(forecast, Forecast))
        self.assertTrue(forecast.interval is not None)
        self.assertTrue(forecast.reception_time() is not None)
        self.assertTrue(isinstance(forecast.location, Location))
        self.assertEqual(1, len(forecast))
        for weather in forecast:
            self.assertTrue(isinstance(weather, Weather))

    def test_forecast_at_place_on_3h_when_forecast_not_found(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_empty_3h_forecast
        result = self.__test_instance.forecast_at_place("London,uk", "3h")
        HttpClient.get_json = original_func
        self.assertIsNone(result)

    def test_forecast_at_coords_failing(self):
        self.assertRaises(ValueError, WeatherManager.forecast_at_coords,
                          self.__test_instance, -100.0, 0.0, '3h', None)
        self.assertRaises(ValueError, WeatherManager.forecast_at_coords,
                          self.__test_instance, 100.0, 0.0, '3h', None)
        self.assertRaises(ValueError, WeatherManager.forecast_at_coords,
                          self.__test_instance, 0.0, -200.0, '3h', None)
        self.assertRaises(ValueError, WeatherManager.forecast_at_coords,
                          self.__test_instance, 0.0, 200.0, '3h', None)
        self.assertRaises(AssertionError, WeatherManager.forecast_at_coords,
                          self.__test_instance, 0.0, 60.0, None, None)
        self.assertRaises(ValueError, WeatherManager.forecast_at_coords,
                          self.__test_instance, 0.0, 60.0, 'unsupported', None)
        self.assertRaises(ValueError, WeatherManager.forecast_at_coords,
                          self.__test_instance, 0.0, 60.0, '3h', -4)

    def test_forecast_at_coords_on_3h(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_3h_forecast_at_coords
        result = \
            self.__test_instance\
                .forecast_at_coords(51.50853, -0.12574, "3h")
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Forecaster))
        forecast = result.forecast
        self.assertTrue(isinstance(forecast, Forecast))
        self.assertTrue(forecast.interval is not None)
        self.assertTrue(forecast.reception_time() is not None)
        self.assertTrue(isinstance(forecast.location, Location))
        self.assertEqual(1, len(forecast))
        for weather in forecast:
            self.assertTrue(isinstance(weather, Weather))

    def test_forecast_at_coords_on_3h_when_forecast_not_found(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_empty_3h_forecast
        result = self.__test_instance.forecast_at_coords(51.50853, -0.12574, '3h')
        HttpClient.get_json = original_func
        self.assertIsNone(result)

    def test_forecast_at_id_on_3h(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_3h_forecast_at_id
        result = self.__test_instance.forecast_at_id(2643743, '3h')
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Forecaster))
        f = result.forecast
        self.assertTrue(isinstance(f, Forecast))
        self.assertTrue(f.interval is not None)
        self.assertTrue(f.reception_time() is not None)
        self.assertTrue(isinstance(f.location, Location))
        self.assertEqual(1, len(f))
        for weather in f:
            self.assertTrue(isinstance(weather, Weather))

    def test_forecast_at_id_on_3h_when_forecast_not_found(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_empty_3h_forecast
        result = self.__test_instance.forecast_at_id(2643743, '3h')
        HttpClient.get_json = original_func
        self.assertIsNone(result)

    def test_forecast_at_id_fails_with_wrong_params(self):
        self.assertRaises(ValueError, WeatherManager.forecast_at_id, self.__test_instance, -1234, '3h', None)
        self.assertRaises(AssertionError, WeatherManager.forecast_at_id, self.__test_instance, 123, None, None)
        self.assertRaises(ValueError, WeatherManager.forecast_at_id, self.__test_instance, 123, 'unsupported', None)
        self.assertRaises(ValueError, WeatherManager.forecast_at_id, self.__test_instance, 123, '3h', -8)

    def test_forecast_at_place_daily(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_daily_forecast
        result = self.__test_instance.forecast_at_place("London,uk", "daily", 2)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Forecaster))
        forecast = result.forecast
        self.assertTrue(isinstance(forecast, Forecast))
        self.assertTrue(forecast.interval is not None)
        self.assertTrue(forecast.reception_time() is not None)
        self.assertTrue(isinstance(forecast.location, Location))
        self.assertEqual(1, len(forecast))
        for weather in forecast:
            self.assertTrue(isinstance(weather, Weather))

    def test_forecast_at_place_daily_when_forecast_not_found(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_empty_daily_forecast
        result = self.__test_instance.forecast_at_place('London,uk', "daily")
        HttpClient.get_json = original_func
        self.assertIsNone(result)

    def test_forecast_at_coords_daily(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_daily_forecast_at_coords
        result = \
            self.__test_instance.forecast_at_coords(51.50853, -0.12574, 'daily', 2)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Forecaster))
        forecast = result.forecast
        self.assertTrue(isinstance(forecast, Forecast))
        self.assertTrue(forecast.interval is not None)
        self.assertTrue(forecast.reception_time() is not None)
        self.assertTrue(isinstance(forecast.location, Location))
        self.assertEqual(1, len(forecast))
        for weather in forecast:
            self.assertTrue(isinstance(weather, Weather))

    def test_forecast_at_coords_daily_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, WeatherManager.forecast_at_coords,
                          self.__test_instance, -100.0, 0.0, 'daily')
        self.assertRaises(ValueError, WeatherManager.forecast_at_coords,
                          self.__test_instance, 100.0, 0.0, 'daily')
        self.assertRaises(ValueError, WeatherManager.forecast_at_coords,
                          self.__test_instance, 0.0, -200.0, 'daily')
        self.assertRaises(ValueError, WeatherManager.forecast_at_coords,
                          self.__test_instance, 0.0, 200.0, 'daily')
        self.assertRaises(AssertionError, WeatherManager.forecast_at_coords,
                          self.__test_instance, 0.0, 60.0, None, 2)
        self.assertRaises(ValueError, WeatherManager.forecast_at_coords,
                          self.__test_instance, 0.0, 60.0, 'unsupported')
        self.assertRaises(ValueError, WeatherManager.forecast_at_coords,
                          self.__test_instance, 0.0, 60.0, 'daily', -5)

    def test_forecast_at_coords_dailty_when_forecast_not_found(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_empty_daily_forecast
        result = self.__test_instance.forecast_at_coords(51.50853, -0.12574, 'daily')
        HttpClient.get_json = original_func
        self.assertIsNone(result)

    def test_forecast_at_id_dailty(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_daily_forecast_at_id
        result = \
            self.__test_instance.forecast_at_id(2643743, 'daily', 2)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Forecaster))
        forecast = result.forecast
        self.assertTrue(isinstance(forecast, Forecast))
        self.assertTrue(forecast.interval is not None)
        self.assertTrue(forecast.reception_time() is not None)
        self.assertTrue(isinstance(forecast.location, Location))
        self.assertEqual(1, len(forecast))
        for weather in forecast:
            self.assertTrue(isinstance(weather, Weather))

    def test_forecast_at_id_daily_when_forecast_not_found(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_empty_daily_forecast
        result = self.__test_instance.forecast_at_id(123456, 'daily')
        HttpClient.get_json = original_func
        self.assertIsNone(result)

    def test_weather_at_places_in_bbox_fails_with_wrong_params(self):
        self.assertRaises(AssertionError, WeatherManager.weather_at_places_in_bbox,
                          self.__test_instance, 12, 32, 15, 37, 'zoom')
        self.assertRaises(ValueError, WeatherManager.weather_at_places_in_bbox,
                          self.__test_instance, 12, 32, 15, 37, -30)
        self.assertRaises(AssertionError, WeatherManager.weather_at_places_in_bbox,
                          self.__test_instance, 12, 32, 15, 37, 10, 'cluster')

    def test_weather_at_places_in_bbox(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_weather_at_places_in_bbox
        results = self.__test_instance\
                .weather_at_places_in_bbox(12,32,15,37,10)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(results, list))
        for result in results:
            self.assertTrue(isinstance(result, Observation))
            self.assertTrue(isinstance(result.weather, Weather))
            self.assertTrue(isinstance(result.location, Location))
            self.assertTrue(result.reception_time() is not None)

    def test_station_tick_history_without_limits(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_station_tick_weather_history
        result = self.__test_instance.station_tick_history(1234)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Historian))
        station_history = result.station_history
        self.assertTrue(isinstance(station_history, StationHistory))
        self.assertTrue(isinstance(station_history.measurements, dict))

    def test_station_tick_history_with_limits(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_station_tick_weather_history
        result = self.__test_instance.station_tick_history(1234, limit=4)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Historian))
        station_history = result.station_history
        self.assertTrue(isinstance(station_history, StationHistory))
        self.assertTrue(isinstance(station_history.measurements, dict))

    def test_station_tick_history_fails_with_wrong_params(self):
        self.assertRaises(ValueError, WeatherManager.station_tick_history,
                          self.__test_instance, 1234, -3)

    def test_station_tick_history_when_forecast_not_found(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_call_api_returning_station_history_with_no_items
        result = self.__test_instance.station_tick_history(1234, limit=4)
        HttpClient.get_json = original_func
        self.assertIsNone(result)

    def test_station_hour_history_without_limits(self):
        original_call = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_station_hour_weather_history
        result = self.__test_instance.station_hour_history(1234)
        HttpClient.get_json = original_call
        self.assertTrue(isinstance(result, Historian))
        station_history = result.station_history
        self.assertTrue(isinstance(station_history, StationHistory))
        self.assertTrue(isinstance(station_history.measurements, dict))

    def test_station_hour_history_with_limits(self):
        original_call = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_station_hour_weather_history
        result = self.__test_instance.station_hour_history(1234, limit=4)
        HttpClient.get_json = original_call
        self.assertTrue(isinstance(result, Historian))
        station_history = result.station_history
        self.assertTrue(isinstance(station_history, StationHistory))
        self.assertTrue(isinstance(station_history.measurements, dict))

    def test_station_hour_history_fails_with_wrong_params(self):
        self.assertRaises(ValueError, WeatherManager.station_hour_history,
                          self.__test_instance, 1234, -3)

    def test_station_hour_history_when_forecast_not_found(self):
        original_call = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_call_api_returning_station_history_with_no_items
        result = self.__test_instance.station_hour_history(1234, limit=4)
        HttpClient.get_json = original_call
        self.assertIsNone(result)

    def test_station_day_history_with_limits(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_call_api_returning_station_day_weather_history
        result = self.__test_instance.station_day_history(1234, limit=4)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Historian))
        station_history = result.station_history
        self.assertTrue(isinstance(station_history, StationHistory))
        self.assertTrue(isinstance(station_history.measurements, dict))

    def test_station_day_history_without_limits(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_call_api_returning_station_day_weather_history
        result = self.__test_instance.station_day_history(1234)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, Historian))
        station_history = result.station_history
        self.assertTrue(isinstance(station_history, StationHistory))
        self.assertTrue(isinstance(station_history.measurements, dict))

    def test_station_day_history_returning_none(self):
        original_http_get = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_call_api_returning_station_day_weather_history
        original_retrieve_station_history = self.__test_instance._retrieve_station_history
        self.__test_instance._retrieve_station_history = self.mock__retrieve_station_history

        result = self.__test_instance.station_day_history(1234, limit=4)

        HttpClient.get_json = original_http_get
        self.__test_instance._retrieve_station_history = original_retrieve_station_history

        self.assertIsNone(result)

    def test_station_day_history_fails_with_wrong_params(self):
        self.assertRaises(ValueError, WeatherManager.station_day_history, self.__test_instance, 1234, -3)

    def test_one_call(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_onecall_data
        result = self.__test_instance.one_call(46.23, 12.7)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, OneCall))
        self.assertTrue(isinstance(result.current, Weather))
        self.assertTrue(isinstance(result.forecast_hourly, list))
        self.assertTrue(all(isinstance(v, Weather) for v in result.forecast_hourly))
        if result.forecast_daily is not None:
            self.assertTrue(all(isinstance(v, Weather) for v in result.forecast_daily))

    def test_one_call_fails(self):
        self.assertRaises(AssertionError, WeatherManager.one_call, self.__test_instance, None, 12.7)
        self.assertRaises(AssertionError, WeatherManager.one_call, self.__test_instance, 46.23, 'test')

    def test_one_call_history_without_time_range(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_onecall_history_data
        result = self.__test_instance.one_call_history(46.23, 12.7)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, OneCall))
        self.assertTrue(isinstance(result.current, Weather))
        self.assertTrue(isinstance(result.forecast_hourly, list))
        self.assertTrue(all(isinstance(v, Weather) for v in result.forecast_hourly))
        if result.forecast_daily is not None:
            self.assertTrue(all(isinstance(v, Weather) for v in result.forecast_daily))

    def test_one_call_history_with_time_range(self):
        original_func = HttpClient.get_json
        HttpClient.get_json = \
            self.mock_api_call_returning_onecall_history_data
        result = self.__test_instance.one_call_history(46.23, 12.7, dt=1577890800)
        HttpClient.get_json = original_func
        self.assertTrue(isinstance(result, OneCall))
        self.assertTrue(isinstance(result.current, Weather))
        self.assertTrue(isinstance(result.forecast_hourly, list))
        self.assertTrue(all(isinstance(v, Weather) for v in result.forecast_hourly))
        if result.forecast_daily is not None:
            self.assertTrue(all(isinstance(v, Weather) for v in result.forecast_daily))

    def test_one_call_history_fails(self):
        self.assertRaises(AssertionError, WeatherManager.one_call_history, self.__test_instance, None, 12.7, 1234567)
        self.assertRaises(AssertionError, WeatherManager.one_call_history, self.__test_instance, 46.23, 'test', 1234567)
        self.assertRaises(ValueError, WeatherManager.one_call_history, self.__test_instance, 46.23, 12.7, 'test')
        self.assertRaises(ValueError, WeatherManager.one_call_history, self.__test_instance, 46.23, 12.7, -987)
