# Exceptions

PyOWM uses custom exception classes. Here you can learn which classes are used and when such exceptions are cast by the library

## Exceptions Hierarchy

```
Exception
|
|___PyOWMError
    |
    |___ConfigurationError
    |   |
    |   |__ConfigurationNotFoundError
    |   |__ConfigurationParseError
    |
    |___APIRequestError
    |   |
    |   |__BadGatewayError
    |   |__TimeoutError
    |   |__InvalidSSLCertificateError
    |
    |___APIResponseError
        |
        |__NotFoundError
        |__UnauthorizedError
        |__ParseAPIResponseError
```

## Exception root causes

  * `PyOWMError` is the base class. Never raised directly
  * `ConfigurationError` parent class for configuration-related exceptions. Never raised directly
  * `ConfigurationNotFoundError` raised when trying to load configuration from a non-existent file
  * `ConfigurationParseError` raised when configuration can be loaded from the file but is in a wrong, unparsable format
  * `APIRequestError` base class for network/infrastructural issues when invoking OWM APIs
  * `BadGatewayError` raised when upstream OWM API backends suffer communication issues.
  * `TimeoutError` raised when calls to the API suffer timeout due to slow response times upstream
  * `InvalidSSLCertificateError` raised when it is impossible to verify the SSL certificates provided by the OWM APIs  
  * `APIResponseError` base class for non-ok API responses from OWM APIs
  * `NotFoundError` raised when the user tries to access resources that do not exist on the OWM APIs
  * `UnauthorizedError` raised when the user tries to access resources she is not authorized to access (eg. you need a paid API subscription)
  * `ParseAPIResponseError` raised upon impossibility to parse the JSON payload of API responses



