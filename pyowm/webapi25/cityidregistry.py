from pyowm.webapi25.location import Location
from pkg_resources import resource_stream

"""
Module containing a registry with lookup methods for OWM-provided city IDs
"""

class CityIDRegistry():

    """
    Initialise a registry that can be used to lookup info about cities.

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
        line = self._lookup_line_by_city_name(city_name)
        return int(line.split(",")[1]) if line is not None else None

    def location_for(self, city_name):
        """
        Returns the *Location* object corresponding to the provided city name.

        :param city_name: the city name you want a *Location* for
        :type city_name: str
        :returns: a *Location* instance or ``None`` if the lookup fails

        """
        line = self._lookup_line_by_city_name(city_name)
        if line is None:
            return None
        tokens = line.split(",")
        return Location(tokens[0], float(tokens[3]), float(tokens[2]),
                        int(tokens[1]), 'NL')

    def _assess_subfile_from(self, city_name):
        c = ord(city_name.lower()[0])
        if c < 97: # not a letter
            raise ValueError('Error: city name must start with a letter')
        elif c in range(97, 103):  # from a to f
            return self._filepath_regex % (97, 102)
        elif c in range(103, 109): # from g to l
            return self._filepath_regex % (103, 108)
        elif c in range(109, 115): # from m to r
            return self._filepath_regex % (109, 114)
        elif c in range (115, 123): # from s to z
            return self._filepath_regex % (115, 122)
        else:
            raise ValueError('Error: city name must start with a letter')

    def _lookup_line_by_city_name(self, city_name):
        filename = self._assess_subfile_from(city_name)
        lines = self._get_lines(filename)
        return self._match_line(city_name, lines)
    
    def _get_lines(self, filename):
        with resource_stream(__name__, filename) as f:
            lines = f.readlines()
            if type(lines[0]) is bytes:
                lines = map(lambda l: l.decode("utf-8"), lines)
            return lines
    
    def _match_line(self, city_name, lines):
        for line in lines:
            if line.startswith(city_name.lower()):
                return line.strip()
        return None

    def __repr__(self):
        return "<%s.%s - filepath_regex=%s>" % (__name__, \
          self.__class__.__name__, self._filepath_regex)