"""
UV Index classes and data structures.
"""

import json
import xml.etree.ElementTree as ET
from pyowm.webapi25.xsd.xmlnsconfig import (
    UVINDEX_XMLNS_URL, UVINDEX_XMLNS_PREFIX)
from pyowm.utils import timeformatutils, timeutils, xmlutils


def uv_intensity_to_exposure_risk(uv_intensity):
    # According to figures in: https://en.wikipedia.org/wiki/Ultraviolet_index
    if 0.0 <= uv_intensity < 2.9:
        return 'low'
    elif 2.9 <= uv_intensity < 5.9:
        return 'moderate'
    elif 5.9 <= uv_intensity <  7.9:
        return 'high'
    elif 7.9 <= uv_intensity < 10.9:
        return 'very high'
    else:
        return 'extreme'


class UVIndex(object):
    """
    A class representing the UltraViolet Index observed in a certain location
    in the world. The location is represented by the
    encapsulated *Location* object.

    :param reception_time: GMT UNIXtime telling when the weather obervation has
        been received from the OWM web API
    :type reception_time: int
    :param location: the *Location* relative to this UV observation
    :type location: *Location*
    :param value: the observed UV intensity value
    :type value: float
    :returns: an *UVIndex* instance
    :raises: *ValueError* when negative values are provided as reception time or
    UV intensity value

    """

    def __init__(self, reception_time, location, value):
        if reception_time < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self._reception_time = reception_time
        self._location = location
        if value < 0.0:
            raise ValueError("'UV intensity must be greater than 0")
        self._value = value

    def get_reception_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the UV has been observed
          from the OWM web API

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
        Returns the *Location* object for this UV index observation

        :returns: the *Location* object

        """
        return self._location

    def get_value(self):
        """
        Returns the UV intensity for this observation

        :returns: float

        """
        return self._value

    def is_forecast(self):
        """
        Tells if the current UV observation refers to the future with respect
        to the current date
        :return: bool
        """
        return timeutils.now(timeformat='unix') < \
               self.get_reception_time(timeformat='unix')

    def get_exposure_risk(self):
        """
        Returns a string stating the risk of harm from unprotected sun exposure
        for the average adult on this UV observation
        :return: str
        """
        return uv_intensity_to_exposure_risk(self._value)

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns:  the JSON string

        """
        return json.dumps({"reception_time": self._reception_time,
                           "Location": json.loads(self._location.to_JSON()),
                           "value": self._value
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
                                         UVINDEX_XMLNS_PREFIX,
                                         UVINDEX_XMLNS_URL)
        return xmlutils.DOM_node_to_XML(root_node, xml_declaration)

    def _to_DOM(self):
        """
        Dumps object data to a fully traversable DOM representation of the
        object.

        :returns: a ``xml.etree.Element`` object

        """
        root_node = ET.Element("uvindex")
        reception_time_node = ET.SubElement(root_node, "reception_time")
        reception_time_node.text = str(self._reception_time)
        value_node = ET.SubElement(root_node, "value")
        value_node.text = str(self._value)
        root_node.append(self._location._to_DOM())
        return root_node

    def __repr__(self):
        return "<%s.%s - reception time=%s>" % (__name__, \
              self.__class__.__name__, self.get_reception_time('iso'))
