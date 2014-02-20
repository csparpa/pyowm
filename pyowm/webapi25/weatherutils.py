#!/usr/bin/env python

"""
Module containing search and filter utilities for *Weather* objects lists
management
"""
from pyowm.exceptions.not_found_error import NotFoundError


def status_matches_any(word_list, weather):
    """
    Checks if one or more keywords in a given list is contained into the
    detailed weather status of a *Weather* object

    :param word_list: a list of string keywords
    :type word_list: list
    :param weather: a *Weather* object
    :type weather: *Weather*
    :returns: ``True`` if one or more matchings are found, ``False`` otherwise

    """
    detailed_status = weather.get_detailed_status().lower()
    for word in word_list:
        if word in detailed_status:
            return True
    return False


def statuses_match_any(word_list, weathers_list):
    """
    Checks if one or more of the detailed statuses of the *Weather* objects
    into the given list contain at least one of the keywords in the given list

    :param word_list: a list of string keywords
    :type word_list: list
    :param weathers_list: a list of *Weather* objects
    :type weathers_list: list
    :returns: ``True`` if one or more matchings are found, ``False`` otherwise
    """
    for weather in weathers_list:
        if status_matches_any(word_list, weather):
            return True
    return False


def filter_by_matching_statuses(word_list, weathers_list):
    """
    Returns a sublist of the given list of *Weather* objects, whose items
    have at least one of the keywords from the given list as part of their
    detailed statuses.

    :param word_list: a list of string keywords
    :type word_list: list
    :param weathers_list: a list of *Weather* objects
    :type weathers_list: list
    :returns: a list of *Weather* objects
    """
    result = []
    for weather in weathers_list:
        if status_matches_any(word_list, weather):
            result.append(weather)
    return result


def is_in_coverage(unixtime, weathers_list):
    """
    Checks if the supplied UNIX time is contained into the time range
    (coverage) defined by the most ancient and most recent *Weather* objects
    in the supplied list

    :param unixtime: the UNIX time to be searched in the time range
    :type unixtime: int/long
    :param weathers_list: the list of *Weather* objects to be scanned for
        global time coverage
    :type weathers_list: list
    :returns: ``True`` if the UNIX time is contained into the time range,
        ``False`` otherwise
    """
    if not weathers_list:
        return False
    else:
        min_of_coverage = min([weather.get_reference_time() \
                               for weather in weathers_list])
        max_of_coverage = max([weather.get_reference_time() \
                               for weather in weathers_list])
        if unixtime < min_of_coverage or unixtime > max_of_coverage:
            return False
        return True


def find_closest_weather(weathers_list, unixtime):
    """
    Extracts from the provided list of Weather objects the item which is
    closest in time to the provided UNIXtime.

    :param weathers_list: a list of *Weather* objects
    :type weathers_list: list
    :param unixtime: a UNIX time
    :type unixtime: long
    :returns: the *Weather* object which is closest in time or ``None`` if the
        list is empty
    """
    if not weathers_list:
        return None
    if not is_in_coverage(unixtime, weathers_list):
        raise NotFoundError('Error: the specified time is not included in ' \
                            'the weather coverage range')
    closest_weather = weathers_list[0]
    time_distance = abs(closest_weather.get_reference_time() - unixtime)
    for weather in weathers_list:
        if abs(weather.get_reference_time() - unixtime) < time_distance:
            time_distance = abs(weather.get_reference_time() - unixtime)
            closest_weather = weather
    return closest_weather
