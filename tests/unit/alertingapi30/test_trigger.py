import unittest
from pyowm.utils import geo
from pyowm.alertingapi30.condition import Condition
from pyowm.alertingapi30.trigger import Trigger
from pyowm.alertingapi30.enums import AlertChannelsEnum


class TestTrigger(unittest.TestCase):

    def test_trigger_fails_with_wrong_parameters(self):
        start = 1526809375
        end = 1527809375
        conditions = [Condition('humidity', 'LESS_THAN', 10)]
        area = [geo.Point(13.6, 46.9)]

        self.assertRaises(AssertionError, Trigger,
                          None, end, conditions, area, alerts=None, alert_channels=None, id=None)
        self.assertRaises(AssertionError, Trigger,
                          start, None, conditions, area, alerts=None, alert_channels=None, id=None)
        self.assertRaises(ValueError, Trigger,
                          end, start, conditions, area, alerts=None, alert_channels=None, id=None)

        self.assertRaises(AssertionError, Trigger,
                          start, end, None, area, alerts=None, alert_channels=None, id=None)
        self.assertRaises(ValueError, Trigger,
                          start, end, [], area, alerts=None, alert_channels=None, id=None)

        self.assertRaises(AssertionError, Trigger,
                          start, end, conditions, None, alerts=None, alert_channels=None, id=None)
        self.assertRaises(ValueError, Trigger,
                          start, end, conditions, [], alerts=None, alert_channels=None, id=None)

        _ = Trigger(start, end, conditions, area, alerts=None, alert_channels=None, id=None)

    def test_defaulted_parameters(self):
        instance = Trigger(1526809375, 1527809375, [Condition('humidity', 'LESS_THAN', 10)],
                           [geo.Point(13.6, 46.9)], alerts=None, alert_channels=None, id=None)
        self.assertIsInstance(instance.alerts, list)
        self.assertEqual(0, len(instance.alerts))
        self.assertIsInstance(instance.alert_channels, list)
        self.assertEqual(1, len(instance.alert_channels))
        self.assertEqual(instance.alert_channels[0], AlertChannelsEnum.OWM_API_POLLING)

    def test_get_alert(self):
        alerts = []
        instance = Trigger(1526809375, 1527809375, [Condition('humidity', 'LESS_THAN', 10)],
                           [geo.Point(13.6, 46.9)], alerts=alerts, alert_channels=None, id=None)
        self.assertIsNone(instance.get_alert('unexistent'))