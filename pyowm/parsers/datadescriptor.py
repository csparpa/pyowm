#!/usr/bin/env python

"""
Module containing PyOWM entities data description abstractions. 
"""

class DataDescriptor(object):
    """
    Abstract framework class that models a descriptor for the data contained into
    a PyOWM object. This class shall be subclassed in order to provide
    descriptions of concrete PyOWM object types.

    """
    def __init__(self):
        if self.__class__ is DataDescriptor:
            raise TypeError("This class is abstract and cannot be instantiated")

    def description(self):
        """
        Abstract method: implementations should return a ``dict`` containing
        as keys the name of the object's properties and as values the path
        where they can be found into the JSON payload of the OWM web API response.
        
        :returns: a ``dict`` mapping object's properties to the path of the 
        correspondent values into the OWM web API JSON payload
        
        """
        raise NotImplementedError("This method is abstract and must be implemented")