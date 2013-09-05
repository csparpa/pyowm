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
        name - location toponym (string)
        lon - location longitude (int/float between -180 and 180 degrees)
        lat - location latitude (int/float between -90 and 90 degress)
        ID - location OpenWeatherMap city ID (int)
        
        For reference about OWM city IDs refer to:
          http://bugs.openweathermap.org/projects/api/wiki/Api_2_5_weather#3-By-city-ID
        """
        
        assert type(name) is str, "'name' must be an string"
        self.name = name
        assert type(lon) is float or type(lon) is int,"'lon' must be a float"
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        self.lon = float(lon)
        assert type(lat) is float or type(lat) is int,"'lat' must be a float"
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        self.lat = float(lat)
        assert type(ID) is int, "'ID' must be an int"
        if ID < 0:
            raise ValueError("'ID' must be greater than 0")
        self.ID = ID
        
    def getName(self):
        """Returns the toponym of the location as a string"""
        return self.name
    
    def getLon(self):
        """Returns the longitude of the location as a float"""
        return self.lon
    
    def getLat(self):
        """Returns the latitude of the location as a float"""
        return self.lat
    
    def getID(self):
        """Returns the OWM city ID of the location"""
        return self.ID
    
    def toJSON(self):
        return dumps({ 'name': self.name, 'coordinates': { 'lon': self.lon, 
            'lat': self.lat}, 'ID': self.ID })
    
    def toXML(self):
        return """<Location><name>%s</name><coordinates><lon>%s</lon><lat>%s</lat></coordinates><ID>%s</ID></Location>""" % (self.name,
            self.lon, self.lat, self.ID)
    
    def __str__(self):
        """Redefine __str__ hook for pretty-printing of Location instances"""
        return '[Location: name=%s lon=%s lat=%s ID=%s]' % (self.name, self.lon, self.lat, self.ID)