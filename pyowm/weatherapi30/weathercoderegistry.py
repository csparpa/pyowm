#!/usr/bin/env python
# -*- coding: utf-8 -*-


WEATHER_CODES_INTERVALS = {
    "rain": [{
        "start": 500,
        "end": 531
    },
    {
        "start": 300,
        "end": 321
    }],
    "sun": [{
        "start": 800,
        "end": 800
    }],
    "clouds": [{
        "start": 801,
        "end": 804
    }],
    "fog": [{
        "start": 741,
        "end": 741
    }],
    "haze": [{
        "start": 721,
        "end": 721
    }],
    "mist": [{
        "start": 701,
        "end": 701
    }],
    "snow": [{
        "start": 600,
        "end": 622
    }],
    "tornado": [{
        "start": 781,
        "end": 781
    },
    {
        "start": 900,
        "end": 900
    }],
    "storm": [{
        "start": 901,
        "end": 901
    },
    {
        "start": 960,
        "end": 961
    }],
    "hurricane": [{
        "start": 902,
        "end": 902
    },
    {
        "start": 962,
        "end": 962
    }]
}


class WeatherCodeRegistry:

    """
    A registry class for looking up weather statuses from weather codes.

    :param code_ranges_dict: a dict containing the mapping between weather
        statuses (eg: "sun","clouds",etc) and weather code ranges
    :type code_ranges_dict: dict
    :returns: a *WeatherCodeRegistry* instance

    """

    def __init__(self, code_ranges_dict):
        assert isinstance(code_ranges_dict, dict)
        self._code_ranges_dict = code_ranges_dict

    def status_for(self, code):
        """
        Returns the weather status related to the specified weather status
        code, if any is stored, ``None`` otherwise.

        :param code: the weather status code whose status is to be looked up
        :type code: int
        :returns: the weather status str or ``None`` if the code is not mapped
        """
        is_in = lambda start, end, n: start <= n <= end
        for status in self._code_ranges_dict:
            for _range in self._code_ranges_dict[status]:
                if is_in(_range['start'],_range['end'],code):
                    return status
        return None

    @classmethod
    def get_instance(cls):
        """
        Factory method returning the default weather code registry
        :return: a `WeatherCodeRegistry` instance
        """
        return WeatherCodeRegistry(WEATHER_CODES_INTERVALS)

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)