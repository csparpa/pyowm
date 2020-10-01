#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import pyowm.commons.exceptions
from pyowm import owm
from pyowm.weatherapi25.one_call import OneCall
from pyowm.weatherapi25.weather import Weather


class IntegrationTestsWebAPI25(unittest.TestCase):
    __owm = owm.OWM(os.getenv('OWM_API_KEY', None)).weather_manager()

    def test_weather_at_place(self):
        """
        Test feature: get currently observed weather at specific location
        """
        o1 = self.__owm.weather_at_place('London,GB')
        o2 = self.__owm.weather_at_place('Kiev')
        self.assertTrue(o1 is not None)
        self.assertTrue(o1.reception_time() is not None)
        loc = o1.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o1.weather
        self.assertTrue(weat is not None)
        self.assertTrue(o2 is not None)
        self.assertTrue(o2.reception_time() is not None)
        loc = o2.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o2.weather
        self.assertTrue(weat is not None)

    def test_weather_at_coords(self):
        """
        Test feature: get currently observed weather at specific coordinates
        """
        o1 = self.__owm.weather_at_coords(41.896144, 12.484589)  # Rome
        o2 = self.__owm.weather_at_coords(-33.936524, 18.503723)  # Cape Town
        self.assertTrue(o1)
        self.assertTrue(o1.reception_time())
        loc = o1.location
        self.assertTrue(loc)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o1.weather
        self.assertTrue(weat)
        self.assertTrue(o2)
        self.assertTrue(o2.reception_time())
        loc = o2.location
        self.assertTrue(loc)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o2.weather
        self.assertTrue(weat)

    def test_weather_at_zipcode(self):
        """
        Test feature: get currently observed weather at specific postcode
        """
        o1 = self.__owm.weather_at_zip_code("94040", "US")
        self.assertTrue(o1)
        self.assertTrue(o1.reception_time())
        loc = o1.location
        self.assertTrue(loc)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o1.weather
        self.assertTrue(weat)

    def test_weather_at_id(self):
        o1 = self.__owm.weather_at_id(5128581)  # New York
        o2 = self.__owm.weather_at_id(703448)  # Kiev'
        self.assertTrue(o1 is not None)
        self.assertTrue(o1.reception_time() is not None)
        loc = o1.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o1.weather
        self.assertTrue(weat is not None)
        self.assertTrue(o2 is not None)
        self.assertTrue(o2.reception_time() is not None)
        loc = o2.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o2.weather
        self.assertTrue(weat is not None)

    def test_weather_at_ids(self):
        # New York, Kiev
        observations = self.__owm.weather_at_ids([5128581, 703448])
        o1 = observations[0]
        o2 = observations[1]
        self.assertTrue(o1 is not None)
        self.assertTrue(o1.reception_time() is not None)
        loc = o1.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o1.weather
        self.assertTrue(weat is not None)
        self.assertTrue(o2 is not None)
        self.assertTrue(o2.reception_time() is not None)
        loc = o2.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o2.weather
        self.assertTrue(weat is not None)

    def test_weather_at_places(self):
        """
        Test feature: find currently observed weather for locations matching
        the specified text search pattern
        """
        # Test using searchtype=accurate
        o1 = self.__owm.weather_at_places("London", "accurate")
        o2 = self.__owm.weather_at_places("Paris", "accurate", 2)
        self.assertTrue(isinstance(o1, list))
        for item in o1:
            self.assertTrue(item)
            self.assertTrue(item.reception_time())
            loc = item.location
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.weather
            self.assertTrue(weat is not None)
        self.assertTrue(isinstance(o2, list))
        self.assertFalse(len(o2) > 2)
        for item in o2:
            self.assertTrue(item)
            self.assertTrue(item.reception_time())
            loc = item.location
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.weather
            self.assertTrue(weat is not None)

        # Test using searchtype=like
        o3 = self.__owm.weather_at_places("London", "like")
        o4 = self.__owm.weather_at_places("Paris", "like", 2)
        self.assertTrue(isinstance(o3, list))
        for item in o3:
            self.assertTrue(item)
            self.assertTrue(item.reception_time())
            loc = item.location
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.weather
            self.assertTrue(weat is not None)
        self.assertTrue(isinstance(o4, list))
        self.assertFalse(len(o4) > 2)
        for item in o4:
            self.assertTrue(item)
            self.assertTrue(item.reception_time())
            loc = item.location
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.weather
            self.assertTrue(weat is not None)

    def test_weather_around_coords(self):
        """
        Test feature: find currently observed weather for locations that are
        nearby the specified coordinates
        """
        o2 = self.__owm.weather_around_coords(57.0, -2.15)  # Scotland
        self.assertTrue(isinstance(o2, list))
        for item in o2:
            self.assertTrue(item is not None)
            self.assertTrue(item.reception_time() is not None)
            loc = item.location
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.weather
            self.assertTrue(weat is not None)
        o1 = self.__owm.weather_around_coords(57.0, -2.15, 2)  # Scotland
        self.assertTrue(isinstance(o1, list))
        for item in o1:
            self.assertTrue(item is not None)
            self.assertTrue(item.reception_time() is not None)
            loc = item.location
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.weather
            self.assertTrue(weat is not None)

    def test_forecast_at_place_on_3h(self):
        """
        Test feature: get 3 hours forecast for a specific location
        """
        fc1 = self.__owm.forecast_at_place("London,GB", "3h")
        fc2 = self.__owm.forecast_at_place('Kiev', "3h")
        self.assertTrue(fc1)
        f1 = fc1.forecast
        self.assertTrue(f1 is not None)
        self.assertTrue(f1.reception_time() is not None)
        loc = f1.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f1:
            self.assertTrue(weather is not None)
        self.assertTrue(fc2 is not None)
        f2 = fc2.forecast
        self.assertTrue(f2 is not None)
        self.assertTrue(f2.reception_time() is not None)
        loc = f2.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f2:
            self.assertTrue(weather is not None)

    def test_forecast_at_coords_on_3h(self):
        """
        Test feature: get 3 hours forecast at a specific geographic coordinate
        """
        # London,uk
        fc1 = self.__owm.forecast_at_coords(51.5073509, -0.1277583, "3h")
        # Kiev
        fc2 = self.__owm.forecast_at_coords(50.4501, 30.5234, "3h")
        self.assertTrue(fc1)
        f1 = fc1.forecast
        self.assertTrue(f1 is not None)
        self.assertTrue(f1.reception_time() is not None)
        loc = f1.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f1:
            self.assertTrue(weather is not None)
        self.assertTrue(fc2 is not None)
        f2 = fc2.forecast
        self.assertTrue(f2 is not None)
        self.assertTrue(f2.reception_time() is not None)
        loc = f2.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f2:
            self.assertTrue(weather is not None)
        with self.assertRaises(ValueError):
            self.__owm.forecast_at_coords(199, 199, '3h')

    def test_forecast_at_id_on_3h(self):
        """
        Test feature: get 3 hours forecast for city ID
        """
        # London,uk
        fc1 = self.__owm.forecast_at_id(2643743, '3h')
        # Kiev
        fc2 = self.__owm.forecast_at_id(703448, '3h')
        self.assertTrue(fc1)
        f1 = fc1.forecast
        self.assertTrue(f1 is not None)
        self.assertTrue(f1.reception_time() is not None)
        loc = f1.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f1:
            self.assertTrue(weather is not None)
        self.assertTrue(fc2 is not None)
        f2 = fc2.forecast
        self.assertTrue(f2 is not None)
        self.assertTrue(f2.reception_time() is not None)
        loc = f2.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f2:
            self.assertTrue(weather is not None)
        # Unexistent
        try:
            fc3 = self.__owm.forecast_at_id(99999999999999, '3h')
            self.fail()
        except pyowm.commons.exceptions.NotFoundError:
            pass  # ok

    def forecast_at_place_daily(self):
        """
        Test feature: get daily forecast for a specific location
        """
        fc1 = self.__owm.forecast_at_place("London,GB", "daily")
        fc2 = self.__owm.forecast_at_place('Kiev', "daily")
        self.assertTrue(fc1)
        f1 = fc1.forecast
        f1 = fc1.forecast
        self.assertTrue(f1 is not None)
        self.assertTrue(f1.reception_time() is not None)
        loc = f1.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f1:
            self.assertTrue(weather is not None)
        self.assertTrue(fc2 is not None)
        f2 = fc2.forecast
        self.assertTrue(f2 is not None)
        self.assertTrue(f2.reception_time() is not None)
        loc = f2.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f2:
            self.assertTrue(weather is not None)

    def test_forecast_at_coords_daily(self):
        """
        Test feature: get daily forecast at a specific geographic coordinate
        """
        fc1 = self.__owm.forecast_at_coords(51.5073509, -0.1277583, 'daily')  # London,uk
        self.assertTrue(fc1)
        f1 = fc1.forecast
        self.assertTrue(f1 is not None)
        self.assertTrue(f1.reception_time() is not None)
        loc = f1.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f1:
            self.assertTrue(weather is not None)
        with self.assertRaises(ValueError):
            self.__owm.forecast_at_coords(199, 199, 'daily')

    def test_forecast_at_id_daily(self):
        """
        Test feature: get daily forecast for a specific city ID
        """
        # London,uk
        fc1 = self.__owm.forecast_at_id(2643743, 'daily')
        # Kiev
        fc2 = self.__owm.forecast_at_id(703448, 'daily')
        try:
            fc3 = self.__owm.forecast_at_id(99999999, 'daily')
            raise AssertionError("APIRequestError was expected here")
        except pyowm.commons.exceptions.NotFoundError:
            pass  # Ok!
        self.assertTrue(fc1)
        f1 = fc1.forecast
        self.assertTrue(f1 is not None)
        self.assertTrue(f1.reception_time() is not None)
        loc = f1.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f1:
            self.assertTrue(weather is not None)
        self.assertTrue(fc2 is not None)
        f2 = fc2.forecast
        self.assertTrue(f2 is not None)
        self.assertTrue(f2.reception_time() is not None)
        loc = f2.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f2:
            self.assertTrue(weather is not None)

    def test_station_tick_history(self):
        """
        Test feature: get station tick weather history for a specific
        meteostation
        """
        try:
            h1 = self.__owm.station_tick_history(39276)
            if h1 is not None:
                sh1 = h1.station_history
                self.assertTrue(sh1 is not None)
                data1 = sh1.measurements
                self.assertTrue(data1 is not None)
                self.assertFalse(0, len(data1))
                h2 = self.__owm.station_tick_history(39276, limit=2)
                self.assertTrue(h2 is not None)
                sh2 = h2.station_history
                self.assertTrue(sh2 is not None)
                data2 = sh2.measurements
                self.assertTrue(data2 is not None)
                self.assertFalse(len(data2) > 2)
                h3 = self.__owm.station_tick_history(987654)  # Shall be None
                self.assertFalse(h3 is not None)
        except pyowm.commons.exceptions.UnauthorizedError:
            pass  # it's a paid-level API feature

    def test_station_hour_history(self):
        """
        Test feature: get station hour weather history for a specific
        meteostation
        """
        try:
            h1 = self.__owm.station_hour_history(123)
            if h1 is not None:
                sh1 = h1.station_history
                self.assertTrue(sh1 is not None)
                data1 = sh1.measurements
                self.assertTrue(data1 is not None)
                self.assertFalse(0, len(data1))
                h2 = self.__owm.station_hour_history(987654)  # Shall be None
                self.assertFalse(h2 is not None)
        except pyowm.commons.exceptions.UnauthorizedError:
            pass  # it's a paid-level API feature

    def test_station_day_history(self):
        """
        Test feature: get station hour weather history for a specific
        meteostation
        """
        try:
            h1 = self.__owm.station_day_history(123)
            if h1 is not None:
                sh1 = h1.station_history
                self.assertTrue(sh1 is not None)
                data1 = sh1.measurements
                self.assertTrue(data1 is not None)
                self.assertFalse(0, len(data1))
                h2 = self.__owm.station_day_history(123, limit=3)
                self.assertTrue(h2 is not None)
                sh2 = h2.station_history
                self.assertTrue(sh2 is not None)
                data2 = sh2.measurements
                self.assertTrue(data2 is not None)
                h3 = self.__owm.station_day_history(987654)  # Shall be None
                self.assertFalse(h3 is not None)
        except pyowm.commons.exceptions.UnauthorizedError:
            pass  # it's a paid-level API feature

    def test_weather_at_places_in_bbox(self):
        o = self.__owm.weather_at_places_in_bbox(0.734720, 38.422663, 1.964651, 39.397204, 10, False)  # Ibiza
        self.assertTrue(isinstance(o, list))
        for item in o:
            self.assertTrue(item is not None)
            self.assertTrue(item.reception_time() is not None)
            loc = item.location
            self.assertTrue(loc is not None)
            weat = item.weather
            self.assertTrue(weat is not None)

    def test_one_call(self):
        result = self.__owm.one_call(lat=46.49, lon=11.33)
        self.assertTrue(isinstance(result, OneCall))
        self.assertEqual(46.49, result.lat)
        self.assertEqual(11.33, result.lon)
        self.assertEqual("Europe/Rome", result.timezone)
        self.assertTrue(isinstance(result.current, Weather))
        self.assertEqual(48, len(result.forecast_hourly))
        for i, weather in enumerate(result.forecast_hourly):
            self.assertTrue(isinstance(weather, Weather), f"entry {i} of forecast_hourly is invalid")
        self.assertEqual(8, len(result.forecast_daily))
        for i, weather in enumerate(result.forecast_daily):
            self.assertTrue(isinstance(weather, Weather), f"entry {i} of forecast_hourly is invalid")

    def test_one_call_historical(self):
        result = self.__owm.one_call_history(lat=48.8576, lon=2.3377)
        self.assertTrue(isinstance(result, OneCall))
        self.assertEqual(48.86, result.lat)
        self.assertEqual(2.34, result.lon)
        self.assertEqual("Europe/Paris", result.timezone)
        self.assertTrue(isinstance(result.current, Weather))
        if result.forecast_hourly is not None:
            for i, weather in enumerate(result.forecast_hourly):
                self.assertTrue(isinstance(weather, Weather), f"entry {i} of forecast_hourly is invalid")
        if result.forecast_daily is not None:
            self.assertEqual(8, len(result.forecast_daily))
            for i, weather in enumerate(result.forecast_daily):
                self.assertTrue(isinstance(weather, Weather), f"entry {i} of forecast_hourly is invalid")


if __name__ == "__main__":
    unittest.main()
