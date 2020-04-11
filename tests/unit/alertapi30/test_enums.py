import unittest

from pyowm.alertapi30.enums import AlertChannelsEnum, OperatorsEnum, WeatherParametersEnum


class TestAlertChannelsEnum(unittest.TestCase):
    def test_items(self):
        alert_channels_enum = AlertChannelsEnum()
        self.assertEqual(alert_channels_enum.items(),
                         [AlertChannelsEnum.OWM_API_POLLING])


class TestOperatorsEnum(unittest.TestCase):
    def test_items(self):
        operators_enum = OperatorsEnum()
        self.assertEqual(sorted(operators_enum.items()), sorted([operators_enum.GREATER_THAN,
                                                                 operators_enum.GREATER_THAN_EQUAL,
                                                                 operators_enum.LESS_THAN,
                                                                 operators_enum.LESS_THAN_EQUAL,
                                                                 operators_enum.EQUAL,
                                                                 operators_enum.NOT_EQUAL]))


class TestWeatherParametersEnum(unittest.TestCase):
    def test_item(self):
        weather_parameters_enum = WeatherParametersEnum()
        self.assertEqual(sorted(weather_parameters_enum.items()),
                         sorted([weather_parameters_enum.CLOUDS, weather_parameters_enum.HUMIDITY,
                                 weather_parameters_enum.PRESSURE, weather_parameters_enum.WIND_DIRECTION,
                                 weather_parameters_enum.WIND_SPEED, weather_parameters_enum.TEMPERATURE]))
