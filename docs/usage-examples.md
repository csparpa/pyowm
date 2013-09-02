PyOWM usage examples
====================

Import the PyOWM library
------------------------
As simple as:

    >>> from pyowm import OWM, Location

We'll be injecting a __Location__ object into the __OWM__ entry point.

Specify a location
------------------
We need to specify the location we want to query the OWM API about weather status or forecasts: this is done by initializing the _OWM_ entry point with a proper _Location_ object.

A _Location_ object can be created by providing one of the following information:

1. the location's toponym (eg: city name)
2. the location's longitude/latitude couple
3. the unique OWM city ID for the location

For the last type, refer to the [OWM API documentation](http://bugs.openweathermap.org/projects/api/wiki/Api_2_5_weather#3-By-city-ID)

In example, we want to issue queries about Pavia (Northern Italy) city


    # Create Location object
    >>> location = Location('Pavia')                        # Set location with toponym
    >>> location = Location({'lon':9.16145,'lat':45.18446}) # Set location with lon/lat
    >>> location = Location(3171366)                        # Set location with OWM city ID

_Location_ objects can be modified at a glance: when a propery is modified, the others are kept in synchro:

    >>> location.getName()
    Pavia
    >>> location.setName('Milano')              # Change city...
    >>> location.getCoordinates()               # ...and notice lon/lat change accordingly
    { 'lon' : 9.18951, 'lat' : 45.464272 }
    >>> location.setCoordinates({'lon':9.16145,'lat':45.18446})
    >>> location.getID()
    3171366
    >>> location.setID(12345)


Create global OWM object
------------------------
Use a _Location_ object and your OWM API key if you have one (read [here](http://openweathermap.org/appid) on how to obtain an API key). Only the first parameter is mandatory:


    >>> apikey = 'G097IueS-9xN712E'
    >>> owm = OWM(location)
    >>> owm2 = OWM(location, apikey)
    
Of course you can change _Location_ and API Key at a later time:
    
    >>> owm.getLocation()
    <Location.Location instance at 0x017CA490>
    >>> owm.setLocation(Location('Venezia'))
    >>> owm.getAPIkey()
    'G09_7IueS-9xN712E'
    >>> owm.setAPIkey('6Lp$0UY220_HaSB45')

Query for current weather
-------------------------
Querying for current weather using an _OWM_ object is simple:

    >>> w = owm.currentWeather()

and returns a _Weather_ object.

A dictionary can be passed to the `owm.currentWeather()` call, containing one or more of the following configuration parameters:

+ Language of the output - `lang: en|ru|it|sp|ua|de|pt|ro|pl|fi|nl|fr|bg|se|zh_tw|zh_cn|tr`
+ Units of Measure - `units: metric|imperial`

Example:

    >>> w = owm.currentWeather({'lang':'ru','units':'imperial'})

For a reference about configuration parameters and default values refer to the [OWM API documentation](http://bugs.openweathermap.org/projects/api/wiki/Api_2_5_weather#4-Other-parameters).


A _Weather_ object encapsulates all data coming from the enquiry issued to the OWM web API, as well as additional information and the related _Location_ object.


Support to weather data interpreting can be found [here](http://bugs.openweathermap.org/projects/api/wiki/Weather_Data#Description-parameters) and [here](http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes) you can read about OWM weather condition codes and icons.

Access weather data using the following methods:

    >>> w.getClouds()                                      # Get cloud coverage
    { 'all' : 12 }
    
    >>> w.getRain()                                        # Get rain volume
    { '3h' : 0 }
    
    >>> w.getSnow()                                        # Get snow volume
    { '3h' : 0 }
    
    >>> w.getWind()                                        # Get wind degree and speed
    { 'deg' : 59, 'speed' : 2.660 }
    
    >>> w.getHumidity()                                    # Get humidity percentage
    99
    
    >>> w.getPressure()                                    # Get atmospheric pressure
    296.519
    
    # Get temperature
    >>> w.getTemperature()                                 # In Kelvin degrees
    299.15
    >>> w.getTemperature(unit='celsius')                   # In Celsius degrees
    26
    >>> w.getTemperatire(unit='fahrenheit')                # In Fahrenheit degrees
    79
    
    # Get maximum temperature
    >>> w.getMaxTemperature()                              # Similar as above
    >>> w.getMaxTemperature(unit='celsius')
    >>> w.getMaxTemperature(unit='fahrenheit')

    # Get minimum temperature
    >>> w.getMaxTemperature()                              # Similar as above
    >>> w.getMaxTemperature(unit='celsius')
    >>> w.getMaxTemperature(unit='fahrenheit')

    >>> w.getStatus()                                      # Get weather short status
    'Clouds'
    >>> w.getDetailedStatus()                              # Get detailed weather status
    'Broken clouds'

    >>> w.getWeatherCode()                                 # Get OWM weather condition code
    803
    
    >>> w.getIconName()                                    # Get weather-related icon name
    '02d'
    >>> w.getIconURL()                                     # Get weather-related icon URL
    'http://openweathermap.org/img/w/04d.png'



Access the related _Location_ object and weather status reference timestamp using:

    >>> l = w.getLocation()                                # Get Location object
    
    # The last time weather data for this location has been queried
    >> w.getReferenceTime()                                # In UNIX GMT time
    1377872206
    >> w.getReferenceTime(format='iso')                    # In ISO 8601 format
    Fri, Aug 30 16:15:00 GMT

Each _Weather_ object encapsulates also an _Ephemeris_ object which carries information about sun ephemerides:

    >>> e = w.getEphemeris()                               # Get the Ephemeris obj
    
    # Get sunrise time
    >>> e.getSunrise()                                     # In UNIX GMT time
    >>> e.getSunrise(format='iso')                         # In ISO 8601 format
    
    # Get sunset time
    >>> e.getSunset()                                      # In UNIX GMT time
    >>> e.getSunset(format='iso')                          # In ISO 8601 format


A nice feature of _Weather_ objects is that you can update the current weather status with a simple call:

    >>> w.update()

If you need a JSON/XML representation of the _Weather_ object (which is _not_ the OWM API raw  response to the former query for current weather!) you can benefit from the following dump methods:

    >>> w.dumpJSON()                                       # Get a JSON representation
    {'base':'gdpsstations','referenceTime':1377851530,'Location':{'name':'Palermo',
    'coordinates':{'lon':13.35976,'lat':38.115822}'ID':2523920},'Ephemeris':
    {'sunrise':1377837306,'sunset':1377884331},'clouds':{'all':12},'rain':{'3h':0},
    'snow':{'3h':0},'wind':{'speed':2.66,'deg':59},'humidity':99,'pressure':1017,
    'temperature':296.71,'minTemperature':295.93,'maxTemperature':297.15,'status':
    'Clouds','detailedStatus':'fewclouds','weatherCode':801,'iconName':'02d'}
    
    >>> w.dumpXML()                                        # Same as above, but in XML
    <weather><base>gdpsstations</base><referenceTime>1377851530</referenceTime>
    <Location><name>Palermo</name><coordinates><lon>13.35976</lon><lat>38.115822</lat>
    </coordinates><ID>2523920</ID></Location><Ephemeris><sunrise>1377837306</sunrise>
    <sunset>1377884331</sunset></Ephemeris><clouds><all>12</all></clouds><rain><3h>0</3h>
    </rain><snow><3h>0</3h></snow><wind><speed>2.66</speed><deg>59</deg></wind>
    <humidity>99</humidity><pressure>1017</pressure><temperature>296.71</temperature>
    <minTemperature>295.93</minTemperature><maxTemperature>297.15</maxTemperature>
    <status>Clouds</status><detailedStatus>fewclouds</detailedStatus>
    <weatherCode>801</weatherCode><iconName>02d</iconName></weather>

Query for weather forecasts
---------------------------
TBD

Find locations
--------------
TBD
