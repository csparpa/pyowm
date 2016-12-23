"""
Integration tests for checking PyOWM caching features
"""

import unittest
import os
from time import time
from pyowm.constants import DEFAULT_API_KEY
from pyowm.webapi25.configuration25 import parsers
from pyowm.webapi25.owm25 import OWM25
from pyowm.caches.lrucache import LRUCache
from pyowm.abstractions.owmcache import OWMCache


class CacheWrapper(OWMCache):
    """
    Wrapper class whose aim is to track down real API calls and cache hits.
    """
    def __init__(self, cache):
        self._cache = cache
        self.__api_calls = 0
        self.__last_request_was_hit = False

    def get(self, request_url):
        result = self._cache.get(request_url)
        if result:
            self.__last_request_was_hit = True
        else:
            self.__last_request_was_hit = False
            self.__api_calls += 1
        return result

    def set(self, request_url, response_json):
        return self._cache.set(request_url, response_json)

    def last_request_was_hit(self):
        return self.__last_request_was_hit

    def api_calls(self):
        return self.__api_calls


class CacheTestWebAPI25(unittest.TestCase):

    API_KEY = os.getenv('OWM_API_KEY', DEFAULT_API_KEY)

    def test_caching_prevents_API_calls(self):
        cache = LRUCache(20, 1000 * 60 * 60)
        wrapped_cache = CacheWrapper(cache)
        owm = OWM25(parsers, self.API_KEY, wrapped_cache)
        self.assertFalse(wrapped_cache.last_request_was_hit())
        self.assertEqual(0, wrapped_cache.api_calls())
        owm.weather_at_place('London,uk')  # Comes from OWM web API
        self.assertFalse(wrapped_cache.last_request_was_hit())
        self.assertEqual(1, wrapped_cache.api_calls())
        owm.weather_at_place('London,uk')  # Comes from cache
        self.assertTrue(wrapped_cache.last_request_was_hit())
        self.assertEqual(1, wrapped_cache.api_calls())
        owm.weather_at_place('London,uk')  # Comes from cache again
        self.assertTrue(wrapped_cache.last_request_was_hit())
        self.assertEqual(1, wrapped_cache.api_calls())
        owm.weather_at_place('Kiev')       # Comes from OWM web API
        self.assertFalse(wrapped_cache.last_request_was_hit())
        self.assertEqual(2, wrapped_cache.api_calls())
        owm.weather_at_place('Kiev')       # Comes from cache
        self.assertTrue(wrapped_cache.last_request_was_hit())
        self.assertEqual(2, wrapped_cache.api_calls())
        owm.weather_at_place('London,uk')  # Comes from cache
        self.assertTrue(wrapped_cache.last_request_was_hit())
        self.assertEqual(2, wrapped_cache.api_calls())

    def test_cache_limits(self):
        """
        Test that when cache is full, cached elements undergo a turnover and
        the real OWM web API is invoked
        """
        cache = LRUCache(3, 1000 * 60 * 60)  # Only three cacheable elements!
        wrapped_cache = CacheWrapper(cache)
        owm = OWM25(parsers, self.API_KEY, wrapped_cache)
        owm.weather_at_place('London,uk')  # Comes from OWM web API
        owm.weather_at_place('Kiev')       # Comes from OWM web API
        owm.weather_at_place('Madrid')     # Comes from OWM web API
        self.assertEqual(3, wrapped_cache.api_calls())
        owm.weather_at_place('London,uk')  # Comes from cache
        owm.weather_at_place('Kiev')  # Comes from cache
        self.assertEqual(3, wrapped_cache.api_calls())
        owm.weather_at_place('Tokyo')
        self.assertEqual(4, wrapped_cache.api_calls())
        owm.weather_at_place('Madrid')  # Now Madrid should have been pulled out of cache
        self.assertEqual(5, wrapped_cache.api_calls())

    def test_caching_times(self):
        """
        Test that subsequent calls to the same endpoint and with the same
        query parameters are cached if OWM instance is configured with a 
        non-null cache.
        """
        cache = LRUCache(20, 1000 * 60 * 60)
        owm = OWM25(parsers, self.API_KEY, cache)
        before_request = time()
        o1 = owm.weather_at_place('London,uk')  # Comes from OWM web API
        after_request = time()
        o2 = owm.weather_at_place('London,uk')  # Comes from cache
        after_cache_hit_1 = time()
        owm.weather_at_place('Kiev')       # Comes from OWM web API
        owm.weather_at_coords(-33.936524, 18.503723)  # Comes from OWM web API
        owm.weather_at_coords(-33.936524, 18.503723)  # Cached, we don't care
        owm.weather_at_coords(-33.936524, 18.503723)  # Cached, we don't care
        before_cache_hit_2 = time()
        o3 = owm.weather_at_place('London,uk')  # Comes from cache
        after_cache_hit_2 = time()
        #Check results: difference in reception time should not be less than 20 sec
        self.assertAlmostEquals(o1.get_reception_time(),
                                o2.get_reception_time(),
                                places=None, msg=None, delta=20)
        self.assertAlmostEquals(o1.get_reception_time(),
                                o3.get_reception_time(),
                                places=None, msg=None, delta=20)
        #Check times: all cache hit times must be less than the former OWM web
        #API request time and ratio between cache hit times and request time
        #should be far less than 1
        req_delay = after_request - before_request
        cache_hit_1_delay = after_cache_hit_1 - after_request
        cache_hit_2_delay = after_cache_hit_2 - before_cache_hit_2
        self.assertTrue(cache_hit_1_delay < req_delay)
        self.assertTrue(cache_hit_2_delay < req_delay)
        self.assertTrue(cache_hit_1_delay / req_delay < 1)
        self.assertTrue(cache_hit_2_delay / req_delay < 1)


if __name__ == "__main__":
    unittest.main()