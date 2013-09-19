TODOs
=====

Code
----
+ Forecaster class:
    - Forecaster.when_rain() -> list rainy Weather objs in forecats
    - Forecaster.when_sun() -> list sunny Weather objs in forecats
    - Forecaster.when_snow() -> list snowy Weather objs in forecats
    - Forecaster.when_fog() -> list foggy Weather objs in forecats
    
      #the following return error if unixtime is not in coverage
    - Forecaster.will_be_rainy_on(datetime|unixtime|iso)
    - Forecaster.will_be_sunny_on(datetime|unixtime|iso)
    - Forecaster.will_be_snowy_on(datetime|unixtime|iso)
    - Forecaster.will_be_foggy_on(datetime|unixtime|iso)
    - Forecaster.get_weather_at(datetime|unixtime|iso) -> the closest Weather in time to the specified time
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
    + explain pywom design choices (eg: names usage, why end users do not deal
      with city IDs, why it is not such a "thin" wrapper, the API is rotting, etc)

Various
-------
+ Sponsorize (FB, Linkedin, blog)
+ (eventual) Provide XML schemas
+ (eventual) Upload egg to cheeseshop or similars
