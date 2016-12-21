# -*- coding: utf-8 -*-

"""
Test case for owm.py module.
Here we don't use mock objects because we don't want to rely on exeternal
mocking libraries; we use monkey patching instead.
Monkey patching pattern:
  1. Keep a reference to the original function to be patched
  2. Replace the original function with the mock version
  3. Call function and get results
  4. Restore the original function (if possible, before unittest assertions
     because they might fail)
"""

import unittest
import time
import sys
from tests.unit.webapi25.json_test_responses import (OBSERVATION_JSON,
     SEARCH_RESULTS_JSON, THREE_HOURS_FORECAST_JSON, DAILY_FORECAST_JSON,
     THREE_HOURS_FORECAST_AT_COORDS_JSON, DAILY_FORECAST_AT_COORDS_JSON,
     THREE_HOURS_FORECAST_AT_ID_JSON, DAILY_FORECAST_AT_ID_JSON,
     CITY_WEATHER_HISTORY_JSON, STATION_TICK_WEATHER_HISTORY_JSON,
     STATION_WEATHER_HISTORY_JSON, THREE_HOURS_FORECAST_NOT_FOUND_JSON,
     DAILY_FORECAST_NOT_FOUND_JSON, STATION_HISTORY_NO_ITEMS_JSON,
     STATION_OBSERVATION_JSON, STATION_AT_COORDS_JSON, 
     WEATHER_AT_STATION_IN_BBOX_JSON, UVINDEX_JSON, COINDEX_JSON, OZONE_JSON)
from pyowm.webapi25.owm25 import OWM25
from pyowm.constants import PYOWM_VERSION
from pyowm.commons.weather_client import WeatherHttpClient
from pyowm.commons.uv_client import UltraVioletHttpClient
from pyowm.commons.airpollution_client import AirPollutionHttpClient
from pyowm.webapi25.forecast import Forecast
from pyowm.webapi25.observation import Observation
from pyowm.webapi25.weather import Weather
from pyowm.webapi25.location import Location
from pyowm.webapi25.forecaster import Forecaster
from pyowm.webapi25.station import Station
from pyowm.webapi25.stationhistory import StationHistory
from pyowm.webapi25.historian import Historian
from pyowm.webapi25.uvindex import UVIndex
from pyowm.webapi25.coindex import COIndex
from pyowm.webapi25.ozone import Ozone
from pyowm.webapi25.forecastparser import ForecastParser
from pyowm.webapi25.observationparser import ObservationParser
from pyowm.webapi25.observationlistparser import ObservationListParser
from pyowm.webapi25.stationparser import StationParser
from pyowm.webapi25.stationlistparser import StationListParser
from pyowm.webapi25.stationhistoryparser import StationHistoryParser
from pyowm.webapi25.weatherhistoryparser import WeatherHistoryParser
from pyowm.webapi25.uvindexparser import UVIndexParser
from pyowm.webapi25.coindexparser import COIndexParser
from pyowm.webapi25.ozone_parser import OzoneParser


class TestOWM25(unittest.TestCase):

    __test_parsers = {
      'observation': ObservationParser(),
      'observation_list': ObservationListParser(),
      'forecast': ForecastParser(),
      'weather_history': WeatherHistoryParser(),
      'station_history': StationHistoryParser(),
      'station': StationParser(),
      'station_list': StationListParser(),
      'uvindex': UVIndexParser(),
      'coindex': COIndexParser(),
      'ozone': OzoneParser()
    }
    __test_instance = OWM25(__test_parsers, 'test_API_key')

    # Mock functions
    def mock_httputils_call_API_returning_single_obs(self, API_subset_URL,
                                                     params_dict):
        return OBSERVATION_JSON

    def mock_httputils_call_API_returning_single_station_obs(self,
                                                             API_subset_URL,
                                                             params_dict):
        return STATION_OBSERVATION_JSON

    def mock_httputils_call_API_ping(self, API_subset_URL, params_dict,
                                     API_timeout):
        return OBSERVATION_JSON

    def mock_httputils_call_API_failing_ping(self, API_subset_URL, params_dict,
                                            API_timeout):
        return None

    def mock_httputils_call_API_returning_multiple_obs(self, API_subset_URL,
                                                     params_dict):
        return SEARCH_RESULTS_JSON

    def mock_httputils_call_API_returning_3h_forecast(self, API_subset_URL,
                                                     params_dict):
        return THREE_HOURS_FORECAST_JSON

    def mock_httputils_call_API_returning_3h_forecast_with_no_items(self,
                                                API_subset_URL, params_dict):
        return THREE_HOURS_FORECAST_NOT_FOUND_JSON

    def mock_httputils_call_API_returning_daily_forecast_with_no_items(self,
                                                API_subset_URL, params_dict):
        return DAILY_FORECAST_NOT_FOUND_JSON

    def mock_httputils_call_API_returning_3h_forecast_at_coords(self,
                                                     API_subset_URL,
                                                     params_dict):
        return THREE_HOURS_FORECAST_AT_COORDS_JSON

    def mock_httputils_call_API_returning_3h_forecast_at_id(self,
                                                            API_subset_URL,
                                                            params_dict):
        return THREE_HOURS_FORECAST_AT_ID_JSON

    def mock_httputils_call_API_returning_daily_forecast(self, API_subset_URL,
                                                     params_dict):
        return DAILY_FORECAST_JSON

    def mock_httputils_call_API_returning_daily_forecast_at_coords(self,
                                                     API_subset_URL,
                                                     params_dict):
        return DAILY_FORECAST_AT_COORDS_JSON

    def mock_httputils_call_API_returning_daily_forecast_at_id(self,
                                                               API_subset_URL,
                                                               params_dict):
        return DAILY_FORECAST_AT_ID_JSON

    def mock_httputils_call_API_returning_city_weather_history(self,
                                                       API_subset_URL,
                                                       params_dict):
        return CITY_WEATHER_HISTORY_JSON

    def mock_httputils_call_API_returning_station_tick_weather_history(self,
                                                       API_subset_URL,
                                                       params_dict):
        return STATION_TICK_WEATHER_HISTORY_JSON

    def mock_httputils_call_API_returning_station_hour_weather_history(self,
                                                       API_subset_URL,
                                                       params_dict):
        return STATION_WEATHER_HISTORY_JSON

    def mock_httputils_call_API_returning_station_day_weather_history(self,
                                                       API_subset_URL,
                                                       params_dict):
        return STATION_WEATHER_HISTORY_JSON

    def mock_httputils_call_API_returning_station_history_with_no_items(self,
                                                       API_subset_URL,
                                                       params_dict):
        return STATION_HISTORY_NO_ITEMS_JSON

    def mock_httputils_call_API_returning_weather_at_stations_in_bbox(self,
                                                       API_subset_URL,
                                                       params_dict):
        return WEATHER_AT_STATION_IN_BBOX_JSON

    def mock_httputils_call_API_returning_station_at_coords(self,
                                                       API_subset_URL,
                                                       params_dict):
        return STATION_AT_COORDS_JSON

    def mock_httputils_call_API_returning_weather_history_at_coords(self,
                                                       API_subset_URL,
                                                       params_dict):
        return CITY_WEATHER_HISTORY_JSON

    def mock_get_uvi_returning_uvindex_around_coords(self, params_dict):
        return UVINDEX_JSON

    def mock_get_coi_returning_coindex_around_coords(self, params_dict):
        return COINDEX_JSON

    def mock_get_o3_returning_coindex_around_coords(self, params_dict):
        return OZONE_JSON

    # Tests

    def test_encode_string(self):
        name = 'testname'
        if sys.version_info > (3, 0):
            result = OWM25._encode_string(name)
            self.assertEquals(result, name)
        else:  # Python 2
            result = OWM25._encode_string(name)
            try:
                result.decode('ascii')
            except:
                self.fail()

    def test_assert_is_string(self):
        a_string = 'test'
        a_non_string = 123
        OWM25._assert_is_string(a_string)
        self.assertRaises(AssertionError, OWM25._assert_is_string, a_non_string)

    def test_assert_is_string_or_unicode(self):
        a_string = 'test'
        a_non_string = 123
        OWM25._assert_is_string_or_unicode(a_string)
        self.assertRaises(AssertionError,
                          OWM25._assert_is_string_or_unicode,
                          a_non_string)

        try:  # only for Python 2
            unicode_value = unicode('test')
            OWM25._assert_is_string_or_unicode(unicode_value)
        except:
            pass

    def test_wrong_API_key(self):
        try:
            OWM25(self.__test_parsers, 1234)
            self.fail("Didn't raise AssertionError")
        except AssertionError:
            pass

    def test_API_key_is_mandatory_with_paid_subscription(self):
        try:
            owm_paid = OWM25(self.__test_parsers, subscription_type='pro')
            self.fail("Didn't raise AssertionError")
        except AssertionError:
            pass

    def test_API_key_accessors(self):
        test_API_key = 'G097IueS-9xN712E'
        owm = OWM25({})
        self.assertFalse(owm.get_API_key())
        owm.set_API_key(test_API_key)
        self.assertEqual(owm.get_API_key(), test_API_key)

    def test_get_subscription_type(self):
        owm_free = OWM25({})
        self.assertEqual(owm_free.get_subscription_type(), 'free')
        owm_paid = OWM25(self.__test_parsers, API_key='xyz',
                         subscription_type='pro')
        self.assertEqual(owm_paid.get_subscription_type(), 'pro')

    def test_is_API_online(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_ping
        result = self.__test_instance.is_API_online()
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(result)

    def test_is_API_online_failure(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_failing_ping
        result = self.__test_instance.is_API_online()
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertFalse(result)

    def test_city_id_registry(self):
        result = self.__test_instance.city_id_registry()
        self.assertTrue(result is not None)

    def test_get_API_version(self):
        self.assertEqual(self.__test_instance.OWM_API_VERSION,
                         self.__test_instance.get_API_version())

    def test_get_version(self):
        self.assertEqual(PYOWM_VERSION, self.__test_instance.get_version())

    def test_language_accessors(self):
        self.assertEqual("en", self.__test_instance.get_language())
        self.__test_instance.set_language("ru")
        self.assertEqual("ru", self.__test_instance.get_language())

    def test_weather_at_place(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_single_obs
        result = self.__test_instance.weather_at_place("London,uk")
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Observation))
        self.assertTrue(result.get_reception_time() is not None)
        loc = result.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = result.get_weather()
        self.assertTrue(weat is not None)

    def test_weather_at_place_fails_with_wrong_parameters(self):
        self.assertRaises(AssertionError,  OWM25.weather_at_place, \
                          self.__test_instance, 3)

    def test_weather_at_coords(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_single_obs
        result = self.__test_instance.weather_at_coords(57.0, -2.15)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Observation))
        self.assertTrue(result.get_reception_time() is not None)
        loc = result.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = result.get_weather()
        self.assertTrue(weat is not None)

    def test_weather_at_zip_code(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_single_obs
        result = self.__test_instance.weather_at_zip_code("2000", "AU")
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Observation))
        self.assertTrue(result.get_reception_time() is not None)
        loc = result.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = result.get_weather()
        self.assertTrue(weat is not None)

    def test_weather_at_coords_fails_when_coordinates_out_of_bounds(self):
        """
        Test failure when providing: lon < -180, lon > 180, lat < -90, lat > 90
        """
        self.assertRaises(ValueError, OWM25.weather_at_coords, \
                          self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, OWM25.weather_at_coords, \
                          self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, OWM25.weather_at_coords, \
                          self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, OWM25.weather_at_coords, \
                          self.__test_instance, 200, 2.5)

    def test_weather_at_id(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_single_obs
        result = self.__test_instance.weather_at_id(5128581)  # New York city, US
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Observation))
        self.assertTrue(result.get_reception_time() is not None)
        loc = result.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = result.get_weather()
        self.assertTrue(weat is not None)

    def test_weather_at_id_fails_when_id_negative(self):
        self.assertRaises(ValueError, OWM25.weather_at_id, \
                          self.__test_instance, -156667)

    def test_weather_at_ids(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_multiple_obs
        result = self.__test_instance.weather_at_ids([5128581, 15647, 78654])
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, list))
        for obs in result:
            self.assertTrue(obs is not None)
            self.assertTrue(isinstance(obs, Observation))
            weat = obs.get_weather()
            self.assertTrue(weat is not None)

    def test_weather_at_ids_fails_when_wrong_parameters(self):
        self.assertRaises(AssertionError, OWM25.weather_at_ids, \
                          self.__test_instance, "test")
        self.assertRaises(ValueError, OWM25.weather_at_ids, \
                          self.__test_instance, [-1, 2, 3])

    def test_weather_at_station(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_single_station_obs
        result = self.__test_instance.weather_at_station(1000)  # station: PAKP
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Observation))
        self.assertTrue(result.get_reception_time() is not None)
        loc = result.get_location()
        self.assertTrue(loc is not None)
        weat = result.get_weather()
        self.assertTrue(weat is not None)

    def test_weather_at_station_fails_when_id_negative(self):
        self.assertRaises(ValueError, OWM25.weather_at_station, \
                          self.__test_instance, -156667)

    def test_weather_at_places(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_multiple_obs
        result = \
            self.__test_instance.weather_at_places("London", "accurate")
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, list))
        self.assertEqual(2, len(result))
        for item in result:
            self.assertTrue(item is not None)
            self.assertTrue(item.get_reception_time())
            loc = item.get_location()
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.get_weather()
            self.assertTrue(weat is not None)

    def test_weather_at_places_fails_with_wrong_params(self):
        self.assertRaises(ValueError, OWM25.weather_at_places, \
                          self.__test_instance, "London", "x")
        self.assertRaises(ValueError, OWM25.weather_at_places, \
                          self.__test_instance, "London", "accurate", -5)

    def test_weather_around_coords(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_multiple_obs
        result = self.__test_instance.weather_around_coords(57.0, -2.15)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, list))
        for item in result:
            self.assertTrue(item is not None)
            self.assertTrue(item.get_reception_time() is not None)
            loc = item.get_location()
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.get_weather()
            self.assertTrue(weat is not None)

    def test_weather_around_coords_fails_when_coordinates_out_of_bounds(self):
        """
        Test failure when providing: lon < -180, lon > 180, lat < -90, lat > 90
        """
        self.assertRaises(ValueError, OWM25.weather_around_coords, \
                          self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, OWM25.weather_around_coords, \
                          self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, OWM25.weather_around_coords, \
                          self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, OWM25.weather_around_coords, \
                          self.__test_instance, 200, 2.5)

    def test_weather_around_coords_fails_with_wrong_params(self):
        self.assertRaises(ValueError, OWM25.weather_around_coords, \
                          self.__test_instance, 43.7, 20.0, -3)

    def test_three_hours_forecast(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_3h_forecast
        result = self.__test_instance.three_hours_forecast("London,uk")
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Forecaster))
        forecast = result.get_forecast()
        self.assertTrue(isinstance(forecast, Forecast))
        self.assertTrue(forecast.get_interval() is not None)
        self.assertTrue(forecast.get_reception_time() is not None)
        self.assertTrue(isinstance(forecast.get_location(), Location))
        self.assertEqual(1, len(forecast))
        for weather in forecast:
            self.assertTrue(isinstance(weather, Weather))

    def test_three_hours_forecast_when_forecast_not_found(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_3h_forecast_with_no_items
        result = self.__test_instance.three_hours_forecast("London,uk")
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertIsNone(result)

    def test_three_hours_forecast_at_coords(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_3h_forecast_at_coords
        result = \
            self.__test_instance\
                .three_hours_forecast_at_coords(51.50853, -0.12574)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Forecaster))
        forecast = result.get_forecast()
        self.assertTrue(isinstance(forecast, Forecast))
        self.assertTrue(forecast.get_interval() is not None)
        self.assertTrue(forecast.get_reception_time() is not None)
        self.assertTrue(isinstance(forecast.get_location(), Location))
        self.assertEqual(1, len(forecast))
        for weather in forecast:
            self.assertTrue(isinstance(weather, Weather))

    def test_three_hours_forecast_at_coords_when_forecast_not_found(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_3h_forecast_with_no_items
        result = self.__test_instance.three_hours_forecast_at_coords(51.50853,
                                                                     -0.12574)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertIsNone(result)

    def test_three_hours_forecast_at_coords_fails_with_wrong_params(self):
        self.assertRaises(ValueError, OWM25.three_hours_forecast_at_coords,
                          self.__test_instance, -100.0, 0.0)
        self.assertRaises(ValueError, OWM25.three_hours_forecast_at_coords,
                          self.__test_instance, 100.0, 0.0)
        self.assertRaises(ValueError, OWM25.three_hours_forecast_at_coords,
                          self.__test_instance, 0.0, -200.0)
        self.assertRaises(ValueError, OWM25.three_hours_forecast_at_coords,
                          self.__test_instance, 0.0, 200.0)

    def test_three_hours_forecast_at_id(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_3h_forecast_at_id
        result = self.__test_instance.three_hours_forecast_at_id(2643743)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Forecaster))
        forecast = result.get_forecast()
        self.assertTrue(isinstance(forecast, Forecast))
        self.assertTrue(forecast.get_interval() is not None)
        self.assertTrue(forecast.get_reception_time() is not None)
        self.assertTrue(isinstance(forecast.get_location(), Location))
        self.assertEqual(1, len(forecast))
        for weather in forecast:
            self.assertTrue(isinstance(weather, Weather))

    def test_three_hours_forecast_at_id_when_forecast_not_found(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_3h_forecast_with_no_items
        result = self.__test_instance.three_hours_forecast_at_id(2643743)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertIsNone(result)

    def test_three_hours_forecast_at_id_fails_with_wrong_params(self):
        self.assertRaises(ValueError, OWM25.three_hours_forecast_at_id,
                          self.__test_instance, -1234)

    def test_daily_forecast(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_daily_forecast
        result = self.__test_instance.daily_forecast("London,uk", 2)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Forecaster))
        forecast = result.get_forecast()
        self.assertTrue(isinstance(forecast, Forecast))
        self.assertTrue(forecast.get_interval() is not None)
        self.assertTrue(forecast.get_reception_time() is not None)
        self.assertTrue(isinstance(forecast.get_location(), Location))
        self.assertEqual(1, len(forecast))
        for weather in forecast:
            self.assertTrue(isinstance(weather, Weather))

    def test_daily_forecast_fails_with_wrong_params(self):
        self.assertRaises(AssertionError, OWM25.daily_forecast,
                          self.__test_instance, 2, 3)
        self.assertRaises(ValueError, OWM25.daily_forecast,
                          self.__test_instance, "London,uk", -3)

    def test_daily_forecast_when_forecast_not_found(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_daily_forecast_with_no_items
        result = self.__test_instance.daily_forecast('London,uk')
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertIsNone(result)

    def test_daily_forecast_at_coords(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_daily_forecast_at_coords
        result = \
            self.__test_instance.daily_forecast_at_coords(51.50853, -0.12574, 2)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Forecaster))
        forecast = result.get_forecast()
        self.assertTrue(isinstance(forecast, Forecast))
        self.assertTrue(forecast.get_interval() is not None)
        self.assertTrue(forecast.get_reception_time() is not None)
        self.assertTrue(isinstance(forecast.get_location(), Location))
        self.assertEqual(1, len(forecast))
        for weather in forecast:
            self.assertTrue(isinstance(weather, Weather))

    def test_daily_forecast_at_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, OWM25.daily_forecast_at_coords,
                          self.__test_instance, 51.50853, -0.12574, -3)
        self.assertRaises(ValueError, OWM25.daily_forecast_at_coords,
                          self.__test_instance, -100.0, 0.0)
        self.assertRaises(ValueError, OWM25.daily_forecast_at_coords,
                          self.__test_instance, 100.0, 0.0)
        self.assertRaises(ValueError, OWM25.daily_forecast_at_coords,
                          self.__test_instance, 0.0, -200.0)
        self.assertRaises(ValueError, OWM25.daily_forecast_at_coords,
                          self.__test_instance, 0.0, 200.0)

    def test_daily_forecast_at_coords_when_forecast_not_found(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_daily_forecast_with_no_items
        result = self.__test_instance.daily_forecast_at_coords(51.50853, -0.12574)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertIsNone(result)

    def test_daily_forecast_at_id(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_daily_forecast_at_id
        result = \
            self.__test_instance.daily_forecast_at_id(2643743, 2)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Forecaster))
        forecast = result.get_forecast()
        self.assertTrue(isinstance(forecast, Forecast))
        self.assertTrue(forecast.get_interval() is not None)
        self.assertTrue(forecast.get_reception_time() is not None)
        self.assertTrue(isinstance(forecast.get_location(), Location))
        self.assertEqual(1, len(forecast))
        for weather in forecast:
            self.assertTrue(isinstance(weather, Weather))

    def test_daily_forecast_at_id_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, OWM25.daily_forecast_at_id,
                          self.__test_instance, -123456, 3)
        self.assertRaises(ValueError, OWM25.daily_forecast_at_id,
                          self.__test_instance, 123456, -3)

    def test_daily_forecast_at_id_when_forecast_not_found(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_daily_forecast_with_no_items
        result = self.__test_instance.daily_forecast_at_id(123456)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertIsNone(result)

    def test_weather_history_at_place(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_city_weather_history
        result = self.__test_instance.weather_history_at_place("London,uk")
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, list))
        for weather in result:
            self.assertTrue(isinstance(weather, Weather))

    def test_weather_history_at_coords(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_weather_history_at_coords
        result = self.__test_instance.weather_history_at_coords(51.503614, -0.107331)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, list))
        for weather in result:
            self.assertTrue(isinstance(weather, Weather))

    def test_weather_history_at_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 51.50853, -0.12574, -3)
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, -100.0, 0.0)
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 100.0, 0.0)
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 0.0, -200.0)
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 0.0, 200.0)

    def test_weather_history_at_coords_fails_with_unordered_time_boundaries(self):
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 51.50853, -0.12574,
                          "2013-09-06 20:26:40+00", "2013-09-06 09:20:00+00")

    def test_weather_history_at_coords_fails_with_time_boundaries_in_the_future(self):
        current_time = int(time.time())
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 51.50853, -0.12574,
                          current_time + 1000, current_time + 2000)

    def test_weather_history_at_place_fails_with_wrong_time_boundaries(self):
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 51.50853, -0.12574, None, 1234567)
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 51.50853, -0.12574, 1234567, None)
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 51.50853, -0.12574, 1234567, None)
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 51.50853, -0.12574, -1234567, None)
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 51.50853, -0.12574, None, -1234567)
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 51.50853, -0.12574, -999, -888)
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 51.50853, -0.12574, "test", 1234567)
        self.assertRaises(ValueError, OWM25.weather_history_at_coords,
                          self.__test_instance, 51.50853, -0.12574, 1234567, "test")

    def test_weather_history_at_place_fails_with_unordered_time_boundaries(self):
        self.assertRaises(ValueError, OWM25.weather_history_at_place,
                          self.__test_instance, "London,uk",
                          "2013-09-06 20:26:40+00", "2013-09-06 09:20:00+00")

    def test_weather_history_at_place_fails_with_time_boundaries_in_the_future(self):
        current_time = int(time.time())
        self.assertRaises(ValueError, OWM25.weather_history_at_place,
                          self.__test_instance, "London,uk",
                          current_time + 1000, current_time + 2000)

    def test_weather_history_at_place_fails_with_wrong_time_boundaries(self):
        self.assertRaises(ValueError, OWM25.weather_history_at_place,
                          self.__test_instance, "London,uk", None, 1234567)
        self.assertRaises(ValueError, OWM25.weather_history_at_place,
                          self.__test_instance, "London,uk", 1234567, None)
        self.assertRaises(ValueError, OWM25.weather_history_at_place,
                          self.__test_instance, "London,uk", 1234567, None)
        self.assertRaises(ValueError, OWM25.weather_history_at_place,
                          self.__test_instance, "London,uk", -1234567, None)
        self.assertRaises(ValueError, OWM25.weather_history_at_place,
                          self.__test_instance, "London,uk", None, -1234567)
        self.assertRaises(ValueError, OWM25.weather_history_at_place,
                          self.__test_instance, "London,uk", -999, -888)
        self.assertRaises(ValueError, OWM25.weather_history_at_place,
                          self.__test_instance, "London,uk", "test", 1234567)
        self.assertRaises(ValueError, OWM25.weather_history_at_place,
                          self.__test_instance, "London,uk", 1234567, "test")

    def test_weather_history_at_place_fails_with_wrong_name(self):
        self.assertRaises(AssertionError, OWM25.weather_history_at_place,
                          self.__test_instance, 1, "test", 1234567)

    def test_weather_history_at_id(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_city_weather_history
        result = self.__test_instance.weather_history_at_id(12345)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, list))
        for weather in result:
            self.assertTrue(isinstance(weather, Weather))

    def test_weather_history_at_id_fails_with_negative_id(self):
        self.assertRaises(ValueError, OWM25.weather_history_at_id,
                          self.__test_instance, -12345,
                          "2013-09-06 20:26:40+00", "2013-09-06 09:20:00+00")

    def test_weather_history_at_id_fails_with_unordered_time_boundaries(self):
        self.assertRaises(ValueError, OWM25.weather_history_at_id,
                          self.__test_instance, 12345,
                          "2013-09-06 20:26:40+00", "2013-09-06 09:20:00+00")

    def test_weather_history_at_id_fails_with_time_boundaries_in_the_future(self):
        current_time = int(time.time())
        self.assertRaises(ValueError, OWM25.weather_history_at_id,
                          self.__test_instance, 12345,
                          current_time + 1000, current_time + 2000)

    def test_weather_history_at_id_fails_with_wrong_time_boundaries(self):
        self.assertRaises(ValueError, OWM25.weather_history_at_id,
                          self.__test_instance, 12345, None, 1234567)
        self.assertRaises(ValueError, OWM25.weather_history_at_id,
                          self.__test_instance, 12345, 1234567, None)
        self.assertRaises(ValueError, OWM25.weather_history_at_id,
                          self.__test_instance, 12345, 1234567, None)
        self.assertRaises(ValueError, OWM25.weather_history_at_id,
                          self.__test_instance, 12345, -1234567, None)
        self.assertRaises(ValueError, OWM25.weather_history_at_id,
                          self.__test_instance, 12345, None, -1234567)
        self.assertRaises(ValueError, OWM25.weather_history_at_id,
                          self.__test_instance, 12345, -999, -888)
        self.assertRaises(ValueError, OWM25.weather_history_at_id,
                          self.__test_instance, 12345, "test", 1234567)
        self.assertRaises(ValueError, OWM25.weather_history_at_id,
                          self.__test_instance, 12345, 1234567, "test")

    def test_weather_at_station_in_bbox(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_weather_at_stations_in_bbox
        results = self.__test_instance\
                .weather_at_stations_in_bbox(49.07,8.87,61.26,65.21)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(results, list))
        for result in results:
            self.assertTrue(isinstance(result, Observation))
            self.assertTrue(isinstance(result.get_weather(), Weather))
            self.assertTrue(isinstance(result.get_location(), Location))
            self.assertTrue(result.get_reception_time() is not None)

    def test_station_tick_history(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_station_tick_weather_history
        result = self.__test_instance.station_tick_history(1234, limit=4)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Historian))
        station_history = result.get_station_history()
        self.assertTrue(isinstance(station_history, StationHistory))
        self.assertTrue(isinstance(station_history.get_measurements(), dict))

    def test_station_tick_history_fails_with_wrong_params(self):
        self.assertRaises(ValueError, OWM25.station_tick_history,
                          self.__test_instance, 1234, -3)

    def test_station_tick_history_when_forecast_not_found(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_station_history_with_no_items
        result = self.__test_instance.station_tick_history(1234, limit=4)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertIsNone(result)

    def test_station_hour_history(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_station_hour_weather_history
        result = self.__test_instance.station_hour_history(1234, limit=4)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Historian))
        station_history = result.get_station_history()
        self.assertTrue(isinstance(station_history, StationHistory))
        self.assertTrue(isinstance(station_history.get_measurements(), dict))

    def test_station_hour_history_fails_with_wrong_params(self):
        self.assertRaises(ValueError, OWM25.station_hour_history,
                          self.__test_instance, 1234, -3)

    def test_station_hour_history_when_forecast_not_found(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_station_history_with_no_items
        result = self.__test_instance.station_hour_history(1234, limit=4)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertIsNone(result)

    def test_station_day_history(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_station_day_weather_history
        result = self.__test_instance.station_day_history(1234, limit=4)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Historian))
        station_history = result.get_station_history()
        self.assertTrue(isinstance(station_history, StationHistory))
        self.assertTrue(isinstance(station_history.get_measurements(), dict))

    def test_station_day_history_fails_with_wrong_params(self):
        self.assertRaises(ValueError, OWM25.station_day_history,
                          self.__test_instance, 1234, -3)

    def test_station_at_coords(self):
        ref_to_original_call_API = WeatherHttpClient.call_API
        WeatherHttpClient.call_API = \
            self.mock_httputils_call_API_returning_station_at_coords
        results = self.__test_instance.station_at_coords(51.5073509,
                                                         -0.1277583, 2)
        WeatherHttpClient.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(results, list))
        for result in results:
            self.assertTrue(isinstance(result, Station))
            self.assertTrue(isinstance(result.get_lon(), float))
            self.assertTrue(isinstance(result.get_lat(), float))
            self.assertTrue(isinstance(result.get_distance(), float))
            self.assertTrue(result.get_name())
            self.assertTrue(isinstance(result.get_last_weather(), Weather))
            self.assertTrue(isinstance(result.get_station_ID(), int))
            self.assertTrue(isinstance(result.get_station_type(), int))
            self.assertTrue(isinstance(result.get_status(), int))

    def test_uvindex_around_coords(self):
        ref_to_original = UltraVioletHttpClient.get_uvi
        UltraVioletHttpClient.get_uvi = \
            self.mock_get_uvi_returning_uvindex_around_coords
        result = self.__test_instance.uvindex_around_coords(45, 9)
        UltraVioletHttpClient.get_uvi = ref_to_original
        self.assertTrue(isinstance(result, UVIndex))
        self.assertIsNotNone(result.get_reference_time())
        self.assertIsNotNone(result.get_reception_time())
        loc = result.get_location()
        self.assertIsNotNone(loc)
        self.assertIsNotNone(loc.get_lat())
        self.assertIsNotNone(loc.get_lon())
        self.assertIsNotNone(result.get_value())
        self.assertIsNotNone(result.get_interval())

    def test_uvindex_around_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, OWM25.uvindex_around_coords, \
                          self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, OWM25.uvindex_around_coords, \
                          self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, OWM25.uvindex_around_coords, \
                          self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, OWM25.uvindex_around_coords, \
                          self.__test_instance, 200, 2.5)

    def test_coindex_around_coords(self):
        ref_to_original = AirPollutionHttpClient.get_coi
        AirPollutionHttpClient.get_coi = \
            self.mock_get_coi_returning_coindex_around_coords
        result = self.__test_instance.coindex_around_coords(45, 9)
        AirPollutionHttpClient.get_coi = ref_to_original
        self.assertTrue(isinstance(result, COIndex))
        self.assertIsNotNone(result.get_reference_time())
        self.assertIsNotNone(result.get_reception_time())
        loc = result.get_location()
        self.assertIsNotNone(loc)
        self.assertIsNotNone(loc.get_lat())
        self.assertIsNotNone(loc.get_lon())
        self.assertIsNotNone(result.get_co_samples())
        self.assertIsNotNone(result.get_interval())

    def test_coindex_around_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, OWM25.coindex_around_coords, \
                          self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, OWM25.coindex_around_coords, \
                          self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, OWM25.coindex_around_coords, \
                          self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, OWM25.coindex_around_coords, \
                          self.__test_instance, 200, 2.5)

    def test_ozone_around_coords(self):
        ref_to_original = AirPollutionHttpClient.get_o3
        AirPollutionHttpClient.get_o3 = \
            self.mock_get_o3_returning_coindex_around_coords
        result = self.__test_instance.ozone_around_coords(45, 9)
        AirPollutionHttpClient.get_o3 = ref_to_original
        self.assertTrue(isinstance(result, Ozone))
        self.assertIsNotNone(result.get_reference_time())
        self.assertIsNotNone(result.get_reception_time())
        loc = result.get_location()
        self.assertIsNotNone(loc)
        self.assertIsNotNone(loc.get_lat())
        self.assertIsNotNone(loc.get_lon())
        self.assertIsNotNone(result.get_du_value())
        self.assertIsNotNone(result.get_interval())

    def test_ozone_around_coords_fails_with_wrong_parameters(self):
        self.assertRaises(ValueError, OWM25.ozone_around_coords, \
                          self.__test_instance, 43.7, -200.0)
        self.assertRaises(ValueError, OWM25.ozone_around_coords, \
                          self.__test_instance, 43.7, 200.0)
        self.assertRaises(ValueError, OWM25.ozone_around_coords, \
                          self.__test_instance, -200, 2.5)
        self.assertRaises(ValueError, OWM25.ozone_around_coords, \
                          self.__test_instance, 200, 2.5)
