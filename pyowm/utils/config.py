#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from pyowm.commons import exceptions
from pyowm.config import DEFAULT_CONFIG
from pyowm.commons.enums import SubscriptionTypeEnum


def get_config_from(path_to_file):
    """
    Loads configuration data from the supplied file and returns it.

    :param path_to_file: path to the configuration file
    :type path_to_file: str
    :returns: the configuration `dict`
    :raises: `ConfigurationNotFoundError` when the supplied filepath is not a regular file; `ConfigurationParseError`
        when the supplied file cannot be parsed
    """
    assert path_to_file is not None
    if not os.path.isfile(path_to_file):
        raise exceptions.ConfigurationNotFoundError(
            'Configuration file not found: {}'.format(path_to_file))
    with open(path_to_file, 'r') as cf:
        try:
            config_data = json.load(cf)
            config_data['subscription_type'] = SubscriptionTypeEnum.lookup_by_name(config_data['subscription_type'])
            return config_data
        except Exception:
            raise exceptions.ConfigurationParseError()


def get_default_config():
    """
    Returns the default PyOWM configuration.

    :returns: the configuration `dict`
    """
    return DEFAULT_CONFIG


def get_default_config_for_subscription_type(name):
    """
    Returns the PyOWM configuration for a specific OWM API Plan subscription type

    :param name: name of the subscription type
    :type name: str
    :returns: the configuration `dict`
    """
    assert isinstance(name, str)
    config = get_default_config()
    config['subscription_type'] = SubscriptionTypeEnum.lookup_by_name(name)
    return config


def get_default_config_for_proxy(http_url, https_url):
    """
    Returns the PyOWM configuration to be used behind a proxy server

    :param http_url: URL connection string for HTTP protocol
    :type http_url: str
    :param https_url: URL connection string for HTTPS protocol
    :type https_url: str
    :returns: the configuration `dict`
    """
    assert isinstance(http_url, str)
    assert isinstance(https_url, str)
    config = get_default_config()
    config['connection']['use_proxy'] = True
    config['proxies']['http'] = http_url
    config['proxies']['https'] = https_url
    return config
