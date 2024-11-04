#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from pyowm.commons.http_client import HttpClient
from pyowm.config import DEFAULT_CONFIG
from pyowm.constants import GEOCODING_API_VERSION
from pyowm.geocodingapi10.geocoding_manager import GeocodingManager
from pyowm.weatherapi30.location import Location


class TestGeocodingManager(unittest.TestCase):

    __test_instance = GeocodingManager('fakeapikey', DEFAULT_CONFIG)

    DIRECT_GEOCODING_JSON = '''[{"name":"London","local_names":{"af":"Londen","ar":"لندن","ascii":"London","az":"London","bg":"Лондон","ca":"Londres","da":"London","de":"London","el":"Λονδίνο","en":"London","eu":"Londres","fa":"لندن","feature_name":"London","fi":"Lontoo","fr":"Londres","gl":"Londres","he":"לונדון","hi":"लंदन","hr":"London","hu":"London","id":"London","it":"Londra","ja":"ロンドン","la":"Londinium","lt":"Londonas","mk":"Лондон","nl":"Londen","no":"London","pl":"Londyn","pt":"Londres","ro":"Londra","ru":"Лондон","sk":"Londýn","sl":"London","sr":"Лондон","th":"ลอนดอน","tr":"Londra","vi":"Luân Đôn","zu":"ILondon"},"lat":51.5085,"lon":-0.1257,"country":"GB"},{"name":"London","local_names":{"ar":"لندن","ascii":"London","bg":"Лондон","de":"London","en":"London","fa":"لندن، انتاریو","feature_name":"London","fi":"London","fr":"London","he":"לונדון","ja":"ロンドン","lt":"Londonas","nl":"London","pl":"London","pt":"London","ru":"Лондон","sr":"Лондон"},"lat":42.9834,"lon":-81.233,"country":"CA"},{"name":"London","local_names":{"ar":"لندن","ascii":"London","en":"London","fa":"لندن، اوهایو","feature_name":"London","sr":"Ландон"},"lat":39.8865,"lon":-83.4483,"country":"US","state":"OH"},{"name":"London","local_names":{"ar":"لندن","ascii":"London","en":"London","fa":"لندن، کنتاکی","feature_name":"London","sr":"Ландон"},"lat":37.129,"lon":-84.0833,"country":"US","state":"KY"},{"name":"London","local_names":{"ascii":"London","ca":"Londres","en":"London","feature_name":"London"},"lat":36.4761,"lon":-119.4432,"country":"US","state":"CA"}]'''
    REVERSE_GEOCODING_JSON = '''[{"name":"London","local_names":{"af":"Londen","ar":"لندن","ascii":"London","az":"London","bg":"Лондон","ca":"Londres","da":"London","de":"London","el":"Λονδίνο","en":"London","eu":"Londres","fa":"لندن","feature_name":"London","fi":"Lontoo","fr":"Londres","gl":"Londres","he":"לונדון","hi":"लंदन","hr":"London","hu":"London","id":"London","it":"Londra","ja":"ロンドン","la":"Londinium","lt":"Londonas","mk":"Лондон","nl":"Londen","no":"London","pl":"Londyn","pt":"Londres","ro":"Londra","ru":"Лондон","sk":"Londýn","sl":"London","sr":"Лондон","th":"ลอนดอน","tr":"Londra","vi":"Luân Đôn","zu":"ILondon"},"lat":51.5085,"lon":-0.1257,"country":"GB"},{"name":"City of Westminster","local_names":{"ascii":"City of Westminster","feature_name":"City of Westminster"},"lat":51.5,"lon":-0.1167,"country":"GB"},{"name":"Lambeth","local_names":{"ascii":"Lambeth","en":"Lambeth","feature_name":"Lambeth"},"lat":51.4963,"lon":-0.1115,"country":"GB"},{"name":"Clerkenwell","local_names":{"ascii":"Clerkenwell","feature_name":"Clerkenwell","hi":"क्लर्कनवेल","ru":"Кларкенуэлл"},"lat":51.5244,"lon":-0.1102,"country":"GB"},{"name":"City of London","local_names":{"ar":"مدينة لندن","ascii":"City of London","bg":"Сити","ca":"La City","de":"London City","el":"Σίτι του Λονδίνου","en":"City of London","fa":"سیتی لندن","feature_name":"City of London","fi":"Lontoon City","fr":"Cité de Londres","gl":"Cidade de Londres","he":"הסיטי של לונדון","hi":"सिटी ऑफ़ लंदन","id":"Kota London","it":"Londra","ja":"シティ・オブ・ロンドン","la":"Civitas Londinium","lt":"Londono Sitis","pt":"Cidade de Londres","ru":"Сити","sr":"Сити","th":"นครลอนดอน","tr":"Londra Şehri","vi":"Thành phố Luân Đôn","zu":"Idolobha weLondon"},"lat":51.5128,"lon":-0.0918,"country":"GB"}]'''
    MALFORMED_JSON = '{"a":"2016-10-01T13:07:01Z","b":[]}'

    def mock_get_json_for_direct_geocoding(self, URI, params):
        return 200, json.loads(self.DIRECT_GEOCODING_JSON)

    def mock_get_json_returning_malformed_json(self, URI, params):
        return 200, json.loads(self.MALFORMED_JSON)

    def mock_get_json_for_reverse_geocoding(self, URI, params):
        return 200, json.loads(self.REVERSE_GEOCODING_JSON)

    def test_geocoding_api_version(self):
        result = self.__test_instance.geocoding_api_version()
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, GEOCODING_API_VERSION)

    def test_instantiation_with_wrong_params(self):
        self.assertRaises(AssertionError, GeocodingManager, None, dict())
        self.assertRaises(AssertionError, GeocodingManager, 'apikey', None)

    def test_geocode_with_wrong_params(self):
        self.assertRaises(AssertionError,
                          GeocodingManager.geocode, self.__test_instance,
                          None)
        self.assertRaises(ValueError,
                          GeocodingManager.geocode, self.__test_instance,
                          'London', 'tooooomany')
        self.assertRaises(ValueError,
                          GeocodingManager.geocode, self.__test_instance,
                          'London', 'GB', 'tooooomany')
        self.assertRaises(AssertionError,
                          GeocodingManager.geocode, self.__test_instance,
                          'London', 'OH', 'US', 'notastring')
        self.assertRaises(AssertionError,
                          GeocodingManager.geocode, self.__test_instance,
                          'London', 'OH', 'US', -6)

    def test_geocode_fails(self):
        ref_to_original = HttpClient.get_json
        HttpClient.get_json = self.mock_get_json_returning_malformed_json
        self.assertRaises(Exception,
                          GeocodingManager.geocode, self.__test_instance,
                          'London', 'GB')
        HttpClient.get_json = ref_to_original

    def test_geocode(self):
        ref_to_original = HttpClient.get_json
        HttpClient.get_json = self.mock_get_json_for_direct_geocoding
        locations = self.__test_instance.geocode('London', 'GB')
        self.assertTrue(isinstance(locations, list))
        self.assertTrue(all([isinstance(l, Location) for l in locations]))
        self.assertTrue(all([l.name == 'London' for l in locations]))
        HttpClient.get_json = ref_to_original

    def test_reverse_geocode_with_wrong_params(self):
        self.assertRaises(AssertionError,
                          GeocodingManager.reverse_geocode, self.__test_instance,
                          None, None)
        self.assertRaises(AssertionError,
                          GeocodingManager.reverse_geocode, self.__test_instance,
                          None, -0.15)
        self.assertRaises(AssertionError,
                          GeocodingManager.reverse_geocode, self.__test_instance,
                          42, None)
        self.assertRaises(ValueError,
                          GeocodingManager.reverse_geocode, self.__test_instance,
                          167, 15)
        self.assertRaises(ValueError,
                          GeocodingManager.reverse_geocode, self.__test_instance,
                          15, 234)
        self.assertRaises(AssertionError,
                          GeocodingManager.reverse_geocode, self.__test_instance,
                          42, 16, 'notanint')
        self.assertRaises(AssertionError,
                          GeocodingManager.reverse_geocode, self.__test_instance,
                          42, 16, -4)

    def test_reverse_geocode_fails(self):
        ref_to_original = HttpClient.get_json
        HttpClient.get_json = self.mock_get_json_returning_malformed_json
        self.assertRaises(Exception,
                          GeocodingManager.reverse_geocode, self.__test_instance,
                          51.5098, -0.1180)
        HttpClient.get_json = ref_to_original

    def test_reverse_geocode(self):
        lat = 51.5098
        lon = -0.1180
        ref_to_original = HttpClient.get_json
        HttpClient.get_json = self.mock_get_json_for_reverse_geocoding
        locations = self.__test_instance.reverse_geocode(lat, lon)
        self.assertTrue(isinstance(locations, list))
        self.assertTrue(all([isinstance(l, Location) for l in locations]))
        HttpClient.get_json = ref_to_original
