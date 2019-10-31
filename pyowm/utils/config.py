#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from pyowm.config import DEFAULT_CONFIG
from pyowm.exceptions import config_error
from pyowm.commons.enums import SubscriptionTypeEnum


def get_config_from(path_to_file):
    """Loads configuration data from the supplied file and returns it.

    :param path_to_file: path to the configuration file
    :type path_to_file: str
    :returns: the configuration `dict`
    :raises: `ConfigurationNotFoundError` when the supplied filepath is not a regular file; `ConfigurationParseError`
        when the supplied file cannot be parsed

    """
    assert path_to_file is not None
    if not os.path.isfile(path_to_file):
        raise config_error.ConfigurationNotFoundError(
            'Configuration file not found: {}'.format(path_to_file))
    with open(path_to_file, 'r') as cf:
        try:
            config_data = json.load(cf)
            config_data['subscription_type'] = SubscriptionTypeEnum.lookup_by_name(
                config_data['subscription_type'])
            return config_data
        except Exception:
            raise config_error.ConfigurationParseError()


def get_default_config():
    """Returns the default PyOWM configuration.

    :returns: the configuration `dict`

    """
    return DEFAULT_CONFIG
