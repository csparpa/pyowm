#!/usr/bin/env python

"""
URL building utilities
"""

from urllib import urlencode
from urllib2 import urlopen, HTTPError, URLError
from pyowm.exceptions import OWM_API_call_exception 


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
        response = urlopen(url)
    except HTTPError as e:
        raise OWM_API_call_exception(e.reason, e.code, e)
        return None
    except URLError as e:
        raise OWM_API_call_exception(e.message, e.code, e)
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
