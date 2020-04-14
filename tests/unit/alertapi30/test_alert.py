#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import unittest

import pyowm.commons.exceptions
from pyowm.alertapi30.alert import Alert, AlertChannel
from pyowm.alertapi30.condition import Condition


class TestAlert(unittest.TestCase):

    def test_alert_fails_with_wrong_parameters(self):

        self.assertRaises(AssertionError, Alert, None, 'trigger1', [dict(a=1, b=2), dict(c=3, d=4)],
                          dict(lon=53, lat=45))
        self.assertRaises(AssertionError, Alert, 123, 'trigger1', [dict(a=1, b=2), dict(c=3, d=4)],
                          dict(lon=53, lat=45))
        self.assertRaises(AssertionError, Alert, 'alert1', None, [dict(a=1, b=2), dict(c=3, d=4)],
                  dict(lon=53, lat=45))
        self.assertRaises(AssertionError, Alert, 'alert1', 1234, [dict(a=1, b=2), dict(c=3, d=4)],
                  dict(lon=53, lat=45))

        self.assertRaises(AssertionError, Alert, 'alert1', 'trigger', None,
                          dict(lon=53, lat=45))
        self.assertRaises(AssertionError, Alert, 'alert1', 'trigger', 'wrong-value',
                          dict(lon=53, lat=45))

        self.assertRaises(AssertionError, Alert, 'alert1', 'trigger', [dict(a=1, b=2), dict(c=3, d=4)], None)
        self.assertRaises(AssertionError, Alert, 'alert1', 'trigger', [dict(a=1, b=2), dict(c=3, d=4)], 'wrong-value')

        self.assertRaises(AssertionError, Alert, 'alert1', 'trigger', [dict(a=1, b=2), dict(c=3, d=4)],
                          dict(lon=53, lat=45), 'wrong-value')

    def test_alert_last_updated_is_none(self):
        alert = Alert('alert1', 'trigger1', [{
            "current_value": 263.576,
            "condition": Condition('humidity', 'LESS_THAN', 10)}],
                      {"lon": 37, "lat": 53})
        self.assertIsNone(alert.last_update)

    def test_from_dict(self):
        the_dict = {
         '_id': '5853dbe27416a400011b1b77',
         'conditions': [{'_id': '5853dbe27416a400011b1b78',
                         'condition': {'amount': 273, 'expression': '$lt', 'name': 'temp'},
                         'current_value': {'max': 258.62, 'min': 258.62}}],
         'coordinates': {'lat': '53', 'lon': '37'},
         'date': '2016-12-17T00:00:00.000Z',
         'last_update': '2016-12-16T11:19:46.352Z',
         'triggerId': '5852816a9aaacb00153134a3'}
        result = Alert.from_dict(the_dict)
        self.assertIsInstance(result, Alert)

        with self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError):
            Alert.from_dict(None)

        with self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError):
            Alert.from_dict(dict(nonexistent='key'))

        value_error_dict = copy.deepcopy(the_dict)
        value_error_dict['last_update'] = 'not_valid_timestamp'
        with self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError):
            Alert.from_dict(value_error_dict)

    def test_to_dict(self):
        condition = Condition('humidity', 'LESS_THAN', 10)
        instance = Alert('alert1', 'trigger1', [{
            "current_value": 263.576,
            "condition": condition.to_dict()}],
            {"lon": 37, "lat": 53},
            1481802090232)
        result = instance.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual('alert1', result['id'])
        self.assertEqual('trigger1', result['trigger_id'])
        self.assertEqual(1, len(result['met_conditions']))
        mc = result['met_conditions'][0]
        self.assertEqual(dict(current_value=263.576, condition=condition.to_dict()), mc)
        self.assertEqual({"lon": 37, "lat": 53}, result['coordinates'])
        self.assertEqual(1481802090232, result['last_update'])

    def test_repr(self):
        the_dict = {
         '_id': '5853dbe27416a400011b1b77',
         'conditions': [{'_id': '5853dbe27416a400011b1b78',
                         'condition': {'amount': 273, 'expression': '$lt', 'name': 'temp'},
                         'current_value': {'max': 258.62, 'min': 258.62}}],
         'coordinates': {'lat': '53', 'lon': '37'},
         'date': '2016-12-17T00:00:00.000Z',
         'last_update': '2016-12-16T11:19:46.352Z',
         'triggerId': '5852816a9aaacb00153134a3'}
        instance = Alert.from_dict(the_dict)
        print(instance)


class TestAlertChannel(unittest.TestCase):

    def test_to_dict(self):
        name = 'foobaz'
        instance = AlertChannel(name)
        self.assertEqual(dict(name=name), instance.to_dict())

    def test_repr(self):
        print(AlertChannel('foobaz'))

    def test_alert_last_updated_is_none(self):
        alert = Alert('alert1', 'trigger1', [{
            "current_value": 263.576,
            "condition": Condition('humidity', 'LESS_THAN', 10)}],
                      {"lon": 37, "lat": 53})
        self.assertIsNone(alert.last_update)
