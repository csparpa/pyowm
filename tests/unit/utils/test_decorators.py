#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import warnings
from pyowm.utils import decorators


class TestDecorators(unittest.TestCase):

    def test_deprecated_decorator(self):

        @decorators.deprecated()
        def warn_function_no_args():
            pass

        with warnings.catch_warnings(record=True) as cm:
            self.assertEqual(len(cm), 0)
            warn_function_no_args()
            self.assertEqual(len(cm), 1)
            self.assertTrue(issubclass(cm[-1].category, DeprecationWarning))

        action = 'modified'
        version = (7, 2, 0)
        name = 'test_name'

        @decorators.deprecated(will_be=action, on_version=version, name=name)
        def warn_function_all_args():
            pass

        with warnings.catch_warnings(record=True) as cm:
            self.assertEqual(len(cm), 0)
            warn_function_all_args()
            self.assertEqual(len(cm), 1)
            self.assertTrue(issubclass(cm[-1].category, DeprecationWarning))
            logged_line = cm[-1].message.args[0]
            self.assertIn(action, logged_line)
            self.assertIn('.'.join(map(str, version)), logged_line)
            self.assertIn(name, logged_line)
