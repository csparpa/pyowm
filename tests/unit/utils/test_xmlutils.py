"""
Test case for xmlutils.py module
"""

import unittest
import xml.etree.ElementTree as ET
from pyowm.utils import xmlutils


class TestXMLUtils(unittest.TestCase):

    def test_create_DOM_node_from_dict(self):
        d = {"a": 43.2, "b": None}
        name = "test"
        test_root_node = ET.Element("root")
        expected = "<root><test><a>43.2</a></test></root>"
        xmlutils.create_DOM_node_from_dict(d, name, test_root_node)
        result_DOM_tree = ET.ElementTree(test_root_node)
        self.assertEqual(expected, ET.tostring(result_DOM_tree.getroot(),
                                                encoding='utf8',
                                                method='html').decode('utf-8'))

    def test_create_DOM_node_from_dict_when_input_is_None(self):
        d = None
        name = "test"
        test_root_node = ET.Element("root")
        expected = "<root></root>"
        xmlutils.create_DOM_node_from_dict(d, name, test_root_node)
        result_DOM_tree = ET.ElementTree(test_root_node)
        self.assertEqual(expected, ET.tostring(result_DOM_tree.getroot(),
                                                encoding='utf8',
                                                method='html').decode('utf-8'))

    def test_DOM_node_to_XML(self):
        XML_declaration_line = "<?xml version='1.0' encoding='utf8'?>\n"
        expected = "<root><x><a>2</a><b>3</b></x></root>"
        test_root_node = ET.Element("root")
        test_child_node = ET.SubElement(test_root_node, "x")
        test_grand_child_node_1 = ET.SubElement(test_child_node, "a")
        test_grand_child_node_1.text = "2"
        test_grand_child_node_1 = ET.SubElement(test_child_node, "b")
        test_grand_child_node_1.text = "3"
        self.assertEqual(expected,
                          xmlutils.DOM_node_to_XML(test_root_node, False))
        self.assertEqual(XML_declaration_line + expected,
                          xmlutils.DOM_node_to_XML(test_root_node))

    def test_annotate_with_XMLNS_with_ElementTree_as_input(self):
        expected = '<root xmlns:p="http://test.com/schemas/f.xsd">' + \
                    '<p:c1><p:gc1>test</p:gc1></p:c1></root>'
        root_node = ET.Element("root")
        c1_node = ET.SubElement(root_node, "c1")
        gc1_node = ET.SubElement(c1_node, "gc1")
        gc1_node.text = "test"
        tree = ET.ElementTree(root_node)
        xmlutils.annotate_with_XMLNS(tree, 'p',
                                     'http://test.com/schemas/f.xsd')
        self.assertEqual(expected, xmlutils.DOM_node_to_XML(tree.getroot(),
                                                            False))

    def test_annotate_with_XMLNS_with_Element_as_input(self):
        expected = '<root xmlns:p="http://test.com/schemas/f.xsd">' + \
                    '<p:c1><p:gc1>test</p:gc1></p:c1></root>'
        root_node = ET.Element("root")
        c1_node = ET.SubElement(root_node, "c1")
        gc1_node = ET.SubElement(c1_node, "gc1")
        gc1_node.text = "test"
        xmlutils.annotate_with_XMLNS(root_node, 'p',
                                     'http://test.com/schemas/f.xsd')
        self.assertEqual(expected, xmlutils.DOM_node_to_XML(root_node, False))
