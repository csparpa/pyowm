#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
from pyowm.weatherapi30.national_weather_alert import NationalWeatherAlert
from pyowm.commons.exceptions import APIResponseError, ParseAPIResponseError


class TestNationalWeatherAlert(unittest.TestCase):

    __test_time_start= 1629648000
    __test_time_end = 1629723600
    __test_sender = "Deutscher Wetterdienst"
    __test_title = "very heavy / persistent rain"
    __test_description = "There is a high potential for the development of very heavy / heavy persistent rain."
    __test_tags = ['Rain']
    __test_instance = NationalWeatherAlert(__test_sender, __test_title, __test_description, __test_time_start,
                                           __test_time_end, __test_tags)

    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'
    __bad_json_2 = '{"message": "test", "cod": "500"}'
    __no_items_json = '{"cod": "200", "count": "0" }'
    __404_json = '{"cod": "404" }'

    NATIONAL_WEATHER_ALERT_JSON_DUMP = '{"sender_name": "Deutscher Wetterdienst", "event": "very heavy / persistent rain", ' \
                                       '"start": 1629648000, "end": 1629723600, "description": "There is a high potential ' \
                                       'for the development of very heavy / heavy persistent rain.", "tags": ["Rain"]}'

    def test_init_failures(self):
        self.assertRaises(AssertionError, NationalWeatherAlert, None, self.__test_title, self.__test_description,
                          self.__test_time_start, self.__test_time_end)
        self.assertRaises(AssertionError, NationalWeatherAlert, self.__test_sender, None, self.__test_description,
                          self.__test_time_start, self.__test_time_end)
        self.assertRaises(AssertionError, NationalWeatherAlert, self.__test_sender, self.__test_title, None,
                          self.__test_time_start, self.__test_time_end)
        self.assertRaises(AssertionError, NationalWeatherAlert, self.__test_sender, self.__test_title, self.__test_description,
                          None, self.__test_time_end)
        self.assertRaises(AssertionError, NationalWeatherAlert, self.__test_sender, self.__test_title, self.__test_description,
                          self.__test_time_start, None)
        self.assertRaises(ValueError, NationalWeatherAlert, self.__test_sender, self.__test_title, self.__test_description,
                          self.__test_time_start, self.__test_time_end, 'testtesttest')

    def test_from_dict(self):
        d = json.loads(self.NATIONAL_WEATHER_ALERT_JSON_DUMP)
        result = NationalWeatherAlert.from_dict(d)
        self.assertTrue(result is not None)
        self.assertFalse(result.sender is None)
        self.assertFalse(result.title is None)
        self.assertFalse(result.description is None)
        self.assertFalse(result.start_time() is None)
        self.assertFalse(result.end_time() is None)
        self.assertTrue(isinstance(result.tags, list))

    def test_from_dict_fails_when_JSON_data_is_None(self):
        with self.assertRaises(ParseAPIResponseError):
            NationalWeatherAlert.from_dict(None)

    def test_to_dict(self):
        expected = json.loads(self.NATIONAL_WEATHER_ALERT_JSON_DUMP)
        result = self.__test_instance.to_dict()
        self.assertEqual(expected, result)

    def test__repr(self):
        print(self.__test_instance)