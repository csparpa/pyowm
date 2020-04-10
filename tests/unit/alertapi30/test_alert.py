import unittest
from pyowm.alertapi30.alert import Alert
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
