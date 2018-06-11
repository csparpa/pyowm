import unittest
from pyowm.alertapi30.alert_manager import AlertManager
from pyowm.constants import ALERT_API_VERSION


class TestAlertManager(unittest.TestCase):

    def test_instantiation_fails_without_api_key(self):
        self.assertRaises(AssertionError, AlertManager, None)

    def test_get_alert_api_version(self):
        instance = AlertManager('APIKey')
        result = instance.alert_api_version()
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, ALERT_API_VERSION)