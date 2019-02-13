import unittest
from pyowm.utils import config
from pyowm.exceptions import config_error


class TesIntegrationConfig(unittest.TestCase):

    def test_get_config_from(self):
        path = 'test_config.json'
        result = config.get_config_from(path)
        self.assertIsInstance(result, dict)

        path = 'non_json'
        self.assertRaises(config_error.ConfigurationParseError, config.get_config_from, path)


if __name__ == "__main__":
    unittest.main()
