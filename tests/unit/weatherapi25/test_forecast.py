import unittest
import json
from datetime import datetime
from pyowm.weatherapi25.location import Location
from pyowm.weatherapi25.weather import Weather
from pyowm.weatherapi25.forecast import Forecast
from pyowm.commons.exceptions import APIResponseError, ParseAPIResponseError
from pyowm.utils.formatting import UTC
from tests.unit.weatherapi25.json_test_responses import (
    THREE_HOURS_FORECAST_JSON, FORECAST_NOT_FOUND_JSON,
    INTERNAL_SERVER_ERROR_JSON, FORECAST_MALFORMED_JSON)


class TestForecast(unittest.TestCase):
    __test_reception_time = 1234567
    __test_iso_reception_time = "1970-01-15 06:56:07+00"
    __test_date_reception_time = datetime.strptime(__test_iso_reception_time,
                                                   '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
    __test_location = Location('test', 12.3, 43.7, 987, 'IT')
    __test_weathers = [Weather(1378459200, 1378496400, 1378449600, 67,
                               {"all": 20}, {"all": 0}, {"deg": 252.002, "speed": 1.100}, 57,
                               {"press": 1030.119, "sea_level": 1038.589},
                               {"temp": 294.199, "temp_kf": -1.899, "temp_max": 296.098,
                                "temp_min": 294.199
                                },
                               "Clouds", "Overcast clouds", 804, "04d", 1000, 300.0, 298.0, 296.0),
                       Weather(1378459690, 1378496480, 1378449510, 23, {"all": 10},
                               {"all": 0}, {"deg": 103.4, "speed": 4.2}, 12,
                               {"press": 1070.119, "sea_level": 1078.589},
                               {"temp": 297.199, "temp_kf": -1.899, "temp_max": 299.0,
                                "temp_min": 295.6
                                },
                               "Clear", "Sky is clear", 804, "02d", 1000, 300.0, 298.0, 296.0)
                       ]
    __test_n_weathers = len(__test_weathers)
    __test_instance = Forecast("daily", __test_reception_time, __test_location,
                               __test_weathers)
    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'
    __bad_json_2 = '{ "city": {"id": 2643743,' \
                   '"name": "London","coord": {"lon": -0.12574,"lat": 51.50853},"country": ' \
                   '"GB","population": 1000000} }'
    __no_items_found_json = '{"count": "0", "city": {"id": 2643743,' \
                            '"name": "London","coord": {"lon": -0.12574,"lat": 51.50853},"country": ' \
                            '"GB","population": 1000000} }'

    FORECAST_JSON_DUMP = '{"reception_time": 1234567, "interval": "daily", ' \
                         '"location": {"country": "IT", "name": "test", ' \
                         '"coordinates": {"lat": 43.7, "lon": 12.3}, "ID": 987}, ' \
                         '"weathers": [{"status": "Clouds", ' \
                         '"visibility_distance": 1000, "humidity": 57, "clouds": 67,' \
                         ' "temperature": {"temp_kf": -1.899, "temp_max": 296.098, ' \
                         '"temp": 294.199, "temp_min": 294.199}, "dewpoint": 300.0,' \
                         ' "snow": {"all": 0}, "detailed_status": "Overcast clouds",' \
                         ' "reference_time": 1378459200, "weather_code": 804, ' \
                         '"humidex": 298.0, "rain": {"all": 20}, ' \
                         '"sunset_time": 1378496400, "pressure": {"press": 1030.119,' \
                         ' "sea_level": 1038.589}, "sunrise_time": 1378449600, ' \
                         '"heat_index": 296.0, "weather_icon_name": "04d", "wind": ' \
                         '{"speed": 1.1, "deg": 252.002}, "utc_offset": null, "uvi": null}, {"status": "Clear", ' \
                         '"visibility_distance": 1000, "humidity": 12, ' \
                         '"clouds": 23, "temperature": {"temp_kf": -1.899, ' \
                         '"temp_max": 299.0, "temp": 297.199, "temp_min": 295.6}, ' \
                         '"dewpoint": 300.0, "snow": {"all": 0}, "detailed_status": ' \
                         '"Sky is clear", "reference_time": 1378459690, ' \
                         '"weather_code": 804, "humidex": 298.0, "rain": {"all": 10},' \
                         ' "sunset_time": 1378496480, "pressure": ' \
                         '{"press": 1070.119, "sea_level": 1078.589}, ' \
                         '"sunrise_time": 1378449510, "heat_index": 296.0, ' \
                         '"weather_icon_name": "02d", "wind": {"speed": 4.2, ' \
                         '"deg": 103.4}, "utc_offset": null, "uvi": null}]}'

    def test_actualize(self):
        weathers = [Weather(1378459200, 1378496400, 1378449600, 67,
                            {"all": 20}, {"all": 0}, {"deg": 252.002, "speed": 1.100}, 57,
                            {"press": 1030.119, "sea_level": 1038.589},
                            {"temp": 294.199, "temp_kf": -1.899, "temp_max": 296.098,
                             "temp_min": 294.199
                             },
                            "Clouds", "Overcast clouds", 804, "04d", 1000, 300.0, 298.0, 296.0),
                    # will this time ever be reached?
                    Weather(9999999999, 1378496480, 1378449510, 23, {"all": 10},
                            {"all": 0}, {"deg": 103.4, "speed": 4.2}, 12,
                            {"press": 1070.119, "sea_level": 1078.589},
                            {"temp": 297.199, "temp_kf": -1.899, "temp_max": 299.0,
                             "temp_min": 295.6
                             },
                            "Clear", "Sky is clear", 804, "02d", 1000, 300.0, 298.0, 296.0)
                    ]
        f = Forecast("daily", self.__test_reception_time, self.__test_location,
                     weathers)
        self.assertEqual(2, len(f))
        f.actualize()
        self.assertEqual(1, len(f))

    def test_init_fails_when_reception_time_is_negative(self):
        self.assertRaises(ValueError, Forecast, "3h", -1234567,
                          self.__test_location, self.__test_weathers)

    def test_get(self):
        index = 1
        self.assertEqual(self.__test_weathers[index],
                         self.__test_instance.get(index))

    def test_getters_return_expected_3h_data(self):
        """
        Test either for "3h" forecast and "daily" ones
        """
        instance = Forecast("3h", self.__test_reception_time,
                            self.__test_location, self.__test_weathers)
        self.assertEqual(instance.interval, "3h")
        self.assertEqual(instance.reception_time(),
                         self.__test_reception_time)
        self.assertEqual(instance.location, self.__test_location)
        self.assertEqual(instance.weathers, self.__test_weathers)

    def test_getters_return_expected_daily_data(self):
        instance = Forecast("daily", self.__test_reception_time,
                            self.__test_location, self.__test_weathers)
        self.assertEqual(instance.interval, "daily")
        self.assertEqual(instance.reception_time(),
                         self.__test_reception_time)
        self.assertEqual(instance.location, self.__test_location)
        self.assertEqual(instance.weathers, self.__test_weathers)

    def test_returning_different_formats_for_reception_time(self):
        instance = self.__test_instance
        self.assertEqual(instance.reception_time(timeformat='iso'),
                         self.__test_iso_reception_time)
        self.assertEqual(instance.reception_time(timeformat='unix'),
                         self.__test_reception_time)
        self.assertEqual(instance.reception_time(timeformat='date'),
                         self.__test_date_reception_time)

    def test__iter__(self):
        instance = self.__test_instance
        counter = 0
        for weather in instance:
            self.assertTrue(isinstance(weather, Weather))
            counter += 1
        self.assertEqual(len(instance.weathers), counter)

    def test__len__(self):
        self.assertEqual(len(self.__test_instance), len(self.__test_weathers))

    def test_from_dict(self):
        result = self.__test_instance.from_dict(json.loads(THREE_HOURS_FORECAST_JSON))
        self.assertTrue(result is not None)
        self.assertTrue(result.reception_time() is not None)
        self.assertFalse(result.interval is not None)
        loc = result.location
        self.assertTrue(loc is not None)
        self.assertTrue(all(v is not None for v in loc.__dict__.values()))
        self.assertTrue(isinstance(result.weathers, list))
        for weather in result:
            self.assertTrue(weather is not None)

    def test_from_dict_fails_when_JSON_data_is_None(self):
        with self.assertRaises(ParseAPIResponseError):
            Forecast.from_dict(None)

    def test_from_dict_with_malformed_JSON_data(self):
        with self.assertRaises(ParseAPIResponseError):
            Forecast.from_dict(json.loads(self.__bad_json))
        with self.assertRaises(ParseAPIResponseError):
            Forecast.from_dict(json.loads(self.__bad_json_2))
        with self.assertRaises(ParseAPIResponseError):
            Forecast.from_dict(json.loads(FORECAST_MALFORMED_JSON))

    def test_from_dict_when_no_results(self):
        result = Forecast.from_dict(json.loads(FORECAST_NOT_FOUND_JSON))
        self.assertFalse(result is None)
        self.assertEqual(0, len(result))
        result = Forecast.from_dict(json.loads(self.__no_items_found_json))
        self.assertEqual(0, len(result))

    def test_from_dict_when_server_error(self):
        with self.assertRaises(APIResponseError):
            Forecast.from_dict(json.loads(INTERNAL_SERVER_ERROR_JSON))

    def test_to_dict(self):
        expected = json.loads(self.FORECAST_JSON_DUMP)
        result = self.__test_instance.to_dict()
        self.assertEqual(expected, result)

    def test__repr(self):
        print(self.__test_instance)