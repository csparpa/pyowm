#!/usr/bin/env python

"""
Module containing utility functions for HTTP client/server interactions
"""

import urllib2
from urllib import urlencode
from pyowm.exceptions import api_call_error


def call_API(API_endpoint_URL, params_dict, API_key):
    
    """
    Invokes a specific OWM web API endpoint URL, returning raw JSON data.
    The functionality is built on the top of Python's ``urllib2`` library.
    
    :param API_endpoint_URL: the API endpoint to be invoked
    :type API_endpoint_URL: str
    :param params_dict: a dictionary containing the query parameters to be used
        in the HTTP request (given as key-value couples in the dict)
    :type params_dict: dict
    :param API_key: the OWM web API key
    :type API_key: str
    :returns: a string containing raw JSON data
    :raises: *APICallError* in chain to exceptions raised by ``urllib2``
    
    """
    # Build full HTTP request URL
    url = build_full_URL(API_endpoint_URL, params_dict, API_key)
    
    # HTTP GET data
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        raise api_call_error.APICallError(e.reason, e)
    except urllib2.URLError as e:
        raise api_call_error.APICallError(e.message, e)
    else:
        return response.read()
    
def build_full_URL(API_endpoint_URL, params_dict, API_key):
    """
    Adds the API key and the query parameters dictionary to the specified API 
    endpoint URL, returning a complete HTTP request URL.
    
    :param API_endpoint_URL: the API endpoint base URL
    :type API_endpoint_URL: str
    :param params_dict: a dictionary containing the query parameters to be used
        in the HTTP request (given as key-value couples in the dict)
    :type params_dict: dict
    :param API_key: the OWM web API key
    :type API_key: str
    :returns: a full string HTTP request URL
    
    """
    params = params_dict.copy()
    if API_key is not None:
        params['APPID'] = API_key
    return build_query_parameters(API_endpoint_URL, params)


def build_query_parameters(base_URL, params_dict):
    """
    Turns dictionary items into query parameters and adds them to the base URL
    
    :param base_URL: the base URL whom the query parameters must be added to
    :type base_URL: str
    :param params_dict: a dictionary containing the query parameters to be used
        in the HTTP request (given as key-value couples in the dict)
    :type params_dict: dict
    :returns: a full string HTTP request URL
    
    """
    return base_URL + '?' + urlencode(params_dict)
