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
you want current the weather be looked up for and the job is done.
You can specify the location either by passing its toponym (eg: "London") or
its geographic coordinates (lon/lat):

    obs = owm.observation_at_place('London,uk')                     # Toponym
    obs = owm.observation_at_coords(-0.107331,51.503614)            # Lon/lat

A _Observation_ object will be returned, containing weather info about the first
location matching the toponym/coordinates you provided. So be precise when
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
    list_of_obs = owm.find_observations_by_name('London',search='accurate')
    # As above but limit result items to 3
    list_of_obs = owm.find_observations_by_name('London',search='accurate',limit=3)
    
    # Find observed weather for all the places whose name contains the word "London"
    list_of_obs = owm.find_observations_by_name('London',search='like')
    # As above but limit result items to 5
    list_of_obs = owm.find_observations_by_name('London',search='like',limit=5)
    
    # Find observed weather for all the places in the surroundings of lon=-2.15,lat=57
    list_of_obs = owm.find_observations_by_coords({'lon':-2.15,'lat':57})
    # As above but limit result items to 8
    list_of_obs = owm.find_observations_by_coords({'lon':-2.15,'lat':57},limit=8)

Getting data from Observation objects
-------------------------------------

_Observation_ objects encapsulate two useful objects: a _Weather_ object that
contains the weather-related data and a _Location_ object that describes the
location for which the weather data are provided.

If you want to know when the weather observation data have been received, just
issue:

    >>> obs.get_reception_time()                           # UNIX UTC time
	1379091600
    >>> obs.get_reception_time(timeformat='iso')           # ISO 8601
	2013-09-13 17:00:00+00

You can retrieve the _Weather_ object like this:

    >>> w = obs.get_weather()

and then access weather data using the following methods:

    >> w.get_reference_time()                              # get time of observation in UTC UNIXtime
    1377872206
    >>> w.get_reference_time(timeformat='iso')             # ...or in ISO 8601
    2013-08-30 14:16:46+00
    
    >>> w.get_clouds()                                     # Get cloud coverage
    12
    
    >>> w.get_rain()                                       # Get rain volume
    {'3h':0}
    
    >>> w.get_snow()                                       # Get snow volume
    {'3h': 0}
    
    >>> w.get_wind()                                       # Get wind degree and speed
    {'deg': 59, 'speed': 2.660}
    
    >>> w.get_humidity()                                   # Get humidity percentage
    99
    
    >>> w.get_pressure()                                   # Get atmospheric pressure
    {'pressure': 1030.119, 'sea_level: 1038.381}
    
    >>> w.get_temperature()                                # Get temperature in Kelvin degs
    {'temp': 293.4, 'temp_kf': -1.89, 'temp_max': 297.5, 'temp_min': 290.9}
    >>> w.get_temperature(unit='celsius')                  # ... or in Celsius degs
    >>> w.get_temperatire(unit='fahrenheit')               # ... or in Fahrenheit degs

    >>> w.get_status()                                     # Get weather short status
    'Clouds'
    >>> w.get_detailedStatus()                             # Get detailed weather status
    'Broken clouds'

    >>> w.get_weather_code()                               # Get OWM weather condition code
    803
    
    >>> w.get_weather_icon_name()                          # Get weather-related icon name
    '02d'

    >>> e.get_sunrise()                                    # Sunrise time (UTC UNIXtime or ISO 8601)
    1377862896
    >>> e.get_sunset()                                     # Sunset time (UTC UNIXtime or ISO 8601)
    1377893277

Support to weather data interpreting can be found [here](http://bugs.openweathermap.org/projects/api/wiki/Weather_Data#Description-parameters) 
and [here](http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes) you can read about OWM weather condition codes and icons.

If you need a JSON/XML representation of the _Weather_ object you can benefit 
from the following methods:

    >>> w.dump_JSON()                                    # Get a JSON representation
    {'base':'gdpsstations','referenceTime':1377851530,'Location':{'name':'Palermo',
    'coordinates':{'lon':13.35976,'lat':38.115822}'ID':2523920},...}
    
    >>> w.dump_XML()                                     # Same as above, but in XML
    <weather><base>gdpsstations</base><referenceTime>1377851530</referenceTime>
    <Location><name>Palermo</name><coordinates><lon>13.35976</lon><lat>38.115822</lat>
    </coordinates><ID>2523920</ID></Location>...</weather>

As said, _Observation_ objects also contain a _Location_ objects with info about
the weather location:

    >>> l = obs.get_location()
    >>> l.get_name()
    'London'
    >>> l.get_lon()
    -0.107331
    >>> l.get_lat()
    51.503614
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
encapsulate a _Forecast_ object, which has all the information about your weather
forecast. If you need to handle it, just go with:

    >>> f = fc.get_forecast()

A _Forecast_ object encapsulates the _Location_ object relative to the forecast
and a list of _Weather_ objects:

    # When has the forecast been received?
    >>> f.get_reception_time()                           # UNIX UTC time
    1379091600
    >>> f.get_reception_time(timeformat='iso')           # ISO 8601
	2013-09-13 17:00:00+00
    
    # Which time interval for the forecast? 
    >>> f.get_interval()
    daily

	# How many weather items are in the forecast?
	>>> len(f)
	20 

	# Get Location
	>>> f.get_location()
	<location.Location at 0x00DADBF0>
	
Once you obtain a _Forecast_ object, reading the forecast data is easy - you can
get the whole list of _Weather_ objects or you can use the built-in iterator:
	
	# Get the list of Weather objects...
	>>> lst = f.get_weathers()
	
	# ...or iterate directly over the Forecast object
	>>> for weather in f:
	      print (weather.get_reference_time(format='iso'),weather.get_status())
	('2013-09-14 14:00:00+0','Clear')
	('2013-09-14 17:00:00+0','Clear')
	('2013-09-14 20:00:00+0','Clouds')
	[...]

The _Forecaster_ class provides a few convenience methods to inspect the
weather forecasts in a human-friendly fashion. You can - for example - ask for 
the GMT time boundaries of the weather forecast data:

    # When in time does the forecast begin?
    >>> fc.when_starts()                                  # UNIX UTC time
    1379090800
    >>> fc.when_starts(timeformat='iso')                  # ISO 8601
    2013-09-13 16:46:40+00
    
    # ...and when will it end?
    >>> fc.when_ends()                                    # UNIX UTC time
    1379902600
    >>> fc.when_ends(timeformat='iso')                    # ISO 8601
    2013-09-23 02:16:40+00

In example, you can ask the _Forecaster_ object to tell which is the weather 
forecast for a specific point in time that you can specify using UNIXtime, an 
ISO8601 formatted string or a Pythone _datetime.datetime_ object (all times must
be provided GMT):

    # Tell me the weather for tomorrow at noon
    >>> tomorrow_at_noon_obj = datetime.datetime(2013, 9, 19, 12, 0)
    >>> tomorrow_at_noon_str = "2013-09-19 12:00+00"
    >>> tomorrow_at_noon_unixtime = 1379592000L
    >>> fc.weather_at(tomorrow_at_noon_obj)
    <weather.Weather at 0x00DF75F7>
    >>> fc.weather_at(tomorrow_at_noon_str)
    <weather.Weather at 0x00DF75F7>
    >>> fc.weather_at(tomorrow_at_noon_unixtime)
    <weather.Weather at 0x00DF75F7>

You will be provided with the _Weather_ sample that lies closest to the time that
you specified. Of course this will work only if the specified time is covered by
the forecast! Otherwise, you will be prompted with an error:

    >>> fc.weather_at("1492-10-12 12:00+00")
    Error: the specified time is not included in the weather forecast

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
    tomorrow_at_noon = "2013-09-19 12:00+00"
    >>> fc.will_be_rainy_on(tomorrow_at_noon)
    False
    >>> fc.will_be_sunny_on(tomorrow_at_noon)
    True
    >>> fc.will_be_foggy_on(tomorrow_at_noon)
    False
    >>> fc.will_be_cloudy_on(tomorrow_at_noon)
    False
    >>> fc.will_be_snowy_on(tomorrow_at_noon)
    False
    >>> fc.will_be_sunny_on(0L)           # Out of weather forecast coverage span
    Error: the specified time is not included in the weather forecast 
    
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

When calling _fc.will_be_*_on_ methods the _Weather_ item which is closest to the
time you specified will be examined. So be precise if your forecast is 3h!
In addition, you can use these methods with either a UNIXtime, a 
_datetime.datetime_ object or an ISO8601-formatted string. 

When calling _fc.when_*_  methods you will be provided with a sublist of the 
_Weather_ objects list in _f_ with items having as weather condition the one
the method queries for.

Printing objects' content
-------------------------
For a quick reading of data, the _Location_, _Weather_,  _Observation_ and
_Forecast_ objects can be printed on-screen, eg:

    >>> l = Location('wonderland', 12.3, 44.7, 9876)
    >>> print l
    [Location: name=wonderland lon=12.3 lat=44.7 ID=9876]