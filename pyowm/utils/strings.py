#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib


def obfuscate_API_key(API_key):
    """
    Return a mostly obfuscated version of the API Key

    :param API_key: input string
    :return: str
    """
    if API_key is not None:
        return (len(API_key)-8)*'*'+API_key[-8:]


def class_from_dotted_path(dotted_path):
    """
    Loads a Python class from the supplied Python dot-separated class path.
    The class must be visible according to the PYTHONPATH variable contents.
    Eg: "package.subpackage.module.MyClass" --> MyClass

    :param dotted_path: the dot-separated path of the class
    :type dotted_path: str
    :return: a `type` object
    """
    assert isinstance(dotted_path, str), 'A string must be provided'
    tokens = dotted_path.split('.')
    modpath, class_name = '.'.join(tokens[:-1]), tokens[-1]
    return getattr(importlib.import_module(modpath), class_name)
