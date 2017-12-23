import requests
from pyowm.exceptions import api_call_error, unauthorized_error, not_found_error, \
    parse_response_error


class HttpClient(object):

    def get_json(self, uri, params=None, headers=None):
        resp = requests.get(uri, params=params, headers=headers)
        HttpClient.check_status_code(resp.status_code, resp.text)
        try:
            return resp.status_code, resp.json()
        except:
            raise parse_response_error.ParseResponseError('Impossible to parse'
                                                          'API response data')

    def post(self, uri, params=None, data=None, headers=None):
        resp = requests.post(uri, params=params, json=data, headers=headers)
        HttpClient.check_status_code(resp.status_code, resp.text)
        # this is a defense against OWM API responses cointaining an empty body!
        try:
            json_data = resp.json()
        except:
            json_data = {}
        return resp.status_code, json_data

    def put(self, uri, params=None, data=None, headers=None):
        resp = requests.put(uri, params=params, json=data, headers=headers)
        HttpClient.check_status_code(resp.status_code, resp.text)
        # this is a defense against OWM API responses cointaining an empty body!
        try:
            json_data = resp.json()
        except:
            json_data = {}
        return resp.status_code, json_data

    def delete(self, uri, params=None, data=None, headers=None):
        resp = requests.delete(uri, params=params, json=data, headers=headers)
        HttpClient.check_status_code(resp.status_code, resp.text)
        # this is a defense against OWM API responses cointaining an empty body!
        try:
            json_data = resp.json()
        except:
            json_data = None
        return resp.status_code, json_data


    @classmethod
    def check_status_code(cls, status_code, payload):
        if status_code < 400:
            return
        if status_code == 400:
            raise api_call_error.APICallError(payload)
        elif status_code == 401:
            raise unauthorized_error.UnauthorizedError('Invalid API Key provided')
        elif status_code == 404:
            raise not_found_error.NotFoundError('Unable to find the resource')
        elif status_code == 502:
            raise api_call_error.BadGatewayError('Unable to contact the upstream server')
        else:
            raise api_call_error.APICallError(payload)

    @classmethod
    def is_success(cls, status_code):
        if 200 <= status_code < 300:
            return True
        return False
