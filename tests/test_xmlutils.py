#!/usr/bin/env python

"""
Test case for xmlutils.py module
"""

import unittest
from pyowm.utils import xmlutils


class Test(unittest.TestCase):


    def test_dict_to_XML(self):
        d = {"a": 43.2, "b": "test", "c": 3 }
        expected = "<a>43.2</a><c>3</c><b>test</b>"
        self.assertEqual(xmlutils.dict_to_XML(d), expected, "")


if __name__ == "__main__":
    unittest.main()