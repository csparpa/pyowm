#!/usr/bin/env python
# -*- coding: utf-8 -*-

def obfuscate_API_key(API_key):
    """
    Return a mostly obfuscated version of the API Key

    :param API_key: input string
    :return: str
    """
    if API_key is not None:
        return (len(API_key)-8)*'*'+API_key[-8:]


def version_tuple_to_str(version_tuple, separator='.'):
    """
    Turns something like (X, Y, Z) into "X.Y.Z"
    :param version_tuple: the tuple identifying a software Semantic version
    :type version_tuple: tuple
    :param separator: the character to be used as separator
    :type separator: str, defaults to '.'
    :return: str
    """
    str_version_tuple = [str(v) for v in version_tuple]
    return separator.join(str_version_tuple)
