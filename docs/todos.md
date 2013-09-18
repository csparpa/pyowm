TODOs
-----
+ Provide a way to None-ify the eventually missing info (eg: sunrise time, etc)
+ Write wiki with library API
+ Explain internals:
    + class diagram
    + explain pywom design choices (eg: names usage, where it is not such a "thin" wrapper, etc)
+ Write better documentation in code
+ Sponsorize (FB, Linkedin, blog)
+ Provide __str__ hooks for each class
+ Test features on different platforms (Linux, MacOS, Win)
+ Test features on Python 3.x and 2.0+
+ (eventual) Provide XML schemas
+ (eventual) Provide utilities for human-friendly OWM data handling in separate
   project: 
    - find current weather for my position (geolocate IP)
    - find forecasts for my position
    - Forecast.weather_at(unixtime) -> the closest Weather in time to the 
      specified unixtime
    - Forecast.will_be_rainy() -> will it rain? returns bool
    - Forecast.will_be_clear() -> will it rain? returns bool
    - Forecast.will_be_snowy() -> will it rain? returns bool
    - Forecast.when_rain(timeformat='unixtime|iso') -> list rainy Weather objs in forecats
    - Forecast.when_sun(timeformat='unixtime|iso') -> list sunny Weather objs in forecats
    - Forecast.when_snow(timeformat='unixtime|iso') -> list rainy Weather objs in forecats
+ (eventual) Upload egg to cheeseshop or similars
