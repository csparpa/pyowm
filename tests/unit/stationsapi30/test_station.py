import unittest
from pyowm.stationsapi30.station import Station


class TestStation(unittest.TestCase):

    def test_failing_instantiations(self):
        with self.assertRaises(AssertionError):
            Station(None,
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -122.43, 37.76, 150, 0)
        with self.assertRaises(AssertionError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    None,
                    "San Francisco Test Station",
                    -122.43, 37.76, 150, 0)
        with self.assertRaises(AssertionError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    None, 37.76, 150, 0)
        with self.assertRaises(AssertionError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -122.43, None, 150, 0)
        with self.assertRaises(AssertionError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -122.43, 37.76, None, 0)

    def test_instantiations_failing_upon_wrong_geocoords(self):
        with self.assertRaises(ValueError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -422.43, 37.76, 150, 0)
        with self.assertRaises(ValueError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -122.43, -97.76, 150, 0)
        with self.assertRaises(ValueError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -122.43, 37.76, -56.9, 0)
