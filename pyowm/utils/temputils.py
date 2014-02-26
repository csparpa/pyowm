#!/usr/bin/env python

"""
Module containing utility functions for temperature units conversion
"""

KELVIN_OFFSET = 273.15
FAHRENHEIT_OFFSET = 32.0
FAHRENHEIT_DEGREE_SCALE = 1.8


def kelvin_to_celsius(kelvintemp):
    """
    Converts a numeric temperature from Kelvin degrees to Celsius degrees

    :param kelvintemp: the Kelvin temperature
    :type kelvintemp: int/long/float
    :returns: the float Celsius temperature
    :raises: *TypeError* when bad argument types are provided

    """
    if kelvintemp < 0:
        raise ValueError(__name__ + \
                         ": negative temperature values not allowed")
    celsiustemp = kelvintemp - KELVIN_OFFSET
    return float("{0:.2f}".format(celsiustemp))


def kelvin_to_fahrenheit(kelvintemp):
    """
    Converts a numeric temperature from Kelvin degrees to Fahrenheit degrees

    :param kelvintemp: the Kelvin temperature
    :type kelvintemp: int/long/float
    :returns: the float Fahrenheit temperature

    :raises: *TypeError* when bad argument types are provided
    """
    if kelvintemp < 0:
        raise ValueError(__name__ + \
                         ": negative temperature values not allowed")
    fahrenheittemp = (kelvintemp - KELVIN_OFFSET) * \
        FAHRENHEIT_DEGREE_SCALE + FAHRENHEIT_OFFSET
    return float("{0:.2f}".format(fahrenheittemp))
