#!/usr/bin/env python

"""
Test case for jsonparser.py module
"""

import unittest
from json_test_responses import OBSERVATION_JSON, OBSERVATION_NOT_FOUND_JSON, \
    SEARCH_RESULTS_JSON, INTERNAL_SERVER_ERROR_JSON, SEARCH_WITH_NO_RESULTS_JSON, \
    FORECAST_NOT_FOUND_JSON, THREE_HOURS_FORECAST_JSON, CITY_WEATHER_HISTORY_JSON, \
    CITY_WEATHER_HISTORY_NO_RESULTS_JSON, CITY_WEATHER_HISTORY_NOT_FOUND_JSON, \
    STATION_TICK_WEATHER_HISTORY_JSON, STATION_WEATHER_HISTORY_NOT_FOUND_JSON
from pyowm.utils import jsonparser
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.location import Location
from pyowm.weather import Weather
from pyowm.stationhistory import StationHistory
from pyowm.exceptions.api_response_error import APIResponseError


class TestJSONParser(unittest.TestCase):

    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'
    
    def test_build_location_from(self):
        dict1 = { "coord": { "lon": -0.12574, "lat": 51.50853 }, "id": 2643743,
                  "name": u"London", "cnt": 9 }
        dict2 = { "city" : { "coord" : { "lat" : 51.50853, "lon" : -0.125739 }, 
                  "country" : "GB", "id" : 2643743, "name" : u"London",
                  "population" : 1000000 }
                 }
        result1 = jsonparser.build_location_from(dict1)
        result2 = jsonparser.build_location_from(dict2)
        self.assertTrue(isinstance(result1, Location))
        self.assertTrue(isinstance(result2, Location))
        self.assertFalse(result1.get_country())
        self.assertTrue(result1.get_ID())
        self.assertTrue(result1.get_lat())
        self.assertTrue(result1.get_lon())
        self.assertTrue(result1.get_name())
        self.assertNotIn(None, result2.__dict__.values())
        
    def test_build_weather_from(self):
        dict1 = {'clouds': {'all': 92}, 'name': u'London',
                 'coord': {'lat': 51.50853, 'lon': -0.12574},
                 'sys': {'country': u'GB', 'sunset': 1378923812,
                         'sunrise': 1378877413
                         },
                 'weather': [
                 { 'main': u'Clouds', 'id': 804, 'icon': u'04d',
                  'description': u'overcastclouds'}
                 ],
                 'cod': 200, 'base': u'gdpsstations', 'dt': 1378895177,
                 'main': {
                      'pressure': 1022,
                      'humidity': 75,
                      'temp_max': 289.82,
                      'temp': 288.44,
                      'temp_min': 287.59
                  },
                  'id': 2643743,
                  'wind': { 'gust': 2.57, 'speed': 1.54, 'deg': 31}
        }
        dict2 = {"dt": 1378897200,
                   "temp": { "day": 289.37,"min": 284.88, "max": 289.37,
                             "night": 284.88, "eve": 287.53, "morn": 289.37
                             },
                   "pressure": 1025.35,
                   "humidity": 71,
                   "weather": [
                   { "id": 500, "main": u"Rain", "description": u"light rain",
                     "icon": u"u10d"}
                   ],"speed": 3.76, "deg": 338, "clouds": 48,"rain": 3
                }
        result1 = jsonparser.build_weather_from(dict1)
        self.assertTrue(isinstance(result1, Weather))
        self.assertNotIn(None, result1.__dict__.values())
        result2 = jsonparser.build_weather_from(dict2)
        self.assertTrue(isinstance(result2, Weather))
        self.assertNotIn(None, result2.__dict__.values())

    def test_parse_observation(self):
        result = jsonparser.parse_observation(OBSERVATION_JSON)
        self.assertTrue(result)
        self.assertFalse(result.get_reception_time() is None)
        self.assertFalse(result.get_location() is None)
        self.assertNotIn(None, result.get_location().__dict__.values())
        self.assertFalse(result.get_weather() is None)
        self.assertNotIn(None, result.get_weather().__dict__.values())
        
    def test_parse_observation_fails_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, jsonparser.parse_observation,
                          self.__bad_json)
        
    def test_parse_observation_when_server_error(self):
        result = jsonparser.parse_observation(OBSERVATION_NOT_FOUND_JSON)
        self.assertTrue(result is None)
        
    def test_parse_weather_search_results(self):
        result = jsonparser.parse_weather_search_results(SEARCH_RESULTS_JSON)
        self.assertFalse(result is None)
        self.assertTrue(isinstance(result, list))
        for item in result:
            self.assertFalse(item is None)
            self.assertFalse(item.get_reception_time() is None)
            self.assertFalse(item.get_location() is None)
            self.assertNotIn(None, item.get_location().__dict__.values())
            self.assertFalse(item.get_weather() is None)
            self.assertNotIn(None, item.get_weather().__dict__.values())
        
    def test_parse_weather_search_results_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, jsonparser.parse_weather_search_results,
                          self.__bad_json)
        
    def test_parse_weather_search_results_when_no_results(self):
        result = jsonparser.parse_weather_search_results(SEARCH_WITH_NO_RESULTS_JSON)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(0, len(result))
        
    def test_parse_weather_search_results_when_server_error(self):
        self.assertRaises(APIResponseError, jsonparser.parse_weather_search_results,
                          INTERNAL_SERVER_ERROR_JSON)

    def test_parse_forecast(self):
        result = jsonparser.parse_forecast(THREE_HOURS_FORECAST_JSON, "3h")
        self.assertTrue(result)
        self.assertTrue(result.get_reception_time())
        self.assertTrue(result.get_interval())
        self.assertTrue(result.get_location())
        self.assertNotIn(None, result.get_location().__dict__.values())
        self.assertTrue(isinstance(result.get_weathers(),list))
        for weather in result:
            self.assertTrue(weather)
            self.assertNotIn(None, weather.__dict__.values())
        
    def test_parse_forecast_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, jsonparser.parse_forecast, 
                          self.__bad_json, "3h")
        
    def test_parse_forecast_when_no_results(self):
        result = jsonparser.parse_forecast(FORECAST_NOT_FOUND_JSON, "3h")
        self.assertFalse(result is None)
        self.assertEqual(0, len(result))
        
    def test_parse_forecast_when_server_error(self):
        self.assertRaises(APIResponseError, jsonparser.parse_forecast,
                          INTERNAL_SERVER_ERROR_JSON, "3h")

    def test_parse_weather_history(self):
        result = jsonparser.parse_weather_history(CITY_WEATHER_HISTORY_JSON)
        self.assertTrue(result)
        self.assertTrue(isinstance(result, list))
        for weather in result:
            self.assertTrue(weather)
            self.assertNotIn(None, weather.__dict__.values())
        
    def test_parse_weather_history_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, jsonparser.parse_weather_history, 
                          self.__bad_json)
        
    def test_parse_weather_history_when_no_results(self):
        result = jsonparser.parse_weather_history(CITY_WEATHER_HISTORY_NO_RESULTS_JSON)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(0, len(result))
        
    def test_parse_weather_history_when_location_not_found(self):
        self.assertFalse(jsonparser.parse_weather_history(
                                          CITY_WEATHER_HISTORY_NOT_FOUND_JSON))
        
    def test_parse_weather_history_when_server_error(self):
        self.assertRaises(APIResponseError, jsonparser.parse_weather_history,
                          INTERNAL_SERVER_ERROR_JSON)
        
    def test_parse_station_history(self):
        result = jsonparser.parse_station_history(STATION_TICK_WEATHER_HISTORY_JSON,
                                                  1234, "day")
        self.assertTrue(result)
        self.assertTrue(isinstance(result, StationHistory))
        self.assertTrue(result.get_measurements())
        
    def test_parse_station_history_with_malformed_JSON_data(self):
        self.assertRaises(ParseResponseError, jsonparser.parse_station_history, 
                          self.__bad_json, 1234, "tick")

    def test_parse_station_history_with_empty_data(self):
        json_data = '{"message": "","cod": "200","type": "hour","station_id": ' \
            '35579,"calctime": 0.1122,"cnt": 1,"list": [{"main": "test","dt": ' \
            '1381140000}]}'
        result = jsonparser.parse_station_history(json_data, 1234, "hour")
        datapoints = result.get_measurements()
        for datapoint in datapoints:
            self.assertTrue(all(value is None for value \
                                in datapoints[datapoint].values()))

    def test_parse_station_history_when_station_not_found(self):
        self.assertFalse(
             jsonparser.parse_station_history(STATION_WEATHER_HISTORY_NOT_FOUND_JSON,
             1234, "hour"))
        
    def test_parse_station_history_when_server_error(self):
        self.assertRaises(APIResponseError, jsonparser.parse_station_history,
                          INTERNAL_SERVER_ERROR_JSON, 1234, "tick")

if __name__ == "__main__":
    unittest.main()