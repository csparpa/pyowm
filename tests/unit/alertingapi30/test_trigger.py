import unittest
from pyowm.utils import geo
from pyowm.alertapi30.condition import Condition
from pyowm.alertapi30.trigger import Trigger
from pyowm.alertapi30.enums import AlertChannelsEnum
from pyowm.alertapi30.alert import Alert


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

        _ = Trigger(start, end, conditions, area, alerts=None, alert_channels=None)

    def test_defaulted_parameters(self):
        instance = Trigger(1526809375, 1527809375, [Condition('humidity', 'LESS_THAN', 10)],
                           [geo.Point(13.6, 46.9)], alerts=None, alert_channels=None)
        self.assertIsInstance(instance.alerts, list)
        self.assertEqual(0, len(instance.alerts))
        self.assertIsInstance(instance.alert_channels, list)
        self.assertEqual(1, len(instance.alert_channels))
        self.assertEqual(instance.alert_channels[0], AlertChannelsEnum.OWM_API_POLLING)

    def test_get_alert(self):
        cond = Condition('humidity', 'LESS_THAN', 10)
        alert = Alert('alert1', 'trigger1', [{
                "current_value": 263.576,
                "condition": cond
            }],
            {"lon": 37, "lat": 53}, 1481802090232
        )
        alerts = [alert]
        instance = Trigger(1526809375, 1527809375, [cond],
                           [geo.Point(13.6, 46.9)], alerts=alerts, alert_channels=None)
        self.assertEqual(alert, instance.get_alert('alert1'))

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
