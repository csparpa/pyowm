#!/usr/bin/env python

"""
Location-related classes and data structures. 
"""

from json import dumps

class Location(object):
    """
    A databox representing a location in the world. A location is defined through
    the following information: toponym, longitude, latitude and OWM city ID.
    """
    
    def __init__(self, name, lon, lat, ID):
        """
        name - location toponym (str)
        lon - location longitude (int/float between -180 and 180 degrees)
        lat - location latitude (int/float between -90 and 90 degress)
        ID - location OpenWeatherMap city ID (int)
        
        For reference about OWM city IDs visit:
          http://bugs.openweathermap.org/projects/api/wiki/Api_2_5_weather#3-By-city-ID
        """
        
        assert type(name) is str, "'name' must be a string"
        self.__name = name
        assert type(lon) is float or type(lon) is int,"'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        self.__lon = float(lon)
        assert type(lat) is float or type(lat) is int,"'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        self.__lat = float(lat)
        assert type(ID) is int, "'ID' must be an int"
        self.__ID = ID
        
    def get_name(self):
        """Returns the toponym of the location as a str"""
        return self.__name
    
    def get_lon(self):
        """Returns the longitude of the location as a float"""
        return self.__lon
    
    def get_lat(self):
        """Returns the latitude of the location as a float"""
        return self.__lat
    
    def get_ID(self):
        """Returns the OWM city ID of the location"""
        return self.__ID
    
    def to_JSON(self):
        """Dumps object fields into a JSON formatted string"""
        return dumps({ 'name': self.__name, 'coordinates': { 'lon': self.__lon, 
            'lat': self.__lat}, 'ID': self.__ID })
    
    def to_XML(self):
        """Dumps object fields into a XML formatted string"""
        return """<Location><name>%s</name><coordinates><lon>%s</lon><lat>%s</lat></coordinates><ID>%s</ID></Location>""" % (self.__name,
            self.__lon, self.__lat, self.__ID)
    
    def __str__(self):
        """Redefine __str__ hook for pretty-printing of Location instances"""
        return '[Location: name=%s lon=%s lat=%s ID=%s]' % (self.__name, self.__lon, self.__lat, self.__ID)