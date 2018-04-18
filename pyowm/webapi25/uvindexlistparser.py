import json
from pyowm.abstractions import jsonparser
from pyowm.exceptions import parse_response_error
from pyowm.webapi25.uvindexparser import UVIndexParser


class UVIndexListParser(jsonparser.JSONParser):
    """
    Concrete *JSONParser* implementation building a list of *UVIndex* instances
    out of raw JSON data coming from OWM web API responses.

    """

    def __init__(self):
        pass

    def parse_JSON(self, JSON_string):
        """
        Parses a list of *UVIndex* instances out of raw JSON data. Only certain
        properties of the data are used: if these properties are not found or
        cannot be parsed, an error is issued.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: a list of *UVIndex* instances or an empty list if no data is
            available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the JSON
            string embeds an HTTP status error (this is an OWM web API 2.5 bug)

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        uvindex_parser = UVIndexParser()
        return [uvindex_parser.parse_JSON(json.dumps(item)) for item in d]

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)
