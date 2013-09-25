#!/usr/bin/env python

"""
Module containing ParseResponseError class
"""

class ParseResponseError(Exception):
    """
    Error class that represents failures when parsing payload data in HTTP 
    responses sent by the OWM web API.
    
    :param cause: the message of the error
    :type cause: str
    :returns: a *ParseResponseError* instance
    """    
    def __init__(self, message):
        self._message = message
        
    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return 'Exception in parsing OWM web API response. Reason: %s' % \
            self._message
        