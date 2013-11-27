'''
Functional tests for the PyOWM library
These are "live" executions, that of course need the OWM web API to be up
and running
'''
import unittest
from time import time
from pyowm.webapi25.configuration25 import parsers
from pyowm.webapi25.owm25 import OWM25
from pyowm.caches.lrucache import LRUCache

class IntegrationTest(unittest.TestCase):
    
    # LRU cache with 20 items and 1 hour expiration time
    __owm = OWM25(parsers, '5746e1a976021a0', LRUCache(20, 1000*60*60))
    
    def test_caching_times(self):
        """
        Test that subsequent calls to the same endpoint and with the same
        query parameters are cached if OWM instance is configured with a 
        non-null cache.
        """
        before_request = time()
        o1 = self.__owm.weather_at('London,uk')  # Comes from OWM web API
        after_request = time()
        o2 = self.__owm.weather_at('London,uk')  # Comes from cache
        after_cache_hit_1 = time()
        self.__owm.weather_at('Kiev')       # Comes from OWM web API
        self.__owm.weather_at_coords(18.503723,-33.936524)  # Comes from OWM web API
        self.__owm.weather_at_coords(18.503723,-33.936524)  # Cached, we don't care
        self.__owm.weather_at_coords(18.503723,-33.936524)  # Cached, we don't care
        before_cache_hit_2 = time()
        o3 = self.__owm.weather_at('London,uk')  # Comes from cache
        after_cache_hit_2 = time()
        #Check results: difference in reception time should not be less than 10 sec
        self.assertAlmostEquals(o1.get_reception_time(), o2.get_reception_time(), places=None, msg=None, delta=20)
        self.assertAlmostEquals(o1.get_reception_time(), o3.get_reception_time(), places=None, msg=None, delta=20)
        
        #Check times: all cache hit times must be less than the former OWM web
        #API request time and ratio between cache hit times and request time
        #should be much less than 1
        req_delay = after_request - before_request
        cache_hit_1_delay = after_cache_hit_1 - after_request
        cache_hit_2_delay = after_cache_hit_2 - before_cache_hit_2
        self.assertTrue(cache_hit_1_delay < req_delay)
        self.assertTrue(cache_hit_2_delay < req_delay)
        self.assertTrue(cache_hit_1_delay/req_delay < 1)
        self.assertTrue(cache_hit_2_delay/req_delay < 1)