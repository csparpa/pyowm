#!/usr/bin/env python

"""
URL building utilities
"""

import urllib2
from urllib import urlencode
from pyowm.exceptions import api_call_exception 


def call_API(API_subset_URL, params_dict, API_key):
    
    """
    Invokes a specific OWM web API subset, returning raw JSON data as a str
        API_subset_URL - spots the API subset to be invoked
        params_dict - the query parameters to be used
        API_key - the OWM API key
    """

    # Build full API subset URL
    url = build_full_URL(API_subset_URL, params_dict, API_key)
    
    # HTTP GET data
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        raise api_call_exception.APICallException(e.reason, e)
        return None
    except urllib2.URLError as e:
        raise api_call_exception.APICallException(e.message, e)
        return None
    else:
        return response.read()
    
def build_full_URL(API_subset_URL, params_dict, API_key):
    params = params_dict.copy()
    if API_key is not None:
        params['APPID'] = API_key
    return build_query_parameters(API_subset_URL, params)


def build_query_parameters(base_URL, params_dict):
    """Turns dictionary items into query params and adds them to the base URL"""
    return base_URL + '?' + urlencode(params_dict)
