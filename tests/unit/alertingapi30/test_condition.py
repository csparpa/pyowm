import unittest
from pyowm.alertapi30.condition import Condition
from pyowm.alertapi30.enums import WeatherParametersEnum, OperatorsEnum


class TestCondition(unittest.TestCase):

    def test_condition_fails_with_wrong_parameters(self):
        self.assertRaises(AssertionError, Condition,
                          None, OperatorsEnum.EQUAL, 67.8)
        self.assertRaises(AssertionError, Condition,
                          123, OperatorsEnum.EQUAL, 67.8)
        self.assertRaises(AssertionError, Condition,
                          WeatherParametersEnum.HUMIDITY, None, 67.8)
        self.assertRaises(AssertionError, Condition,
                          WeatherParametersEnum.HUMIDITY, 123, 67.8)
        self.assertRaises(AssertionError, Condition,
                          WeatherParametersEnum.HUMIDITY, OperatorsEnum.EQUAL, None)
        self.assertRaises(AssertionError, Condition,
                          WeatherParametersEnum.HUMIDITY, OperatorsEnum.EQUAL, 'string')
