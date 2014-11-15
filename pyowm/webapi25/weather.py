#!/usr/bin/env python

"""
Module containing weather data classes and data structures.
"""

import json
import xml.etree.ElementTree as ET
from pyowm.webapi25.xsd.xmlnsconfig import (
    WEATHER_XMLNS_PREFIX, WEATHER_XMLNS_URL)
from pyowm.utils import timeformatutils, temputils, xmlutils


class Weather(object):
    """
    A class encapsulating raw weather data.
    A reference about OWM weather codes and icons can be found at:
    http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes

    :param reference_time: GMT UNIX time of weather measurement
    :type reference_time: int
    :param sunset_time: GMT UNIX time of sunset
    :type sunset_time: int
    :param sunrise_time: GMT UNIX time of sunrise
    :type sunrise_time: int
    :param clouds: cloud coverage percentage
    :type clouds: int
    :param rain: precipitation info
    :type rain: dict
    :param snow: snow info
    :type snow: dict
    :param wind: wind info
    :type wind: dict
    :param humidity: atmospheric humidity percentage
    :type humidity: int
    :param pressure: atmospheric pressure info
    :type pressure: dict
    :param temperature: temperature info
    :type temperature: dict
    :param status: short weather status
    :type status: Unicode
    :param detailed_status: detailed weather status
    :type detailed_status: Unicode
    :param weather_code: OWM weather condition code
    :type weather_code: int
    :param weather_icon_name: weather-related icon name
    :type weather_icon_name: Unicode
    :returns:  a *Weather* instance
    :raises: *ValueError* when negative values are provided

    """

    def __init__(self, reference_time, sunset_time, sunrise_time, clouds, rain,
                 snow, wind, humidity, pressure, temperature, status,
                 detailed_status, weather_code, weather_icon_name):
        if reference_time < 0:
            raise ValueError("'reference_time' must be greater than 0")
        self._reference_time = reference_time
        if sunset_time < 0:
            raise ValueError("'sunset_time' must be greatear than 0")
        self._sunset_time = sunset_time
        if sunrise_time < 0:
            raise ValueError("'sunrise_time' must be greatear than 0")
        self._sunrise_time = sunrise_time
        if clouds < 0:
            raise ValueError("'clouds' must be greater than 0")
        self._clouds = clouds
        self._rain = rain
        self._snow = snow
        self._wind = wind
        if humidity < 0:
            raise ValueError("'humidity' must be greatear than 0")
        self._humidity = humidity
        self._pressure = pressure
        self._temperature = temperature
        self._status = status
        self._detailed_status = detailed_status
        self._weather_code = weather_code
        self._weather_icon_name = weather_icon_name

    def get_reference_time(self, timeformat='unix'):
        """Returns the GMT time telling when the weather was measured

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError when negative values are provided

        """
        return timeformatutils.timeformat(self._reference_time, timeformat)

    def get_sunset_time(self, timeformat='unix'):
        """Returns the GMT time of sunset

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError

        """
        return timeformatutils.timeformat(self._sunset_time, timeformat)

    def get_sunrise_time(self, timeformat='unix'):
        """Returns the GMT time of sunrise

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError

        """
        return timeformatutils.timeformat(self._sunrise_time, timeformat)

    def get_clouds(self):
        """Returns the cloud coverage percentage as an int

        :returns: the cloud coverage percentage

        """
        return self._clouds

    def get_rain(self):
        """Returns a dict containing precipitation info

        :returns: a dict containing rain info

        """
        return self._rain

    def get_snow(self):
        """Returns a dict containing snow info

        :returns: a dict containing snow info

        """
        return self._snow

    def get_wind(self):
        """Returns a dict containing wind info

        :returns: a dict containing wind info

        """
        return self._wind

    def get_humidity(self):
        """Returns the atmospheric humidity as an int

        :returns: the humidity

        """
        return self._humidity

    def get_pressure(self):
        """Returns a dict containing atmospheric pressure info

        :returns: a dict containing pressure info

        """
        return self._pressure

    def get_temperature(self, unit='kelvin'):
        """Returns a dict with temperature info

        :param unit: the unit of measure for the temperature values. May be:
            '*kelvin*' (default), '*celsius*' or '*fahrenheit*'
        :type unit: str
        :returns: a dict containing temperature values.
        :raises: ValueError when unknown temperature units are provided

        """
        # This is due to the fact that the OWM web API responses are mixing
        # absolute temperatures and temperature deltas together
        to_be_converted = dict()
        not_to_be_converted = dict()
        for label, temp in self._temperature.items():
            if temp is None or temp < 0:
                not_to_be_converted[label] = temp
            else:
                to_be_converted[label] = temp
        converted = temputils.kelvin_dict_to(to_be_converted, unit)
        return dict(list(converted.items()) + \
                    list(not_to_be_converted.items()))

    def get_status(self):
        """Returns the short weather status as a Unicode string

        :returns: the short weather status

        """
        return self._status

    def get_detailed_status(self):
        """Returns the detailed weather status as a Unicode string

        :returns: the detailed weather status

        """
        return self._detailed_status

    def get_weather_code(self):
        """Returns the OWM weather condition code as an int

        :returns: the OWM weather condition code

        """
        return self._weather_code

    def get_weather_icon_name(self):
        """Returns weather-related icon name as a Unicode string.

        :returns: the icon name.

        """
        return self._weather_icon_name

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns: the JSON string

        """
        return json.dumps({'reference_time': self._reference_time,
                           'sunset_time': self._sunset_time,
                           'sunrise_time': self._sunrise_time,
                           'clouds': self._clouds,
                           'rain': self._rain,
                           'snow': self._snow,
                           'wind': self._wind,
                           'humidity': self._humidity,
                           'pressure': self._pressure,
                           'temperature': self._temperature,
                           'status': self._status,
                           'detailed_status': self._detailed_status,
                           'weather_code': self._weather_code,
                           'weather_icon_name': self._weather_icon_name})

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
                                         WEATHER_XMLNS_PREFIX,
                                         WEATHER_XMLNS_URL)
        return xmlutils.DOM_node_to_XML(root_node, xml_declaration). \
            encode('utf-8')

    def _to_DOM(self):
        """
        Dumps object data to a fully traversable DOM representation of the
        object.

        :returns: a ``xml.etree.Element`` object

        """
        root_node = ET.Element("weather")
        status_node = ET.SubElement(root_node, "status")
        status_node.text = self._status
        weather_code_node = ET.SubElement(root_node, "weather_code")
        weather_code_node.text = str(self._weather_code)
        xmlutils.create_DOM_node_from_dict(self._rain, "rain", root_node)
        xmlutils.create_DOM_node_from_dict(self._snow, "snow", root_node)
        xmlutils.create_DOM_node_from_dict(self._pressure, "pressure",
                                             root_node)
        node_sunrise_time = ET.SubElement(root_node, "sunrise_time")
        node_sunrise_time.text = str(self._sunrise_time)
        weather_icon_name_node = ET.SubElement(root_node, "weather_icon_name")
        weather_icon_name_node.text = self._weather_icon_name
        clouds_node = ET.SubElement(root_node, "clouds")
        clouds_node.text = str(self._clouds)
        xmlutils.create_DOM_node_from_dict(self._temperature,
                                                "temperature", root_node)
        detailed_status_node = ET.SubElement(root_node, "detailed_status")
        detailed_status_node.text = self._detailed_status
        reference_time_node = ET.SubElement(root_node, "reference_time")
        reference_time_node.text = str(self._reference_time)
        sunset_time_node = ET.SubElement(root_node, "sunset_time")
        sunset_time_node.text = str(self._sunset_time)
        humidity_node = ET.SubElement(root_node, "humidity")
        humidity_node.text = str(self._humidity)
        xmlutils.create_DOM_node_from_dict(self._wind, "wind", root_node)
        return root_node

    def __repr__(self):
        return "<%s.%s - reference time=%s, status=%s>" % (__name__, \
              self.__class__.__name__, self.get_reference_time('iso'),
              self._status)


def weather_from_dictionary(d):
    """
    Builds a *Weather* object out of a data dictionary. Only certain
    properties of the dictionary are used: if these properties are not
    found or cannot be read, an error is issued.

    :param d: a data dictionary
    :type d: dict
    :returns: a *Weather* instance
    :raises: *KeyError* if it is impossible to find or read the data
        needed to build the instance

    """
    # -- times
    reference_time = d['dt']
    if 'sys' in d and 'sunset' in d['sys']:
        sunset_time = d['sys']['sunset']
    else:
        sunset_time = 0
    if 'sys' in d and 'sunrise' in d['sys']:
        sunrise_time = d['sys']['sunrise']
    else:
        sunrise_time = 0
    # -- clouds
    if 'clouds' in d:
        if isinstance(d['clouds'], int) or isinstance(d['clouds'], float):
            clouds = d['clouds']
        elif 'all' in d['clouds']:
            clouds = d['clouds']['all']
        else:
            clouds = 0
    else:
        clouds = 0
    # -- rain
    if 'rain' in d:
        if isinstance(d['rain'], int) or isinstance(d['rain'], float):
            rain = {'all': d['rain']}
        else:
            rain = d['rain'].copy()
    else:
        rain = {}
    # -- wind
    if 'wind' in d:
        wind = d['wind'].copy()
    else:
        wind = {}
    # -- humidity
    if 'humidity' in d:
        humidity = d['humidity']
    elif 'main' in d and 'humidity' in d['main']:
        humidity = d['main']['humidity']
    else:
        humidity = 0
    # -- snow
    if 'snow' in d:
        if isinstance(d['snow'], int) or isinstance(d['snow'], float):
            snow = {'all': d['snow']}
        else:
            snow = d['snow'].copy()
    else:
        snow = {}
    # -- pressure
    if 'pressure' in d:
        atm_press = d['pressure']
    elif 'main' in d and 'pressure' in d['main']:
        atm_press = d['main']['pressure']
    else:
        atm_press = None
    if 'main' in d and 'sea_level' in d['main']:
        sea_level_press = d['main']['sea_level']
    else:
        sea_level_press = None
    pressure = {'press': atm_press, 'sea_level': sea_level_press}
    # -- temperature
    if 'temp' in d:
        temperature = d['temp'].copy()
    elif 'main' in d and 'temp' in d['main']:
        temp = d['main']['temp']
        if 'temp_kf' in d['main']:
            temp_kf = d['main']['temp_kf']
        else:
            temp_kf = None
        if 'temp_max' in d['main']:
            temp_max = d['main']['temp_max']
        else:
            temp_max = None
        if 'temp_min' in d['main']:
            temp_min = d['main']['temp_min']
        else:
            temp_min = None
        temperature = {'temp': temp,
                       'temp_kf': temp_kf,
                       'temp_max': temp_max,
                       'temp_min': temp_min
                       }
    else:
        temperature = {}
    # -- weather status info
    if 'weather' in d:
        # Sometimes provided with a leading upper case!
        status = d['weather'][0]['main'].lower()
        detailed_status = d['weather'][0]['description'].lower()
        weather_code = d['weather'][0]['id']
        weather_icon_name = d['weather'][0]['icon']
    else:
        status = ''
        detailed_status = ''
        weather_code = 0
        weather_icon_name = ''

    return Weather(reference_time, sunset_time, sunrise_time, clouds,
                rain, snow, wind, humidity, pressure, temperature,
                status, detailed_status, weather_code,
                weather_icon_name)
