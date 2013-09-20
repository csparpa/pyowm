#!/usr/bin/env python

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
from json_test_responses import OBSERVATION_JSON, SEARCH_RESULTS_JSON, \
    THREE_HOURS_FORECAST_JSON, DAILY_FORECAST_JSON
from pyowm import OWM
from pyowm.utils import httputils
from pyowm.forecast import Forecast
from pyowm.observation import Observation
from pyowm.weather import Weather
from pyowm.location import Location
from pyowm.forecaster import Forecaster

class TestOWM(unittest.TestCase):
    
    __test_instance = OWM('test_API_key')
    
    # Mock functions
    def mock_httputils_call_API_returning_single_obs(self, API_subset_URL, 
                                                     params_dict, API_key):
        """Mock implementation of httputils.call_API"""
        return OBSERVATION_JSON
    
    def mock_httputils_call_API_returning_multiple_obs(self, API_subset_URL, 
                                                     params_dict, API_key):
        """Mock implementation of httputils.call_API"""
        return SEARCH_RESULTS_JSON
    
    def mock_httputils_call_API_returning_3h_forecast(self, API_subset_URL, 
                                                     params_dict, API_key):
        """Mock implementation of httputils.call_API"""
        return THREE_HOURS_FORECAST_JSON
    
    def mock_httputils_call_API_returning_daily_forecast(self, API_subset_URL, 
                                                     params_dict, API_key):
        """Mock implementation of httputils.call_API"""
        return DAILY_FORECAST_JSON

    # Tests
    def test_test_API_key_accessors(self):
        test_API_key = 'G097IueS-9xN712E'
        owm = OWM()
        self.assertEqual(owm.get_API_key(), None)
        owm.set_API_key(test_API_key)
        self.assertEqual(owm.get_API_key(), test_API_key)
        
    def test_test_version_print_methods(self):
        lib_version = self.__test_instance.get_version()
        API_version = self.__test_instance.get_API_version()
        self.assertIsInstance(lib_version, str)
        self.assertIsInstance(API_version, str)

    def test_observation_at_place(self):
        """
        Test that owm.observation_at_place returns a valid Observation object.
        We need to monkey patch the inner call to httputils.call_API function
        """
        ref_to_original_call_API = httputils.call_API
        httputils.call_API = self.mock_httputils_call_API_returning_single_obs
        result = self.__test_instance.observation_at_place("London,uk")
        httputils.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Observation))
        self.assertTrue(result.get_reception_time())
        self.assertTrue(result.get_location())
        self.assertNotIn(None, result.get_location().__dict__.values())
        self.assertTrue(result.get_weather())
        self.assertNotIn(None, result.get_weather().__dict__.values())
    
    def test_observation_at_coords(self):
        """
        Test that owm.observation_at_coords returns a valid Observation object.
        We need to monkey patch the inner call to httputils.call_API function
        """
        ref_to_original_call_API = httputils.call_API
        httputils.call_API = self.mock_httputils_call_API_returning_single_obs
        result = self.__test_instance.observation_at_coords(-2.15,57.0)
        httputils.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Observation))
        self.assertTrue(result.get_reception_time())
        self.assertTrue(result.get_location())
        self.assertNotIn(None, result.get_location().__dict__.values())
        self.assertTrue(result.get_weather())
        self.assertNotIn(None, result.get_weather().__dict__.values())

    def test_observation_at_coords_fails_when_coordinates_out_of_bounds(self):
        """
        Test failure when providing: lon < -180, lon > 180, lat < -90, lat > 90
        """
        self.assertRaises(ValueError, OWM.observation_at_coords, \
                          self.__test_instance, -200.0, 43.7)
        self.assertRaises(ValueError, OWM.observation_at_coords, \
                          self.__test_instance, 200.0, 43.7)
        self.assertRaises(ValueError, OWM.observation_at_coords, \
                          self.__test_instance, 2.5, -200)
        self.assertRaises(ValueError, OWM.observation_at_coords, \
                          self.__test_instance, 2.5, 200)
        
    def test_find_observations_by_name(self):
        """
        Test that owm.find_observations_by_name returns a list of valid 
        Observation objects. We need to monkey patch the inner call to 
        httputils.call_API function
        """
        ref_to_original_call_API = httputils.call_API
        httputils.call_API = self.mock_httputils_call_API_returning_multiple_obs
        result = self.__test_instance.find_observations_by_name("London","accurate")
        httputils.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, list))
        self.assertEqual(2, len(result))
        for item in result:
            self.assertTrue(item)
            self.assertTrue(item.get_reception_time())
            self.assertTrue(item.get_location())
            self.assertNotIn(None, item.get_location().__dict__.values())
            self.assertTrue(item.get_weather())
            self.assertNotIn(None, item.get_weather().__dict__.values())
        
    def test_find_observations_by_name_fails_with_wrong_params(self):
        """
        Test method failure providing: a bad value for 'searchtype' and a
        negative value for 'limit'
        """
        self.assertRaises(ValueError, OWM.find_observations_by_name, \
                          self.__test_instance, "London", "x")
        self.assertRaises(ValueError, OWM.find_observations_by_name, \
                          self.__test_instance, "London", "accurate", -5)

    def test_find_observations_by_coords(self):
        """
        Test that owm.find_observations_by_coords returns a list of valid 
        Observation objects. We need to monkey patch the inner call to 
        httputils.call_API function
        """
        ref_to_original_call_API = httputils.call_API
        httputils.call_API = self.mock_httputils_call_API_returning_multiple_obs
        result = self.__test_instance.find_observations_by_coords(-2.15,57.0)
        httputils.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, list))
        for item in result:
            self.assertTrue(item)
            self.assertTrue(item.get_reception_time())
            self.assertTrue(item.get_location())
            self.assertNotIn(None, item.get_location().__dict__.values())
            self.assertTrue(item.get_weather())
            self.assertNotIn(None, item.get_weather().__dict__.values())
        
    def test_find_observations_by_coords_fails_when_coordinates_out_of_bounds(self):
        """
        Test failure when providing: lon < -180, lon > 180, lat < -90, lat > 90
        """
        self.assertRaises(ValueError, OWM.find_observations_by_coords, \
                          self.__test_instance, -200.0, 43.7)
        self.assertRaises(ValueError, OWM.find_observations_by_coords, \
                          self.__test_instance, 200.0, 43.7)
        self.assertRaises(ValueError, OWM.find_observations_by_coords, \
                          self.__test_instance, 2.5, -200)
        self.assertRaises(ValueError, OWM.find_observations_by_coords, \
                          self.__test_instance, 2.5, 200)
        
    def test_find_observations_by_coords_fails_with_wrong_params(self):
        """
        Test method failure providing a negative value for 'limit'
        """
        self.assertRaises(ValueError, OWM.find_observations_by_coords, \
                          self.__test_instance, -200.0, 43.7, -3)

    def test_three_hours_forecast(self):
        """
        Test that owm.three_hours_forecast returns a valid Forecast object. 
        We need to monkey patch the inner call to httputils.call_API function
        """
        ref_to_original_call_API = httputils.call_API
        httputils.call_API = self.mock_httputils_call_API_returning_3h_forecast
        result = self.__test_instance.three_hours_forecast("London,uk")
        httputils.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Forecaster))        
        forecast = result.get_forecast()
        self.assertTrue(isinstance(forecast, Forecast))
        self.assertTrue(forecast.get_interval())
        self.assertTrue(forecast.get_reception_time())
        self.assertTrue(isinstance(forecast.get_location(), Location))
        self.assertEqual(1, len(forecast))
        for weather in forecast:
            self.assertTrue(isinstance(weather, Weather))
            self.assertNotIn(None, weather.__dict__.values())
            
    def test_daily_forecast(self):
        """
        Test that owm.daily_forecast returns a valid Forecast object. 
        We need to monkey patch the inner call to httputils.call_API function
        """
        ref_to_original_call_API = httputils.call_API
        httputils.call_API = self.mock_httputils_call_API_returning_daily_forecast
        result = self.__test_instance.daily_forecast("London,uk")
        httputils.call_API = ref_to_original_call_API
        self.assertTrue(isinstance(result, Forecaster))
        forecast = result.get_forecast()
        self.assertTrue(isinstance(forecast, Forecast))
        self.assertTrue(forecast.get_interval())
        self.assertTrue(forecast.get_reception_time())
        self.assertTrue(isinstance(forecast.get_location(), Location))
        self.assertEqual(1, len(forecast))
        for weather in forecast:
            self.assertTrue(isinstance(weather, Weather))
            self.assertNotIn(None, weather.__dict__.values())
            
    def test_daily_forecast_fails_with_wrong_params(self):
        """
        Test method failure providing a negative value for 'limit'
        """
        self.assertRaises(ValueError, OWM.daily_forecast, self.__test_instance, \
                          "London,uk", -3)
 
if __name__ == "__main__":
    unittest.main()