# -*- coding: utf-8 -*-

'''
Functional test for checking that external configuration modules can be
injected by the user and their values are correctly used
'''
import unittest
import pyowm
from api_key import API_KEY


class ConfigurationInjectionTestsWebAPI25(unittest.TestCase):

    _config_module_name = 'tests.functional.webapi25.external_configuration'
    _non_existent_config_module_name = 'this_will_never_be_a_config_module'

    def test(self):
        pyowm.OWM(API_KEY, '2.5', self._config_module_name)

    def test_library_is_instantiated_with_wrong_API_version(self):
        self.assertRaises(ValueError, pyowm.OWM, 'abcd', '0.0')

    def test_library_is_instantiated_with_external_config(self):
        """
        Test that library is smoothly instantiated also when injecting external
        configuration
        """
        try:
            pyowm.OWM(API_KEY, '2.5', self._config_module_name)
        except Exception:
            self.fail("Error raised during library instantiation")

    def test_error_raised_when_providing_non_existent_external_config(self):
        """
        Test that library instantiation raises an error when trying to inject
        a non-existent external configuration module
        """
        self.assertRaises(Exception, pyowm.OWM, API_KEY, '2.5',
                          self._non_existent_config_module_name)

    def test_library_performs_API_calls_with_external_config(self):
        """
        Test that API works correctly with external config values. For testing
        purposes, we do that by specifying None values for JSON parsers, which
        leads to errors raising
        """
        try:
            instance = \
                pyowm.OWM(API_KEY, '2.5',
                          self._config_module_name)
        except:
            self.fail("Error raised during library instantiation")
        self.assertRaises(Exception, instance.weather_at_place, 'London,uk')


if __name__ == "__main__":
    unittest.main()