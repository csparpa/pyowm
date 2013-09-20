#!/usr/bin/env python

"""
Search and filter utilities for Weather lists management
"""

def status_matches_any(word_list, weather):
    """
    Checks if one or more words in a given list is contained into the
    detailed weather statuses of a Weather object
    
    word_list - list of str
    weather - Weather object
    """
    detailed_status = weather.get_detailed_status().lower()
    for word in word_list:
        if word in detailed_status:
            return True
    return False

def statuses_match_any(word_list, weather_list):
    """
    Checks if one or more of the detailed statuses of the Weather objects 
    into the given list contain at least one of the words in the given word 
    list
    
    word_list - list of str
    weather_list - list of Weather objects
    """
    for weather in weather_list:
        if status_matches_any(word_list, weather):
            return True
    return False
        
def filter_by_matching_statuses(word_list, weather_list):
    """
    Returns a sublist of the given list of Weather objects, whose items
    have at least one of the words in the given list as part of their
    detailed statuses
    
    word_list - list of str
    weather_list - list of Weather objects
    """
    result = []
    for weather in weather_list:
        if status_matches_any(word_list, weather):
            result.append(weather)
    return result

def find_closest_weather(weather_list, unixtime):
    """
    Extracts from the provided list of Weather objects the one which is
    closest in time to the provided unixtime
    
    weather_list - list of Weather objects
    unixtime - UNIXtime (long)
    """
    closest_weather = weather_list[0]
    time_distance = abs(closest_weather.get_reference_time() - unixtime)
    for weather in weather_list:
        if abs(weather.get_reference_time() - unixtime) < time_distance:
            time_distance = abs(weather.get_reference_time() - unixtime)
            closest_weather = weather
    return closest_weather