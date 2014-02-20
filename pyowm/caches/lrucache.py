#!/usr/bin/env python

"""
Module containing LRU cache related class
"""

from datetime import datetime
from pyowm.abstractions.owmcache import OWMCache
from pyowm.commons.frontlinkedlist import FrontLinkedList
from pyowm.utils.converter import to_UNIXtime


class LRUCache(OWMCache):
    """
    This cache is made out of a 'table' dict and the 'usage_recency' linked
    list.'table' maps uses requests' URLs as keys and stores JSON raw responses
    as values. 'usage_recency' tracks down the "recency" of the OWM web API
    requests: the more recent a request, the more the element will be far from
    the "death" point of the recency list. Items in 'usage_recency' are the
    requests' URLs themselves.
    The implemented LRU caching mechanism is the following:

    - cached elements must expire after a certain time passed into the cache.
      So when an element is looked up and found in the cache, its insertion
      timestamp is compared to the current one: if the difference is higher
      than a prefixed value, then the lookup is considered a MISS: the
      element is removed either from 'table' and from 'usage_recency' and must
      be requested again to the OWM web API. If the time difference is ok,
      then the lookup is considered a HIT.
    - when a GET results in a HIT, promote the element to the front of the
      recency list updating its cache insertion timestamp and return the
      data to the cache clients
    - when a GET results in a MISS, return ``None``
    - when a SET is issued, check if the maximum size of the cache has
      been reached: if so, discard the least recently used item from the
      recency list and the dict; then add the element to 'table' recording its
      timestamp and finally add it at the front of the recency list.

    :param cache_max_size: the maximum size of the cache in terms of cached
        OWM web API responses. A reasonable default value is provided.
    :type cache_max_size: int
    :param item_lifetime_millis: the maximum lifetime allowed for a cache item
        in milliseconds. A reasonable default value is provided.
    :type item_lifetime_millis: int
    :returns: a new *LRUCache* instance

    """

    __CACHE_MAX_SIZE = 20  # Maximum number of elements that fit the cache
    __ITEM_LIFETIME_MILLISECONDS = 1000*60*10  # Ten minutes

    def __init__(self, cache_max_size=__CACHE_MAX_SIZE,
                 item_lifetime_millis=__ITEM_LIFETIME_MILLISECONDS):
        assert cache_max_size > 0 and item_lifetime_millis > 0, "wrong cache" \
            " init parameters"
        self.__table = {}
        self.__usage_recency = FrontLinkedList()
        self.__max_size = cache_max_size
        self.__item_lifetime = item_lifetime_millis

    def get(self, request_url):
        """
        In case of a hit, returns the JSON string which represents the OWM web
        API response to the request being identified by a specific string URL
        and updates the recency of this request.

        :param request_url: an URL that uniquely identifies the request whose
            response is to be looked up
        :type request_url: str
        :returns: a JSON str in case of cache hit or ``None`` otherwise

        """
        try:
            cached_item = self.__table[request_url]
            curr_time = to_UNIXtime(datetime.now())
            if curr_time - cached_item['insertion_time'] > self.__item_lifetime:
                # Cache item has expired
                self.__clean_item(request_url)
                return None
            cached_item['insertion_time'] = curr_time  # Update insertion time
            self.__promote(request_url)
            return cached_item['data']
        except:
            return None

    def set(self, request_url, response_json):
        """
        Checks if the maximum size of the cache has been reached and in case
        discards the least recently used item from 'usage_recency' and 'table';
        then adds the response_json to be cached to the 'table' dict using as
        a lookup key the request_url of the request that generated the value;
        finally adds it at the front of 'usage_recency'

        :param request_url: the request URL that uniquely identifies the
            request whose response is to be cached
        :type request_url: str
        :param response_json: the response JSON to be cached
        :type response_json: str

        """
        if (self.size() == self.__max_size):
            popped = self.__usage_recency.pop()
            del self.__table[popped]
        current_time = to_UNIXtime(datetime.now())
        if request_url not in self.__table:
            self.__table[request_url] = {'data': response_json,
                                         'insertion_time': current_time}
            self.__usage_recency.add(request_url)
        else:
            self.__table[request_url]['insertion_time'] = current_time
            self.__promote(request_url)

    def __promote(self, request_url):
        """
        Moves the cache item specified by request_url to the front of the
        'usage_recency' list
        """
        self.__usage_recency.remove(request_url)
        self.__usage_recency.add(request_url)

    def __clean_item(self, request_url):
        """
        Removes the specified item from the cache's datastructures

        :param request_url: the request URL
        :type request_url: str

        """
        del self.__table[request_url]
        self.__usage_recency.remove(request_url)

    def clean(self):
        """
        Empties the cache

        """
        self.__table.clear()
        for item in self.__usage_recency:
            self.__usage_recency.remove(item)

    def size(self):
        """
        Returns the number of elements that are currently stored into the cache

        :returns: an int

        """
        return len(self.__table)

    def __repr__(self):
        return "<%s.%s - size=%s, max size=%s, item lifetime=%s>" % \
            (__name__, self.__class__.__name__, str(self.size()),
             self.__max_size, self.__item_lifetime)
