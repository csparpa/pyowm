#!/usr/bin/env python

class ParseResponseException(Exception):
    """
    Exception that represents failures when parsing responses sent by the 
    OWM web API.
    """    
    def __init__(self, message):
        """
        cause - the message of the exception (str)
        """
        self.message = message
        
    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return 'Exception in parsing OWM web API response. Reason: %s' % \
            self.message
        