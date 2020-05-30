#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import copy
from pyowm import owm
from pyowm.alertapi30.condition import Condition
from pyowm.alertapi30.enums import WeatherParametersEnum, OperatorsEnum
from pyowm.utils import geo


class IntegrationTestsAlertAPI30(unittest.TestCase):

    __owm = owm.OWM(os.getenv('OWM_API_KEY', None))

    cond1 = Condition(WeatherParametersEnum.HUMIDITY, OperatorsEnum.LESS_THAN, 10)
    cond2 = Condition(WeatherParametersEnum.CLOUDS, OperatorsEnum.LESS_THAN, 90)
    start = '2019-07-01 14:17:00+00'
    end = '2019-07-02 14:17:00+00'
    # a rectangle around the city of Moscow
    area1 = geo.Polygon.from_dict({
        "type": "Polygon",
        "coordinates": [
            [
                [
                    36.826171875,
                    55.17259379606185
                ],
                [
                    39.012451171875,
                    55.17259379606185
                ],
                [
                    39.012451171875,
                    56.15778819063682
                ],
                [
                    36.826171875,
                    56.15778819063682
                ],
                [
                    36.826171875,
                    55.17259379606185
                ]
            ]
        ]})
    # somewhere in Dubai

    area2 = geo.Point.from_dict({
        "type": "Point",
        "coordinates": [
            55.29693603515625,
            25.186301620540558
    ]})

    def test_triggers_CRUD(self):

        mgr = self.__owm.alert_manager()

        # check if any previous triggers exist on this account
        n_old_triggers = len(mgr.get_triggers())

        # create trigger1
        trigger1 = mgr.create_trigger(self.start, self.end, conditions=[self.cond1], area=[self.area1])

        # create trigger2
        trigger2 = mgr.create_trigger(self.start, self.end, conditions=[self.cond2], area=[self.area2])

        # Read all created triggers
        triggers = mgr.get_triggers()
        self.assertEqual(n_old_triggers + 2, len(triggers))

        # Read one by one
        result = mgr.get_trigger(trigger1.id)
        self.assertEqual(trigger1.id, result.id)
        self.assertEqual(trigger1.start_after_millis, result.start_after_millis)
        self.assertEqual(trigger1.end_after_millis, result.end_after_millis)
        self.assertEqual(len(trigger1.conditions), len(result.conditions))
        self.assertEqual(len(trigger1.area), len(result.area))

        result = mgr.get_trigger(trigger2.id)
        self.assertEqual(trigger2.id, result.id)
        self.assertEqual(trigger2.start_after_millis, result.start_after_millis)
        self.assertEqual(trigger2.end_after_millis, result.end_after_millis)
        self.assertEqual(len(trigger2.conditions), len(result.conditions))
        self.assertEqual(len(trigger2.area), len(result.area))

        # Update a trigger
        modified_trigger2 = copy.deepcopy(trigger2)
        modified_trigger2.conditions = [self.cond1, self.cond2]

        mgr.update_trigger(modified_trigger2)
        result = mgr.get_trigger(modified_trigger2.id)

        self.assertEqual(modified_trigger2.id, result.id)
        self.assertEqual(modified_trigger2.start_after_millis, result.start_after_millis)
        self.assertEqual(modified_trigger2.end_after_millis, result.end_after_millis)
        self.assertEqual(len(modified_trigger2.area), len(result.area))
        # of course, conditions have been modified with respect to former trigger 2
        self.assertNotEqual(len(trigger2.conditions), len(result.conditions))
        self.assertEqual(len(modified_trigger2.conditions), len(result.conditions))

        # Delete triggers one by one
        mgr.delete_trigger(trigger1)
        triggers = mgr.get_triggers()
        self.assertEqual(n_old_triggers + 1, len(triggers))

        mgr.delete_trigger(modified_trigger2)
        triggers = mgr.get_triggers()
        self.assertEqual(n_old_triggers, len(triggers))


if __name__ == "__main__":
    unittest.main()
