#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime as dt
from pyowm.commons import exceptions
from pyowm.utils import formatting


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
            t = dt.fromisoformat(padded_created_at.replace("Z", "+00:00"))
            self.created_at = formatting.timeformat(t, 'unix')
        self.updated_at = updated_at
        if self.updated_at is not None:
            padded_updated_at = self._format_micros(updated_at)
            t = dt.fromisoformat(padded_updated_at.replace("Z", "+00:00"))
            self.updated_at = formatting.timeformat(t, 'unix')
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
        return formatting.timeformat(self.created_at, timeformat)

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
        return formatting.timeformat(self.updated_at, timeformat)

    @classmethod
    def from_dict(cls, the_dict):
        """
        Parses a *Station* instance out of a data dictionary. Only certain properties of the data dictionary
        are used: if these properties are not found or cannot be parsed, an exception is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: a *Station* instance or ``None`` if no data is available
        :raises: *ParseAPIResponseError* if it is impossible to find or parse the data needed to build the result

        """
        if the_dict is None:
            raise exceptions.ParseAPIResponseError('Data is None')
        id = the_dict.get('ID', None) or the_dict.get('id', None)
        external_id = the_dict.get('external_id', None)
        lon = the_dict.get('longitude', None)
        lat = the_dict.get('latitude', None)
        alt = the_dict.get('altitude', None)
        name = the_dict.get('name', None)
        rank = the_dict.get('rank', None)
        created_at = the_dict.get('created_at', None)
        updated_at = the_dict.get('updated_at', None)
        return Station(id, created_at, updated_at, external_id, name, lon, lat, alt, rank)

    def to_dict(self):
        """Dumps object to a dictionary

        :returns: a `dict`

        """
        return {
            'id': self.id,
            'external_id': self.external_id,
            'name': self.name,
            'created_at': formatting.to_ISO8601(self.created_at),
            'updated_at': formatting.to_ISO8601(self.updated_at),
            'latitude': self.lat,
            'longitude': self.lon,
            'altitude': self.alt if self.alt is not None else 'None',
            'rank': self.rank}

    def __repr__(self):
        return '<%s.%s - id=%s, external_id=%s, name=%s>' \
               % (__name__, self.__class__.__name__,
                  self.id, self.external_id, self.name)
