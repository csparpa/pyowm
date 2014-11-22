"""
Module containing APICallError class
"""

import os


class APICallError(Exception):
    """
    Error class that represents failures when invoking OWM web API, in example
    due to network errors.

    :param message: the message of the error
    :type message: str
    :param triggering_error: optional *Exception* object that triggered this
        error (defaults to ``None``)
    :type triggering_error: an *Exception* subtype
    """
    def __init__(self, message, triggering_error=None):
        self._message = message
        self._triggering_error = triggering_error

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['Exception in calling OWM web API.', os.linesep,
                       'Reason: ', self._message.decode('utf-8'), os.linesep,
                       'Caused by: ', str(self._triggering_error)])
