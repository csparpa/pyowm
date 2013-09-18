TODOs
=====

Code
----
+ Forecast class:
    - Forecast.when_starts(timeformat='unixtime|iso') -> when in time does the forecast start?
    - Forecast.when_ends(timeformat='unixtime|iso') -> when in time will the forecast end?
    - Forecast.will_have_rain() -> will it rain during the coverage period? returns bool
    - Forecast.will_have_sun() -> will it be sunny during the coverage period? returns bool
    - Forecast.will_have_snow() -> will it snow during the coverage period? returns bool

    - Forecast.when_rain() -> list rainy Weather objs in forecats
    - Forecast.when_sun() -> list sunny Weather objs in forecats
    - Forecast.when_snow() -> list snowy Weather objs in forecats
    
      #return error if unixtime is not in coverage
    - Forecast.will_be_rainy_on(datetime|unixtime)
    - Forecast.will_be_sunny_on(datetime|unixtime)
    - Forecast.will_be_snowy_on(datetime|unixtime)
    - Forecast.get_weather_at(datetime|unixtime) -> the closest Weather in time to the specified unixtime,
+ Implement remaining features
+ (eventual) Provide utilities for human-friendly OWM data handling in separate
   project: 
    - find current weather for my position (geolocate IP?)
    - find forecasts for my position (geolocate IP?)
+ Provide __str__ hooks for each class

Test
----
+ Test features on different platforms (Linux, MacOS, Win)
+ Test features on Python 3.x and 2.0+

Docs
----
+ Write wiki with library API
+ Write better documentation in code
+ Explain internals:
    + class diagram
    + explain pywom design choices (eg: names usage, where it is not such a "thin" wrapper, etc)

Various
-------
+ Sponsorize (FB, Linkedin, blog)
+ (eventual) Provide XML schemas
+ (eventual) Upload egg to cheeseshop or similars
