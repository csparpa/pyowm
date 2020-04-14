#!/usr/bin/env python
# -*- coding: utf-8 -*-


class PyOWMError(Exception):
    """Generic base class for PyOWM exceptions"""
    pass


class ConfigurationError(PyOWMError):
    """Generic base class for configuration related errors"""
    pass


class ConfigurationNotFoundError(ConfigurationError):
    """Raised when configuration source file is not available"""
    pass


class ConfigurationParseError(ConfigurationError):
    """Raised on failures in parsing configuration data"""
    pass


class APIRequestError(PyOWMError):
    """
    Error class that represents network/infrastructural failures when invoking OWM Weather API, in
    example due to network errors.
    """
    pass


class BadGatewayError(APIRequestError):
    """
    Error class that represents 502 errors - i.e when upstream backend
    cannot communicate with API gateways.
    """
    pass


class TimeoutError(APIRequestError):
    """
    Error class that represents response timeout conditions
    """
    pass


class InvalidSSLCertificateError(APIRequestError):
    """
    Error class that represents failure in verifying the SSL certificate provided
    by the OWM API
    """
    pass


class APIResponseError(PyOWMError):
    """
    Generic base class for exceptions representing HTTP error status codes in OWM Weather API
    responses
    """
    pass


class NotFoundError(APIResponseError):
    """
    Error class that represents the situation when an entity is not found.
    """
    pass


class UnauthorizedError(APIResponseError):
    """
    Error class that represents the situation when an entity cannot be retrieved
    due to user subscription insufficient capabilities.
    """
    pass


class ParseAPIResponseError(PyOWMError):
    """
    Error class that represents failures when parsing payload data in HTTP
    responses sent by the OWM Weather API.
    """
    pass
