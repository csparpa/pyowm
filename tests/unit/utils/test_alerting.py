import unittest
from pyowm.utils import alerting
from pyowm.utils import geo


class TestCondition(unittest.TestCase):

    def test_condition_fails_with_wrong_parameters(self):
        self.assertRaises(AssertionError, alerting.Condition,
                          123, 'EQUAL', 67.8)
        self.assertRaises(ValueError, alerting.Condition,
                          'NOT_ALLOWED', 'EQUAL', 67.8)
        self.assertRaises(AssertionError, alerting.Condition,
                          'HUMIDITY', 123, 67.8)
        self.assertRaises(ValueError, alerting.Condition,
                          'HUMIDITY', '$xyz', 67.8)
        self.assertRaises(AssertionError, alerting.Condition,
                          'HUMIDITY', 'EQUAL', None)
        self.assertRaises(AssertionError, alerting.Condition,
                          'HUMIDITY', 'EQUAL', 'string')

    def test_condition_parameter_case_is_not_significant(self):
        condition_1 = alerting.Condition('TEMPERATURE', 'LESS_THAN', 89.0)
        condition_2 = alerting.Condition('temperature', 'LESS_THAN', 89.0)
        self.assertEqual(condition_1.weather_param, condition_2.weather_param)


class TestTrigger(unittest.TestCase):

    def test_trigger_fails_with_wrong_parameters(self):
        start = 1526809375
        end = 1527809375
        conditions = [alerting.Condition('humidity', 'LESS_THAN', 10)]
        area = [geo.Point(13.6, 46.9)]

        self.assertRaises(AssertionError, alerting.Trigger,
                          None, end, conditions, area, alerts=None, alert_channels=None, id=None)
        self.assertRaises(AssertionError, alerting.Trigger,
                          start, None, conditions, area, alerts=None, alert_channels=None, id=None)
        self.assertRaises(ValueError, alerting.Trigger,
                          end, start, conditions, area, alerts=None, alert_channels=None, id=None)

        self.assertRaises(AssertionError, alerting.Trigger,
                          start, end, None, area, alerts=None, alert_channels=None, id=None)
        self.assertRaises(ValueError, alerting.Trigger,
                          start, end, [], area, alerts=None, alert_channels=None, id=None)

        self.assertRaises(AssertionError, alerting.Trigger,
                          start, end, conditions, None, alerts=None, alert_channels=None, id=None)
        self.assertRaises(ValueError, alerting.Trigger,
                          start, end, conditions, [], alerts=None, alert_channels=None, id=None)

        _ = alerting.Trigger(start, end, conditions, area, alerts=None, alert_channels=None, id=None)

    def test_defaulted_parameters(self):
        instance = alerting.Trigger(1526809375, 1527809375, [alerting.Condition('humidity', 'LESS_THAN', 10)],
                                    [geo.Point(13.6, 46.9)], alerts=None, alert_channels=None, id=None)
        self.assertIsInstance(instance.alerts, list)
        self.assertEqual(0, len(instance.alerts))
        self.assertIsInstance(instance.alert_channels, list)
        self.assertEqual(1, len(instance.alert_channels))
        self.assertEqual(instance.alert_channels[0], alerting.AlertChannelsEnum.OWM_API_POLLING)

    def test_get_alert(self):
        alerts = []
        instance = alerting.Trigger(1526809375, 1527809375, [alerting.Condition('humidity', 'LESS_THAN', 10)],
                                    [geo.Point(13.6, 46.9)], alerts=alerts, alert_channels=None, id=None)
        self.assertIsNone(instance.get_alert('unexistent'))
