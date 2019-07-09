#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
from pyowm.alertapi30.alert_manager import AlertManager
from pyowm.alertapi30.trigger import Trigger
from pyowm.alertapi30.alert import Alert
from pyowm.alertapi30.condition import Condition
from pyowm.commons.http_client import HttpClient
from pyowm.config import DEFAULT_CONFIG
from pyowm.utils import geo
from pyowm.constants import ALERT_API_VERSION


class MockHttpClient(HttpClient):

    # 1 trigger
    test_trigger_json = '''{"_id":"5852816a9aaacb00153134a3","__v":0,"alerts":
    {"8b48b2cd21c23d2894466caccba1ed1f":{"conditions":[{"current_value":{"min":263.576,"max":263.576},"condition":
    {"name":"temp","expression":"$lt","amount":273,"_id":"5852816a9aaacb00153134a5"}}],"last_update":1481802090232,
    "date":1482181200000,"coordinates":{"lon":37,"lat":53}}},"area":[{"type":"Point","_id":"5852816a9aaacb00153134a4",
    "coordinates":[37,53]}],"conditions":[{"name":"temp","expression":"$lt","amount":273,"_id":"5852816a9aaacb00153134a5"}],
    "time_period":{"end":{"amount":432000000,"expression":"after"},"start":{"amount":132000000,"expression":"after"}}}'''

    def get_json(self, uri, params=None, headers=None):
        return 200, [json.loads(self.test_trigger_json)]

    def post(self, uri, params=None, data=None, headers=None):
        return 200, json.loads(self.test_trigger_json)

    def put(self, uri, params=None, data=None, headers=None):
        return 200, [json.loads(self.test_trigger_json)]

    def delete(self, uri, params=None, data=None, headers=None):
        return 204, [json.loads(self.test_trigger_json)]


class MockHttpClientTwoTriggers(HttpClient):
    # 2 triggers
    test_triggers_json = '''[ {"_id":"585280edbe54110025ea52bb","__v":0,"alerts":{},"area":[{"type":"Point",
    "_id":"585280edbe54110025ea52bc","coordinates":[53,37]}],"conditions":[{"name":"temp","expression":"$lt",
    "amount":273,"_id":"585280edbe54110025ea52bd"}],"time_period":{"end":{"amount":432000000,"expression":"after"},
    "start":{"amount":132000000,"expression":"after"}}},{"_id":"5852816a9aaacb00153134a3","__v":0,"alerts":
    {"8b48b2cd21c23d2894466caccba1ed1f":{"conditions":[{"current_value":{"min":263.576,"max":263.576},"condition":
    {"name":"temp","expression":"$lt","amount":273,"_id":"5852816a9aaacb00153134a5"}}],"last_update":1481802090232,
    "date":1482181200000,"coordinates":{"lon":37,"lat":53}}},"area":[{"type":"Point","_id":"5852816a9aaacb00153134a4",
    "coordinates":[37,53]}],"conditions":[{"name":"temp","expression":"$lt","amount":273,"_id":"5852816a9aaacb00153134a5"}],
    "time_period":{"end":{"amount":432000000,"expression":"after"},"start":{"amount":132000000,"expression":"after"}}}]'''

    def get_json(self, uri, params=None, headers=None):
        return 200, json.loads(self.test_triggers_json)


class MockHttpClientOneTrigger(HttpClient):
    # 1 trigger
    test_trigger_json = '''{"_id":"5852816a9aaacb00153134a3","__v":0,"alerts":
    {"8b48b2cd21c23d2894466caccba1ed1f":{"conditions":[{"current_value":{"min":263.576,"max":263.576},"condition":
    {"name":"temp","expression":"$lt","amount":273,"_id":"5852816a9aaacb00153134a5"}}],"last_update":1481802090232,
    "date":1482181200000,"coordinates":{"lon":37,"lat":53}}},"area":[{"type":"Point","_id":"5852816a9aaacb00153134a4",
    "coordinates":[37,53]}],"conditions":[{"name":"temp","expression":"$lt","amount":273,"_id":"5852816a9aaacb00153134a5"}],
    "time_period":{"end":{"amount":432000000,"expression":"after"},"start":{"amount":132000000,"expression":"after"}}}'''

    def get_json(self, uri, params=None, headers=None):
        return 200, json.loads(self.test_trigger_json)


class MockHttpClientTwoAlerts(HttpClient):
    # 2 alerts
    test_alerts_json = '''[{"_id": "5853dbe27416a400011b1b77","date": "2016-12-17T00:00:00.000Z","last_update": 
    "2016-12-16T11:19:46.352Z","triggerId": "5852816a9aaacb00153134a3","__v": 0,"conditions": [{"current_value": 
    {"max": 258.62,"min": 258.62},"_id": "5853dbe27416a400011b1b78","condition": {"amount": 273,"expression": 
    "$lt","name": "temp"}}],"coordinates": {"lat": "53","lon": "37"}},{"_id": "5853dbe27416a400011b1b79","date": 
    "2016-12-17T03:00:00.000Z","last_update": "2016-12-16T11:19:46.352Z","triggerId": "5852816a9aaacb00153134a3",
    "__v": 0,"conditions": [{"current_value": {"max": 259.277,"min": 259.277},"_id": "5853dbe27416a400011b1b7a",
    "condition": {"amount": 273,"expression": "$lt","name": "temp"}}],"coordinates": {"lat": "53","lon": "37"}}]'''

    def get_json(self, uri, params=None, headers=None):
        return 200, json.loads(self.test_alerts_json)

    def delete(self, uri, params=None, data=None, headers=None):
        return 204, json.loads(self.test_alerts_json)


class MockHttpClientOneAlert(HttpClient):
    # 1 alert
    test_alert_json = '''{"_id": "5853dbe27416a400011b1b77","date": "2016-12-17T00:00:00.000Z","last_update": 
    "2016-12-16T11:19:46.352Z","triggerId": "5852816a9aaacb00153134a3","__v": 0,"conditions": [{"current_value": 
    {"max": 258.62,"min": 258.62},"_id": "5853dbe27416a400011b1b78","condition": {"amount": 273,"expression": 
    "$lt","name": "temp"}}],"coordinates": {"lat": "53","lon": "37"}}'''

    def get_json(self, uri, params=None, headers=None):
        return 200, json.loads(self.test_alert_json)

    def delete(self, uri, params=None, data=None, headers=None):
        return 204, json.loads(self.test_alert_json)


class TestAlertManager(unittest.TestCase):
    _cond1 = Condition('humidity', 'LESS_THAN', 10)
    _cond2 = Condition('temp', 'GREATER_THAN_EQUAL', 100.6)
    _trigger = Trigger(1526809375, 1527809375, [_cond1, _cond2],
                       [geo.Point(13.6, 46.9)], alerts=[], alert_channels=None, id='trigger-id')
    _alert = Alert('alert1', 'trigger1', [{
                "current_value": 263.576,
                "condition": _cond1
            }],
            {"lon": 37, "lat": 53}, 1481802090232)

    def factory(self, _kls):
        sm = AlertManager('APIKey', DEFAULT_CONFIG)
        sm.http_client = _kls('APIKey', DEFAULT_CONFIG, 'anyurl.com')
        return sm

    def test_instantiation_with_wrong_params(self):
        self.assertRaises(AssertionError, AlertManager, None, dict())
        self.assertRaises(AssertionError, AlertManager, 'apikey', None)

    def test_get_alert_api_version(self):
        instance = AlertManager('APIKey', DEFAULT_CONFIG)
        result = instance.alert_api_version()
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, ALERT_API_VERSION)

    def test_get_triggers(self):
        instance = self.factory(MockHttpClientTwoTriggers)
        results = instance.get_triggers()
        self.assertEqual(2, len(results))
        t = results[0]
        self.assertIsInstance(t, Trigger)

    def test_get_trigger_fails_with_wrong_input(self):
        instance = AlertManager('APIKey', DEFAULT_CONFIG)
        with self.assertRaises(AssertionError):
            instance.get_trigger(None)
        with self.assertRaises(AssertionError):
            instance.get_trigger(123)

    def test_get_trigger(self):
        instance = self.factory(MockHttpClientOneTrigger)
        result = instance.get_trigger('any-id')
        self.assertIsInstance(result, Trigger)

    def test_create_trigger(self):
        instance = self.factory(MockHttpClient)
        result = instance.create_trigger(1526809375, 1527809375, [self._cond1, self._cond2], [geo.Point(13.6, 46.9)], alert_channels=None)
        self.assertIsInstance(result, Trigger)

    def test_create_trigger_fails_with_wrong_inputs(self):
        instance = self.factory(MockHttpClient)
        with self.assertRaises(AssertionError):
            instance.create_trigger(None, 1527809375, [self._cond1, self._cond2], [geo.Point(13.6, 46.9)], alert_channels=None)
        with self.assertRaises(AssertionError):
            instance.create_trigger(1526809375, None, [self._cond1, self._cond2], [geo.Point(13.6, 46.9)], alert_channels=None)
        with self.assertRaises(ValueError):
            instance.create_trigger(1526809375, 1327809375, [self._cond1, self._cond2], [geo.Point(13.6, 46.9)], alert_channels=None)
        with self.assertRaises(AssertionError):
            instance.create_trigger(1526809375, 1527809375, None, [geo.Point(13.6, 46.9)], alert_channels=None)
        with self.assertRaises(ValueError):
            instance.create_trigger(1526809375, 1527809375, [], [geo.Point(13.6, 46.9)], alert_channels=None)
        with self.assertRaises(AssertionError):
            instance.create_trigger(1526809375, 1527809375, [self._cond1, self._cond2], None, alert_channels=None)
        with self.assertRaises(ValueError):
            instance.create_trigger(1526809375, 1527809375, [self._cond1, self._cond2], [], alert_channels=None)

    def test_delete_trigger_fails_with_wrong_input(self):
        instance = AlertManager('APIKey', DEFAULT_CONFIG)
        with self.assertRaises(AssertionError):
            instance.delete_trigger(None)
        with self.assertRaises(AssertionError):
            self._trigger.id = 123
            instance.delete_trigger(self._trigger)

    def test_delete_trigger(self):
        instance = self.factory(MockHttpClient)
        trigger = Trigger.from_dict(json.loads(MockHttpClient.test_trigger_json))
        result = instance.delete_trigger(trigger)
        self.assertIsNone(result)

    def test_update_trigger_fails_with_wrong_input(self):
        instance = AlertManager('APIKey', DEFAULT_CONFIG)
        with self.assertRaises(AssertionError):
            instance.update_trigger(None)
        with self.assertRaises(AssertionError):
            self._trigger.id = 123
            instance.update_trigger(self._trigger)

    def test_update_trigger(self):
        instance = self.factory(MockHttpClient)
        modified_trigger = Trigger.from_dict(json.loads(MockHttpClient.test_trigger_json))
        modified_trigger.id = '5852816a9aaacb00153134a3'
        modified_trigger.end = self._trigger.end_after_millis + 10000
        result = instance.update_trigger(modified_trigger)
        self.assertIsNone(result)

    def test_get_alerts_for_fails_with_wrong_input(self):
        instance = AlertManager('APIKey', DEFAULT_CONFIG)
        with self.assertRaises(AssertionError):
            instance.get_alerts_for(None)
        with self.assertRaises(AssertionError):
            self._trigger.id = 123
            instance.get_alerts_for(self._trigger)

    def test_get_alerts_for(self):
        instance = self.factory(MockHttpClientTwoAlerts)
        self._trigger.id = 'trigger-id'
        results = instance.get_alerts_for(self._trigger)
        self.assertEqual(2, len(results))
        self.assertIsInstance(results[0], Alert)
        self.assertIsInstance(results[1], Alert)

    def test_get_alert_fails_with_wrong_input(self):
        instance = AlertManager('APIKey', DEFAULT_CONFIG)
        with self.assertRaises(AssertionError):
            instance.get_alert(None, self._trigger)
        with self.assertRaises(AssertionError):
            instance.get_alert(123, self._trigger)
        with self.assertRaises(AssertionError):
            instance.get_alert('alert-id', None)
        with self.assertRaises(AssertionError):
            self._trigger.id = 123
            instance.get_alert('alert-id', self._trigger)

    def test_get_alert(self):
        self._trigger.id = 'trigger-id'
        instance = self.factory(MockHttpClientOneAlert)
        result = instance.get_alert('alert-id', self._trigger)
        self.assertIsInstance(result, Alert)

    def test_delete_all_alerts_for_fails_with_wrong_input(self):
        instance = AlertManager('APIKey', DEFAULT_CONFIG)
        with self.assertRaises(AssertionError):
            instance.delete_all_alerts_for(None)
        with self.assertRaises(AssertionError):
            self._trigger.id = 123
            instance.delete_all_alerts_for(self._trigger)

    def test_delete_all_alerts_for(self):
        instance = self.factory(MockHttpClientTwoAlerts)
        result = instance.delete_all_alerts_for(self._trigger)
        self.assertIsNone(result)

    def test_delete_alert_fails_with_wrong_input(self):
        instance = AlertManager('APIKey', DEFAULT_CONFIG)
        with self.assertRaises(AssertionError):
            instance.delete_alert(None)
        with self.assertRaises(AssertionError):
            self._alert.id = 123
            instance.delete_alert(self._alert)
        self._alert.id = 'alert-id'
        self._alert.trigger_id = None
        with self.assertRaises(AssertionError):
            instance.delete_alert(self._alert)
        self._alert.trigger_id = 789
        with self.assertRaises(AssertionError):
            instance.delete_alert(self._alert)

    def test_delete_alert(self):
        instance = self.factory(MockHttpClientOneAlert)
        result = instance.delete_alert(self._alert)
        self.assertIsNone(result)

    def test_repr(self):
        print(AlertManager('APIKey', DEFAULT_CONFIG))
