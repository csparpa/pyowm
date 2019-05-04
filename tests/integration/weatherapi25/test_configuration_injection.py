#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import pyowm
from pyowm.config import DEFAULT_CONFIG


class ConfigurationInjectionTestsWebAPI25(unittest.TestCase):

    _config_module_name = 'tests.integration.weatherapi25.external_configuration'
    _non_existent_config_module_name = 'this_will_never_be_a_config_module'
    API_KEY = os.getenv('OWM_API_KEY', DEFAULT_CONFIG['api_key'])

    def test(self):
        pyowm.OWM(self.API_KEY, (2, 5, 0), self._config_module_name)

    def test_library_is_instantiated_with_wrong_API_version(self):
        self.assertRaises(ValueError, pyowm.OWM, 'abcd', '0.0')

    def test_library_is_instantiated_with_external_config(self):
        """
        Test that library is smoothly instantiated also when injecting external
        configuration
        """
        try:
            pyowm.OWM(self.API_KEY, (2, 5, 0), self._config_module_name)
        except Exception:
            self.fail("Error raised during library instantiation")

    def test_error_raised_when_providing_non_existent_external_config(self):
        """
        Test that library instantiation raises an error when trying to inject
        a non-existent external configuration module
        """
        self.assertRaises(Exception, pyowm.OWM, self.API_KEY, '2.5',
                          self._non_existent_config_module_name)


if __name__ == "__main__":
    unittest.main()