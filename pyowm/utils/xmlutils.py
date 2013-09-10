#!/usr/bin/env python

"""
XML formatting utilities
"""

def dict_to_XML(d):
    """
    Returns an XML representation of a plain Python dictionary
    """
    return "".join(["<"+str(key)+">"+str(d[key])+"</"+str(key)+">" for key in d if d[key] is not None])


