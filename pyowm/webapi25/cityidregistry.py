#!/usr/bin/env python

"""
Module containing a registry with lookup methods for OWM-provided city IDs
"""

class CityIDRegistry():

    """
    Initialise a registry that can be used

    :param filepath_regex: Python format string that gives the path of the files
           that store the city IDs information.
           Eg: ``folder1/folder2/%02d-%02d.txt``
    :type filepath_regex: str
    :returns: a *CityIDRegistry* instance

    """
    def __init__(self, filepath_regex):
        self._filepath_regex = filepath_regex

    def id_for(self, city_name):
        """
        Returns the long ID corresponding to the provided city name.

        :param city_name: the city name whose ID is looked up
        :type city_name: str
        :returns: a long or ``None`` if the lookup fails

        """
        pass

    def location_for(self, city_name):
        """
        Returns the *Location* object corresponding to the provided city name.

        :param city_name: the city name you want a *Location* for
        :type city_name: str
        :returns: a *Location* instance or ``None`` if the lookup fails

        """
        pass

