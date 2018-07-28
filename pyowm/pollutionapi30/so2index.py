"""
Sulphur Dioxide classes and data structures.
"""

import json
import xml.etree.ElementTree as ET
from pyowm.pollutionapi30.xsd.xmlnsconfig import SO2INDEX_XMLNS_URL, SO2INDEX_XMLNS_PREFIX
from pyowm.utils import timeformatutils, timeutils, xmlutils


class SO2Index(object):
    """
    A class representing the Sulphur Dioxide Index observed in a certain location
    in the world. The index is made up of several measurements, each one at a
    different atmospheric pressure. The location is represented by the
    encapsulated *Location* object.

    :param reference_time: GMT UNIXtime telling when the SO2 data has been measured
    :type reference_time: int
    :param location: the *Location* relative to this SO2 observation
    :type location: *Location*
    :param interval: the time granularity of the SO2 observation
    :type interval: str
    :param so2_samples: the SO2 samples
    :type so2_samples: list of dicts
    :param reception_time: GMT UNIXtime telling when the SO2 observation has
        been received from the OWM web API
    :type reception_time: int
    :returns: an *SOIndex* instance
    :raises: *ValueError* when negative values are provided as reception time,
      SO2 samples are not provided in a list

    """

    def __init__(self, reference_time, location, interval, so2_samples, reception_time):
        if reference_time < 0:
            raise ValueError("'reference_time' must be greater than 0")
        self._reference_time = reference_time
        self._location = location
        self._interval = interval
        if not isinstance(so2_samples, list):
            raise ValueError("'so2_samples' must be a list")
        self._so2_samples = so2_samples
        if reception_time < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self._reception_time = reception_time

    def get_reference_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the SO2 samples have been measured

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError when negative values are provided

        """
        return timeformatutils.timeformat(self._reference_time, timeformat)

    def get_reception_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the SO2 observation has been received
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
        Returns the *Location* object for this SO2 index measurement

        :returns: the *Location* object

        """
        return self._location

    def get_interval(self):
        """
        Returns the time granularity interval for this SO2 index measurement

        :return: str
        """
        return self._interval

    def get_so2_samples(self):
        """
        Returns the SO2 samples for this index

        :returns: list of dicts

        """
        return self._so2_samples

    def is_forecast(self):
        """
        Tells if the current SO2 observation refers to the future with respect
        to the current date
        :return: bool
        """
        return timeutils.now(timeformat='unix') < \
               self.get_reference_time(timeformat='unix')

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns:  the JSON string

        """
        return json.dumps({"reference_time": self._reference_time,
                           "location": json.loads(self._location.to_JSON()),
                           "interval": self._interval,
                           "so2_samples": self._so2_samples,
                           "reception_time": self._reception_time,
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
                                         SO2INDEX_XMLNS_PREFIX,
                                         SO2INDEX_XMLNS_URL)
        return xmlutils.DOM_node_to_XML(root_node, xml_declaration)

    def _to_DOM(self):
        """
        Dumps object data to a fully traversable DOM representation of the
        object.

        :returns: a ``xml.etree.Element`` object

        """
        root_node = ET.Element("so2index")
        reference_time_node = ET.SubElement(root_node, "reference_time")
        reference_time_node.text = str(self._reference_time)
        reception_time_node = ET.SubElement(root_node, "reception_time")
        reception_time_node.text = str(self._reception_time)
        interval_node = ET.SubElement(root_node, "interval")
        interval_node.text = str(self._interval)
        so2_samples_node = ET.SubElement(root_node, "so2_samples")
        for smpl in self._so2_samples:
            s = smpl.copy()
            # turn values to 12 decimal digits-formatted strings
            s['pressure'] = '{:.12e}'.format(s['pressure'])
            s['value'] = '{:.12e}'.format(s['value'])
            s['precision'] = '{:.12e}'.format(s['precision'])
            xmlutils.create_DOM_node_from_dict(s, "so2_sample",
                                               so2_samples_node)
        root_node.append(self._location._to_DOM())
        return root_node

    def __repr__(self):
        return "<%s.%s - reference time=%s, reception time=%s, location=%s, " \
               "interval=%s>" % (
                    __name__,
                    self.__class__.__name__,
                    self.get_reference_time('iso'),
                    self.get_reception_time('iso'),
                    str(self._location),
                    self._interval)
