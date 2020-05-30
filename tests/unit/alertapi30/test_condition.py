#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import pyowm.commons.exceptions
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

    def test_from_dict(self):
        expected = Condition(WeatherParametersEnum.TEMPERATURE, OperatorsEnum.GREATER_THAN, 78.6, id='123456')
        the_dict = dict(name='temp', expression='$gt',
                        amount=78.6, _id='123456')
        result = Condition.from_dict(the_dict)
        self.assertEqual(expected.weather_param, result.weather_param)
        self.assertEqual(expected.operator, result.operator)
        self.assertEqual(expected.amount, result.amount)
        self.assertEqual(expected.id, result.id)

        with self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError):
            Condition.from_dict(None)

        with self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError):
            Condition.from_dict(dict(nonexistent='key'))

    def test_to_dict(self):
        instance = Condition(WeatherParametersEnum.TEMPERATURE, OperatorsEnum.GREATER_THAN, 78.6, id='123456')
        result = instance.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual('123456', result['id'])
        self.assertEqual(WeatherParametersEnum.TEMPERATURE, result['weather_param'])
        self.assertEqual(OperatorsEnum.GREATER_THAN, result['operator'])
        self.assertEqual(78.6, result['amount'])

    def test_repr(self):
        print(Condition(WeatherParametersEnum.TEMPERATURE, OperatorsEnum.GREATER_THAN, 78.6, id='123456'))
