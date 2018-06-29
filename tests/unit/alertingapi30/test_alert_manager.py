import unittest
import json
from pyowm.alertapi30.alert_manager import AlertManager
from pyowm.alertapi30.trigger import Trigger
from pyowm.commons.http_client import HttpClient
from pyowm.constants import ALERT_API_VERSION


class MockHttpClient(HttpClient):
    # 2 triggers
    test_station_json = '''[ {"_id":"585280edbe54110025ea52bb","__v":0,"alerts":{},"area":[{"type":"Point",
    "_id":"585280edbe54110025ea52bc","coordinates":[53,37]}],"conditions":[{"name":"temp","expression":"$lt",
    "amount":273,"_id":"585280edbe54110025ea52bd"}],"time_period":{"end":{"amount":432000000,"expression":"exact"},
    "start":{"amount":132000000,"expression":"exact"}}},{"_id":"5852816a9aaacb00153134a3","__v":0,"alerts":
    {"8b48b2cd21c23d2894466caccba1ed1f":{"conditions":[{"current_value":{"min":263.576,"max":263.576},"condition":
    {"name":"temp","expression":"$lt","amount":273,"_id":"5852816a9aaacb00153134a5"}}],"last_update":1481802090232,
    "date":1482181200000,"coordinates":{"lon":37,"lat":53}}},"area":[{"type":"Point","_id":"5852816a9aaacb00153134a4",
    "coordinates":[37,53]}],"conditions":[{"name":"temp","expression":"$lt","amount":273,"_id":"5852816a9aaacb00153134a5"}],
    "time_period":{"end":{"amount":432000000,"expression":"exact"},"start":{"amount":132000000,"expression":"exact"}}}]'''

    def get_json(self, uri, params=None, headers=None):
        return 200, json.loads(self.test_station_json)


class TestAlertManager(unittest.TestCase):

    def factory(self, _kls):
        sm = AlertManager('APIKey')
        sm.http_client = _kls()
        return sm

    def test_instantiation_fails_without_api_key(self):
        self.assertRaises(AssertionError, AlertManager, None)

    def test_get_alert_api_version(self):
        instance = AlertManager('APIKey')
        result = instance.alert_api_version()
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, ALERT_API_VERSION)

    def test_get_triggers(self):
        instance = self.factory(MockHttpClient)
        results = instance.get_triggers()
        self.assertEqual(2, len(results))
        t = results[0]
        self.assertIsInstance(t, Trigger)