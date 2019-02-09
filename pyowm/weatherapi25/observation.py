"""
Weather observation classes and data structures.
"""

import json
import xml.etree.ElementTree as ET
from pyowm.weatherapi25.xsd.xmlnsconfig import (
    OBSERVATION_XMLNS_URL, OBSERVATION_XMLNS_PREFIX)
from time import time
from pyowm.weatherapi25 import location
from pyowm.weatherapi25 import weather
from pyowm.utils import timeformatutils, xmlutils
from pyowm.exceptions import parse_response_error, api_response_error


class Observation(object):
    """
    A class representing the weather which is currently being observed in a
    certain location in the world. The location is represented by the
    encapsulated *Location* object while the observed weather data are held by
    the encapsulated *Weather* object.

    :param reception_time: GMT UNIXtime telling when the weather obervation has
        been received from the OWM Weather API
    :type reception_time: int
    :param location: the *Location* relative to this observation
    :type location: *Location*
    :param weather: the *Weather* relative to this observation
    :type weather: *Weather*
    :returns: an *Observation* instance
    :raises: *ValueError* when negative values are provided as reception time

    """

    def __init__(self, reception_time, location, weather):
        if reception_time < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self._reception_time = reception_time
        self._location = location
        self._weather = weather

    def get_reception_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the observation has been received
          from the OWM Weather API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError when negative values are provided

        """
        return timeformatutils.timeformat(self._reception_time, timeformat)

    def get_location(self):
        """
        Returns the *Location* object for this observation

        :returns: the *Location* object

        """
        return self._location

    def get_weather(self):
        """
        Returns the *Weather* object for this observation

        :returns: the *Weather* object

        """
        return self._weather

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns:  the JSON string

        """
        return json.dumps({"reception_time": self._reception_time,
                           "Location": json.loads(self._location.to_JSON()),
                           "Weather": json.loads(self._weather.to_JSON())
                           })

    def to_XML(self, xml_declaration=True, xmlns=True):
        """
        Dumps object fields to an XML-formatted string. The 'xml_declaration'
        switch  enables printing of a leading standard XML line containing XML
        version and encoding. The 'xmlns' switch enables printing of qualified
        XMLNS prefixes.

        :param XML_declaration: if ``True`` (default) prints a leading XML
            declaration line
        :type XML_declaration: bool
        :param xmlns: if ``True`` (default) prints full XMLNS prefixes
        :type xmlns: bool
        :returns: an XML-formatted string

        """
        root_node = self._to_DOM()
        if xmlns:
            xmlutils.annotate_with_XMLNS(root_node,
                                         OBSERVATION_XMLNS_PREFIX,
                                         OBSERVATION_XMLNS_URL)
        return xmlutils.DOM_node_to_XML(root_node, xml_declaration)

    def _to_DOM(self):
        """
        Dumps object data to a fully traversable DOM representation of the
        object.

        :returns: a ``xml.etree.Element`` object

        """
        root_node = ET.Element("observation")
        reception_time_node = ET.SubElement(root_node, "reception_time")
        reception_time_node.text = str(self._reception_time)
        root_node.append(self._location._to_DOM())
        root_node.append(self._weather._to_DOM())
        return root_node

    @classmethod
    def from_dict(cls, the_dict):
        """
        Parses an *Observation* instance out of a data dictionary. Only certain properties of the data dictionary
        are used: if these properties are not found or cannot be parsed, an exception is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: an *Observation* instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the input dict embeds an HTTP status error

        """
        # Check if server returned errors: this check overcomes the lack of use
        # of HTTP error status codes by the OWM API 2.5. This mechanism is
        # supposed to be deprecated as soon as the API fully adopts HTTP for
        # conveying errors to the clients
        if the_dict is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        if 'message' in the_dict and 'cod' in the_dict:
            if the_dict['cod'] == "404":
                print("OWM API: observation data not available")
                return None
            else:
                raise api_response_error.APIResponseError(
                                      "OWM API: error - response payload", the_dict['cod'])
        try:
            place = location.location_from_dictionary(the_dict)
        except KeyError:
            raise parse_response_error.ParseResponseError(
                                      ''.join([__name__, ': impossible to read location info from JSON data']))
        try:
            w = weather.weather_from_dictionary(the_dict)
        except KeyError:
            raise parse_response_error.ParseResponseError(
                                      ''.join([__name__, ': impossible to read weather info from JSON data']))
        current_time = int(round(time()))
        return Observation(current_time, place, w)

    def to_dict(self):
        """Dumps object to a dictionary

        :returns: a `dict`

        """
        return {"reception_time": self._reception_time,
                "Location": json.loads(self._location.to_JSON()),
                "Weather": json.loads(self._weather.to_JSON())}

    def __repr__(self):
        return "<%s.%s - reception time=%s>" % (__name__, self.__class__.__name__,
                                                self.get_reception_time('iso'))

    @classmethod
    def from_dict_of_lists(self, the_dict):
        """
        Parses a list of *Observation* instances out of raw input dict containing a list. Only certain properties of
        the data are used: if these properties are not found or cannot be parsed, an error is issued.

        :param the_dict: a raw JSON string
        :type the_dict: str
        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: a `list` of *Observation* instances or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the OWM API returns an HTTP status error

        """
        if the_dict is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        if 'cod' in the_dict:
            # Check if server returned errors: this check overcomes the lack of use
            # of HTTP error status codes by the OWM API 2.5. This mechanism is
            # supposed to be deprecated as soon as the API fully adopts HTTP for
            # conveying errors to the clients
            if the_dict['cod'] == "200" or the_dict['cod'] == 200:
                pass
            else:
                if the_dict['cod'] == "404" or the_dict['cod'] == 404:
                    print("OWM API: data not found")
                    return None
                else:
                    raise api_response_error.APIResponseError("OWM API: error - response payload", int(the_dict['cod']))

        # Handle the case when no results are found
        if 'count' in the_dict and the_dict['count'] == "0":
            return []
        if 'cnt' in the_dict and the_dict['cnt'] == 0:
            return []
        if 'list' in the_dict:
            return [Observation.from_dict(item) for item in the_dict['list']]

        # no way out..
        raise parse_response_error.ParseResponseError(''.join([__name__, ': impossible to read JSON data']))
