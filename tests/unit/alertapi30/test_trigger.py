#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import copy
import unittest

import pyowm.commons.exceptions
from pyowm.alertapi30.condition import Condition
from pyowm.alertapi30.trigger import Trigger
from pyowm.alertapi30.enums import AlertChannelsEnum
from pyowm.alertapi30.alert import Alert
from pyowm.utils import geo


class TestTrigger(unittest.TestCase):

    def test_trigger_fails_with_wrong_parameters(self):
        start_after_millis = 450000
        end_after_millis = 470000
        conditions = [Condition('humidity', 'LESS_THAN', 10)]
        area = [geo.Point(13.6, 46.9)]

        self.assertRaises(AssertionError, Trigger,
                          None, end_after_millis, conditions, area, alerts=None, alert_channels=None, id=None)
        self.assertRaises(AssertionError, Trigger,
                          start_after_millis, None, conditions, area, alerts=None, alert_channels=None, id=None)
        self.assertRaises(AssertionError, Trigger,
                          'test', end_after_millis, conditions, area, alerts=None, alert_channels=None, id=None)
        self.assertRaises(AssertionError, Trigger,
                          start_after_millis, 'test', conditions, area, alerts=None, alert_channels=None, id=None)
        self.assertRaises(ValueError, Trigger,
                          end_after_millis, start_after_millis, conditions, area, alerts=None, alert_channels=None, id=None)

        self.assertRaises(AssertionError, Trigger,
                          start_after_millis, end_after_millis, None, area, alerts=None, alert_channels=None, id=None)
        self.assertRaises(ValueError, Trigger,
                          start_after_millis, end_after_millis, [], area, alerts=None, alert_channels=None, id=None)

        self.assertRaises(AssertionError, Trigger,
                          start_after_millis, end_after_millis, conditions, None, alerts=None, alert_channels=None, id=None)
        self.assertRaises(ValueError, Trigger,
                          start_after_millis, end_after_millis, conditions, [], alerts=None, alert_channels=None, id=None)

        _ = Trigger(start_after_millis, end_after_millis, conditions, area, alerts=None, alert_channels=None)

    def test_defaulted_parameters(self):
        instance = Trigger(1526809375, 1527809375, [Condition('humidity', 'LESS_THAN', 10)],
                           [geo.Point(13.6, 46.9)], alerts=None, alert_channels=None)
        self.assertIsInstance(instance.alerts, list)
        self.assertEqual(0, len(instance.alerts))
        self.assertIsInstance(instance.alert_channels, list)
        self.assertEqual(1, len(instance.alert_channels))
        self.assertEqual(instance.alert_channels[0], AlertChannelsEnum.OWM_API_POLLING)

    def test_init(self):
        alert_channels = [AlertChannelsEnum.items()]
        instance = Trigger(1526809375, 1527809375, [Condition('humidity', 'LESS_THAN', 10)],
                           [geo.Point(13.6, 46.9)], alerts=None, alert_channels=alert_channels)
        self.assertEqual(instance.alert_channels, alert_channels)

    def test_get_alert(self):
        cond = Condition('humidity', 'LESS_THAN', 10)
        alert = Alert('alert1', 'trigger1', [{
                "current_value": 263.576,
                "condition": cond
            }],
            {"lon": 37, "lat": 53}, 1481802090232
        )
        alert_two = copy.deepcopy(alert)
        alert_two.id = 'alert_two'
        alerts = [alert_two, alert]     # Second alert has to be 1st element to have full coverage
        instance = Trigger(1526809375, 1527809375, [cond],
                           [geo.Point(13.6, 46.9)], alerts=alerts, alert_channels=None)
        self.assertEqual(alert, instance.get_alert('alert1'))

        # Trigger without alerts
        instance.alerts = []
        self.assertIsNone(instance.get_alert(alert_id='alert1'))

    def test_get_alerts(self):
        cond = Condition('humidity', 'LESS_THAN', 10)
        alert1 = Alert('alert1', 'trigger1', [{
                "current_value": 263.576,
                "condition": cond
            }],
            {"lon": 37, "lat": 53}, 1481802090232
        )
        alert2 = Alert('alert2', 'trigger1', [{
                "current_value": 111.576,
                "condition": cond
            }],
            {"lon": 37, "lat": 53}, 1481802100000
        )
        alerts = [alert1, alert2]
        instance = Trigger(1526809375, 1527809375, [cond],
                           [geo.Point(13.6, 46.9)], alerts=alerts, alert_channels=None)
        result = instance.get_alerts()
        self.assertTrue(isinstance(result, list))
        self.assertTrue(alert1 in result)
        self.assertTrue(alert2 in result)

    def test_get_alerts_since(self):
        cond = Condition('humidity', 'LESS_THAN', 10)
        alert1 = Alert('alert1', 'trigger1', [{
                "current_value": 263.576,
                "condition": cond
            }],
            {"lon": 37, "lat": 53}, 1000
        )
        alert2 = Alert('alert2', 'trigger1', [{
                "current_value": 111.576,
                "condition": cond
            }],
            {"lon": 37, "lat": 53}, 3000
        )
        alert3 = Alert('alert3', 'trigger1', [{
                "current_value": 119.332,
                "condition": cond
            }],
            {"lon": 37, "lat": 53}, 9000
        )
        alert4 = Alert('alert4', 'trigger1', [{
                "current_value": 119.332,
                "condition": cond
            }],
            {"lon": 37, "lat": 53}, 12000
        )
        alerts = [alert1, alert2, alert3, alert4]
        instance = Trigger(1526809375, 1527809375, [cond],
                           [geo.Point(13.6, 46.9)], alerts=alerts, alert_channels=None)

        result = instance.get_alerts_since(4000)
        self.assertEqual(2, len(result))
        self.assertTrue(alert3 in result)
        self.assertTrue(alert4 in result)

        result = instance.get_alerts_since(3000)
        self.assertEqual(3, len(result))
        self.assertTrue(alert2 in result)
        self.assertTrue(alert3 in result)
        self.assertTrue(alert4 in result)

        result = instance.get_alerts_since(15000)
        self.assertEqual(0, len(result))

    def test_get_alerts_on(self):
        cond1 = Condition('humidity', 'LESS_THAN', 10)
        cond2 = Condition('temp', 'GREATER_THAN_EQUAL', 100.6)
        alert1 = Alert('alert1', 'trigger1', [{
                "current_value": 8.576,
                "condition": cond1
            }],
            {"lon": 37, "lat": 53}, 1000
        )
        alert2 = Alert('alert2', 'trigger1', [{
                "current_value": 111.576,
                "condition": cond2
            }],
            {"lon": 37, "lat": 53}, 3000
        )
        alert3 = Alert('alert3', 'trigger1', [{
                "current_value": 119.332,
                "condition": cond2
            }],
            {"lon": 37, "lat": 53}, 9000
        )
        alert4 = Alert('alert4', 'trigger1', [{
                "current_value": 7.332,
                "condition": cond1
            }],
            {"lon": 37, "lat": 53}, 12000
        )
        alerts = [alert1, alert2, alert3, alert4]
        instance = Trigger(1526809375, 1527809375, [cond1, cond2],
                           [geo.Point(13.6, 46.9)], alerts=alerts, alert_channels=None)
        result = instance.get_alerts_on('temp')
        self.assertEqual(2, len(result))
        self.assertTrue(alert2 in result)
        self.assertTrue(alert3 in result)

        result = instance.get_alerts_on('humidity')
        self.assertEqual(2, len(result))
        self.assertTrue(alert1 in result)
        self.assertTrue(alert4 in result)

        result = instance.get_alerts_on('wind_direction')
        self.assertEqual(0, len(result))

    def test_from_dict(self):
        the_dict = json.loads('''{"_id":"5852816a9aaacb00153134a3","__v":0,"alerts":{"8b48b2cd21c23d2894466caccba1ed1f":{"conditions":[
        {"current_value":{"min":263.576,"max":263.576},"condition":{"name":"temp","expression":"$lt","amount":273,
        "_id":"5852816a9aaacb00153134a5"}}],"last_update":1481802090232,"date":1482181200000,"coordinates":{"lon":37,
        "lat":53}}},"area":[{"type":"Point","_id":"5852816a9aaacb00153134a4","coordinates":[37,53]}],"conditions":
        [{"name":"temp","expression":"$lt","amount":273,"_id":"5852816a9aaacb00153134a5"}],"time_period":{"end":{
        "amount":432060000,"expression":"after"},"start":{"amount":432000000,"expression":"after"}}}''')
        result = Trigger.from_dict(the_dict)
        self.assertTrue(isinstance(result, Trigger))

        self.assertEqual(432000000, result.start_after_millis)
        self.assertEqual(432060000, result.end_after_millis)
        self.assertTrue(isinstance(result.conditions, list))
        self.assertTrue(isinstance(result.area, list))
        self.assertTrue(isinstance(result.alerts, list))
        self.assertTrue(isinstance(result.alert_channels, list))
        self.assertEqual('5852816a9aaacb00153134a3', result.id)

        with self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError):
            Trigger.from_dict(None)

        with self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError):
            Trigger.from_dict(dict(nonexistent='key'))

        with self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError):
            Trigger.from_dict(json.loads('''{"_id":"5852816a9aaacb00153134a3","__v":0,"alerts":{"8b48b2cd21c23d2894466caccba1ed1f":{"conditions":[
        {"current_value":{"min":263.576,"max":263.576},"condition":{"name":"temp","expression":"$lt","amount":273,
        "_id":"5852816a9aaacb00153134a5"}}],"last_update":1481802090232,"date":1482181200000,"coordinates":{"lon":37,
        "lat":53}}},"area":[{"type":"Point","_id":"5852816a9aaacb00153134a4","coordinates":[37,53]}],"conditions":
        [{"name":"temp","expression":"$lt","amount":273,"_id":"5852816a9aaacb00153134a5"}],"time_period":{"end":{
        "amount":432000000,"expression":"exact"},"start":{"amount":132000000,"expression":"before"}}}'''))

        # ValueError check
        with self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError):
            the_dict['time_period']['end']['expression'] = 'before'
            Trigger.from_dict(the_dict)


    def test_to_dict(self):
        cond = Condition('humidity', 'LESS_THAN', 10)
        instance = Trigger(1526809375, 1527809375, [cond], [geo.Point(13.6, 46.9)], alerts=[], alert_channels=None, id='myid')
        result = instance.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual('myid', result['id'])
        self.assertEqual(1526809375, result['start_after_millis'])
        self.assertEqual(1527809375, result['end_after_millis'])
        self.assertEqual([dict(name='OWM API POLLING')], result['alert_channels'])
        self.assertEqual(list(), result['alerts'])
        self.assertEqual([{'type': 'Point', 'coordinates': [13.6, 46.9]}], result['area'])
        self.assertEqual([{'id': None, 'weather_param': 'humidity', 'operator': 'LESS_THAN', 'amount': 10}], result['conditions'])

    def test_repr(self):
        instance = Trigger(1526809375, 1527809375, [Condition('humidity', 'LESS_THAN', 10)],
                           [geo.Point(13.6, 46.9)], alerts=None, alert_channels=None)
        print(instance)
