#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.commons.databoxes import ImageType, SubscriptionType


class SubscriptionTypeEnum:
    """
    Allowed OpenWeatherMap subscription types

    """
    FREE = SubscriptionType('free', 'api', False)
    STARTUP = SubscriptionType('startup', 'api', True)
    DEVELOPER = SubscriptionType('developer', 'api', True)
    PROFESSIONAL = SubscriptionType('professional', 'api', True)
    ENTERPRISE = SubscriptionType('enterprise', 'api', True)

    @classmethod
    def lookup_by_name(cls, name):
        for i in SubscriptionTypeEnum.items():
            if i.name == name:
                return i
        raise ValueError('Subscription type not allowed')

    @classmethod
    def items(cls):
        """
        All values for this enum
        :return: list of `pyowm.commons.enums.SubscriptionType`

        """
        return [
            cls.FREE,
            cls.STARTUP,
            cls.DEVELOPER,
            cls.PROFESSIONAL,
            cls.ENTERPRISE
        ]

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)


class ImageTypeEnum:
    """
    Allowed image types on OWM APIs

    """
    PNG = ImageType('PNG', 'image/png')
    GEOTIFF = ImageType('GEOTIFF', 'image/tiff')

    @classmethod
    def lookup_by_mime_type(cls, mime_type):
        for i in ImageTypeEnum.items():
            if i.mime_type == mime_type:
                return i
        return None

    @classmethod
    def lookup_by_name(cls, name):
        for i in ImageTypeEnum.items():
            if i.name == name:
                return i
        return None

    @classmethod
    def items(cls):
        """
        All values for this enum
        :return: list of `pyowm.commons.enums.ImageType`

        """
        return [
            cls.PNG,
            cls.GEOTIFF
        ]

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)
