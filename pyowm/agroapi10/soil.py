#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.utils import formatting, measurables


class Soil:

    """
    Soil data over a specific Polygon

    :param reference_time: UTC UNIX time of soil data measurement
    :type reference_time: int
    :param surface_temp: soil surface temperature in Kelvin degrees
    :type surface_temp: float
    :param ten_cm_temp: soil temperature at 10 cm depth in Kelvin degrees
    :type ten_cm_temp: float
    :param moisture: soil moisture in m^3/m^3
    :type moisture: float
    :param polygon_id: ID of the polygon this soil data was measured upon
    :type polygon_id: str
    :returns: a `Soil` instance
    :raises: `AssertionError` when any of the mandatory fields is `None` or has wrong type
    """

    def __init__(self, reference_time, surface_temp, ten_cm_temp, moisture, polygon_id=None):
        assert reference_time is not None
        assert isinstance(reference_time, int), 'reference time must be a UNIX int timestamp'
        if reference_time < 0:
            raise ValueError("reference_time must be greater than 0")
        self._reference_time = reference_time
        assert surface_temp is not None
        assert isinstance(surface_temp, float) or isinstance(surface_temp, int), 'surface_temp must be a number'
        self._surface_temp = surface_temp
        assert ten_cm_temp is not None
        assert isinstance(ten_cm_temp, float) or isinstance(ten_cm_temp, int), 'ten_cm_temp must be a number'
        self._ten_cm_temp = ten_cm_temp
        assert moisture is not None
        assert isinstance(moisture, float) or isinstance(moisture, int), 'moisture must be a number'
        if moisture < 0.:
            raise ValueError("moisture must be greater than 0")
        self.moisture = moisture
        self.polygon_id = polygon_id

    def reference_time(self, timeformat='unix'):
        """Returns the UTC time telling when the soil data was measured

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str

        """
        return formatting.timeformat(self._reference_time, timeformat)

    def surface_temp(self, unit='kelvin'):
        """Returns the soil surface temperature

        :param unit: the unit of measure for the temperature value. May be:
            '*kelvin*' (default), '*celsius*' or '*fahrenheit*'
        :type unit: str
        :returns: a float
        :raises: ValueError when unknown temperature units are provided

        """
        if unit == 'kelvin':
            return self._surface_temp
        if unit == 'celsius':
            return measurables.kelvin_to_celsius(self._surface_temp)
        if unit == 'fahrenheit':
            return measurables.kelvin_to_fahrenheit(self._surface_temp)
        else:
            raise ValueError('Wrong temperature unit')

    def ten_cm_temp(self, unit='kelvin'):
        """Returns the soil temperature measured 10 cm below surface

        :param unit: the unit of measure for the temperature value. May be:
            '*kelvin*' (default), '*celsius*' or '*fahrenheit*'
        :type unit: str
        :returns: a float
        :raises: ValueError when unknown temperature units are provided

        """
        if unit == 'kelvin':
            return self._ten_cm_temp
        if unit == 'celsius':
            return measurables.kelvin_to_celsius(self._ten_cm_temp)
        if unit == 'fahrenheit':
            return measurables.kelvin_to_fahrenheit(self._ten_cm_temp)
        else:
            raise ValueError('Wrong temperature unit')

    @classmethod
    def from_dict(cls, the_dict):
        assert isinstance(the_dict, dict)
        reference_time = the_dict['reference_time']
        surface_temp = the_dict['surface_temp']
        ten_cm_temp = the_dict['ten_cm_temp']
        moisture = the_dict['moisture']
        polygon_id = the_dict.get('polygon_id', None)
        return Soil(reference_time, surface_temp, ten_cm_temp, moisture, polygon_id)

    def to_dict(self):
        return {'reference_time': self._reference_time,
                'surface_temp': self._surface_temp,
                'ten_cm_temp': self._ten_cm_temp,
                'moisture': self.moisture,
                'polygon_id': self.polygon_id}

    def __repr__(self):
        return "<%s.%s - polygon_id=%s,reference time=%s,>" % (__name__, self.__class__.__name__,
                                                               self.polygon_id, self.reference_time('iso'))
