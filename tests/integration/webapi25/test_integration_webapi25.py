# -*- coding: utf-8 -*-

"""
Integration tests for the PyOWM library
These are "live" executions, that of course need the OWM web API to be up
and running
"""

import unittest
import os
from datetime import datetime
from pyowm.constants import DEFAULT_API_KEY
from pyowm.webapi25.configuration25 import parsers
from pyowm.webapi25.owm25 import OWM25
from pyowm.exceptions import api_call_error, unauthorized_error


class IntegrationTestsWebAPI25(unittest.TestCase):

    __owm = OWM25(parsers, os.getenv('OWM_API_KEY', DEFAULT_API_KEY))

    def test_is_API_online(self):
        self.assertTrue(self.__owm.is_API_online())

    def test_weather_at_place(self):
        """
        Test feature: get currently observed weather at specific location
        """
        o1 = self.__owm.weather_at_place('London,uk')
        o2 = self.__owm.weather_at_place('Kiev')
        self.assertTrue(o1 is not None)
        self.assertTrue(o1.get_reception_time() is not None)
        loc = o1.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o1.get_weather()
        self.assertTrue(weat is not None)
        self.assertTrue(o2 is not None)
        self.assertTrue(o2.get_reception_time() is not None)
        loc = o2.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o2.get_weather()
        self.assertTrue(weat is not None)

    def test_weather_at_coords(self):
        """
        Test feature: get currently observed weather at specific coordinates
        """
        o1 = self.__owm.weather_at_coords(41.896144, 12.484589)  # Rome
        o2 = self.__owm.weather_at_coords(-33.936524, 18.503723)  # Cape Town
        self.assertTrue(o1)
        self.assertTrue(o1.get_reception_time())
        loc = o1.get_location()
        self.assertTrue(loc)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o1.get_weather()
        self.assertTrue(weat)
        self.assertTrue(o2)
        self.assertTrue(o2.get_reception_time())
        loc = o2.get_location()
        self.assertTrue(loc)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o2.get_weather()
        self.assertTrue(weat)

    def test_weather_at_zipcode(self):
        """
        Test feature: get currently observed weather at specific postcode
        """
        o1 = self.__owm.weather_at_zip_code("94040", "US")
        self.assertTrue(o1)
        self.assertTrue(o1.get_reception_time())
        loc = o1.get_location()
        self.assertTrue(loc)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o1.get_weather()
        self.assertTrue(weat)

    def test_weather_at_id(self):
        o1 = self.__owm.weather_at_id(5128581) # New York
        o2 = self.__owm.weather_at_id(703448) # Kiev'
        o3 = self.__owm.weather_at_id(99999999) # Shall be None
        self.assertTrue(o1 is not None)
        self.assertTrue(o1.get_reception_time() is not None)
        loc = o1.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o1.get_weather()
        self.assertTrue(weat is not None)
        self.assertTrue(o2 is not None)
        self.assertTrue(o2.get_reception_time() is not None)
        loc = o2.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o2.get_weather()
        self.assertTrue(weat is not None)
        self.assertFalse(o3 is not None)

    def test_weather_at_ids(self):
        # New York, Kiev
        observations = self.__owm.weather_at_ids([5128581,703448])
        o1 = observations[0]
        o2 = observations[1]
        self.assertTrue(o1 is not None)
        self.assertTrue(o1.get_reception_time() is not None)
        loc = o1.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o1.get_weather()
        self.assertTrue(weat is not None)
        self.assertTrue(o2 is not None)
        self.assertTrue(o2.get_reception_time() is not None)
        loc = o2.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        weat = o2.get_weather()
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
            self.assertTrue(item.get_reception_time())
            loc = item.get_location()
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.get_weather()
            self.assertTrue(weat is not None)
        self.assertTrue(isinstance(o2, list))
        self.assertFalse(len(o2) > 2)
        for item in o2:
            self.assertTrue(item)
            self.assertTrue(item.get_reception_time())
            loc = item.get_location()
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.get_weather()
            self.assertTrue(weat is not None)

        # Test using searchtype=like
        o3 = self.__owm.weather_at_places("London", "like")
        o4 = self.__owm.weather_at_places("Paris", "like", 2)
        self.assertTrue(isinstance(o3, list))
        for item in o3:
            self.assertTrue(item)
            self.assertTrue(item.get_reception_time())
            loc = item.get_location()
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.get_weather()
            self.assertTrue(weat is not None)
        self.assertTrue(isinstance(o4, list))
        self.assertFalse(len(o4) > 2)
        for item in o4:
            self.assertTrue(item)
            self.assertTrue(item.get_reception_time())
            loc = item.get_location()
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.get_weather()
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
            self.assertTrue(item.get_reception_time() is not None)
            loc = item.get_location()
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.get_weather()
            self.assertTrue(weat is not None)
        o1 = self.__owm.weather_around_coords(57.0, -2.15, 2)  # Scotland
        self.assertTrue(isinstance(o1, list))
        for item in o1:
            self.assertTrue(item is not None)
            self.assertTrue(item.get_reception_time() is not None)
            loc = item.get_location()
            self.assertTrue(loc is not None)
            self.assertTrue(all(v is not None for v in loc.__dict__.values()))
            weat = item.get_weather()
            self.assertTrue(weat is not None)

    def test_three_hours_forecast(self):
        """
        Test feature: get 3 hours forecast for a specific location
        """
        fc1 = self.__owm.three_hours_forecast("London,uk")
        fc2 = self.__owm.three_hours_forecast('Kiev')
        self.assertTrue(fc1)
        f1 = fc1.get_forecast()
        self.assertTrue(f1 is not None)
        self.assertTrue(f1.get_reception_time() is not None)
        loc = f1.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f1:
            self.assertTrue(weather is not None)
        self.assertTrue(fc2 is not None)
        f2 = fc2.get_forecast()
        self.assertTrue(f2 is not None)
        self.assertTrue(f2.get_reception_time() is not None)
        loc = f2.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f2:
            self.assertTrue(weather is not None)

    def test_three_hours_forecast_at_coords(self):
        """
        Test feature: get 3 hours forecast at a specific geographic coordinate
        """
        # London,uk
        fc1 = self.__owm.three_hours_forecast_at_coords(51.5073509, -0.1277583)
        # Kiev
        fc2 = self.__owm.three_hours_forecast_at_coords(50.4501, 30.5234)
        self.assertTrue(fc1)
        f1 = fc1.get_forecast()
        self.assertTrue(f1 is not None)
        self.assertTrue(f1.get_reception_time() is not None)
        loc = f1.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f1:
            self.assertTrue(weather is not None)
        self.assertTrue(fc2 is not None)
        f2 = fc2.get_forecast()
        self.assertTrue(f2 is not None)
        self.assertTrue(f2.get_reception_time() is not None)
        loc = f2.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f2:
            self.assertTrue(weather is not None)
        with self.assertRaises(ValueError):
            self.__owm.three_hours_forecast_at_coords(199, 199)

    def test_three_hours_forecast_at_id(self):
        """
        Test feature: get 3 hours forecast for city ID
        """
        # London,uk
        fc1 = self.__owm.three_hours_forecast_at_id(2643743)
        # Kiev
        fc2 = self.__owm.three_hours_forecast_at_id(703448)
        # Shall be None
        fc3 = self.__owm.three_hours_forecast_at_id(99999999)
        self.assertTrue(fc1)
        f1 = fc1.get_forecast()
        self.assertTrue(f1 is not None)
        self.assertTrue(f1.get_reception_time() is not None)
        loc = f1.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f1:
            self.assertTrue(weather is not None)
        self.assertTrue(fc2 is not None)
        f2 = fc2.get_forecast()
        self.assertTrue(f2 is not None)
        self.assertTrue(f2.get_reception_time() is not None)
        loc = f2.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f2:
            self.assertTrue(weather is not None)
        self.assertEqual(fc3, None)

    def test_daily_forecast(self):
        """
        Test feature: get daily forecast for a specific location
        """
        fc1 = self.__owm.daily_forecast("London,uk")
        fc2 = self.__owm.daily_forecast('Kiev')
        self.assertTrue(fc1)
        f1 = fc1.get_forecast()
        self.assertTrue(f1 is not None)
        self.assertTrue(f1.get_reception_time() is not None)
        loc = f1.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f1:
            self.assertTrue(weather is not None)
        self.assertTrue(fc2 is not None)
        f2 = fc2.get_forecast()
        self.assertTrue(f2 is not None)
        self.assertTrue(f2.get_reception_time() is not None)
        loc = f2.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f2:
            self.assertTrue(weather is not None)

    def test_daily_forecast_at_coords(self):
        """
        Test feature: get daily forecast at a specific geographic coordinate
        """
        fc1 = self.__owm.daily_forecast_at_coords(51.5073509, -0.1277583) # London,uk
        self.assertTrue(fc1)
        f1 = fc1.get_forecast()
        self.assertTrue(f1 is not None)
        self.assertTrue(f1.get_reception_time() is not None)
        loc = f1.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f1:
            self.assertTrue(weather is not None)
        with self.assertRaises(ValueError):
            self.__owm.daily_forecast_at_coords(199, 199)

    def test_daily_forecast_at_id(self):
        """
        Test feature: get daily forecast for a specific city ID
        """
        # London,uk
        fc1 = self.__owm.daily_forecast_at_id(2643743)
        # Kiev
        fc2 = self.__owm.daily_forecast_at_id(703448)
        try:
            fc3 = self.__owm.daily_forecast_at_id(99999999)
            raise AssertionError("APICallError was expected here")
        except api_call_error.APICallError:
            pass  # Ok!
        self.assertTrue(fc1)
        f1 = fc1.get_forecast()
        self.assertTrue(f1 is not None)
        self.assertTrue(f1.get_reception_time() is not None)
        loc = f1.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f1:
            self.assertTrue(weather is not None)
        self.assertTrue(fc2 is not None)
        f2 = fc2.get_forecast()
        self.assertTrue(f2 is not None)
        self.assertTrue(f2.get_reception_time() is not None)
        loc = f2.get_location()
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        for weather in f2:
            self.assertTrue(weather is not None)

    def test_weather_history_at_place(self):
        """
        Test feature: get weather history for a specific location
        """
        start_iso = "2013-09-06 09:20:00+00"
        start_unix = 1378459200
        start_date = datetime(2013, 9, 6, 9, 20, 0)
        end_iso = "2013-09-06 20:26:40+00"
        end_unix = 1378499200
        end_date = datetime(2013, 9, 6, 20, 26, 40)
        try:
            l1 = self.__owm.weather_history_at_place("London,UK")
            if l1 is not None:
                for weather in l1:
                    self.assertTrue(weather is not None)
            l2 = self.__owm.weather_history_at_place('Kiev', start_unix, end_unix)
            if l2 is not None:
                for weather in l2:
                    self.assertTrue(weather is not None)
            l3 = self.__owm.weather_history_at_place('Rome', start_iso, end_iso)
            if l3 is not None:
                for weather in l3:
                    self.assertTrue(weather is not None)
            l4 = self.__owm.weather_history_at_place('Berlin', start_date, end_date)
            if l4 is not None:
                for weather in l4:
                    self.assertTrue(weather is not None)
            l5 = self.__owm.weather_history_at_place('QmFoPIlbf')  # Shall be None
            self.assertTrue(l5 is None)
        except unauthorized_error.UnauthorizedError:
            pass  # it's a paid-level API feature

    def test_weather_history_at_coords(self):
        try:
            l1 = self.__owm.weather_history_at_coords(51.5073509, -0.1277583)
            if l1 is not None:
                for weather in l1:
                    self.assertTrue(weather is not None)

        except unauthorized_error.UnauthorizedError:
            pass  # it's a paid-level API feature

    def test_weather_history_at_id(self):
        """
        Test feature: get weather history for a specific city ID
        """
        try:
            start_iso = "2013-09-06 09:20:00+00"
            start_unix = 1378459200
            start_date = datetime(2013, 9, 6, 9, 20, 0)
            end_iso = "2013-09-06 20:26:40+00"
            end_unix = 1378499200
            end_date = datetime(2013, 9, 6, 20, 26, 40)
            l1 = self.__owm.weather_history_at_id(2756723) # Dongen
            if l1 is not None:
                for weather in l1:
                    self.assertTrue(weather is not None)
            l2 = self.__owm.weather_history_at_id(2756723, start_unix, end_unix)
            if l2 is not None:
                for weather in l2:
                    self.assertTrue(weather is not None)
            l3 = self.__owm.weather_history_at_id(2756723, start_iso, end_iso)
            if l3 is not None:
                for weather in l3:
                    self.assertTrue(weather is not None)
            l4 = self.__owm.weather_history_at_id(2756723, start_date, end_date)
            if l4 is not None:
                for weather in l4:
                    self.assertTrue(weather is not None)
        except unauthorized_error.UnauthorizedError:
            pass  # it's a paid-level API feature

    def test_station_at_coords(self):
        """
        Test feature: get a list of meteostations nearest to a geographical
        point
        """
        s1 = self.__owm.station_at_coords(51.5073509, -0.1277583, 2)
        self.assertEqual(2, len(s1))
        for station in s1:
            self.assertTrue(station is not None)
            self.assertTrue(
                    all(v is not None for v in station.__dict__.values()))
        with self.assertRaises(ValueError):
            self.__owm.station_at_coords(51.5073509, 220)
        with self.assertRaises(ValueError):
            self.__owm.station_at_coords(220, -0.1277583)
        with self.assertRaises(ValueError):
            self.__owm.station_at_coords(51.5073509, -0.1277583, -3)
        with self.assertRaises(AssertionError):
            self.__owm.station_at_coords(51.5073509, -0.1277582, 'foo')

    def test_station_tick_history(self):
        """
        Test feature: get station tick weather history for a specific
        meteostation
        """
        try:
            h1 = self.__owm.station_tick_history(39276)
            if h1 is not None:
                sh1 = h1.get_station_history()
                self.assertTrue(sh1 is not None)
                data1 = sh1.get_measurements()
                self.assertTrue(data1 is not None)
                self.assertFalse(0, len(data1))
                h2 = self.__owm.station_tick_history(39276, limit=2)
                self.assertTrue(h2 is not None)
                sh2 = h2.get_station_history()
                self.assertTrue(sh2 is not None)
                data2 = sh2.get_measurements()
                self.assertTrue(data2 is not None)
                self.assertFalse(len(data2) > 2)
                h3 = self.__owm.station_tick_history(987654)  # Shall be None
                self.assertFalse(h3 is not None)
        except unauthorized_error.UnauthorizedError:
            pass  # it's a paid-level API feature

    def test_station_hour_history(self):
        """
        Test feature: get station hour weather history for a specific
        meteostation
        """
        try:
            h1 = self.__owm.station_hour_history(123)
            if h1 is not None:
                sh1 = h1.get_station_history()
                self.assertTrue(sh1 is not None)
                data1 = sh1.get_measurements()
                self.assertTrue(data1 is not None)
                self.assertFalse(0, len(data1))
                h2 = self.__owm.station_hour_history(987654)  # Shall be None
                self.assertFalse(h2 is not None)
        except unauthorized_error.UnauthorizedError:
            pass  # it's a paid-level API feature

    def test_station_day_history(self):
        """
        Test feature: get station hour weather history for a specific
        meteostation
        """
        try:
            h1 = self.__owm.station_day_history(123)
            if h1 is not None:
                sh1 = h1.get_station_history()
                self.assertTrue(sh1 is not None)
                data1 = sh1.get_measurements()
                self.assertTrue(data1 is not None)
                self.assertFalse(0, len(data1))
                h2 = self.__owm.station_day_history(123, limit=3)
                self.assertTrue(h2 is not None)
                sh2 = h2.get_station_history()
                self.assertTrue(sh2 is not None)
                data2 = sh2.get_measurements()
                self.assertTrue(data2 is not None)
                h3 = self.__owm.station_day_history(987654)  # Shall be None
                self.assertFalse(h3 is not None)
        except unauthorized_error.UnauthorizedError:
            pass  # it's a paid-level API feature

    def test_weather_at_station(self):
        """
        Test feature: get current weather measurement for a specific
        meteostation
        """
        o = self.__owm.weather_at_station(1000)
        self.assertTrue(o is not None)
        self.assertTrue(o.get_reception_time() is not None)
        weat = o.get_weather()
        self.assertTrue(weat is not None)

    def test_weather_at_stations_in_bbox(self):
        """
        Test feature: get current weather observations from meteostations
        inside of a bounding box determined by geo-coordinates.
        """
        o = self.__owm.weather_at_stations_in_bbox(49.07,8.87,61.26,65.21)
        self.assertTrue(isinstance(o, list))
        for item in o:
            self.assertTrue(item is not None)
            self.assertTrue(item.get_reception_time() is not None)
            loc = item.get_location()
            self.assertTrue(loc is not None)
            weat = item.get_weather()
            self.assertTrue(weat is not None)

    def test_uvindex_around_coords(self):
        """
        Test feature: get UV index around geo-coordinates.
        """
        u = self.__owm.uvindex_around_coords(45,9)
        self.assertIsNotNone(u)
        self.assertIsNotNone(u.get_value())
        self.assertIsNotNone(u.get_reception_time())
        self.assertIsNotNone(u.get_interval())
        self.assertIsNotNone(u.get_location())

    def test_coindex_around_coords(self):
        """
        Test feature: get CO index around geo-coordinates.
        """
        u = self.__owm.coindex_around_coords(45, 9)
        self.assertIsNotNone(u)
        self.assertIsNotNone(u.get_co_samples())
        self.assertIsNotNone(u.get_reception_time())
        self.assertIsNotNone(u.get_reference_time())
        self.assertIsNotNone(u.get_interval())
        self.assertIsNotNone(u.get_location())

    def test_ozone_around_coords(self):
        """
        Test feature: get ozone around geo-coordinates.
        """
        u = self.__owm.ozone_around_coords(45, 9)
        self.assertIsNotNone(u)
        self.assertIsNotNone(u.get_du_value())
        self.assertIsNotNone(u.get_reception_time())
        self.assertIsNotNone(u.get_reference_time())
        self.assertIsNotNone(u.get_interval())
        self.assertIsNotNone(u.get_location())

if __name__ == "__main__":
    unittest.main()
