#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest

from pyowm.commons.exceptions import ParseAPIResponseError, APIResponseError
from pyowm.utils import geo
from pyowm.weatherapi25.one_call import OneCall
from pyowm.weatherapi25.weather import Weather


class TestWeather(unittest.TestCase):

    def test_one_call_from_dict(self):
        result = OneCall.from_dict(self.__test_data_bozen)
        self.assertTrue(isinstance(result, OneCall))
        self.assertEqual(46.49, result.lat)
        self.assertEqual(11.33, result.lon)
        self.assertEqual("Europe/Rome", result.timezone)
        self.assertTrue(isinstance(result.current, Weather))
        self.assertEqual(1587744158, result.current.reference_time())
        self.assertEqual(48, len(result.forecast_hourly))
        dt_hourly = 1587744000
        for i, weather in enumerate(result.forecast_hourly):
            self.assertTrue(isinstance(weather, Weather), f"entry {i} of forecast_hourly is invalid")
            self.assertEqual(dt_hourly, weather.reference_time())
            dt_hourly += 3600
        self.assertEqual(8, len(result.forecast_daily))
        dt_daily = 1587726000
        for i, weather in enumerate(result.forecast_daily):
            self.assertTrue(isinstance(weather, Weather), f"entry {i} of forecast_hourly is invalid")
            self.assertEqual(dt_daily, weather.reference_time())
            dt_daily += 86400

    def test_one_call_historical_from_dict(self):
        result = OneCall.from_dict(self.__test_data_hostorical_bozen)
        self.assertTrue(isinstance(result, OneCall))
        self.assertEqual(46.49, result.lat)
        self.assertEqual(11.33, result.lon)
        self.assertEqual("Europe/Rome", result.timezone)
        self.assertTrue(isinstance(result.current, Weather))
        self.assertEqual(1587686400, result.current.reference_time())
        self.assertEqual(11, len(result.forecast_hourly))
        dt_hourly = 1587686400
        for i, weather in enumerate(result.forecast_hourly):
            self.assertTrue(isinstance(weather, Weather), f"entry {i} of forecast_hourly is invalid")
            self.assertEqual(dt_hourly, weather.reference_time())
            dt_hourly += 3600
        self.assertIsNone(result.forecast_daily)

    def test_one_call_current_none(self):
        self.assertRaises(ValueError, lambda: OneCall(46.49, 11.33, None, None, None, None))

    def test_one_call_from_dict_none(self):
        self.assertRaises(ParseAPIResponseError, lambda: OneCall.from_dict(None))

    def test_one_call_from_dict_error_400(self):
        data = {
            "cod": "400",
            "message": "Nothing to geocode"
        }
        self.assertRaises(APIResponseError, lambda: OneCall.from_dict(data))

    def test_one_call_from_dict_error_404(self):
        data = {
            "cod": "404",
            "message": "Not found"
        }
        self.assertIsNone(OneCall.from_dict(data))

    def test_one_call_from_dict_error_429(self):
        data = {
            "cod": "429",
            "message": "Your account is temporary blocked due to exceeding of requests limitation "
                       "of your subscription type. Please choose the proper subscription "
                       "http://openweathermap.org/price"
        }
        self.assertRaises(APIResponseError, lambda: OneCall.from_dict(data))

    def test_one_call_from_dict_when_other_errors(self):
        data = {
            "cod": "413",
            "message": "entity too large"
        }
        self.assertRaises(APIResponseError, lambda: OneCall.from_dict(data))

    def test_one_call_from_dict_current_missing(self):
        data={
        "lat": 46.49,
        "lon": 11.33,
        "timezone": "Europe/Rome"
        }
        self.assertRaises(ParseAPIResponseError, lambda: OneCall.from_dict(data))

    def test_to_geopoint(self):
        instance = OneCall.from_dict(self.__test_data_bozen)
        result_1 = instance.to_geopoint()
        self.assertTrue(isinstance(result_1, geo.Point))
        expected_geojson = json.dumps({
            "coordinates": [11.33, 46.49],
            "type": "Point"
        })
        self.assertEqual(sorted(expected_geojson),
                         sorted(result_1.geojson()))

        instance.lat = None
        self.assertIsNone(instance.to_geopoint())

        instance.lon = None
        self.assertIsNone(instance.to_geopoint())

    __test_data_bozen = {
        "lat": 46.49,
        "lon": 11.33,
        "timezone": "Europe/Rome",
        "current": {
            "dt": 1587744158,
            "sunrise": 1587701469,
            "sunset": 1587752042,
            "temp": 295.34,
            "feels_like": 291.46,
            "pressure": 1008,
            "humidity": 22,
            "dew_point": 272.7,
            "uvi": 6.63,
            "clouds": 20,
            "visibility": 10000,
            "wind_speed": 2.6,
            "wind_deg": 170,
            "weather": [
                {
                    "id": 801,
                    "main": "Clouds",
                    "description": "few clouds",
                    "icon": "02d"
                }
            ]
        },
        "hourly": [
            {
                "dt": 1587744000,
                "temp": 295.34,
                "feels_like": 291.77,
                "pressure": 1008,
                "humidity": 22,
                "dew_point": 272.7,
                "clouds": 20,
                "wind_speed": 2.15,
                "wind_deg": 217,
                "weather": [
                    {
                        "id": 801,
                        "main": "Clouds",
                        "description": "few clouds",
                        "icon": "02d"
                    }
                ]
            },
            {
                "dt": 1587747600,
                "temp": 292.9,
                "feels_like": 290.43,
                "pressure": 1009,
                "humidity": 40,
                "dew_point": 278.93,
                "clouds": 59,
                "wind_speed": 2.14,
                "wind_deg": 210,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "rain": {
                    "1h": 0.14
                }
            },
            {
                "dt": 1587751200,
                "temp": 289.8,
                "feels_like": 288.13,
                "pressure": 1010,
                "humidity": 54,
                "dew_point": 280.46,
                "clouds": 82,
                "wind_speed": 1.48,
                "wind_deg": 203,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "rain": {
                    "1h": 0.2
                }
            },
            {
                "dt": 1587754800,
                "temp": 287.81,
                "feels_like": 286.87,
                "pressure": 1012,
                "humidity": 61,
                "dew_point": 280.38,
                "clouds": 95,
                "wind_speed": 0.41,
                "wind_deg": 210,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04n"
                    }
                ]
            },
            {
                "dt": 1587758400,
                "temp": 287.33,
                "feels_like": 286.14,
                "pressure": 1012,
                "humidity": 61,
                "dew_point": 279.93,
                "clouds": 99,
                "wind_speed": 0.63,
                "wind_deg": 19,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04n"
                    }
                ]
            },
            {
                "dt": 1587762000,
                "temp": 286.76,
                "feels_like": 285.17,
                "pressure": 1012,
                "humidity": 60,
                "dew_point": 280.39,
                "clouds": 100,
                "wind_speed": 0.95,
                "wind_deg": 17,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04n"
                    }
                ]
            },
            {
                "dt": 1587765600,
                "temp": 286.09,
                "feels_like": 284.28,
                "pressure": 1013,
                "humidity": 60,
                "dew_point": 279.66,
                "clouds": 100,
                "wind_speed": 1.08,
                "wind_deg": 20,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04n"
                    }
                ]
            },
            {
                "dt": 1587769200,
                "temp": 285.37,
                "feels_like": 283.34,
                "pressure": 1013,
                "humidity": 60,
                "dew_point": 278.94,
                "clouds": 93,
                "wind_speed": 1.21,
                "wind_deg": 15,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04n"
                    }
                ]
            },
            {
                "dt": 1587772800,
                "temp": 284.85,
                "feels_like": 282.67,
                "pressure": 1013,
                "humidity": 59,
                "dew_point": 278.39,
                "clouds": 85,
                "wind_speed": 1.22,
                "wind_deg": 14,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04n"
                    }
                ]
            },
            {
                "dt": 1587776400,
                "temp": 284.48,
                "feels_like": 282.22,
                "pressure": 1012,
                "humidity": 59,
                "dew_point": 277.99,
                "clouds": 69,
                "wind_speed": 1.24,
                "wind_deg": 15,
                "weather": [
                    {
                        "id": 803,
                        "main": "Clouds",
                        "description": "broken clouds",
                        "icon": "04n"
                    }
                ]
            },
            {
                "dt": 1587780000,
                "temp": 284.17,
                "feels_like": 281.84,
                "pressure": 1011,
                "humidity": 59,
                "dew_point": 277.74,
                "clouds": 81,
                "wind_speed": 1.27,
                "wind_deg": 16,
                "weather": [
                    {
                        "id": 803,
                        "main": "Clouds",
                        "description": "broken clouds",
                        "icon": "04n"
                    }
                ]
            },
            {
                "dt": 1587783600,
                "temp": 283.85,
                "feels_like": 281.48,
                "pressure": 1011,
                "humidity": 59,
                "dew_point": 277.4,
                "clouds": 86,
                "wind_speed": 1.24,
                "wind_deg": 16,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04n"
                    }
                ]
            },
            {
                "dt": 1587787200,
                "temp": 283.66,
                "feels_like": 281.32,
                "pressure": 1011,
                "humidity": 59,
                "dew_point": 277.13,
                "clouds": 89,
                "wind_speed": 1.16,
                "wind_deg": 16,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04n"
                    }
                ]
            },
            {
                "dt": 1587790800,
                "temp": 284.48,
                "feels_like": 282.14,
                "pressure": 1011,
                "humidity": 57,
                "dew_point": 277.43,
                "clouds": 91,
                "wind_speed": 1.23,
                "wind_deg": 13,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04d"
                    }
                ]
            },
            {
                "dt": 1587794400,
                "temp": 286.9,
                "feels_like": 285.07,
                "pressure": 1011,
                "humidity": 51,
                "dew_point": 278.19,
                "clouds": 93,
                "wind_speed": 0.68,
                "wind_deg": 9,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04d"
                    }
                ]
            },
            {
                "dt": 1587798000,
                "temp": 290.19,
                "feels_like": 288.61,
                "pressure": 1010,
                "humidity": 42,
                "dew_point": 278.4,
                "clouds": 96,
                "wind_speed": 0.38,
                "wind_deg": 4,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04d"
                    }
                ]
            },
            {
                "dt": 1587801600,
                "temp": 293.17,
                "feels_like": 291.79,
                "pressure": 1010,
                "humidity": 35,
                "dew_point": 278.43,
                "clouds": 88,
                "wind_speed": 0.11,
                "wind_deg": 160,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04d"
                    }
                ]
            },
            {
                "dt": 1587805200,
                "temp": 295.62,
                "feels_like": 294.06,
                "pressure": 1009,
                "humidity": 30,
                "dew_point": 278.19,
                "clouds": 75,
                "wind_speed": 0.35,
                "wind_deg": 218,
                "weather": [
                    {
                        "id": 803,
                        "main": "Clouds",
                        "description": "broken clouds",
                        "icon": "04d"
                    }
                ]
            },
            {
                "dt": 1587808800,
                "temp": 297.42,
                "feels_like": 295.72,
                "pressure": 1009,
                "humidity": 27,
                "dew_point": 278.29,
                "clouds": 68,
                "wind_speed": 0.56,
                "wind_deg": 225,
                "weather": [
                    {
                        "id": 803,
                        "main": "Clouds",
                        "description": "broken clouds",
                        "icon": "04d"
                    }
                ]
            },
            {
                "dt": 1587812400,
                "temp": 298.78,
                "feels_like": 296.92,
                "pressure": 1008,
                "humidity": 24,
                "dew_point": 278.17,
                "clouds": 57,
                "wind_speed": 0.65,
                "wind_deg": 235,
                "weather": [
                    {
                        "id": 803,
                        "main": "Clouds",
                        "description": "broken clouds",
                        "icon": "04d"
                    }
                ]
            },
            {
                "dt": 1587816000,
                "temp": 299.23,
                "feels_like": 297.38,
                "pressure": 1008,
                "humidity": 25,
                "dew_point": 278.73,
                "clouds": 50,
                "wind_speed": 0.89,
                "wind_deg": 293,
                "weather": [
                    {
                        "id": 802,
                        "main": "Clouds",
                        "description": "scattered clouds",
                        "icon": "03d"
                    }
                ]
            },
            {
                "dt": 1587819600,
                "temp": 298.5,
                "feels_like": 296.01,
                "pressure": 1008,
                "humidity": 25,
                "dew_point": 278.38,
                "clouds": 27,
                "wind_speed": 1.64,
                "wind_deg": 310,
                "weather": [
                    {
                        "id": 802,
                        "main": "Clouds",
                        "description": "scattered clouds",
                        "icon": "03d"
                    }
                ]
            },
            {
                "dt": 1587823200,
                "temp": 297.55,
                "feels_like": 295.26,
                "pressure": 1007,
                "humidity": 27,
                "dew_point": 278.6,
                "clouds": 44,
                "wind_speed": 1.44,
                "wind_deg": 307,
                "weather": [
                    {
                        "id": 802,
                        "main": "Clouds",
                        "description": "scattered clouds",
                        "icon": "03d"
                    }
                ]
            },
            {
                "dt": 1587826800,
                "temp": 297.67,
                "feels_like": 295.92,
                "pressure": 1006,
                "humidity": 28,
                "dew_point": 279.18,
                "clouds": 47,
                "wind_speed": 0.84,
                "wind_deg": 294,
                "weather": [
                    {
                        "id": 802,
                        "main": "Clouds",
                        "description": "scattered clouds",
                        "icon": "03d"
                    }
                ]
            },
            {
                "dt": 1587830400,
                "temp": 296.42,
                "feels_like": 294.46,
                "pressure": 1006,
                "humidity": 30,
                "dew_point": 279.08,
                "clouds": 44,
                "wind_speed": 1.11,
                "wind_deg": 225,
                "weather": [
                    {
                        "id": 802,
                        "main": "Clouds",
                        "description": "scattered clouds",
                        "icon": "03d"
                    }
                ]
            },
            {
                "dt": 1587834000,
                "temp": 293.55,
                "feels_like": 291.41,
                "pressure": 1006,
                "humidity": 44,
                "dew_point": 281.96,
                "clouds": 45,
                "wind_speed": 2.3,
                "wind_deg": 198,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "rain": {
                    "1h": 0.23
                }
            },
            {
                "dt": 1587837600,
                "temp": 290.03,
                "feels_like": 288.79,
                "pressure": 1007,
                "humidity": 58,
                "dew_point": 282.84,
                "clouds": 46,
                "wind_speed": 1.3,
                "wind_deg": 194,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "rain": {
                    "1h": 0.79
                }
            },
            {
                "dt": 1587841200,
                "temp": 287.84,
                "feels_like": 287.2,
                "pressure": 1007,
                "humidity": 63,
                "dew_point": 282,
                "clouds": 7,
                "wind_speed": 0.16,
                "wind_deg": 101,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10n"
                    }
                ],
                "rain": {
                    "1h": 0.73
                }
            },
            {
                "dt": 1587844800,
                "temp": 287.29,
                "feels_like": 286.27,
                "pressure": 1008,
                "humidity": 63,
                "dew_point": 281.64,
                "clouds": 23,
                "wind_speed": 0.52,
                "wind_deg": 59,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10n"
                    }
                ],
                "rain": {
                    "1h": 0.63
                }
            },
            {
                "dt": 1587848400,
                "temp": 286.83,
                "feels_like": 285.94,
                "pressure": 1008,
                "humidity": 65,
                "dew_point": 281.54,
                "clouds": 27,
                "wind_speed": 0.35,
                "wind_deg": 36,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10n"
                    }
                ],
                "rain": {
                    "1h": 0.68
                }
            },
            {
                "dt": 1587852000,
                "temp": 286.7,
                "feels_like": 285.69,
                "pressure": 1008,
                "humidity": 65,
                "dew_point": 281.46,
                "clouds": 38,
                "wind_speed": 0.48,
                "wind_deg": 41,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10n"
                    }
                ],
                "rain": {
                    "1h": 0.41
                }
            },
            {
                "dt": 1587855600,
                "temp": 286.86,
                "feels_like": 286.06,
                "pressure": 1008,
                "humidity": 65,
                "dew_point": 281.67,
                "clouds": 46,
                "wind_speed": 0.22,
                "wind_deg": 10,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10n"
                    }
                ],
                "rain": {
                    "1h": 0.41
                }
            },
            {
                "dt": 1587859200,
                "temp": 287.07,
                "feels_like": 286.38,
                "pressure": 1008,
                "humidity": 66,
                "dew_point": 281.98,
                "clouds": 55,
                "wind_speed": 0.21,
                "wind_deg": 12,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10n"
                    }
                ],
                "rain": {
                    "1h": 0.51
                }
            },
            {
                "dt": 1587862800,
                "temp": 286.96,
                "feels_like": 286.25,
                "pressure": 1008,
                "humidity": 67,
                "dew_point": 282.07,
                "clouds": 100,
                "wind_speed": 0.28,
                "wind_deg": 37,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10n"
                    }
                ],
                "rain": {
                    "1h": 0.51
                }
            },
            {
                "dt": 1587866400,
                "temp": 287.12,
                "feels_like": 286.37,
                "pressure": 1008,
                "humidity": 67,
                "dew_point": 282.22,
                "clouds": 99,
                "wind_speed": 0.38,
                "wind_deg": 1,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10n"
                    }
                ],
                "rain": {
                    "1h": 0.23
                }
            },
            {
                "dt": 1587870000,
                "temp": 287,
                "feels_like": 286.37,
                "pressure": 1008,
                "humidity": 67,
                "dew_point": 282.16,
                "clouds": 99,
                "wind_speed": 0.18,
                "wind_deg": 353,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10n"
                    }
                ],
                "rain": {
                    "1h": 0.26
                }
            },
            {
                "dt": 1587873600,
                "temp": 286.92,
                "feels_like": 286.21,
                "pressure": 1007,
                "humidity": 67,
                "dew_point": 282.04,
                "clouds": 99,
                "wind_speed": 0.27,
                "wind_deg": 321,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10n"
                    }
                ],
                "rain": {
                    "1h": 0.15
                }
            },
            {
                "dt": 1587877200,
                "temp": 287.13,
                "feels_like": 286.54,
                "pressure": 1008,
                "humidity": 66,
                "dew_point": 282.12,
                "clouds": 99,
                "wind_speed": 0.08,
                "wind_deg": 338,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "rain": {
                    "1h": 0.15
                }
            },
            {
                "dt": 1587880800,
                "temp": 287.44,
                "feels_like": 286.83,
                "pressure": 1008,
                "humidity": 66,
                "dew_point": 282.43,
                "clouds": 100,
                "wind_speed": 0.21,
                "wind_deg": 193,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "rain": {
                    "1h": 0.13
                }
            },
            {
                "dt": 1587884400,
                "temp": 287.34,
                "feels_like": 286.57,
                "pressure": 1008,
                "humidity": 68,
                "dew_point": 282.69,
                "clouds": 100,
                "wind_speed": 0.57,
                "wind_deg": 218,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "rain": {
                    "1h": 0.18
                }
            },
            {
                "dt": 1587888000,
                "temp": 287.59,
                "feels_like": 286.83,
                "pressure": 1008,
                "humidity": 67,
                "dew_point": 282.82,
                "clouds": 100,
                "wind_speed": 0.55,
                "wind_deg": 217,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "rain": {
                    "1h": 0.37
                }
            },
            {
                "dt": 1587891600,
                "temp": 287.45,
                "feels_like": 286.84,
                "pressure": 1008,
                "humidity": 68,
                "dew_point": 282.8,
                "clouds": 100,
                "wind_speed": 0.37,
                "wind_deg": 224,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "rain": {
                    "1h": 0.78
                }
            },
            {
                "dt": 1587895200,
                "temp": 287.4,
                "feels_like": 286.84,
                "pressure": 1008,
                "humidity": 68,
                "dew_point": 282.82,
                "clouds": 100,
                "wind_speed": 0.28,
                "wind_deg": 181,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "rain": {
                    "1h": 0.7
                }
            },
            {
                "dt": 1587898800,
                "temp": 287.8,
                "feels_like": 286.97,
                "pressure": 1008,
                "humidity": 67,
                "dew_point": 282.88,
                "clouds": 100,
                "wind_speed": 0.73,
                "wind_deg": 170,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "rain": {
                    "1h": 0.25
                }
            },
            {
                "dt": 1587902400,
                "temp": 289.06,
                "feels_like": 287.59,
                "pressure": 1008,
                "humidity": 62,
                "dew_point": 283.04,
                "clouds": 100,
                "wind_speed": 1.66,
                "wind_deg": 197,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04d"
                    }
                ]
            },
            {
                "dt": 1587906000,
                "temp": 289.83,
                "feels_like": 288.06,
                "pressure": 1008,
                "humidity": 59,
                "dew_point": 283.1,
                "clouds": 99,
                "wind_speed": 2.09,
                "wind_deg": 205,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04d"
                    }
                ]
            },
            {
                "dt": 1587909600,
                "temp": 290.69,
                "feels_like": 288.92,
                "pressure": 1008,
                "humidity": 55,
                "dew_point": 282.77,
                "clouds": 99,
                "wind_speed": 2,
                "wind_deg": 206,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "rain": {
                    "1h": 0.16
                }
            },
            {
                "dt": 1587913200,
                "temp": 290.85,
                "feels_like": 289.01,
                "pressure": 1008,
                "humidity": 53,
                "dew_point": 282.36,
                "clouds": 99,
                "wind_speed": 1.96,
                "wind_deg": 202,
                "weather": [
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04d"
                    }
                ]
            }
        ],
        "daily": [
            {
                "dt": 1587726000,
                "sunrise": 1587701469,
                "sunset": 1587752042,
                "temp": {
                    "day": 295.34,
                    "min": 284.76,
                    "max": 295.34,
                    "night": 284.76,
                    "eve": 289.14,
                    "morn": 295.34
                },
                "feels_like": {
                    "day": 292.2,
                    "night": 282.56,
                    "eve": 287.28,
                    "morn": 292.2
                },
                "pressure": 1008,
                "humidity": 22,
                "dew_point": 272.7,
                "wind_speed": 1.54,
                "wind_deg": 224,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "clouds": 20,
                "rain": 0.39,
                "uvi": 6.63
            },
            {
                "dt": 1587812400,
                "sunrise": 1587787768,
                "sunset": 1587838523,
                "temp": {
                    "day": 299.23,
                    "min": 286.83,
                    "max": 299.23,
                    "night": 287.07,
                    "eve": 290.03,
                    "morn": 286.9
                },
                "feels_like": {
                    "day": 297.38,
                    "night": 286.38,
                    "eve": 288.79,
                    "morn": 285.07
                },
                "pressure": 1008,
                "humidity": 25,
                "dew_point": 278.73,
                "wind_speed": 0.89,
                "wind_deg": 293,
                "weather": [
                    {
                        "id": 501,
                        "main": "Rain",
                        "description": "moderate rain",
                        "icon": "10d"
                    }
                ],
                "clouds": 50,
                "rain": 4.47,
                "uvi": 6.33
            },
            {
                "dt": 1587898800,
                "sunrise": 1587874069,
                "sunset": 1587925004,
                "temp": {
                    "day": 289.06,
                    "min": 286.78,
                    "max": 290.85,
                    "night": 286.78,
                    "eve": 287.8,
                    "morn": 287.44
                },
                "feels_like": {
                    "day": 287.59,
                    "night": 286.17,
                    "eve": 286.96,
                    "morn": 286.83
                },
                "pressure": 1008,
                "humidity": 62,
                "dew_point": 283.04,
                "wind_speed": 1.66,
                "wind_deg": 197,
                "weather": [
                    {
                        "id": 501,
                        "main": "Rain",
                        "description": "moderate rain",
                        "icon": "10d"
                    }
                ],
                "clouds": 100,
                "rain": 7.17,
                "uvi": 6.19
            },
            {
                "dt": 1587985200,
                "sunrise": 1587960371,
                "sunset": 1588011485,
                "temp": {
                    "day": 295.01,
                    "min": 286.95,
                    "max": 295.01,
                    "night": 287.33,
                    "eve": 288.71,
                    "morn": 286.95
                },
                "feels_like": {
                    "day": 292.5,
                    "night": 286.67,
                    "eve": 287.47,
                    "morn": 286.29
                },
                "pressure": 1010,
                "humidity": 41,
                "dew_point": 282.21,
                "wind_speed": 2.92,
                "wind_deg": 209,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "clouds": 48,
                "rain": 2.64,
                "uvi": 6.42
            },
            {
                "dt": 1588071600,
                "sunrise": 1588046674,
                "sunset": 1588097965,
                "temp": {
                    "day": 291.76,
                    "min": 285.84,
                    "max": 291.76,
                    "night": 285.84,
                    "eve": 287.71,
                    "morn": 287.12
                },
                "feels_like": {
                    "day": 289.89,
                    "night": 284.41,
                    "eve": 286.58,
                    "morn": 285.98
                },
                "pressure": 1007,
                "humidity": 54,
                "dew_point": 283.6,
                "wind_speed": 2.41,
                "wind_deg": 202,
                "weather": [
                    {
                        "id": 501,
                        "main": "Rain",
                        "description": "moderate rain",
                        "icon": "10d"
                    }
                ],
                "clouds": 99,
                "rain": 7.02,
                "uvi": 6.38
            },
            {
                "dt": 1588158000,
                "sunrise": 1588132979,
                "sunset": 1588184446,
                "temp": {
                    "day": 290.42,
                    "min": 285.39,
                    "max": 291.79,
                    "night": 285.39,
                    "eve": 287.32,
                    "morn": 286.38
                },
                "feels_like": {
                    "day": 288.24,
                    "night": 283.69,
                    "eve": 285.48,
                    "morn": 285.4
                },
                "pressure": 1005,
                "humidity": 54,
                "dew_point": 282.28,
                "wind_speed": 2.41,
                "wind_deg": 192,
                "weather": [
                    {
                        "id": 501,
                        "main": "Rain",
                        "description": "moderate rain",
                        "icon": "10d"
                    }
                ],
                "clouds": 87,
                "rain": 8.82,
                "uvi": 5.87
            },
            {
                "dt": 1588244400,
                "sunrise": 1588219284,
                "sunset": 1588270926,
                "temp": {
                    "day": 293.3,
                    "min": 281.05,
                    "max": 293.3,
                    "night": 281.05,
                    "eve": 283.77,
                    "morn": 285.22
                },
                "feels_like": {
                    "day": 290.94,
                    "night": 278.19,
                    "eve": 281.77,
                    "morn": 283.68
                },
                "pressure": 1004,
                "humidity": 35,
                "dew_point": 278.64,
                "wind_speed": 1.54,
                "wind_deg": 202,
                "weather": [
                    {
                        "id": 501,
                        "main": "Rain",
                        "description": "moderate rain",
                        "icon": "10d"
                    }
                ],
                "clouds": 98,
                "rain": 9,
                "uvi": 6.16
            },
            {
                "dt": 1588330800,
                "sunrise": 1588305591,
                "sunset": 1588357407,
                "temp": {
                    "day": 294.49,
                    "min": 280.76,
                    "max": 294.49,
                    "night": 280.76,
                    "eve": 286.2,
                    "morn": 283.2
                },
                "feels_like": {
                    "day": 292.05,
                    "night": 277.61,
                    "eve": 283.86,
                    "morn": 280.84
                },
                "pressure": 1009,
                "humidity": 27,
                "dew_point": 275.96,
                "wind_speed": 1,
                "wind_deg": 207,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d"
                    }
                ],
                "clouds": 31,
                "rain": 1.92,
                "uvi": 6.93
            }
        ]
    }

    __test_data_hostorical_bozen = {
        "lat": 46.49,
        "lon": 11.33,
        "timezone": "Europe/Rome",
        "current": {
            "dt": 1587686400,
            "sunrise": 1587701469,
            "sunset": 1587752042,
            "temp": 278.15,
            "feels_like": 275.45,
            "pressure": 1017,
            "humidity": 82,
            "dew_point": 275.34,
            "uvi": 7.36,
            "clouds": 0,
            "wind_speed": 1.51,
            "wind_deg": 106,
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01n"
                }
            ]
        },
        "hourly": [
            {
                "dt": 1587686400,
                "sunrise": 1587701469,
                "sunset": 1587752042,
                "temp": 278.15,
                "feels_like": 275.45,
                "pressure": 1017,
                "humidity": 82,
                "dew_point": 275.34,
                "clouds": 0,
                "wind_speed": 1.51,
                "wind_deg": 106,
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01n"
                    }
                ]
            },
            {
                "dt": 1587690000,
                "sunrise": 1587701469,
                "sunset": 1587752042,
                "temp": 277.79,
                "feels_like": 274.21,
                "pressure": 1016,
                "humidity": 71,
                "dew_point": 273.01,
                "clouds": 0,
                "wind_speed": 2.24,
                "wind_deg": 57,
                "wind_gust": 3.13,
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01n"
                    }
                ]
            },
            {
                "dt": 1587693600,
                "sunrise": 1587701469,
                "sunset": 1587752042,
                "temp": 277.95,
                "feels_like": 275.39,
                "pressure": 1016,
                "humidity": 86,
                "dew_point": 275.81,
                "clouds": 0,
                "wind_speed": 1.43,
                "wind_deg": 77,
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01n"
                    }
                ]
            },
            {
                "dt": 1587697200,
                "sunrise": 1587701469,
                "sunset": 1587752042,
                "temp": 277.66,
                "feels_like": 274.23,
                "pressure": 1005,
                "humidity": 86,
                "dew_point": 275.53,
                "clouds": 5,
                "visibility": 10000,
                "wind_speed": 2.6,
                "wind_deg": 350,
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01n"
                    }
                ]
            },
            {
                "dt": 1587700800,
                "sunrise": 1587701469,
                "sunset": 1587752042,
                "temp": 277.66,
                "feels_like": 275.21,
                "pressure": 1006,
                "humidity": 81,
                "dew_point": 274.69,
                "clouds": 0,
                "visibility": 10000,
                "wind_speed": 1,
                "wind_deg": 0,
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01n"
                    }
                ]
            },
            {
                "dt": 1587704400,
                "sunrise": 1587701469,
                "sunset": 1587752042,
                "temp": 278.57,
                "feels_like": 276.27,
                "pressure": 1008,
                "humidity": 81,
                "dew_point": 275.58,
                "clouds": 0,
                "visibility": 10000,
                "wind_speed": 1,
                "wind_deg": 0,
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01d"
                    }
                ]
            },
            {
                "dt": 1587708000,
                "sunrise": 1587701469,
                "sunset": 1587752042,
                "temp": 280.47,
                "feels_like": 278.85,
                "pressure": 1009,
                "humidity": 81,
                "dew_point": 277.43,
                "clouds": 0,
                "visibility": 10000,
                "wind_speed": 0.5,
                "wind_deg": 0,
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01d"
                    }
                ]
            },
            {
                "dt": 1587711600,
                "sunrise": 1587701469,
                "sunset": 1587752042,
                "temp": 281.18,
                "feels_like": 278.88,
                "pressure": 1003,
                "humidity": 58,
                "dew_point": 273.43,
                "clouds": 0,
                "visibility": 10000,
                "wind_speed": 0.5,
                "wind_deg": 0,
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01d"
                    }
                ]
            },
            {
                "dt": 1587715200,
                "sunrise": 1587701469,
                "sunset": 1587752042,
                "temp": 286.21,
                "feels_like": 283.69,
                "pressure": 1008,
                "humidity": 44,
                "dew_point": 274.25,
                "clouds": 7,
                "visibility": 10000,
                "wind_speed": 1,
                "wind_deg": 0,
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01d"
                    }
                ]
            },
            {
                "dt": 1587718800,
                "sunrise": 1587701469,
                "sunset": 1587752042,
                "temp": 288.22,
                "feels_like": 285.89,
                "pressure": 1005,
                "humidity": 42,
                "dew_point": 275.42,
                "clouds": 7,
                "visibility": 10000,
                "wind_speed": 1,
                "wind_deg": 0,
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01d"
                    }
                ]
            },
            {
                "dt": 1587722400,
                "sunrise": 1587701469,
                "sunset": 1587752042,
                "temp": 290.36,
                "feels_like": 287.86,
                "pressure": 1003,
                "humidity": 34,
                "dew_point": 274.38,
                "clouds": 20,
                "visibility": 10000,
                "wind_speed": 1,
                "wind_deg": 0,
                "weather": [
                    {
                        "id": 801,
                        "main": "Clouds",
                        "description": "few clouds",
                        "icon": "02d"
                    }
                ]
            }
        ]
    }
