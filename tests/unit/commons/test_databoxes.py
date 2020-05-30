#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pyowm.commons.databoxes import ImageType, Satellite, SubscriptionType


class TestImageType(unittest.TestCase):

    def test_repr(self):
        instance = ImageType('PDF', 'application/pdf')
        repr(instance)


class TestSatellite(unittest.TestCase):

    def test_repr(self):
        instance = Satellite('Terrasat', 'tst')
        repr(instance)


class TestSubscriptionType(unittest.TestCase):

    def test_repr(self):
        instance = SubscriptionType('startup', 'pro', True)
        repr(instance)