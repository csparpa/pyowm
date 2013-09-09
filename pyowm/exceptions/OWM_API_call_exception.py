#!/usr/bin/env python

class OWM_API_call_exception(Exception):
    """
    Exception that represents failures when invoking OWM web API.
    """    
    def __init__(self, message, error_code, raisable):
        """
        cause - the message of the exception (str)
        error_code - the related HTTP error status code
        raisable - the encapsulated lower-level exception
        """
        self.message = message
        self.error_code = error_code
        self.raisable = raisable
        
    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return 'Exception in calling OWM web API --- status code: %s --- reason: %s' % (self.error_code, self.message)