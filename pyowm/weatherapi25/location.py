#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.commons import exceptions
from pyowm.utils import geo


class Location:
    """
    A class representing a location in the world. A location is defined through
    a toponym, a couple of geographic coordinates such as longitude and
    latitude and a numeric identifier assigned by the OWM Weather API that uniquely
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
    :param _id: the location's OWM city ID
    :type ID: int
    :param country: the location's country (``None`` by default)
    :type country: Unicode
    :returns: a *Location* instance
    :raises: *ValueError* if lon or lat values are provided out of bounds
    """

    def __init__(self, name, lon, lat, _id, country=None):
        self.name = name
        if lon is None or lat is None:
            raise ValueError("Either 'lon' or 'lat' must be specified")
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        self.lon = float(lon)
        self.lat = float(lat)
        self.id = _id
        self.country = country

    def to_geopoint(self):
        """
        Returns the geoJSON compliant representation of this location

        :returns: a ``pyowm.utils.geo.Point`` instance

        """
        if self.lon is None or self.lat is None:
            return None
        return geo.Point(self.lon, self.lat)

    @classmethod
    def from_dict(cls, the_dict):
        """
        Parses a *Location* instance out of a data dictionary. Only certain properties of the data dictionary
        are used: if these properties are not found or cannot be parsed, an exception is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: a *Location* instance or ``None`` if no data is available
        :raises: *ParseAPIResponseError* if it is impossible to find or parse the data needed to build the result

        """
        if the_dict is None:
            raise exceptions.ParseAPIResponseError('Data is None')
        country = None
        if 'sys' in the_dict and 'country' in the_dict['sys']:
            country = the_dict['sys']['country']
        data = the_dict['city'] if 'city' in the_dict else the_dict
        name = data['name'] if 'name' in data else None
        ID = int(data['id']) if 'id' in data else None
        if 'coord' in data:
            lon = data['coord'].get('lon', 0.0)
            lat = data['coord'].get('lat', 0.0)
        elif 'station' in data and 'coord' in data['station']:
            if 'lon' in data['station']['coord']:
                lon = data['station']['coord'].get('lon', 0.0)
            elif 'lng' in data['station']['coord']:
                lon = data['station']['coord'].get('lng', 0.0)
            else:
                lon = 0.0
            lat = data['station']['coord'].get('lat', 0.0)
        elif 'lat' in the_dict and 'lon' in the_dict:
            lat = the_dict['lat']
            lon = the_dict['lon']
        else:
            raise KeyError("Impossible to read geographical coordinates from JSON")
        if 'country' in data:
            country = data['country']
        return Location(name, lon, lat, ID, country)

    def to_dict(self):
        """Dumps object to a dictionary

        :returns: a `dict`

        """
        return {'name': self.name,
                'coordinates': {'lon': self.lon, 'lat': self.lat},
                'ID': self.id,
                'country': self.country}

    def __repr__(self):
        return "<%s.%s - id=%s, name=%s, lon=%s, lat=%s>" % (__name__, \
                                                             self.__class__.__name__, self.id, self.name, str(self.lon), \
                                                             str(self.lat))