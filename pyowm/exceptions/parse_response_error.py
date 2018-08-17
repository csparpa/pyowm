"""
Module containing ParseResponseError class
"""
import os
from pyowm.exceptions import OWMError


class ParseResponseError(OWMError):
    """
    Error class that represents failures when parsing payload data in HTTP
    responses sent by the OWM Weather API.

    :param cause: the message of the error
    :type cause: str
    :returns: a *ParseResponseError* instance
    """
    def __init__(self, cause):
        self._message = cause

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['Exception in parsing OWM Weather API response',
                        os.linesep, 'Reason: ', self._message])
