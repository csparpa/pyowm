#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pyowm.commons import exceptions
from pyowm.utils import formatting


class AggregatedMeasurement:
    """
    A class representing an aggregation of measurements done by the Stations API
    on a specific time-frame. Values for the aggregation time-frame can be: 'm'
    (minute), 'h' (hour) or 'd' (day)

    :param station_id: unique station identifier
    :type station_id: str
    :param timestamp: reference UNIX timestamp for this measurement
    :type timestamp: int
    :param aggregated_on: aggregation time-frame for this measurement
    :type aggregated_on: string between 'm','h' and 'd'
    :param temp: optional dict containing temperature data
    :type temp: dict or `None`
    :param humidity: optional dict containing humidity data
    :type humidity: dict or `None`
    :param wind: optional dict containing wind data
    :type wind: dict or `None`
    :param pressure: optional dict containing pressure data
    :type pressure: dict or `None`
    :param precipitation: optional dict containing precipitation data
    :type precipitation: dict or `None`
    """

    ALLOWED_AGGREGATION_TIME_FRAMES = ['m', 'h', 'd']

    def __init__(self, station_id, timestamp, aggregated_on, temp=None,
                 humidity=None, wind=None, pressure=None, precipitation=None):
        assert station_id is not None
        assert isinstance(timestamp, int)
        assert not timestamp < 0
        assert aggregated_on is not None
        if aggregated_on not in self.ALLOWED_AGGREGATION_TIME_FRAMES:
            raise ValueError('"aggregated_on" must be among: m, h, d')
        self.station_id = station_id
        self.timestamp = timestamp
        self.aggregated_on = aggregated_on
        self.temp = dict() if temp is None else temp
        self.humidity = dict() if humidity is None else humidity
        self.wind = dict() if wind is None else wind
        self.pressure = dict() if pressure is None else pressure
        self.precipitation = dict() if precipitation is None else precipitation

    def creation_time(self, timeformat='unix'):
        """Returns the UTC time of creation of this aggregated measurement

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time, '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00`` or `date` for
            a ``datetime.datetime`` object
        :type timeformat: str
        :returns: an int or a str or a ``datetime.datetime`` object or None
        :raises: ValueError

        """
        if self.timestamp is None:
            return None
        return formatting.timeformat(self.timestamp, timeformat)

    @classmethod
    def from_dict(cls, the_dict):
        """
        Parses an *AggregatedMeasurement* instance out of a data dictionary. Only certain properties of the data dictionary
        are used: if these properties are not found or cannot be parsed, an exception is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: an *AggregatedMeasurement* instance or ``None`` if no data is available
        :raises: *ParseAPIResponseError* if it is impossible to find or parse the data needed to build the result

        """
        if the_dict is None:
            raise exceptions.ParseAPIResponseError('Data is None')
        station_id = the_dict.get('station_id', None)
        ts = the_dict.get('date', None)
        if ts is not None:
            ts = int(ts)
        aggregated_on = the_dict.get('type', None)
        temp = the_dict.get('temp', dict())
        humidity = the_dict.get('humidity', dict())
        wind = the_dict.get('wind', dict())
        pressure = the_dict.get('pressure', dict())
        precipitation = the_dict.get('precipitation', dict())
        return AggregatedMeasurement(station_id, ts, aggregated_on, temp=temp, humidity=humidity, wind=wind,
                                     pressure=pressure, precipitation=precipitation)

    def to_dict(self):
        """Dumps object fields into a dict

        :returns: a dict

        """
        return {'station_id': self.station_id,
                'timestamp': self.timestamp,
                'aggregated_on': self.aggregated_on,
                'temp': self.temp,
                'humidity': self.humidity,
                'wind': self.wind,
                'pressure': self.pressure,
                'precipitation': self.precipitation}

    def __repr__(self):
        return '<%s.%s - station_id=%s, created_at=%s>' \
               % (__name__, self.__class__.__name__,
                  self.station_id, self.creation_time())


class Measurement:

    def __init__(self, station_id, timestamp, temperature=None, wind_speed=None,
                 wind_gust=None, wind_deg=None, pressure=None, humidity=None,
                 rain_1h=None, rain_6h=None, rain_24h=None, snow_1h=None,
                 snow_6h=None, snow_24h=None, dew_point=None, humidex=None,
                 heat_index=None, visibility_distance=None, visibility_prefix=None,
                 clouds_distance=None, clouds_condition=None, clouds_cumulus=None,
                 weather_precipitation=None, weather_descriptor=None,
                 weather_intensity=None, weather_proximity=None,
                 weather_obscuration=None, weather_other=None):
        assert station_id is not None
        assert isinstance(timestamp, int)
        assert not timestamp < 0
        self.station_id = station_id
        self.timestamp = timestamp
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.wind_gust = wind_gust
        self.wind_deg = wind_deg
        self.pressure = pressure
        self.humidity = humidity
        self.rain_1h = rain_1h
        self.rain_6h = rain_6h
        self.rain_24h = rain_24h
        self.snow_1h = snow_1h
        self.snow_6h = snow_6h
        self.snow_24h = snow_24h
        self.dew_point = dew_point
        self.humidex = humidex
        self.heat_index = heat_index
        self.visibility_distance = visibility_distance
        self.visibility_prefix = visibility_prefix
        self.clouds_distance = clouds_distance
        self.clouds_condition = clouds_condition
        self.clouds_cumulus = clouds_cumulus
        self.weather_precipitation = weather_precipitation
        self.weather_descriptor = weather_descriptor
        self.weather_intensity = weather_intensity
        self.weather_proximity = weather_proximity
        self.weather_obscuration = weather_obscuration
        self.weather_other = weather_other

    def creation_time(self, timeformat='unix'):
        """Returns the UTC time of creation of this raw measurement

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time, '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00`` or `date` for
            a ``datetime.datetime`` object
        :type timeformat: str
        :returns: an int or a str or a ``datetime.datetime`` object or None
        :raises: ValueError

        """
        if self.timestamp is None:
            return None
        return formatting.timeformat(self.timestamp, timeformat)

    @classmethod
    def from_dict(cls, the_dict):
        if 'station_id' not in the_dict:
            raise KeyError('"station_id" must be provided')
        station_id = the_dict['station_id']
        if 'timestamp' not in the_dict:
            raise KeyError('"timestamp" must be provided')
        timestamp = the_dict['timestamp']

        temperature = the_dict.get('temperature', None)
        wind_speed = the_dict.get('wind_speed', None)
        wind_gust = the_dict.get('wind_gust', None)
        wind_deg = the_dict.get('wind_deg', None)
        pressure = the_dict.get('pressure', None)
        humidity = the_dict.get('humidity', None)
        rain_1h = the_dict.get('rain_1h', None)
        rain_6h = the_dict.get('rain_6h', None)
        rain_24h = the_dict.get('rain_24h', None)
        snow_1h = the_dict.get('snow_1h', None)
        snow_6h = the_dict.get('snow_6h', None)
        snow_24h = the_dict.get('snow_24h', None)
        dew_point = the_dict.get('dew_point', None)
        humidex = the_dict.get('humidex', None)
        heat_index = the_dict.get('heat_index', None)
        visibility_distance = the_dict.get('visibility_distance', None)
        visibility_prefix = the_dict.get('visibility_prefix', None)
        clouds_distance = the_dict.get('clouds_distance', None)
        clouds_condition = the_dict.get('clouds_condition', None)
        clouds_cumulus = the_dict.get('clouds_cumulus', None)
        weather_precipitation = the_dict.get('weather_precipitation', None)
        weather_descriptor = the_dict.get('weather_descriptor', None)
        weather_intensity = the_dict.get('weather_intensity', None)
        weather_proximity = the_dict.get('weather_proximity', None)
        weather_obscuration = the_dict.get('weather_obscuration', None)
        weather_other = the_dict.get('weather_other', None)
        return Measurement(station_id, timestamp, temperature=temperature,
            wind_speed=wind_speed, wind_gust=wind_gust, wind_deg=wind_deg,
            pressure=pressure, humidity=humidity,rain_1h=rain_1h,rain_6h=rain_6h,
            rain_24h=rain_24h,snow_1h=snow_1h,snow_6h=snow_6h,snow_24h=snow_24h,
            dew_point=dew_point,humidex=humidex,heat_index=heat_index,
            visibility_distance=visibility_distance,visibility_prefix=visibility_prefix,
            clouds_distance=clouds_distance,clouds_condition=clouds_condition,
            clouds_cumulus=clouds_cumulus,weather_precipitation=weather_precipitation,
            weather_descriptor=weather_descriptor,weather_intensity=weather_intensity,
            weather_proximity=weather_proximity,weather_obscuration=weather_obscuration,
            weather_other=weather_other)

    def to_dict(self):
        """Dumps object fields into a dictionary

        :returns: a dict

        """
        return {
            'station_id': self.station_id,
            'timestamp': self.timestamp,
            'temperature': self.temperature,
            'wind_speed': self.wind_speed,
            'wind_gust': self.wind_gust,
            'wind_deg': self.wind_deg,
            'pressure': self.pressure,
            'humidity': self.humidity,
            'rain_1h': self.rain_1h,
            'rain_6h': self.rain_6h,
            'rain_24h': self.rain_24h,
            'snow_1h': self.snow_1h,
            'snow_6h': self.snow_6h,
            'snow_24h': self.snow_24h,
            'dew_point': self.dew_point,
            'humidex': self.humidex,
            'heat_index': self.heat_index,
            'visibility_distance': self.visibility_distance,
            'visibility_prefix': self.visibility_prefix,
            'clouds_distance': self.clouds_distance,
            'clouds_condition': self.clouds_condition,
            'clouds_cumulus': self.clouds_cumulus,
            'weather_precipitation': self.weather_precipitation,
            'weather_descriptor': self.weather_descriptor,
            'weather_intensity': self.weather_intensity,
            'weather_proximity': self.weather_proximity,
            'weather_obscuration': self.weather_obscuration,
            'weather_other': self.weather_other}

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns: the JSON string

        """
        return json.dumps(self.to_dict())

    def __repr__(self):
        return '<%s.%s - station_id=%s, created_at=%s>' \
               % (__name__, self.__class__.__name__,
                  self.station_id, self.creation_time())
