"""
Test case for nullowmcache.py module.
"""

import unittest
from pyowm.caches.nullcache import NullCache


class TestNullCache(unittest.TestCase):

    def test_get_always_returns_null(self):
        instance = NullCache()
        self.assertFalse(instance.get("abcdefghi"))
