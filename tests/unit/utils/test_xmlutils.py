#!/usr/bin/env python

"""
Test case for xmlutils.py module
"""

import unittest
import xml.etree.ElementTree as ET
from pyowm.utils import xmlutils


class TestXMLUtils(unittest.TestCase):

    def test_create_DOM_node_from_dict(self):
        d = {"a": 43.2, "b": None, "c": 3, "d": "try"}
        name = "test"
        test_root_node = ET.Element("root")
        expected = "<root><test><a>43.2</a><c>3</c><d>try</d></test></root>"
        xmlutils.create_DOM_node_from_dict(d, name, test_root_node)
        result_DOM_tree = ET.ElementTree(test_root_node)
        self.assertEquals(expected, ET.tostring(result_DOM_tree.getroot(),
                                                encoding='utf8',
                                                method='html'))

    def test_create_DOM_node_from_dict_when_input_is_None(self):
        d = None
        name = "test"
        test_root_node = ET.Element("root")
        expected = "<root></root>"
        xmlutils.create_DOM_node_from_dict(d, name, test_root_node)
        result_DOM_tree = ET.ElementTree(test_root_node)
        self.assertEquals(expected, ET.tostring(result_DOM_tree.getroot(),
                                                encoding='utf8',
                                                method='html'))

    def test_DOM_node_to_XML(self):
        expected = "<root><x><a>2</a><b>3</b></x></root>"
        test_root_node = ET.Element("root")
        test_child_node = ET.SubElement(test_root_node, "x")
        test_grand_child_node_1 = ET.SubElement(test_child_node, "a")
        test_grand_child_node_1.text = "2"
        test_grand_child_node_1 = ET.SubElement(test_child_node, "b")
        test_grand_child_node_1.text = "3"
        result = xmlutils.DOM_node_to_XML(test_root_node)
        self.assertEquals(expected, result)


if __name__ == "__main__":
    unittest.main()
