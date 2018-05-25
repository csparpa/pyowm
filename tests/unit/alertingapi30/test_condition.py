import unittest
from pyowm.alertingapi30.condition import Condition


class TestCondition(unittest.TestCase):

    def test_condition_fails_with_wrong_parameters(self):
        self.assertRaises(AssertionError, Condition,
                          123, 'EQUAL', 67.8)
        self.assertRaises(ValueError, Condition,
                          'NOT_ALLOWED', 'EQUAL', 67.8)
        self.assertRaises(AssertionError, Condition,
                          'HUMIDITY', 123, 67.8)
        self.assertRaises(ValueError, Condition,
                          'HUMIDITY', '$xyz', 67.8)
        self.assertRaises(AssertionError, Condition,
                          'HUMIDITY', 'EQUAL', None)
        self.assertRaises(AssertionError, Condition,
                          'HUMIDITY', 'EQUAL', 'string')

    def test_condition_parameter_case_is_not_significant(self):
        condition_1 = Condition('TEMPERATURE', 'LESS_THAN', 89.0)
        condition_2 = Condition('temperature', 'LESS_THAN', 89.0)
        self.assertEqual(condition_1.weather_param, condition_2.weather_param)
