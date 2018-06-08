import unittest
from pyowm.alertingapi30.alert import Alert


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
