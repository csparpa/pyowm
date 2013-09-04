#!/usr/bin/env python

"""
Location-related classes and data structures. 
"""

class Location(object):
    """
    A databox representing a location in the world. A location is defined through
    the following information: toponym, geographic coordinates and OWM city ID.
    """
    
    def __init__(self, name, coordinates, ID):
	assert type(name) is str, "'name' must be an string"
        self.name = name
        assert type(coordinates) is dict ,"'coordinates' must be a dict" 
        self.coordinates = coordinates
        assert type(ID) is int, "'ID' must be an int"
        self.ID = ID
        
    def getName(self):
        """Returns the toponym of the location"""
        return self.name
    
    def getCoordinates(self):
        """Returns the lon/lat coordinates of the location as a dict"""
        return self.coordinates
    
    def getID(self):
        """Returns the OWM city ID of the location"""
        return self.ID
    
    def dumpJSON(self):
        raise Exception('Not yet implemented')
    
    def dumpXML(self):
        raise Exception('Not yet implemented')
    
    def __print__(self):
        raise Exception('Not yet implemented')