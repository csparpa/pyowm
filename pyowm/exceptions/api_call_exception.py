#!/usr/bin/env python

class APICallException(Exception):
    """
    Exception that represents failures when invoking OWM web API.
    """    
    def __init__(self, message, raisable):
        """
        cause - the message of the exception (str)
        raisable - the encapsulated lower-level exception
        """
        self.message = message
        self.raisable = raisable
        
    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return 'Exception in calling OWM web API. Reason: %s' % self.message