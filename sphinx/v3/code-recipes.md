# Code recipes

This section provides code snippets you can use to quickly get started with PyOWM when performing common enquiries
related to weather data.

Table of contents:
  * [Library initialization](#library_init)
  * [Identifying cities and places via city IDs](#identifying_places)
  * [OneCall data](#onecall)
  * [Weather data](#weather_data)
  * [Air pollution data](#airpollution_data)  
  * [Weather forecasts](#weather_forecasts)
  * [Meteostation historic measurements](#station_measurements)


<div id="library_init"/>

**Very important news**
OpenWeatherMap API recently "blocked" calls towards a few legacy API endpoints whenever requested by **clients using non-recent free API keys.**

This means that if you use PyOWM methods such as the ones for getting observed or forecasted weather, PyOWM might return authorization errors
This behaviour is not showing if you use API keys issued a long time ago. 

The *proper way to obtain such data is to call the "OneCall" methods using your API key*





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
The OWM API can be asked to return localized *detailed statuses* for weather data
**In PyOWM this means that you can specify a language and you'll retrieve `Weather` objects having the `detailed_status`
field localized in that language. Localization is not provided for `status` field instead, so pay attention to that.**

The list of supported languages is given by:
```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
owm.supported_languages
```
Check out [https://openweathermap.org/current](https://openweathermap.org/current) for reference on supported languages

English is the default language on the OWM API - but you can change it:

```python
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'fr'  # your language here, eg. French
owm = OWM('your-api-key', config_dict)
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Paris, FR')
observation.weather.detailed_status  # Nuageux
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

## Identifying cities and places

You can easily get the City ID of a known toponym, as well as its geographic coordinates
Also you can leverage direct/reverse geocoding 

### City IDs

The following calls will not result in any OWM API call in the background, so they will only happen locally to your machine.

#### Obtain the city ID registry
As easy as:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
reg = owm.city_id_registry()
```

#### Get the ID of a city given its name
Once you've got it, use the city ID registry to lookup the ID of a city given its name:

```python
list_of_tuples = london = reg.ids_for('London', matching='like')
print(list_of_tuples)     # This will give something like: 
                          # [ (2643743, 'London', 'GB', None, 51.50853, -0.12574),  
                          #   (1006984, 'East London', 'ZA', None, -33.015289, 27.911619),
                          #   (1644003, 'Glondong', 'ID', None, -6.7924, 111.891602), 
                          #   ... ]
```

**This call searches for all the places that contain the string `'London'` in their names, in any part of the world**. 
This is because the search matching criterion we've used is `like` (this is the default one, if you don't specify it)

The other available matching criterion is `exact`, which retrieves all places having exactly `'London'` as their name,
in any part of the world (be careful that this operation is case-sensitive !)

Let's try to search for the same city with an exact match:

```python
list_of_tuples = london = reg.ids_for('London', matching='exact')
print(list_of_tuples)     # This will give something like: 
                          # [ (2643743, 'London', 'GB', None, 51.50853, -0.12574),  
                          #   (4119617, 'London', 'US', 'AR', 35.328972, -93.25296),
                          #   (4298960, 'London', 'US', 'KY', 37.128979, -84.08326)
                          #   ... ]
```

As you can see, all results are exactly named `'London'`. 

All the above searches give you back a list of tuples: each tuple is in the format `(city_id, name, country, state, lat, lon)` (fields as
self-explanatory).


### City disambiguation
As you might have guessed, there is a high probability that your city is not unique in the world, and multiple cities with the same name exist in other countries
Therefore: whenever you search for a specific city in a specific country then also pass in the 2-letter country name and - even further - also specify a 2-letter state name if you're searching for places in the United States.

Eg: if you search for the British `London` you'll get multiple results. You then should also specify the country (`GB`) in order to narrow the search only to Great Britain.

Let's search for it:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
reg = owm.city_id_registry()
list_of_tuples = reg.ids_for('London', matching='exact')                 # lots of results, spread all over the world
list_of_tuples = reg.ids_for('London', country='GB', matching='exact')   # only one: [(2643743, 'London', 'GB', None, 51.50853, -0.12574)]
london_gb = list_of_tuples[0]
id_of_lonfon_gb = london_gb[0]                                           # ID of London, GB
```

Whenever searching cities in the US, you'd better also specify the relevant US-state.
For instance, `'Ontario'` is a city in Canada and multiple aliases exist in different US-states:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
reg = owm.city_id_registry()

# All Ontario cities in the uS
ontarios_in_us = reg.ids_for('Ontario', country='US', matching='exact')  # five results

# Ontario in Canade
ontario_in_canada = reg.ids_for('Ontario', country='CA', matching='exact')  # one result: [(6093943, 'Ontario', 'CA', None, 49.250141, -84.499832)]

# Ontario in the state of New York
ontario_in_ny = reg.ids_for('Ontario', country='US', state='NY', matching='exact')  # one result: [(5129887, 'Ontario', 'US', 'NY', 43.220901, -77.283043)]
```

#### Get geographic coordinates of a city given its name
Just use call `locations_for` on the registry: this will give you a `Location` object containing lat & lon

Let's find geocoords for Tokyo (Japan):

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
reg = owm.city_id_registry()
list_of_locations = reg.locations_for('Tokyo', country='JP', matching='exact')
tokyo = list_of_locations[0]
lat = tokyo.lat   # 35.689499
lon = tokyo.lon   # 139.691711
```

#### Get GeoJSON geometry (point) for a city given its name
PyOWM encapsulates [GeoJSON](https://pypi.org/project/geojson/) geometry objects that are compliant with the GeoJSON specification.

This means, for example, that you can get a `Point` geometry using the registry. Let's find the geometries for all `Rome` cities in the world:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
reg = owm.city_id_registry()
list_of_geopoints = reg.geopoints_for('Rome', matching='exact')
```

### Direct/reverse geocoding

Simply put:
  - DIRECT GEOCODING: from toponym to geocoords
  - REVERSE GEOCODING: from geocoords to toponyms


Both geocoding actions are performed via a `geocoding_manager` object and will require an actual call to be made to the
OWM API: so please bear that in mind because that will count against your amount of allowed API calls

#### Direct geocoding of a toponym

The call is very similar to `ids_for` and `locations_for`.

You at least need to specify the toponym name and country ISO code (eg. `GB`, `IT`, `JP`, ...), while if the input 
toponym is in the United States you should also specify the `state_code` parameter 

The call returns a list of `Location` object instances (in case of no ambiguity, only one item in the list will be returned)
You can then get the lat/lon from the object instances themselves

Results can be limited with the `limit` parameter

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.geocoding_manager()

# geocode London (no country specified) - we'll get many results
list_of_locations = mgr.geocode('London')
a_london = list_of_locations[0]  # taking the first London in the list
a_london.lat
a_london.lon 

# geocode London (Great Britain) - we'll get up to three Londons that exist in GB
list_of_locations = mgr.geocode('London', country='GB', limit=3)

# geocode London (Ohio, United States of America): we'll get all the Londons in Ohio
list_of_locations = mgr.geocode('London', country='US', state_code='OH')
```

#### Reverse geocoding of geocoordinates
With reverse geocoding you input a lat/lon float couple and retrieve a list all the `Location` objects associated with 
these coordinates.

Results can be limited with the `limit` parameter

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.geocoding_manager()

# London
lat = 51.5098
lon = -0.1180

# reverse geocode London
list_of_locations = mgr.reverse_geocode(lat, lon)  # list contains: City of London, Islington, Lewisham, ...
```


<div id="onecall"/>

## OneCall data

With the OneCall Api you can get the current weather, hourly forecast for the next 48 hours and the daily forecast for the next seven days in one call.

One Call objects can be thought of as datasets that "photograph" observed and forecasted weather for a location: such photos are given for a specific timestamp.

It is possible to get:
  - current OneCall data: the "photo" given for today)
  - historical OneCall data: "photos" given for past days, up to 5 

### Current OneCall data

#### What is the feels like temperature (°C) tomorrow morning?
Always in Berlin:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=52.5244, lon=13.4105)

one_call.forecast_daily[0].temperature('celsius').get('feels_like_morn', None) #Ex.: 7.7
```

#### What's the wind speed in three hours?

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

#### What's the current humidity?

Always in Berlin:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=52.5244, lon=13.4105)

one_call.current.humidity # Eg.: 81
```

#### Requesting only part of the available OneCall data, in imperial units


```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=52.5244, lon=13.4105, exclude='minutely,hourly', units='imperial')

# in this exacmple, the data in the one_call object will be in imperial units
# possible units are defined by the One Call API, here: https://openweathermap.org/api/one-call-api
# as of 2020.08.07 available values are: 'metric' or 'imperial'
# the various units for the different options are shown here: https://openweathermap.org/weather-data
one_call.current.temperature() # Eg.: 74.07 (deg F)

# the example above does not retrieve minutely or hourly data, so it will not be available in the one_call object
# available exclude options are defined by the One Call API
# BUT using 'current' will error, as the pyowm one_call requires it
# as of 2020.08.07 available values are: 'minutely', 'hourly', 'daily'
# multiple exclusions may be combined with a comma, as above
one_call.forecast_hourly # empty because it was excluded from the request
```

#### Checking available National Weather Alerts for a location
Many countries have early warning systems in place to notify about upcoming severe weather events/conditions.
Each alert has a title, a description, start/end timestamps and is tagged with labels.
You can check if any national alert has been issued for a specific location this way:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=52.5244, lon=13.4105)
national_weather_alerts = one_call. national_weather_alerts

for alert in national_weather_alerts:
    alert.sender                      # issuing national authority
    alert.title                       # brief description
    alert.description                 # long description
    alert.start_time()                # start time in UNIX epoch
    alert.end_time(timeformat='ISO')  # end time in ISO format
```


### Historical OneCall data

Remember the "photograph" metaphor for OneCall data. You can query for "photos" given for past days: when you do that,
be aware that such a photo carries along weather forecasts (hourly and daily) that *might* refer to the past

This is because - as said above - the One Call API returns hourly forecasts for a streak of 48 hours and daily forecast 
for a streak of 7 days, both streaks beginning from the timestamp which the OneCall object refers to

In case of doubt, anyway, you can always _check the reference timestamp_ for the `Weather` objects embedded into the
OneCall object and check if it's in the past or not.


#### What was the observed weather yesterday at this time?

Always in Berlin: 

```python
from pyowm.owm import OWM
from pyowm.utils import timestamps, formatting

owm = OWM('your-api-key')
mgr = owm.weather_manager()

# what is the epoch for yesterday at this time?
yesterday_epoch = formatting.to_UNIXtime(timestamps.yesterday())

one_call_yesterday = mgr.one_call_history(lat=52.5244, lon=13.4105, dt=yesterday_epoch)

observed_weather = one_call_yesterday.current
```

#### What was the weather forecasted 3 days ago for the subsequent 48 hours ?

No way we move from Berlin:

```python
from pyowm.owm import OWM
from pyowm.utils import timestamps
from datetime import datetime, timedelta, timezone

owm = OWM('your-api-key')
mgr = owm.weather_manager()

# what is the epoch for 3 days ago at this time?
three_days_ago_epoch = int((datetime.now() - timedelta(days=3)).replace(tzinfo=timezone.utc).timestamp())

one_call_three_days_ago = mgr.one_call_history(lat=52.5244, lon=13.4105, dt=three_days_ago_epoch)

list_of_forecasted_weathers = one_call_three_days_ago.forecast_hourly
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
rain_dict = mgr.weather_at_place('Berlin,DE').weather.rain
rain_dict['1h']
rain_dict['3h']
```

### Get current pressure on a location
Pressure is similar to rain, you get a dict with hPa values and these keys: `press` (atmospheric pressure on the 
ground, sea level if [no sea level or ground level data](https://openweathermap.org/weather-data)) `sea_level` 
(on the sea level, if location is on the sea) and `grnd_level`. Note that `press` used below refers to the
dict value in 

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
pressure_dict = mgr.weather_at_place('Berlin,DE').weather.barometric_pressure()
pressure_dict['press']
pressure_dict['sea_level']
pressure_dict['grnd_level']
```

Pressure values are given in the metric hPa, or hectopascals (1 hPa is equivalent to 100 pascals). You can easily 
convert these values to inches of mercury, or inHg, which is a unit commonly used in the United States. Similar to above,
we can do:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
obs = mgr.weather_at_place('Berlin,DE')

# the default unit is hPa
pressure_dict_unspecified = obs.weather.barometric_pressure()
pressure_dict_in_hg = obs.weather.barometric_pressure(unit='inHg')
```

### Get current visibility distance on a location
You might want to know how clearly you can see objects in Berlin. This is the visibility distance, an average distance
taken from an Observation object and given in meters. You can also convert this value to kilometers or miles.

```python
from pyowm.owm import OWM

owm = OWM('your-api-key')
mgr = owm.weather_manager()
obs = mgr.weather_at_place('Berlin,DE')

# the default value provided by our call (in meters)
visibility = obs.weather.visibility_distance

# kilometers is the default conversion unit
visibility_in_kms = obs.weather.visibility()
visibility_in_miles = obs.weather.visibility(unit='miles')
```

### Get today's sunrise and sunset times for a location
You can get precise timestamps for sunrise and sunset times on a location.
Sunrise can be `None` for locations in polar night, as well as sunset can be `None` in case of polar days
Supported time units are: `unix` (default, UNIX time), `iso` (format `YYYY-MM-DD HH:MM:SS+00:00`) or `datetime` 
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
weather_at_moscow = mgr.weather_at_coords(moscow_lat, moscow_lon).weather 
```

### Get weather at city IDs

You can enquire the observed weather on a city ID:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
my_city_id = 2643743 #London
weather = mgr.weather_at_id(my_city_id).weather 
```

or on a list of city IDs:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
my_list_of_city_ids = [2643743 , 4517009, 5056033]
list_of_observations = mgr.weather_at_ids(my_list_of_city_ids)
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

**>>>IMPORTANT NOTE<<<**: OpenWeatherMap has deprecated legacy weather forecasts endpoints, therefore you could get
errors if you invoke them
The recommended way to get weather forecasts is now the [*OneCall* API]((#onecall))


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
three_h_forecast = mgr.forecast_at_place('Berlin,DE', '3h').forecast
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
forecaster.when_starts('iso')                            # 2020-03-10 14:00:00+00:00'
forecaster.when_ends('iso')                              # 2020-03-16 14:00:00+00:00'
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
three_h_forecaster = mgr.forecast_at_place('Berlin,DE', '3h')
tomorrow_at_five = timestamps.tomorrow(17, 0)                      # datetime object for tomorrow at 5 PM
weather = three_h_forecaster.get_weather_at(tomorrow_at_five)           # the weather you're looking for
```

You are provided with the `Weather` object that lies closest to the time that you specified (5 PM)

### Is it going to rain tomorrow?

Say you want to know if you need to carry an umbrella around in Berlin tomorrow.

```python
from pyowm.utils import timestamps
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
three_h_forecaster = mgr.forecast_at_place('Berlin,DE', '3h')

# Is it going to rain tomorrow?
tomorrow = timestamps.tomorrow()                   # datetime object for tomorrow
three_h_forecaster.will_be_rainy_at(tomorrow)           # True
```

### Will it snow or be foggy in the next days?

In Berlin:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
three_h_forecaster = mgr.forecast_at_place('Berlin,DE', '3h')

# Is it going to be snowy in the next 5 days ?
three_h_forecaster.will_have_snow()    # False

# Is it going to be foggy in the next 5 days ?
three_h_forecaster.will_have_fog()    # True
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


<div id="airpollution_data"/>

## Air pollution data

Instead of getting a `weather_manager`, get from the main OWM object a `airpollution_manager` and use it

### Getting air pollution concentrations and Air Quality Index on geographic coords 
Air polluting agents concentration can be queried in one shot:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.airpollution_manager()

air_status = mgr.air_quality_at_coords(51.507351, -0.127758)  # London, GB

# you can then get values for all of these air pollutants
air_status.co
air_status.no
air_status.no2
air_status.o3
air_status.so2
air_status.pm2_5
air_status.pm10
air_status.nh3

# and for air quality index
air_status.aqi 
```

### Getting forecasts for air pollution on geographic coords 
We can get also get forecasts for air pollution agents concentration and air quality index:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.airpollution_manager()

list_of_forecasts = mgr.air_quality_forecast_at_coords(51.507351, -0.127758)  # London, GB

# Each item in the list_of_forecasts is an AirStatus object 
for air_status in list_of_forecasts:
    air_status.co
    air_status.no
    air_status.no2
    air_status.o3
    air_status.so2
    air_status.pm2_5
    air_status.pm10
    air_status.nh3
    air_status.aqi  # air quality index
```

### Getting historical air pollution data on geographic coords 
We can get also get historical values for air pollution agents concentration and air quality index:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.airpollution_manager()

# fetch history from a certain point in time up to now...
start = 1606223802  # November 24, 2020
list_of_historical_values = mgr.air_quality_history_at_coords(51.507351, -0.127758, start)  # London, GB

# ...or fetch history on a closed timeframe in the past
end = 1613864065  # February 20, 2021
list_of_historical_values = mgr.air_quality_history_at_coords(51.507351, -0.127758, start, end=end)  # London, GB

# Each item in the list_of_historical_values is an AirStatus object 
for air_status in list_of_historical_values:
    air_status.co
    air_status.no
    air_status.no2
    air_status.o3
    air_status.so2
    air_status.pm2_5
    air_status.pm10
    air_status.nh3
    air_status.aqi  # air quality index
```



<div id="station_measurements"/>

## Meteostation historic measurements

_This is a legacy feature of the OWM Weather API_

Weather data measurements history for a specific meteostation is available in three sampling intervals:
 
 - ``'tick'`` (which stands for minutely)
 - ``'hour'``
 - ``'day'``

The amount of datapoints returned can be limited. Queries can be made as follows: 

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()

station_id = 39276

# Get tick historic data for a meteostation
historian = mgr.station_tick_history(station_id, limit=4)  # only 4 data items

# Get hourly historic data for the same station, no limits
historian = mgr.station_hour_history(station_id)

# Get hourly historic data for the same station, no limits
historian = mgr.station_day_history(station_id)
```

All of the above mentioned calls return a `Historian` object.
Each measurement is composed by:
   - a UNIX epoch timestamp
   - a temperature sample
   - a humidity sample
   - a pressure sample
   - a rain volume sample
   - wind speed sample

Use the convenience methods provided by `Historiam` to get time series for temperature, wind, etc..
These convenience methods are especially useful if you need to chart the historic time series of the measured physical entities:

```python

# Get the temperature time series (in different units of measure)
historian.temperature_series()                     # defaults to Kelvin, eg.  [(1381327200, 293.4), (1381327260, 293.6), ...]
historian.temperature_series(unit="celsius")       # now in Celsius
historian.temperature_series("fahrenheit")         # you get the gig  

# Get the humidity time series
historian.humidity_series()


# Get the pressure time series
historian.pressure_series()

# Get the rain volume time series
historian.rain_series()

# Get the wind speed time series
historian.wind_series()
```

Each of the above methods returns a list of tuples, each tuple being a couple in the form: `(UNIX epoch, measured value)`.
Be aware that whenever measured values are missing `None` placeholders are put.

You can also get minimum, maximum and average values of each series:

```python
# Get the minimum temperature value in the series
historian.min_temperature(unit="celsius")  # eg. (1381327200, 20.25)

# Get the maximum rain value in the series
historian.max_rain()  # eg. (1381327200, 20.25)

# Get the average wind value in the series
historian.average_wind()  # eg. 4.816
```

### Get raw meteostation measurements data

Make the proper call based on the sampling interval of interest and obtain the resulting `Historian` object:

```python
raw_measurements_dict = historian.station_history.measurements  # dict of raw measurement dicts, indexed by time of sampling:
```

The `raw_measurements_dict` contains multiple sub-dicts, each one being a a data item. Example:
```
{
  1362933983: {
    "temperature": 266.25,
    "humidity": 27.3,
    "pressure": 1010.02,
    "rain": None,
    "wind": 4.7
  }
  # [...]
}
``` 
