OWM: class
==========
Fields
------
+ APIkey: string

Methods
-------
+ getAPIkey: string
+ setAPIkey: void
+ observation: Observation
+ findObservationsByName: list of Observations
+ findObservationsByCoords: list of Observations
+ 3hForecast: Forecast
+ dailyForecast: Forecast


Location: class
===============
Fields
------
+ name: string
+ lon: int
+ lat: int
+ ID: int

Methods
-------
+ getName: string
+ getLon: int
+ getLat: int
+ getID: string
+ toJSON: string
+ toXML: string


Observation: class
==================
Fields
------
+ receptionTime: int
+ location: Location
+ weather: Weather

Methods
-------
+ getReceptionTime: int
+ getLocation: Location
+ getWeather: Weather
+ toJSON: string
+ toXML: string

Forecast: class
===============

Fields
------
+ type: string
+ receptionTime: int
+ location: Location
+ items: list of Weather objs

Methods
-------
+ getType: string
+ getReceptionTime: int
+ getLocation: Location
+ getItems: list of Weather objs
+ toJSON: string
+ toXML: string


Weather: class
==============

Fields
------
+ base: string
+ referenceTime: int
+ sunset: int
+ sunrise: int
+ clouds: int
+ rain: dict
+ snow: dict
+ wind:dict
+ humidity: int
+ pressure: float
+ temperature: dict
+ status: string
+ detailedStatus: string
+ weatherCode: int
+ iconName: string

Methods
-------
+ getClouds: int
+ getRain: dict
+ getSnow: dict
+ getWind: dict
+ getHumidity: int
+ getPressure: float
+ getTemperature: dict
+ getStatus: string
+ getDetailedStatus: string
+ getWeatherCode: int
+ getIconName: string
+ getLocation: Location
+ getReferenceTime: int
+ getSunset: int
+ getSunrise: int
+ toJSON: string
+ toXML: string