OWM: class
==========
Fields
------
+ API_key: string

Methods
-------
+ get_API_key: string
+ set_API_key: void
+ get_API_version: float
+ get_version: float
+ observation_at_place: Observation
+ observation_at_coords: Observation
+ find_observations_by_name: list of Observations
+ find_observations_by_coords: list of Observations
+ three_hours_forecast: Forecast
+ daily_forecast: Forecast


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
+ get_name: string
+ get_lon: int
+ get_lat: int
+ get_ID: string
+ to_JSON: string
+ to_XML: string


Observation: class
==================
Fields
------
+ reception_time: long
+ location: Location
+ weather: Weather

Methods
-------
+ get_reception_time: long
+ get_location: Location
+ get_weather: Weather
+ to_JSON: string
+ to_XML: string

Forecast: class
===============

Fields
------
+ span: int
+ reception_time: long
+ location: Location
+ items: list of Weather objs

Methods
-------
+ get_span: int
+ get_reception_time: long
+ get_location: Location
+ get_items: list of Weather objs
+ to_JSON: string
+ to_XML: string


Weather: class
==============

Fields
------
+ reference_time: long
+ sunset: long
+ sunrise: long
+ clouds: int
+ rain: dict
+ snow: dict
+ wind:dict
+ humidity: int
+ pressure: dict
+ temperature: dict
+ status: string
+ detailed_status: string
+ weather_code: int
+ weather_icon_name: string

Methods
-------
+ get_clouds: int
+ get_rain: dict
+ get_snow: dict
+ get_wind: dict
+ get_humidity: int
+ get_pressure: float
+ get_temperature: dict
+ get_status: string
+ get_detailed_status: string
+ get_weather_code: int
+ get_icon_name: string
+ get_location: Location
+ get_reference_time: long
+ get_sunset: long
+ get_sunrise: long
+ to_JSON: string
+ to_XML: string