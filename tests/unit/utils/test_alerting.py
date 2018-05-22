import unittest
from pyowm.utils import alerting


class TestCondition(unittest.TestCase):

    def test_condition_fails_with_wrong_parameters(self):
        self.assertRaises(AssertionError, alerting.Condition,
                          123, 'EQUAL', 67.8)
        self.assertRaises(ValueError, alerting.Condition,
                          'NOT_ALLOWED', 'EQUAL', 67.8)
        self.assertRaises(AssertionError, alerting.Condition,
                          'HUMIDITY', 123, 67.8)
        self.assertRaises(ValueError, alerting.Condition,
                          'HUMIDITY', '$xyz', 67.8)
        self.assertRaises(AssertionError, alerting.Condition,
                          'HUMIDITY', 'EQUAL', None)
        self.assertRaises(AssertionError, alerting.Condition,
                          'HUMIDITY', 'EQUAL', 'string')

    def test_condition_parameter_case_is_not_significant(self):
        condition_1 = alerting.Condition('TEMPERATURE', 'LESS_THAN', 89.0)
        condition_2 = alerting.Condition('temperature', 'LESS_THAN', 89.0)
        self.assertEqual(condition_1.weather_param, condition_2.weather_param)