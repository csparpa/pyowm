import json
from datetime import datetime as dt
import xml.etree.ElementTree as ET
from pyowm.stationsapi30.xsd.xmlnsconfig import (
    STATION_XMLNS_PREFIX, STATION_XMLNS_URL)
from pyowm.utils import xmlutils, timeformatutils


class Station:
    """
    A class representing a meteostation in Stations API.
    A reference about OWM stations can be found at:
    http://openweathermap.org/stations

    :param id: unique OWM identifier for the station
    :type id: str
    :param created_at: UTC timestamp marking the station registration.
    :type created_at: str in format %Y-%m-%dT%H:%M:%S.%fZ
    :param updated_at: UTC timestamp marking the last update to this station
    :type updated_at: str in format %Y-%m-%dT%H:%M:%S.%fZ
    :param external_id: user-given identifier for the station
    :type external_id: str
    :param name: user-given name for the station
    :type name: str
    :param lon: longitude of the station
    :type lon: float
    :param lat: latitude of the station
    :type lat: float
    :param alt: altitude of the station
    :type alt: float
    :param rank: station rank
    :type rank: int
    """

    def __init__(self, id, created_at, updated_at, external_id, name,
                 lon, lat, alt, rank):
        assert id is not None
        assert external_id is not None
        assert lon is not None
        assert lat is not None
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        self._lon = float(lon)
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        if alt is not None:
            if alt < 0.0:
                raise ValueError("'alt' value must not be negative")
        self.id = id
        self.created_at = created_at
        if self.created_at is not None:
            padded_created_at = self._format_micros(created_at)
            t = dt.strptime(padded_created_at,
                            '%Y-%m-%dT%H:%M:%S.%fZ').replace(
                                tzinfo=timeformatutils.UTC())
            self.created_at = timeformatutils.timeformat(t, 'unix')
        self.updated_at = updated_at
        if self.updated_at is not None:
            padded_updated_at = self._format_micros(updated_at)
            t = dt.strptime(padded_updated_at,
                            '%Y-%m-%dT%H:%M:%S.%fZ').replace(
                                tzinfo=timeformatutils.UTC())
            self.updated_at = timeformatutils.timeformat(t, 'unix')
        self.external_id = external_id
        self.name = name
        self.lon = lon
        self.lat = lat
        self.alt = alt
        self.rank = rank

    def _format_micros(self, datestring):
        parts = datestring[:-1].split('.')
        if len(parts) == 1:
            if datestring.endswith('Z'):
                return datestring[:-1] + '.000000Z'
            else:
                return datestring + '.000000Z'
            return datestring
        else:
            if len(parts[-1]) > 6:
                micros = parts[-1][:6]
            else:
                micros = parts[-1]
            return '.'.join(
                parts[:-1] + ['{:06d}'.format(int(micros))]) + 'Z'

    def creation_time(self, timeformat='unix'):
        """Returns the UTC time of creation of this station

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time, '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00`` or `date` for
            a ``datetime.datetime`` object
        :type timeformat: str
        :returns: an int or a str or a ``datetime.datetime`` object or None
        :raises: ValueError

        """
        if self.created_at is None:
            return None
        return timeformatutils.timeformat(self.created_at, timeformat)

    def last_update_time(self, timeformat='unix'):
        """Returns the UTC time of the last update on this station's metadata

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time, '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00`` or `date` for
            a ``datetime.datetime`` object
        :type timeformat: str
        :returns: an int or a str or a ``datetime.datetime`` object or None
        :raises: ValueError

        """
        if self.updated_at is None:
            return None
        return timeformatutils.timeformat(self.updated_at, timeformat)

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns: the JSON string

        """
        return json.dumps({'id': self.id,
                           'external_id': self.external_id,
                           'name': self.name,
                           'created_at': timeformatutils.to_ISO8601(self.created_at),
                           'updated_at': timeformatutils.to_ISO8601(self.updated_at),
                           'lat': self.lat,
                           'lon': self.lon,
                           'alt': self.alt if self.alt is not None else 'None',
                           'rank': self.rank})

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
                                         STATION_XMLNS_PREFIX,
                                         STATION_XMLNS_URL)
        return xmlutils.DOM_node_to_XML(root_node, xml_declaration)

    def _to_DOM(self):
        """
        Dumps object data to a fully traversable DOM representation of the
        object.

        :returns: a ``xml.etree.Element`` object

        """
        root_node = ET.Element('station')
        created_at_node = ET.SubElement(root_node, "created_at")
        created_at_node.text = \
            timeformatutils.to_ISO8601(self.created_at)if self.created_at is not None else 'null'
        updated_at_node = ET.SubElement(root_node, "updated_at")
        updated_at_node.text = \
            timeformatutils.to_ISO8601(self.updated_at)if self.updated_at is not None else 'null'
        station_id_node = ET.SubElement(root_node, 'id')
        station_id_node.text = str(self.id)
        station_id_node = ET.SubElement(root_node, 'external_id')
        station_id_node.text = str(self.external_id)
        station_name_node = ET.SubElement(root_node, 'name')
        station_name_node.text = str(self.name) if self.name is not None else 'null'
        lat_node = ET.SubElement(root_node, 'lat')
        lat_node.text = str(self.lat)
        lon_node = ET.SubElement(root_node, 'lon')
        lon_node.text = str(self.lon)
        alt_node = ET.SubElement(root_node, 'alt')
        alt_node.text = str(self.alt) if self.alt is not None else 'null'
        rank_node = ET.SubElement(root_node, 'rank')
        rank_node.text = str(self.rank) if self.rank is not None else 'null'

        return root_node

    def __repr__(self):
        return '<%s.%s - id=%s, external_id=%s, name=%s>' \
               % (__name__, self.__class__.__name__,
                  self.id, self.external_id, self.name)
