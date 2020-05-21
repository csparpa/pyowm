# Code recipes

This section provides code snippets you can use to quickly get started with PyOWM when performing common enquiries
related to weather data.

Table of contents:
  * [Library initialization](#library_init)
  * [Identifying cities and places via city IDs](#identifying_places)
  * [Weather data](#weather_data)
  * [Weather forecasts](#weather_forecasts)
  * [OneCall data](#onecall)

<div id="library_init"/>

## Library initialization

### Initialize PyOWM with default configuration and a free API key
```python
from pyowm.owm import OWM
owm = OWM('your-free-api-key')
```

### Initialize PyOWM with configuration loaded from an external JSON file
You can setup a configuration file and then have PyOWM read it. The file must contain a valid JSON document with the
following format:

```
{
    "subscription_type": free|startup|developer|professional|enterprise
    "language": en|ru|ar|zh_cn|ja|es|it|fr|de|pt|... (check https://openweathermap.org/current) 
    "connection": {
        "use_ssl": true|false,
        "verify_ssl_certs": true|false,
        "use_proxy": true|false,
        "timeout_secs": N
    },
    "proxies": {
        "http": HTTP_URL,
        "https": SOCKS5_URL
    }
}
```

```python
from pyowm.owm import OWM
from pyowm.utils.config import get_config_from
config_dict = get_config_from('/path/to/configfile.json')
owm = OWM('your-free-api-key', config_dict)
```

### Initialize PyOWM with a paid subscription - eg: professional
If you bought a paid subscription then you need to provide PyOWM both your paid API key and the subscription type that you've bought

```python
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config_for_subscription_type
config_dict = get_default_config_for_subscription_type('professional')
owm = OWM('your-paid-api-key', config_dict)
```

### Use PyOWM behind a proxy server
If you have an HTTP or SOCKS5 proxy server you need to provide PyOWM two URLs; one for each HTTP and HTTPS protocols.
URLs are in the form: 'protocol://username:password@proxy_hostname:proxy_port'

```python
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config_for_proxy
config_dict = get_default_config_for_proxy(
    'http://user:pass@192.168.1.77:8464',
    'https://user:pass@192.168.1.77:8934'
)
owm = OWM('your-api-key', config_dict)
```

### Language setting
English is the default - but you can change it
Check out [https://openweathermap.org/current](https://openweathermap.org/current) for the complete list of supported languages

```python
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'pt'  # your language here
owm = OWM('your-api-key', config_dict)
```

### Get PyOWM configuration
Configuration can be changed: just get it, it's a plain Python dict
```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
config_dict = owm.configuration
```

### Get the version of PyOWM library
```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
version_tuple = (major, minor, patch) = owm.version
```

<div id="identifying_places"/>

## Identifying cities and places via city IDs

### Obtain the city ID registry
Use the city ID registry to lookup the ID of a city given its name
```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
city_id_registry = owm.city_id_registry()
```

### Get the ID of a city given its name
Don't forget that there is a high probabilty that your city is not unique in the world, and multiple cities with the same name exist in other countries
Therefore specify toponyms and country 2-letter names separated by comma. Eg: if you search for the British `London` you'll likely multiple results: 
you then should also specify the country (`GB`) to narrow the search only to Great Britain.

Let's search for it:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
reg = owm.city_id_registry()
list_of_tuples = london = reg.ids_for('London')                               # lots of results
list_of_tuples = london = reg.ids_for('London', country='GB')                 # only one: [ (2643743,, 'London, GB') ]
id_of_london_city = list_of_tuples[0][0]
```

The search here was by default case insensitive: you could have tried

```python
list_of_tuples = london = reg.ids_for('london', country='GB')                 # notice the lowercase
list_of_tuples = london = reg.ids_for('LoNdoN', country='GB')                 # notice the camelcase
```
and would get the very same results as above.


### Get the IDs of cities whose name cointain a specific string

In order yo find all cities with names having your string as a substring you need to use the optional parameter `matching='like'`

In example, let's find IDs for all British cities having the string `london` in their names:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
reg = owm.city_id_registry()
list_of_tuples = reg.ids_for('london', country='GB', matching='like')  # We'll get [(2643741, 'City of London', 'GB'), 
                                                                       #            (2648110, 'Greater London', 'GB'), 
                                                                       #            (7535661, 'London Borough of Harrow', 'GB'),
                                                                       #            (2643743, 'London', 'GB'),
                                                                       #            (2643734, 'Londonderry County Borough', 'GB')]
```

### Get geographic coordinates of a city given its name
Just use call `locations_for` on the registry: this will give you a `Location` object containing lat & lon

Let's find geocoords for Moscow (Russia):

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
reg = owm.city_id_registry()
list_of_locations = reg.locations_for('moscow', country='RU')
moscow = list_of_locations[0][0]
lat = moscow.lat   # 55.75222
lon = moscow.lon   # 37.615555
```

### Get GeoJSON geometry (point) for a city given its name
PyOWM encapsulates [GeoJSON](https://pypi.org/project/geojson/) geometry objects that are compliant with the GeoJSON specification.

This means, for example, that you can get a `Point` geometry using the registry. Let's find the geometries for all `Rome` cities in the world:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
reg = owm.city_id_registry()
list_of_geopoints = reg.geopoints_for('rome')
```

<div id="weather_data"/>

## Observed weather

### Obtain a Weather API manager object
The manager object is used to query weather data, including observations, forecasts, etc
```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
weather_mgr = owm.weather_manager()
```

### Get current weather status on a location
Queries work best by specifying toponyms and country 2-letter names separated by comma. Eg: instead of using
`seattle` try using `seattle,WA`

Say now we want the currently observed weather in London (Great Britain):

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
observation = mgr.weather_at_place('London,GB')  # the observation object is a box containing a weather object
weather = observation.weather
weather.status           # short version of status (eg. 'Rain')
weather.detailed_status  # detailed version of status (eg. 'light rain')
```

The weather object holds all weather-related info

### Get current and today's min-max temperatures in a location
Temperature can be retrieved in Kelvin, Celsius and Fahrenheit units

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
weather = mgr.weather_at_place('Tokyo,JP').weather
temp_dict_kelvin = weather.temperature()   # a dict in Kelvin units (default when no temperature units provided)
temp_dict_kelvin['temp_min']
temp_dict_kelvin['temp_max']
temp_dict_fahrenheit = weather.temperature('fahrenheit')  # a dict in Fahrenheit units
temp_dict_celsius = weather.temperature('celsius')  # guess?
```

### Get current wind info on a location
Wind is a dict,with the following information: wind speed, degree  (meteorological) and gusts.
Available measurement units for speed and gusts are: meters/sec (default), miles/hour, knots and Beaufort scale.

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Tokyo,JP')
wind_dict_in_meters_per_sec = observation.weather.wind()   # Default unit: 'meters_sec'
wind_dict_in_meters_per_sec['speed']
wind_dict_in_meters_per_sec['deg']
wind_dict_in_meters_per_sec['gust']
wind_dict_in_miles_per_h = mgr.weather_at_place('Tokyo,JP').wind(unit='miles_hour')
wind_dict_in_knots = mgr.weather_at_place('Tokyo,JP').wind(unit='knots')
wind_dict_in_beaufort = mgr.weather_at_place('Tokyo,JP').wind(unit='beaufort')  # Beaufort is 0-12 scale
```

### Get current rain amount on a location
Also rain amount is a dict, with keys: `1h` an `3h`, containing the mms of rain fallen in the last 1 and 3 hours

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
rain_dict = mgr.weather_at_place('Berlin,DE').observation.rain
rain_dict['1h']
rain_dict['3h']
```

### Get current pressure on a location
Pressure is similar to rain: you get a dict with keys: `press` (atmospheric pressure on the ground in hPa) and `sea_level` 
(on the sea level, if location is on the sea)

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
pressure_dict = mgr.weather_at_place('Berlin,DE').observation.pressure
pressure_dict['press']
pressure_dict['sea_level']
```

### Get today's sunrise and sunset times for a location
You can get precise timestamps for sunrise and sunset times on a location.
Sunrise can be `None` for locations in polar night, as well as sunset can be `None` in case of polar days
Supported time units are: `unix` (default, UNIX time), `iso` (format `YYYY-MM-DD HH:MM:SS+00`) or `datetime` 
(gives a plain Python `datetime.datetime` object)

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Berlin,DE')
weather = observation.weather
sunrise_unix = weather.sunrise_time()  # default unit: 'unix'
sunrise_iso = weather.sunrise_time(timeformat='iso')
sunrise_date = weather.sunrise_time(timeformat='date')
sunrset_unix = weather.sunset_time()  # default unit: 'unix'
sunrset_iso = weather.sunset_time(timeformat='iso')
sunrset_date = weather.sunset_time(timeformat='date')
```


### Get weather on geographic coordinates
```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
my_city_id = 12345
moscow_lat = 55.75222
moscow_lon = 37.615555
weather_at_moscow = owm.weather_at_coords(moscow_lat, moscow_lon).weather 
```

### Get weather at city IDs

You can enquire the observed weather on a city ID:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
my_city_id = 12345
weather = owm.weather_at_id(my_city_id).weather 
```

or on a list of city IDs:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
my_list_of_city_ids = [12345, 67890, 54321]
list_of_observations = owm.weather_at_ids(my_list_of_city_ids)
corresponding_weathers_list = [ obs.weather for obs in list_of_observations ]
```

### Current weather search based on string similarity

In one shot, you can query for currently observed weather:

 * for all the places whose name equals the string you provide (use ``'accurate'``)
 * for all the places whose name contains the string you provide (use ``'like'``)


You can control how many items the returned list will contain by using the ``limit`` parameter

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
obs_list = mgr.weather_at_places('London', 'accurate')        # Find observed weather in all the "London"s in the world
obs_list = mgr.weather_at_places('London', 'like', limit=5)   # Find observed weather for all the places whose name contains 
                                                              # the word "London". Limit the results to 5 only
```

### Current weather radial search (circle) 

In one shot, you can query for currently observed weather for all the cities whose lon/lat coordinates lie inside a circle
whose center is the geocoords you provide. You can control how many cities you want to find by using the ``limit`` parameter.

The radius of the search circle is automatically determined to include the number of cities that you want to obtain (default is: 10)


```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
obs_list = mgr.weather_around_coords(57, -2.15, limit=8)  # Find observed weather for all the places in the 
                                                          # surroundings of lat=57,lon=-2.15, limit results to 8 only
```

### Current weather search in bounding box
In one shot, you can query for currently observed weather for all the cities whose lon/lat coordinates lie inside the
specified rectangle (bounding box)

A bounding box is determined by specifying:
  * the north latitude boundary (`lat_top`)
  * the south latitude boundary (`lat_bottom`)
  * the west longitude boundary (`lon_left`)
  * the east longitude boundary (`lon_right`)

Also, an integer `zoom` level needs to be specified (defaults to 10): this works along with . The lower the zoom level,
the "higher in the sky" OWM looks for cities inside the bounding box (think of it as the inverse of elevation)

The `clustering` parameter is off by default. With `clustering=True` you ask for server-side clustering of cities: this 
will result in fewer results when the bounding box shows high city density 


```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()

# This bounding box roughly encloses Cairo city (Egypt)
lat_top = 30.223475116500158
lat_bottom = 29.888280933159265
lon_left = 31.0034179688
lon_right = 31.5087890625

# This which should give you around 5 results
obs_list = mgr.weather_at_places_in_bbox(lon_left, lat_bottom, lon_right, lat_top, zoom=10)  

# This only gives 1
obs_list = mgr.weather_at_places_in_bbox(lon_left, lat_bottom, lon_right, lat_top, zoom=5)  
```



<div id="weather_forecasts"/>

## Weather forecasts

### Get forecast on a location
Just like for observed weather info, you can fetch weather forecast info on a specific toponym.
As usual, provide toponym + country code for better results.

Forecast are provided for the next 5 days.

A `Forecast` object contains a list of `Weather` objects, each one having a specific reference time in the future.
The time interval among `Weather` objects can be 1 day (`daily` forecast) or 3 hours ('3h' forecast).

Let's fetch forecast on Berlin (Germany):

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
daily_forecast = mgr.forecast_at_place('Berlin,DE', 'daily').forecast
3h_forecast = mgr.forecast_at_place('Berlin,DE', '3h').forecast
```
Now that you got the `Forecast` object, you can either manipulate it directly or use PyOWM conveniences to quickly slice and dice the embedded `Weather` objects

Let's take a look at the first option (see further on for the second one): a `Forecast` object is iterable on the weathers

```python
nr_of_weathers = len(daily_forecast)
for weather in daily_forecast:
    weather.get_reference_time('iso'), weather.get_status()  # ('2020-03-10 14:00:00+0','Clear')
                                                             # ('2020-03-11 14:00:00+0','Clouds')
                                                             # ('2020-03-12 14:00:00+0','Clouds')
                                                             # ...
```

Something useful is forecast actualization, as you might want to remove from the `Forecast` all the embedded `Weather` objects that refer to a time in the past with respect to now.
This is useful especially if store the fetched forecast for subsequent computations.

```python
# Say now is: 2020-03-10 18:30:00+0
daily_forecast.actualize()
for weather in daily_forecast:
    weather.get_reference_time('iso'), weather.get_status()  # ('2020-03-11 14:00:00+0','Clouds')
                                                             # ('2020-03-12 14:00:00+0','Clouds')
                                                             # ...
```

### Know when a forecast weather streak starts and ends
Say we get the 3h forecast on Berlin. You want to know when the forecasted weather streak starts and ends

Use the `Forecaster` convenience class as follows.

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
forecaster = mgr.forecast_at_place('Berlin,DE', '3h')    # this gives you a Forecaster object
forecaster.when_starts('iso')                            # 2020-03-10 14:00:00+00'
forecaster.when_ends('iso')                              # 2020-03-16 14:00:00+00'
```

### Get forecasted weather for tomorrow
Say you want to know the weather on Berlin, say, globally for tomorrow.
Easily done with the `Forecaster` convenience class and PyOWM's `timestamps` utilities:

```python
from pyowm.utils import timestamps
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
daily_forecaster = mgr.forecast_at_place('Berlin,DE', 'daily')
tomorrow = timestamps.tomorrow()                                   # datetime object for tomorrow
weather = daily_forecaster.get_weather_at(tomorrow)                # the weather you're looking for
```

Then say you want to know weather for tomorrow on Berlin at 5 PM:

```python
from pyowm.utils import timestamps
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
3h_forecaster = mgr.forecast_at_place('Berlin,DE', '3h')
tomorrow_at_five = timestamps.tomorrow(17, 0)                      # datetime object for tomorrow at 5 PM
weather = 3h_forecaster.get_weather_at(tomorrow_at_five)           # the weather you're looking for
```

You are provided with the `Weather` object that lies closest to the time that you specified (5 PM)

### Is it going to rain tomorrow?

Say you want to know if you need to carry an umbrella around in Berlin tomorrow.

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
3h_forecaster = mgr.forecast_at_place('Berlin,DE', '3h')

# Is it going to rain tomorrow?
tomorrow = timestamps.tomorrow()                   # datetime object for tomorrow
3h_forecaster.will_be_rainy_at(tomorrow)           # True
```

### Will it snow or be foggy in the next days?

In Berlin:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
3h_forecaster = mgr.forecast_at_place('Berlin,DE', '3h')

# Is it going to be snowy in the next 5 days ?
3h_forecaster.will_have_snow()    # False

# Is it going to be foggy in the next 5 days ?
3h_forecaster.will_have_fog()    # True
```

### When will the weather be sunny in the next five days?

Always in Berlin:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
daily_forecaster = mgr.forecast_at_place('Berlin,DE', 'daily')

list_of_weathers = daily_forecaster.when_clear()
```

This will give you the list of `Weather` objects in the 5 days forecast when it will be sunny. So if only 2 in the next 5 days will be sunny, you'll get 2 objects
The list will be empty if none of the upcoming days will be sunny.

### Which of the next 5 days will be the coldest? And which one the most rainy ?

Always in Berlin:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
daily_forecaster = mgr.forecast_at_place('Berlin,DE', 'daily')

daily_forecaster.most_cold()     # this weather is of the coldest day
daily_forecaster.most_rainy()    # this weather is of the most rainy day
```

### Get forecast on geographic coordinates
TBD

### Get forecast on city ID
TBD

### Get forecast on geographic coordinates
TBD

<div id="onecall"/>

## OneCall data

With the OneCall Api you can get the current weather, hourly forecast for the next 48 hours and the daily forecast for the next seven days in one call.

Below some examples:

### What is the feels like temperature (°C) tomorrow morning?
Always in Berlin:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=52.5244, lon=13.4105)

one_call.forecast_daily[0].temperature('celsius').get('feels_like_morn', None) #Ex.: 7.7
```

### What's the wind speed in three hours?

__Attention: The first entry in forecast_hourly is the current hour.__
If you send the request at 18:36 UTC then the first entry in forecast_hourly is from 18:00 UTC.

Always in Berlin:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=52.5244, lon=13.4105)

one_call.forecast_hourly[3].wind().get('speed', 0) # Eg.: 4.42
```

### What's the current humidity?

Always in Berlin:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=52.5244, lon=13.4105)

one_call.current.humidity # Eg.: 81
```
