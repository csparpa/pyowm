#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pyowm.exceptions import parse_response_error, api_response_error
from pyowm.utils import formatting, temperature
from pyowm.weatherapi25.uris import ICONS_BASE_URI


class Weather:
    """
    A class encapsulating raw weather data.
    A reference about OWM weather codes and icons can be found at:
    http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes

    :param reference_time: GMT UNIX time of weather measurement
    :type reference_time: int
    :param sunset_time: GMT UNIX time of sunset or None on polar days
    :type sunset_time: int or None
    :param sunrise_time: GMT UNIX time of sunrise or None on polar nights
    :type sunrise_time: int or None
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
    :param visibility_distance: visibility distance
    :type visibility_distance: float
    :param dewpoint: dewpoint
    :type dewpoint: float
    :param humidex: Canadian humidex
    :type humidex: float
    :param heat_index: heat index
    :type heat_index: float
    :returns:  a *Weather* instance
    :raises: *ValueError* when negative values are provided

    """

    def __init__(self, reference_time, sunset_time, sunrise_time, clouds, rain,
                 snow, wind, humidity, pressure, temperature, status,
                 detailed_status, weather_code, weather_icon_name,
                 visibility_distance, dewpoint, humidex, heat_index):
        if reference_time < 0:
            raise ValueError("'reference_time' must be greater than 0")
        self.ref_time = reference_time
        if sunset_time < 0:
            sunset_time = None
        self.sset_time = sunset_time
        if sunrise_time < 0:
            sunrise_time = None
        self.srise_time = sunrise_time
        if clouds < 0:
            raise ValueError("'clouds' must be greater than 0")
        self.clouds = clouds
        self.rain = rain
        self.snow = snow
        self.wnd = wind
        if humidity < 0:
            raise ValueError("'humidity' must be greatear than 0")
        self.humidity = humidity
        self.pressure = pressure
        self.temp = temperature
        self.status = status
        self.detailed_status = detailed_status
        self.weather_code = weather_code
        self.weather_icon_name = weather_icon_name
        if visibility_distance is not None and visibility_distance < 0:
            raise ValueError("'visibility_distance' must be greater than 0")
        self.visibility_distance = visibility_distance
        self.dewpoint = dewpoint
        if humidex is not None and humidex < 0:
            raise ValueError("'humidex' must be greater than 0")
        self.humidex = humidex
        if heat_index is not None and heat_index < 0:
            raise ValueError("'heat index' must be grater than 0")
        self.heat_index = heat_index

    def reference_time(self, timeformat='unix'):
        """Returns the GMT time telling when the weather was measured

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError when negative values are provided

        """
        return formatting.timeformat(self.ref_time, timeformat)

    def sunset_time(self, timeformat='unix'):
        """Returns the GMT time of sunset

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: an int or a str or None
        :raises: ValueError

        """
        if self.sset_time is None:
            return None
        return formatting.timeformat(self.sset_time, timeformat)

    def sunrise_time(self, timeformat='unix'):
        """Returns the GMT time of sunrise

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: an int or a str or None
        :raises: ValueError

        """
        if self.srise_time is None:
            return None
        return formatting.timeformat(self.srise_time, timeformat)

    def wind(self, unit='meters_sec'):
        """Returns a dict containing wind info

        :param unit: the unit of measure for the wind values. May be:
            '*meters_sec*' (default), '*miles_hour*  or '*kilometers_hour*'
        :type unit: str
        :returns: a dict containing wind info

        """
        if unit == 'meters_sec':
            return self.wnd
        elif unit == 'miles_hour':
            wind_dict = {k: self.wnd[k]
                         for k in self.wnd if self.wnd[k] is not None}
            return temperature.metric_wind_dict_to_imperial(wind_dict)
        elif unit == 'km_hour':
            wind_dict = {k: self.wnd[k]
                         for k in self.wnd if self.wnd[k] is not None}
            return temperature.metric_wind_dict_to_km_h(wind_dict)
        else:
            raise ValueError("Invalid value for target wind conversion unit")

    def temperature(self, unit='kelvin'):
        """Returns a dict with temperature info

        :param unit: the unit of measure for the temperature values. May be:
            '*kelvin*' (default), '*celsius*' or '*fahrenheit*'
        :type unit: str
        :returns: a dict containing temperature values.
        :raises: ValueError when unknown temperature units are provided

        """
        # This is due to the fact that the OWM Weather API responses are mixing
        # absolute temperatures and temperature deltas together
        to_be_converted = dict()
        not_to_be_converted = dict()
        for label, temp in self.temp.items():
            if temp is None or temp < 0:
                not_to_be_converted[label] = temp
            else:
                to_be_converted[label] = temp
        converted = temperature.kelvin_dict_to(to_be_converted, unit)
        return dict(list(converted.items()) +
                    list(not_to_be_converted.items()))

    def weather_icon_url(self):
        """Returns weather-related icon URL as a string.

        :returns: the icon URL.

        """
        return ICONS_BASE_URI % self.weather_icon_name

    def __repr__(self):
        return "<%s.%s - reference time=%s, status=%s, detailed status=%s>" % (
            __name__, self.__class__.__name__, self.reference_time('iso'), self.status.lower(), self.detailed_status.lower())

    @classmethod
    def from_dict(cls, the_dict):
        """
        Parses a *Weather* instance out of a data dictionary. Only certain properties of the data dictionary
        are used: if these properties are not found or cannot be parsed, an exception is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: a *Weather* instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the input dict embeds an HTTP status error

        """
        if the_dict is None:
            raise parse_response_error.ParseResponseError('Data is None')
        # -- times
        if 'dt' in the_dict:
            reference_time = the_dict['dt']
        elif 'dt' in the_dict['last']:
            reference_time = the_dict['last']['dt']
        if 'sys' in the_dict and 'sunset' in the_dict['sys']:
            sunset_time = the_dict['sys']['sunset']
        else:
            sunset_time = 0
        if 'sys' in the_dict and 'sunrise' in the_dict['sys']:
            sunrise_time = the_dict['sys']['sunrise']
        else:
            sunrise_time = 0
        # -- calc
        if 'calc' in the_dict:
            if 'dewpoint' in the_dict['calc']:
                dewpoint = the_dict['calc']['dewpoint']
            else:
                dewpoint = None
            if 'humidex' in the_dict['calc']:
                humidex = the_dict['calc']['humidex']
            else:
                humidex = None
            if 'heatindex' in the_dict['calc']:
                heat_index = the_dict['calc']['heatindex']
            else:
                heat_index = None
        elif 'last' in the_dict:
            if 'calc' in the_dict['last']:
                if 'dewpoint' in the_dict['last']['calc']:
                    dewpoint = the_dict['last']['calc']['dewpoint']
                else:
                    dewpoint = None
                if 'humidex' in the_dict['last']['calc']:
                    humidex = the_dict['last']['calc']['humidex']
                else:
                    humidex = None
                if 'heatindex' in the_dict['last']['calc']:
                    heat_index = the_dict['last']['calc']['heatindex']
                else:
                    heat_index = None
        else:
            dewpoint = None
            humidex = None
            heat_index = None
        # -- visibility
        if 'visibility' in the_dict:
            if isinstance(the_dict['visibility'], int):
                visibility_distance = the_dict['visibility']
            elif 'distance' in the_dict['visibility']:
                visibility_distance = the_dict['visibility']['distance']
            else:
                visibility_distance = None
        elif 'last' in the_dict and 'visibility' in the_dict['last']:
            if isinstance(the_dict['last']['visibility'], int):
                visibility_distance = the_dict['last']['visibility']
            elif 'distance' in the_dict['last']['visibility']:
                visibility_distance = the_dict['last']['visibility']['distance']
            else:
                visibility_distance = None
        else:
            visibility_distance = None
        # -- clouds
        if 'clouds' in the_dict:
            if isinstance(the_dict['clouds'], int) or isinstance(the_dict['clouds'], float):
                clouds = the_dict['clouds']
            elif 'all' in the_dict['clouds']:
                clouds = the_dict['clouds']['all']
            else:
                clouds = 0
        else:
            clouds = 0
        # -- rain
        if 'rain' in the_dict:
            if isinstance(the_dict['rain'], int) or isinstance(the_dict['rain'], float):
                rain = {'all': the_dict['rain']}
            else:
                if the_dict['rain'] is not None:
                    rain = the_dict['rain'].copy()
                else:
                    rain = dict()
        else:
            rain = dict()
        # -- wind
        if 'wind' in the_dict and the_dict['wind'] is not None:
            wind = the_dict['wind'].copy()
        elif 'last' in the_dict:
            if 'wind' in the_dict['last'] and the_dict['last']['wind'] is not None:
                wind = the_dict['last']['wind'].copy()
            else:
                wind = dict()
        else:
            wind = dict()
            if 'speed' in the_dict:
                wind['speed'] = the_dict['speed']
            if 'deg' in the_dict:
                wind['deg'] = the_dict['deg']
        # -- humidity
        if 'humidity' in the_dict:
            humidity = the_dict['humidity']
        elif 'main' in the_dict and 'humidity' in the_dict['main']:
            humidity = the_dict['main']['humidity']
        elif 'last' in the_dict and 'main' in the_dict['last'] and 'humidity' in the_dict['last']['main']:
            humidity = the_dict['last']['main']['humidity']
        else:
            humidity = 0
        # -- snow
        if 'snow' in the_dict:
            if isinstance(the_dict['snow'], int) or isinstance(the_dict['snow'], float):
                snow = {'all': the_dict['snow']}
            else:
                if the_dict['snow'] is not None:
                    snow = the_dict['snow'].copy()
                else:
                    snow = dict()
        else:
            snow = dict()
        # -- pressure
        if 'pressure' in the_dict:
            atm_press = the_dict['pressure']
        elif 'main' in the_dict and 'pressure' in the_dict['main']:
            atm_press = the_dict['main']['pressure']
        elif 'last' in the_dict:
            if 'main' in the_dict['last']:
                atm_press = the_dict['last']['main']['pressure']
        else:
            atm_press = None
        if 'main' in the_dict and 'sea_level' in the_dict['main']:
            sea_level_press = the_dict['main']['sea_level']
        else:
            sea_level_press = None
        pressure = {'press': atm_press, 'sea_level': sea_level_press}
        # -- temperature
        if 'temp' in the_dict:
            if the_dict['temp'] is not None:
                temperature = the_dict['temp'].copy()
            else:
                temperature = dict()
        elif 'main' in the_dict and 'temp' in the_dict['main']:
            temp = the_dict['main']['temp']
            if 'temp_kf' in the_dict['main']:
                temp_kf = the_dict['main']['temp_kf']
            else:
                temp_kf = None
            if 'temp_max' in the_dict['main']:
                temp_max = the_dict['main']['temp_max']
            else:
                temp_max = None
            if 'temp_min' in the_dict['main']:
                temp_min = the_dict['main']['temp_min']
            else:
                temp_min = None
            temperature = {'temp': temp,
                           'temp_kf': temp_kf,
                           'temp_max': temp_max,
                           'temp_min': temp_min
                           }
        elif 'last' in the_dict:
            if 'main' in the_dict['last']:
                temperature = dict(temp=the_dict['last']['main']['temp'])
        else:
            temperature = dict()
        # -- weather status info
        if 'weather' in the_dict:
            status = the_dict['weather'][0]['main']
            detailed_status = the_dict['weather'][0]['description']
            weather_code = the_dict['weather'][0]['id']
            weather_icon_name = the_dict['weather'][0]['icon']
        else:
            status = ''
            detailed_status = ''
            weather_code = 0
            weather_icon_name = ''

        return Weather(reference_time, sunset_time, sunrise_time, clouds,
                       rain, snow, wind, humidity, pressure, temperature,
                       status, detailed_status, weather_code, weather_icon_name,
                       visibility_distance, dewpoint, humidex, heat_index)

    @classmethod
    def from_dict_of_lists(cls, the_dict):
        """
        Parses a list of *Weather* instances out of an input dict. Only certain properties of the data are used: if
        these properties are not found or cannot be parsed, an error is issued.

        :param the_dict: the input dict
        :type the_dict: dict
        :returns: a list of *Weather* instances or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the data needed to build the result,
            *APIResponseError* if the input dict an HTTP status error

        """
        if the_dict is None:
            raise parse_response_error.ParseResponseError('Data is None')
        # Check if server returned errors: this check overcomes the lack of use
        # of HTTP error status codes by the OWM API 2.5. This mechanism is
        # supposed to be deprecated as soon as the API fully adopts HTTP for
        # conveying errors to the clients
        if 'message' in the_dict and 'cod' in the_dict:
            if the_dict['cod'] == "404":
                print("OWM API: data not found - response payload: " + \
                      json.dumps(the_dict))
                return None
            elif the_dict['cod'] != "200":
                raise api_response_error.APIResponseError(
                                      "OWM API: error - response payload: " + json.dumps(the_dict), the_dict['cod'])
        # Handle the case when no results are found
        if 'cnt' in the_dict and the_dict['cnt'] == "0":
            return []
        else:
            if 'list' in the_dict:
                try:
                    return [Weather.from_dict(item) for item in the_dict['list']]
                except KeyError:
                    raise parse_response_error.ParseResponseError(
                              ''.join([__name__, ': impossible to read weather info from input data'])
                          )
            else:
                raise parse_response_error.ParseResponseError(
                              ''.join([__name__, ': impossible to read weather list from input data']))

    def to_dict(self):
        """Dumps object to a dictionary

        :returns: a `dict`

        """
        return {'reference_time': self.ref_time,
                'sunset_time': self.sset_time,
                'sunrise_time': self.srise_time,
                'clouds': self.clouds,
                'rain': self.rain,
                'snow': self.snow,
                'wind': self.wnd,
                'humidity': self.humidity,
                'pressure': self.pressure,
                'temperature': self.temp,
                'status': self.status,
                'detailed_status': self.detailed_status,
                'weather_code': self.weather_code,
                'weather_icon_name': self.weather_icon_name,
                'visibility_distance': self.visibility_distance,
                'dewpoint': self.dewpoint,
                'humidex': self.humidex,
                'heat_index': self.heat_index}
