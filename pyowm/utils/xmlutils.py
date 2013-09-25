#!/usr/bin/env python

"""
Module containing utility functions for generating XML strings
"""

def dict_to_XML(d):
    """
    Returns an XML representation of a plain Python dictionary, in example:
    {"a": 3, "b": "foo"}. The dictionary should not contain ``None`` values
    and nested dictionaries.
    :param d: the input dictionary
    :type d: dict
    :returns the XML string representation of the dictionary
    """
    return "".join(["<"+str(key)+">"+str(d[key])+"</"+str(key)+">" \
                    for key in d if d[key] is not None])


