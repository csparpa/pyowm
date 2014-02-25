#!/usr/bin/env python

"""
Module containing utility functions for generating XML strings
"""

import xml.etree.ElementTree as ET


def create_DOM_node_from_dict(d, name, parent_node):
    """
    Dumps dict data to an ``xml.etree.ElementTree.SubElement`` DOM subtree
    object and attaches it to the specified DOM parent node. The created
    subtree object is named after the specified name. No DOM node is generated
    for eventual ``None`` values found inside the dict

    :param d: the input dictionary
    :type d: dict
    :param name: the name for the DOM subtree to be created
    :type name: str
    :param parent_node: the parent DOM node the newly created subtree must be
        attached to
    :type parent_node: ``xml.etree.ElementTree.Element`` or derivative objects
    :returns: a ``xml.etree.ElementTree.SubElementTree`` object

    """
    root_dict_node = ET.SubElement(parent_node, name)
    for key, value in d.items():
        if value is not None:
            node = ET.SubElement(root_dict_node, key)
            node.text = str(value)
    return root_dict_node


def DOM_node_to_XML(node):
    """
    Prints a DOM node to its Unicode representation.

    :param node: the input DOM node
    :type node: an ``xml.etree.ElementTree.Element`` object
    :returns: a Unicode object

    """
    xml_chunk = ET.tostring(node, encoding='utf8', method='xml')
    result = xml_chunk.split("<?xml version='1.0' encoding='utf8'?>\n")[1]
    return unicode(result)
