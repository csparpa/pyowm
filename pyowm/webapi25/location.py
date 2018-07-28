"""
Module containing location-related classes and data structures.
"""

import json
import xml.etree.ElementTree as ET
from pyowm.webapi25.xsd.xmlnsconfig import (
    LOCATION_XMLNS_URL, LOCATION_XMLNS_PREFIX)
from pyowm.utils import xmlutils, geo


class Location(object):
    """
    A class representing a location in the world. A location is defined through
    a toponym, a couple of geographic coordinates such as longitude and
    latitude and a numeric identifier assigned by the OWM web API that uniquely
    spots the location in the world. Optionally, the country specification may
    be provided.

    Further reference about OWM city IDs can be found at:
    http://bugs.openweathermap.org/projects/api/wiki/Api_2_5_weather#3-By-city-ID

    :param name: the location's toponym
    :type name: Unicode
    :param lon: the location's longitude, must be between -180.0 and 180.0
    :type lon: int/float
    :param lat: the location's latitude, must be between -90.0 and 90.0
    :type lat: int/float
    :param ID: the location's OWM city ID
    :type ID: int
    :param country: the location's country (``None`` by default)
    :type country: Unicode
    :returns: a *Location* instance
    :raises: *ValueError* if lon or lat values are provided out of bounds
    """

    def __init__(self, name, lon, lat, ID, country=None):
        self._name = name
        if lon is None or lat is None:
            raise ValueError("Either 'lon' or 'lat' must be specified")
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        self._lon = float(lon)
        self._lat = float(lat)
        self._ID = ID
        self._country = country

    def get_name(self):
        """
        Returns the toponym of the location

        :returns: the Unicode toponym

        """
        return self._name

    def get_lon(self):
        """
        Returns the longitude of the location

        :returns: the float longitude

        """
        return self._lon

    def get_lat(self):
        """
        Returns the latitude of the location

        :returns: the float latitude

        """
        return self._lat

    def get_ID(self):
        """
        Returns the OWM city ID of the location

        :returns: the int OWM city ID

        """
        return self._ID

    def get_country(self):
        """
        Returns the country of the location

        :returns: the Unicode country

        """
        return self._country

    def to_geopoint(self):
        """
        Returns the geoJSON compliant representation of this location

        :returns: a ``pyowm.utils.geo.Point`` instance

        """
        if self._lon is None or self._lat is None:
            return None
        return geo.Point(self._lon, self._lat)


    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns:  the JSON string

        """
        return json.dumps({'name': self._name,
                         'coordinates': {'lon': self._lon,
                                         'lat': self._lat
                                        },
                         'ID': self._ID,
                         'country': self._country})

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
                                         LOCATION_XMLNS_PREFIX,
                                         LOCATION_XMLNS_URL)
        return xmlutils.DOM_node_to_XML(root_node, xml_declaration)

    def _to_DOM(self):
        """
        Dumps object data to a fully traversable DOM representation of the
        object.

        :returns: a ``xml.etree.Element`` object

        """
        root_node = ET.Element("location")
        name_node = ET.SubElement(root_node, "name")
        name_node.text = self._name
        coords_node = ET.SubElement(root_node, "coordinates")
        lon_node = ET.SubElement(coords_node, "lon")
        lon_node.text = str(self._lon)
        lat_node = ET.SubElement(coords_node, "lat")
        lat_node.text = str(self._lat)
        id_node = ET.SubElement(root_node, "ID")
        id_node.text = str(self._ID)
        country_node = ET.SubElement(root_node, "country")
        country_node.text = self._country
        return root_node

    def __repr__(self):
        return "<%s.%s - id=%s, name=%s, lon=%s, lat=%s>" % (__name__, \
          self.__class__.__name__, self._ID, self._name, str(self._lon), \
          str(self._lat))


def location_from_dictionary(d):
    """
    Builds a *Location* object out of a data dictionary. Only certain
    properties of the dictionary are used: if these properties are not
    found or cannot be read, an error is issued.

    :param d: a data dictionary
    :type d: dict
    :returns: a *Location* instance
    :raises: *KeyError* if it is impossible to find or read the data
        needed to build the instance

    """
    country = None
    if 'sys' in d and 'country' in d['sys']:
        country = d['sys']['country']
    if 'city' in d:
        data = d['city']
    else:
        data = d
    if 'name' in data:
        name = data['name']
    else:
        name = None
    if 'id' in data:
        ID = int(data['id'])
    else:
        ID = None
    if 'coord' in data:
        lon = data['coord'].get('lon', 0.0)
        lat = data['coord'].get('lat', 0.0)
    elif 'coord' in data['station']:
        if 'lon' in data['station']['coord']:
            lon = data['station']['coord'].get('lon', 0.0)
        elif 'lng' in data['station']['coord']:
            lon = data['station']['coord'].get('lng', 0.0)
        else:
            lon = 0.0
        lat = data['station']['coord'].get('lat', 0.0)
    else:
        raise KeyError("Impossible to read geographical coordinates from JSON")
    if 'country' in data:
        country = data['country']
    return Location(name, lon, lat, ID, country)
