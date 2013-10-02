PyOWM usage examples
====================

Import the PyOWM library
------------------------
As simple as:

    >>> from pyowm import OWM

Create global OWM object
------------------------
Use your OWM API key if you have one (read [here](http://openweathermap.org/appid) 
on how to obtain an API key).

    >>> API_key = 'G097IueS-9xN712E'
    >>> owm = OWM(API_key)
    
Of course you can change your API Key at a later time if you need:

    >>> owm.get_API_key()
    'G09_7IueS-9xN712E'
    >>> owm.set_API_key('6Lp$0UY220_HaSB45')

Getting currently observed weather for a specific location
----------------------------------------------------------
Querying for current weather is simple: provide an _OWM_ object with the location
you want the current weather be looked up for and the job is done.
You can specify the location either by passing its toponym (eg: "London") or
its geographic coordinates (lon/lat):

    obs = owm.weather_at('London,uk')                          # Toponym
    obs = owm.weather_at_coords(-0.107331,51.503614)           # Lon/lat

A _Observation_ object will be returned, containing weather info about the 
location matching the toponym/coordinates you provided. Be precise when
specifying locations!
    
    
Currently observed weather extended search
------------------------------------------
You can query for currently observed weather:

+ for all the places whose name equals the toponym you provide (use _search='accurate'_)
+ for all the places whose name contains the toponym you provide (use _search='like'_)
+ for all the places whose lon/lat coordinates are in the surroundings of the lon/lat couple you provide

In all cases, a list of _Observation_ objects is returned, each one describing 
the weather currently observed in one of the places matching the search.
You can control how many items the returned list will contain by using the
_limit_ parameter.

Examples:

    # Find observed weather in all the "London"s in the world
    obs_list = owm.find_weather_by_name('London', 'accurate')
    # As above but limit result items to 3
    obs_list = owm.find_weather_by_name('London',searchtype='accurate',limit=3)
    
    # Find observed weather for all the places whose name contains the word "London"
    obs_list = owm.find_weather_by_name('London', 'like')
    # As above but limit result items to 5
    obs_list = owm.find_weather_by_name('London',searchtype='like', 5)
    
    # Find observed weather for all the places in the surroundings of lon=-2.15,lat=57
    obs_list = owm.find_weather_by_coords(-2.15, 57)
    # As above but limit result items to 8
    obs_list = owm.find_weather_by_coords(-2.15, 57, limit=8)

Getting data from Observation objects
-------------------------------------

_Observation_ objects stores two useful objects: a _Weather_ object that
contains the weather-related data and a _Location_ object that describes the
location for which the weather data is provided.

If you want to know when the weather observation data have been received, just
call:

    >>> obs.get_reception_time()                           # UNIX GMT time
    1379091600L
    >>> obs.get_reception_time(timeformat='iso')           # ISO 8601
    '2013-09-13 17:00:00+00'

You can retrieve the _Weather_ object like this:

    >>> w = obs.get_weather()

and then access weather data using the following methods:

    >>> w.get_reference_time()                             # get time of observation in GMT UNIXtime
    1377872206L
    >>> w.get_reference_time(timeformat='iso')             # ...or in ISO 8601
    '2013-08-30 14:16:46+00'
    
    >>> w.get_clouds()                                     # Get cloud coverage
    65
    
    >>> w.get_rain()                                       # Get rain volume
    {'3h': 0}
    
    >>> w.get_snow()                                       # Get snow volume
    {}
    
    >>> w.get_wind()                                       # Get wind degree and speed
    {'deg': 59, 'speed': 2.660}
    
    >>> w.get_humidity()                                   # Get humidity percentage
    67
    
    >>> w.get_pressure()                                   # Get atmospheric pressure
    {'press': 1009, 'sea_level': 1038.381}
    
    >>> w.get_temperature()                                # Get temperature in Kelvin degs
    {'temp': 293.4, 'temp_kf': None, 'temp_max': 297.5, 'temp_min': 290.9}
    >>> w.get_temperature(unit='celsius')                  # ... or in Celsius degs
    >>> w.get_temperatire('fahrenheit')                    # ... or in Fahrenheit degs

    >>> w.get_status()                                     # Get weather short status
    'clouds'
    >>> w.get_detailedS_status()                           # Get detailed weather status
    'Broken clouds'

    >>> w.get_weather_code()                               # Get OWM weather condition code
    803
    
    >>> w.get_weather_icon_name()                          # Get weather-related icon name
    '02d'

    >>> w.get_sunrise_time()                               # Sunrise time (GMT UNIXtime or ISO 8601)
    1377862896L
    >>> w.get_sunset_time('iso')                           # Sunset time (GMT UNIXtime or ISO 8601)
    '2013-08-30 20:07:57+00'

Support to weather data interpreting can be found [here](http://bugs.openweathermap.org/projects/api/wiki/Weather_Data#Description-parameters) 
and [here](http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes) you can read about OWM weather condition codes and icons.

As said, _Observation_ objects also contain a _Location_ objects with info about
the weather location:

    >>> l = obs.get_location()
    >>> l.get_name()
    'London'
    >>> l.get_lon()
    -0.12574
    >>> l.get_lat()
    51.50863
    >>> l.get_ID()
    2643743

The last call returns the OWM city ID of the location - refer to the 
[OWM API documentation](http://bugs.openweathermap.org/projects/api/wiki/Api_2_5_weather#3-By-city-ID)
for details.

Getting weather forecasts
-------------------------
The OWM web API currently provides weather forecasts that are sampled :

+ every 3 hours
+ every day (24 hours)

The 3h forecasts are provided for a streak of 5 days since the request time and
daily forecasts are provided for a maximum streak of 14 days since the request 
time (but also shorter streaks can be obtained).

You can query for 3h forecasts for a location using:

    # Query for 3 hours weather forecast for the next 5 days over London
    >>> fc = owm.three_hours_forecast('London,uk')
    
You can query for daily forecasts using:

    # Query for daily weather forecast for the next 14 days over London
    >>> fc = owm.daily_forecast('London,uk')
    
and in this case you can limit the amount of days the weather forecast streak
will contain by using:

    # Daily weather forecast just for the next 6 days over London
    >>> fc = owm.daily_forecast('London,uk',limit=6)
    
Both of the above calls return a _Forecaster_ object. _Forecaster_ objects 
contain a _Forecast_ object, which has all the information about your weather
forecast. If you need to manipulate the latter, just go with:

    >>> f = fc.get_forecast()

A _Forecast_ object encapsulates the _Location_ object relative to the forecast
and a list of _Weather_ objects:

    # When has the forecast been received?
    >>> f.get_reception_time()                           # UNIX GMT time
    1379091600L
    >>> f.get_reception_time('iso')                      # ISO 8601
    '2013-09-13 17:00:00+00'
    
    # Which time interval for the forecast? 
    >>> f.get_interval()
    'daily'

    # How many weather items are in the forecast?
    >>> len(f)
    20 

    # Get Location
    >>> f.get_location()
    <pyowm.location.Location object at 0x01921DF0>
    
Once you obtain a _Forecast_ object, reading the forecast data is easy - you can
get the whole list of _Weather_ objects or you can use the built-in iterator:
    
    # Get the list of Weather objects...
    >>> lst = f.get_weathers()
    
    # ...or iterate directly over the Forecast object
    >>> for weather in f:
          print (weather.get_reference_time('iso'),weather.get_status())
    ('2013-09-14 14:00:00+0','Clear')
    ('2013-09-14 17:00:00+0','Clear')
    ('2013-09-14 20:00:00+0','Clouds')

The _Forecaster_ class provides a few convenience methods to inspect the
weather forecasts in a human-friendly fashion. You can - for example - ask for 
the GMT time boundaries of the weather forecast data:

    # When in time does the forecast begin?
    >>> fc.when_starts()                                  # UNIX GMT time
    1379090800L
    >>> fc.when_starts('iso')                             # ISO 8601
    '2013-09-13 16:46:40+00'
    
    # ...and when will it end?
    >>> fc.when_ends()                                    # UNIX GMT time
    1379902600L
    >>> fc.when_ends('iso')                               # ISO 8601
    '2013-09-23 02:16:40+00'

In example, you can ask the _Forecaster_ object to tell which is the weather 
forecast for a specific point in time. You can specify this time using UNIXtime,
an ISO8601-formatted string or a Pythone _datetime.datetime_ object (all times 
must are handled as GMT):

    # Tell me the weather for tomorrow at this hour
    >>> from datetime import datetime
    >>> date_tomorrow = datetime(2013, 9, 19, 12, 0)
    >>> str_tomorrow = "2013-09-19 12:00+00"
    >>> unix_tomorrow = 1379592000L
    >>> fc.get_weather_at(date_tomorrow)
    <weather.Weather at 0x00DF75F7>
    >>> fc.get_weather_at(str_tomorrow)
    <weather.Weather at 0x00DF75F7>
    >>> fc.get_weather_at(unix_tomorrow)
    <weather.Weather at 0x00DF75F7>

You will be provided with the _Weather_ sample that lies closest to the time that
you specified. Of course this will work only if the specified time is covered by
the forecast! Otherwise, you will be prompted with an error:

    >>> fc.get_weather_at("1492-10-12 12:00:00+00")
    pyowm.exceptions.not_found_error.NotFoundError: The searched item was not found.
    Reason: Error: the specified time is not included in the weather coverage range

Keep in mind that you can leverage the convenience _timeutils_ module's functions
to quickly build datetime objects:

    >>> from pyowm import timeutils
    >>> timeutils.tomorrow()                              # Tomorrow at this hour
    datetime.datetime(2013, 9, 19, 12, 0)
    >>> timeutils.yesterday(23, 27)                       # Yesterday at 23:27
    datetime.datetime(2013, 9, 19, 12, 0)
    >>> timeutils.next_three_hours()
    datetime.datetime(2013, 9, 18, 15, 0)                 # 3 hours from now
    >>> t = datetime.datetime(2013, 19, 27, 8, 47, 0)
    >>> timeutils.next_three_hours(t)
    datetime.datetime(2013, 19, 27, 11, 47, 0)            # 3 hours from a specific datetime    
    
Other useful convenicence methods in class _Forecaster_ are:

    # Will it rain, be sunny, foggy or snow during the covered period?
    >>> fc.will_have_rain()
    True
    >>> fc.will_have_sun()
    True
    >>> fc.will_have_fog()
    False
    >>> fc.will_have_clouds()
    False
    >>> fc.will_have_snow()
    False
    
    # Will it be rainy, sunny, foggy or snowy at the specified GMT time?
    time = "2013-09-19 12:00+00"
    >>> fc.will_be_rainy_at(time)
    False
    >>> fc.will_be_sunny_at(time)
    True
    >>> fc.will_be_foggy_at(time)
    False
    >>> fc.will_be_cloudy_at(time)
    False
    >>> fc.will_be_snowy_at(time)
    False
    >>> fc.will_be_sunny_at(0L)           # Out of weather forecast coverage
    pyowm.exceptions.not_found_error.NotFoundError: The searched item was not found.
    Reason: Error: the specified time is not included in the weather coverage range
    
    # List the weather elements for which the condition will be: 
    # rain, sun, fog and snow
    >>> fc.when_rain()
    [<weather.Weather at 0x00DB22F7>,<weather.Weather at 0x00DB2317>]
    >>> fc.when_sun()
    [<weather.Weather at 0x00DB62F7>]
    >> fc.when_clouds()
    [<weather.Weather at 0x00DE22F7>]
    >>> fc.when_fog()
    [<weather.Weather at 0x00DC22F7>.]
    >>> fc.when_snow()
    []                                   # It won't snow: empty list

When calling _fc.will_be_*_at_ methods you can specify either a UNIXtime, a 
_datetime.datetime_ object or an ISO8601-formatted string (format: ""). A boolean
value will be returned, telling if the queried weather condition will apply to
the time you specify (the check will be performed on the _Weather_ object of
the forecast which is closest in time to the time value that you provided).

When calling _fc.when_*_  methods you will be provided with a sublist of the 
_Weather_ objects list in _f_ with items having as weather condition the one
the method queries for.

Printing objects' content
-------------------------
For a quick reading of data, the _Location_, _Weather_, _Observation_ and
_Forecast_ objects can be printed on-screen, eg:

    >>> print location
    [Location: name=wonderland lon=12.3 lat=44.7 ID=9876]

Dumping objects' content to JSON and XML
----------------------------------------
_Location_, _Weather_, _Observation_ and _Forecast_ objects can be dumped to 
JSON or XML strings:

    # Dump a Weather object to JSON...
    >>> w.to_JSON()
    {'referenceTime':1377851530,'Location':{'name':'Palermo',
    'coordinates':{'lon':13.35976,'lat':38.115822}'ID':2523920},...}
    
    #... and to XML
    >>> w.to_XML()
    <weather><referenceTime>1377851530</referenceTime>
    <Location><name>Palermo</name><coordinates><lon>13.35976</lon><lat>38.115822</lat>
    </coordinates><ID>2523920</ID></Location>...</weather>
