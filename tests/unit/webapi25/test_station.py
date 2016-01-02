"""
Test case for station.py module
"""

import unittest

from pyowm.webapi25.station import Station
from pyowm.webapi25.weather import Weather
from tests.unit.webapi25.json_test_dumps import STATION_JSON_DUMP
from tests.unit.webapi25.xml_test_dumps import STATION_XML_DUMP


class TestStation(unittest.TestCase):

    __test_name = 'KNGU'
    __test_station_type = 1
    __test_status = 50
    __test_station_ID = 2865
    __test_lat = 36.9375
    __test_lon = -76.2893
    __test_distance = 18.95
    __test_last_weather_instance = Weather(1378459200, 1378496400, 1378449600,
            67, {"all": 20}, {"all": 0}, {"deg": 252.002, "speed": 1.100}, 57,
            {"press": 1030.119, "sea_level": 1038.589}, {"temp": 294.199,
            "temp_kf": -1.899, "temp_max": 296.098, "temp_min": 294.199 },
            "Clouds", "Overcast clouds", 804, "04d", 1000, 300.0, 298.0, 296.0)

    __test_instance = Station(__test_name, __test_station_ID,
                              __test_station_type, __test_status, __test_lat,
                              __test_lon, __test_distance,
                              __test_last_weather_instance)

    def test_init_fails_with_invalid_coords(self):
        self.assertRaises(ValueError, Station, self.__test_name, 
                          self.__test_station_ID, self.__test_station_type,
                          self.__test_status, 120.0, self.__test_lon,
                          self.__test_distance,
                          self.__test_last_weather_instance)
        self.assertRaises(ValueError, Station, self.__test_name,
                          self.__test_station_ID, self.__test_station_type,
                          self.__test_status, self.__test_lat, 220.0,
                          self.__test_distance,
                          self.__test_last_weather_instance)

    def test_getters_return_expected_data(self):
        self.assertEqual(self.__test_name, self.__test_instance.get_name())
        self.assertEqual(self.__test_station_type,
                         self.__test_instance.get_station_type())
        self.assertEqual(self.__test_status, self.__test_instance.get_status())
        self.assertEqual(self.__test_station_ID,
                         self.__test_instance.get_station_ID())
                          
        self.assertEqual(self.__test_lat, self.__test_instance.get_lat())
        self.assertEqual(self.__test_lon, self.__test_instance.get_lon())
        self.assertEqual(self.__test_last_weather_instance,
                         self.__test_instance.get_last_weather())

    # Test JSON and XML comparisons by ordering strings (this overcomes
    # interpeter-dependant serialization of XML/JSON objects)

    def test_to_JSON(self):
        ordered_base_json = ''.join(sorted(STATION_JSON_DUMP))
        ordered_actual_json = ''.join(sorted(self.__test_instance.to_JSON()))
        self.assertEqual(ordered_base_json, ordered_actual_json)

    def test_to_XML(self):
        ordered_base_xml = ''.join(sorted(STATION_XML_DUMP))
        ordered_actual_xml = ''.join(sorted(self.__test_instance.to_XML()))
        self.assertEqual(ordered_base_xml, ordered_actual_xml)
