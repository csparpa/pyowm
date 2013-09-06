#!/usr/bin/env python

"""
Test case for observation.py module
"""

import unittest
from pyowm import Location

class Test(unittest.TestCase):

    testReceptionTime = 1234567
    testLocation = Location('test', 12.3, 43.7, 987)
    #testWeather 


if __name__ == "__main__":
    unittest.main()