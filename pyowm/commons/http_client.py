from pyowm.exceptions import api_call_error, unauthorized_error, not_found_error


class HttpClient(object):

    @classmethod
    def check_status_code(cls, status_code, payload):
        if status_code < 400:
            return
        if status_code == 401:
            raise unauthorized_error.UnauthorizedError('Invalid API Key provided')
        elif status_code == 404:
            raise not_found_error.NotFoundError('Unable to find the resource')
        elif status_code == 502:
            raise api_call_error.BadGatewayError('Unable to contact the upstream server')
        else:
            raise api_call_error.APICallError(payload)
