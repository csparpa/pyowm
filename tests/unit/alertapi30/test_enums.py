import unittest

from pyowm.alertapi30.enums import AlertChannelsEnum, OperatorsEnum


class TestAlertChannelsEnum(unittest.TestCase):
    def test_items(self):
        alert_channels_enum = AlertChannelsEnum()
        self.assertEqual(alert_channels_enum.items(),
                         [AlertChannelsEnum.OWM_API_POLLING])


class TestOperatorsEnum(unittest.TestCase):
    def test_items(self):
        operators_enum = OperatorsEnum()
        self.assertEqual(sorted(operators_enum.items()), sorted([operators_enum.GREATER_THAN,
                                                                 operators_enum.GREATER_THAN_EQUAL,
                                                                 operators_enum.LESS_THAN,
                                                                 operators_enum.LESS_THAN_EQUAL,
                                                                 operators_enum.EQUAL,
                                                                 operators_enum.NOT_EQUAL]))
