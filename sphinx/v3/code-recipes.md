# Code recipes

This section provides code snippets you can use to quickly get started with PyOWM when performing common enquiries
related to weather data.

Table of contents:
  * [Library initialization](#library_init)
  * [Identifying cities and places](#identifying_places)
  * [Weather data](#weather_data)
  * [Geometries](#geometries)

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

## City IDs

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
list_of_tuples = london = reg.ids_for('london')                               # notice the lowercase
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

You can do nice things using geometries: please take a look at the [Geometries](#geometries) docs section

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
wind_dict_in_meters_per_sec = mgr.weather_at_place('Tokyo,JP').wind()   # Default unit: 'meters_sec'
wind_dict_in_meters_per_sec['speed']
wind_dict_in_meters_per_sec['deg']
wind_dict_in_meters_per_sec['gust']
wind_dict_in_miles_per_h = mgr.weather_at_place('Tokyo,JP').wind(unit='miles_hour')
wind_dict_in_knots = mgr.weather_at_place('Tokyo,JP').wind(unit='knots')
wind_dict_in_beaufort = mgr.weather_at_place('Tokyo,JP').wind(unit='beaufort')  # Beaufort is 0-12 scale


### Get current rain amount on a location
Also rain amount is a dict, with keys: `1h` an `3h`, containing the mms of rain fallen in the last 1 and 3 hours

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
rain_dict = mgr.weather_at_place('Berlin,DE').rain
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
pressure_dict = mgr.weather_at_place('Berlin,DE').pressure
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
weather = mgr.weather_at_place('Berlin,DE')
sunrise_unix = weather.sunrise_time()  # default unit: 'unix'
sunrise_iso = weather.sunrise_time(timeformat='iso')
sunrise_date = weather.sunrise_time(timeformat='date')
sunrset_unix = weather.sunset_time()  # default unit: 'unix'
sunrset_iso = weather.sunset_time(timeformat='iso')
sunrset_date = weather.sunset_time(timeformat='date')
```


<div id="geometries"/>
TBD