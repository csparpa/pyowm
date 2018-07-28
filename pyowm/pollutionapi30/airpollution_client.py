from pyowm.utils import timeformatutils
from pyowm.pollutionapi30.uris import CO_INDEX_URL, OZONE_URL, NO2_INDEX_URL, SO2_INDEX_URL
from pyowm.commons import http_client


class AirPollutionHttpClient(object):

    """
    A class representing the OWM Air Pollution web API, which is a subset of the
    overall OWM API.

    :param API_key: a Unicode object representing the OWM Air Pollution web API key
    :type API_key: Unicode
    :param httpclient: an *httpclient.HttpClient* instance that will be used to \
         send requests to the OWM Air Pollution web API.
    :type httpclient: an *httpclient.HttpClient* instance

    """

    def __init__(self, API_key, httpclient):
        self._API_key = API_key
        self._client = httpclient

    def _trim_to(self, date_object, interval):
        if interval == 'minute':
            return date_object.strftime('%Y-%m-%dT%H:%MZ')
        elif interval == 'hour':
            return date_object.strftime('%Y-%m-%dT%HZ')
        elif interval == 'day':
            return date_object.strftime('%Y-%m-%dZ')
        elif interval == 'month':
            return date_object.strftime('%Y-%mZ')
        elif interval == 'year':
            return date_object.strftime('%YZ')
        else:
            raise ValueError("The interval provided for the search "
                             "window is invalid")

    def get_coi(self, params_dict):
        """
        Invokes the CO Index endpoint

        :param params_dict: dict of parameters
        :returns: a string containing raw JSON data
        :raises: *ValueError*, *APICallError*

        """
        lat = str(params_dict['lat'])
        lon = str(params_dict['lon'])
        start = params_dict['start']
        interval = params_dict['interval']

        # build request URL
        if start is None:
            timeref = 'current'
        else:
            if interval is None:
                timeref = self._trim_to(timeformatutils.to_date(start), 'year')
            else:
                timeref = self._trim_to(timeformatutils.to_date(start), interval)

        fixed_url = '%s/%s,%s/%s.json' % (CO_INDEX_URL, lat, lon, timeref)
        uri = http_client.HttpClient.to_url(fixed_url, self._API_key, None)
        _, json_data = self._client.cacheable_get_json(uri)
        return json_data

    def get_o3(self, params_dict):
        """
        Invokes the O3 Index endpoint

        :param params_dict: dict of parameters
        :returns: a string containing raw JSON data
        :raises: *ValueError*, *APICallError*

        """
        lat = str(params_dict['lat'])
        lon = str(params_dict['lon'])
        start = params_dict['start']
        interval = params_dict['interval']

        # build request URL
        if start is None:
            timeref = 'current'
        else:
            if interval is None:
                timeref = self._trim_to(
                    timeformatutils.to_date(start), 'year')
            else:
                timeref = self._trim_to(
                    timeformatutils.to_date(start), interval)

        fixed_url = '%s/%s,%s/%s.json' % (OZONE_URL, lat, lon, timeref)
        uri = http_client.HttpClient.to_url(fixed_url, self._API_key, None)
        _, json_data = self._client.cacheable_get_json(uri)
        return json_data


    def get_no2(self, params_dict):
        """
        Invokes the NO2 Index endpoint

        :param params_dict: dict of parameters
        :returns: a string containing raw JSON data
        :raises: *ValueError*, *APICallError*

        """
        lat = str(params_dict['lat'])
        lon = str(params_dict['lon'])
        start = params_dict['start']
        interval = params_dict['interval']

        # build request URL
        if start is None:
            timeref = 'current'
        else:
            if interval is None:
                timeref = self._trim_to(
                    timeformatutils.to_date(start), 'year')
            else:
                timeref = self._trim_to(
                    timeformatutils.to_date(start), interval)

        fixed_url = '%s/%s,%s/%s.json' % (NO2_INDEX_URL, lat, lon, timeref)
        uri = http_client.HttpClient.to_url(fixed_url, self._API_key, None)
        _, json_data = self._client.cacheable_get_json(uri)
        return json_data


    def get_so2(self, params_dict):
        """
        Invokes the SO2 Index endpoint

        :param params_dict: dict of parameters
        :returns: a string containing raw JSON data
        :raises: *ValueError*, *APICallError*

        """
        lat = str(params_dict['lat'])
        lon = str(params_dict['lon'])
        start = params_dict['start']
        interval = params_dict['interval']

        # build request URL
        if start is None:
            timeref = 'current'
        else:
            if interval is None:
                timeref = self._trim_to(
                    timeformatutils.to_date(start), 'year')
            else:
                timeref = self._trim_to(
                    timeformatutils.to_date(start), interval)

        fixed_url = '%s/%s,%s/%s.json' % (SO2_INDEX_URL, lat, lon, timeref)
        uri = http_client.HttpClient.to_url(fixed_url, self._API_key, None)
        _, json_data = self._client.cacheable_get_json(uri)
        return json_data

    def __repr__(self):
        return "<%s.%s - httpclient=%s>" % \
               (__name__, self.__class__.__name__, str(self._client))