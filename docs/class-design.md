OWM: class
==========
Fields
------
+ APIkey: string
+ location: Location

Methods
-------
+ getLocation: Location
+ setLocation: void
+ getAPIkey: string
+ setAPIkey: void
+ currentWeather: Weather


Location: class
===============
Fields
------
+ name: string
+ coordinates: dict
+ ID: string

Methods
-------
+ getName: string
+ setName: void
+ getCoordinates: dict
+ setCoordinates: void
+ getID: string
+ setID: void


Weather: class
==============

Fields
------
+ base: string
+ referenceTime: int
+ location: Location
+ ephemeris: Ephemeris
+ clouds: dict
+ rain: dict
+ snow: dict
+ wind:dict
+ humidity: int
+ pressure: float
+ temperature: float
+ minTemperature: float
+ maxTemperature: float
+ status: string
+ detailedStatus: string
+ weatherCode: int
+ iconName: string

Methods
-------
+ getClouds: dict
+ getRain: dict
+ getSnow: dict
+ getWind: dict
+ getHumidity: int
+ getPressure: float
+ getTemperature: float
+ getMaxTemperature: float
+ getMinTemperature: float
+ getStatus: string
+ getDetailedStatus: string
+ getWeatherCode: int
+ getIconName: string
+ getIconURL: string
+ getLocation: Location
+ getReferenceTime: int/string
+ getEphemeris: Ephemeris
+ update: void
+ dumpJSON: string
+ dumpXML: string 


Ephemeris: class
================

Fields
------
+ sunrise: int
+ sunset: int

Methods
-------
+ getSunrise: int/string
+ getSunset: int/string