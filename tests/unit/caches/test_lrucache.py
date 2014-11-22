"""
Test case for lrucache.py module.
"""

import unittest
from time import sleep
from pyowm.caches.lrucache import LRUCache


class TestLRUCache(unittest.TestCase):

    __test_url = "http://test.com/path?param=value"
    __test_data = "test_data"

    def test_miss_getting_old_items(self):
        instance = LRUCache(3, 1)  # 1 millisecond lifetime for cache items
        instance.set(self.__test_url, self.__test_data)
        cache_size = instance.size()
        sleep(2)  # wait 2 seconds
        result = instance.get(self.__test_url)
        self.assertFalse(result)
        self.assertEqual(cache_size - 1, instance.size())

    def test_hit_when_getting_freshly_inserted_items(self):
        instance = LRUCache(3, 1000 * 60 * 60)  # 1 hour lifetime for items
        instance.set(self.__test_url, self.__test_data)
        result = instance.get(self.__test_url)
        self.assertEqual(self.__test_data, result)

    def test_set_cache_item(self):
        instance = LRUCache(3, 1000 * 60 * 60)  # 1 hour lifetime for items
        cache_size = instance.size()
        ref_to_original_set = LRUCache.set
        instance.set(self.__test_url, self.__test_data)
        LRUCache.set = ref_to_original_set
        self.assertEqual(cache_size + 1, instance.size())
        result = instance.get(self.__test_url)
        self.assertEqual(self.__test_data, result)

    def test_cache_max_size_preserved_when_setting(self):
        instance = LRUCache(3, 1000 * 60 * 60)  # max 3 items
        instance.set("1", "aaa")
        instance.set("2", "bbb")
        instance.set("3", "ccc")
        cache_size = instance.size()
        instance.set("4", "ddd")
        self.assertEqual(cache_size, instance.size())

    def test_clean_cache(self):
        instance = LRUCache(3, 1000 * 60 * 60)  # max 3 items
        instance.set("1", "aaa")
        instance.set("2", "bbb")
        instance.set("3", "ccc")
        self.assertEqual(3, instance.size())
        instance.clean()
        self.assertEqual(0, instance.size())

    def test_insert_already_cached_item(self):
        instance = LRUCache(3, 1000 * 60 * 60)  # max 3 items
        instance.set("1", "aaa")
        instance.set("2", "bbb")
        self.assertEqual(2, instance.size())
        most_recent_cache_item = instance._usage_recency._first_node
        instance.set("1", "aaa")
        self.assertEqual(2, instance.size())
        result = instance._usage_recency._first_node
        self.assertNotEqual(most_recent_cache_item, result)