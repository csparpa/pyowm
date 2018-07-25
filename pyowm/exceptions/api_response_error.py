"""
Module containing APIResponseError class
"""

import os
from pyowm.exceptions import OWMError


class APIResponseError(OWMError):
    """
    Error class that represents HTTP error status codes in OWM web API
    responses.

    :param cause: the message of the error
    :type cause: str
    :param status_code: the HTTP error status code
    :type status_code: int
    :returns: a *APIResponseError* instance
    """
    def __init__(self, cause, status_code):
        self._message = cause
        self.status_code = status_code

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['HTTP status code %s was returned by the OWM API' % str(self.status_code), os.linesep, 'Reason: ',
                        self._message])


class NotFoundError(APIResponseError):
    """
    Error class that represents the situation when an entity is not found into
    a collection of entities.

    :param cause: the message of the error
    :type cause: str
    :param status_code: the HTTP error status code
    :type status_code: int
    :returns: a *NotFoundError* instance
    """
    def __init__(self, cause, status_code=404):
        self._message = cause
        self.status_code = status_code

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['The searched item was not found.', os.linesep,
                        'Reason: ', self._message])


class UnauthorizedError(APIResponseError):
    """
    Error class that represents the situation when an entity cannot be retrieved
    due to user subscription unsufficient capabilities.

    :param cause: the message of the error
    :type cause: str
    :param status_code: the HTTP error status code
    :type status_code: int
    :returns: a *UnauthorizedError* instance
    """
    def __init__(self, cause, status_code=403):
        self._message = cause
        self._status_code = status_code

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['Your API subscription level does not allow to perform '
                        'this operation', os.linesep,
                        'Reason: ', self._message])