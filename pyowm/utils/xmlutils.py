#!/usr/bin/env python

"""
Module containing utility functions for generating XML strings
"""


def make_tag(tag_name, tag_content):
    """
    Returns an XML string containing a tag having the specified name and
    content. If tag content is ``None``, then an empty tag is created; when tag
    name is ``None`` a *ValueError* is raised.

    :param tag_name: the tag name
    :type tag_name: str
    :param tag_content: the input dictionary
    :type tag_content: any string-convertible data
    :raises: *ValueError* when tag name is ``None``

    """
    if tag_name is None:
        raise ValueError
    if tag_content is None:
        tag_content = ""
    return "".join(["<", str(tag_name), ">", str(tag_content), "</",
                    str(tag_name), ">"])


def dict_to_XML(d):
    """
    Returns an XML representation of a plain Python dictionary, in example:
    {"a": 3, "b": "foo"}. The dictionary should not contain ``None`` values
    and nested dictionaries.

    :param d: the input dictionary
    :type d: dict
    :returns: the XML string representation of the dictionary

    """
    return "".join([make_tag(key, d[key]) for key in d if d[key] is not None])
