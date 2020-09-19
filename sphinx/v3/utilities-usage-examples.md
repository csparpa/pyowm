# PyOWM utility functions usage example

PyOWM provides a few packages that contain utility functions. 

Some of them are specifically designed to be used by the core PyOWM classes but others you can use to make your life
easier when operating PyOWM!

All utility modules live inside the `pyowm.utils` package

Here are most useful modules:

  * `config`: handling of PyOWM configuration
  * `formatting`: formatting of timestamp entities (Python native types, UNIX epochs and ISO-8601 strings)
  * `geo`: handling of geographic entities such as points, polygons and their geoJSON representation
  * `measureables`: conversions among physical units (eg. temperature, wind)
  * `timestamps`: human friendly timestamps generation
  
  
## `config` module
```python
from pyowm.utils.config import get_default_config, get_default_config_for_subscription_type, \ 
    get_default_config_for_proxy, get_config_from 

config_dict = get_default_config()                                       # loads the default config dict
config_dict = get_default_config_for_subscription_type('professional')   # loads the config dict for the specified subscription type
config_dict = get_config_from('/path/to/configfile.json')                # loads the config dict from the  specified JSON file
config_dict = get_default_config_for_proxy('http_url', 'https_url')      # loads the config dict to be used behind a proxy whose URLs are specified
```

## `formatting` module
```python
from datetime import datetime as dt
from pyowm.utils import formatting

unix_value = formatting.timeformat(dt.today(), 'unix')        # from datetime to UNIX
iso_str_value = formatting.timeformat(dt.today(), 'iso')      # from datetime to ISO-8601 string
datetime_value = formatting.timeformat(1590100263, 'date')    # from UNIX to datetime
iso_str_value = formatting.timeformat(1590100263, 'iso')      # from UNIX to ISO-8601 string
datetime_value = formatting.timeformat('2020-05-21 22:31:03+00:00', 'date') # from ISO-8601 string to datetime
unix_value = formatting.timeformat('2020-05-21 22:31:03+00:00', 'unix') # from ISO-8601 string to UNIX
```

## `geo` module

The module provides classes to represent geometry features:
  - `Point`
  - `Multipoint` (aka point set)
  - `Polygon`
  - `Multipolygon` (aka polygon set)

Geometry features are used eg. in OWM Alert API to provide geographical boundaries for alert setting.

PyOWM uses standard geometry types defined by the [GeoJSON Format Specification - RFC 7946](https://tools.ietf.org/html/rfc7946) data interchange format.  

### Common geometry methods

All geometry types can be dumped to a GeoJSON string and to a Python `dict`

```python
from pyowm.utils import geo
point = geo.Point(20.8, 30.9)
point.geojson()  # '{"type": "Point", "coordinates": [20.8, 30.9]}'
point.to_dict()  #  {'type': 'Point', 'coordinates': [20.8, 30.9]}
```

All geometry types also feature a static factory method: you provide the dictionary and the factory returns the object
instance

```python
from pyowm.utils.geo import Point
point_dict = {'type': 'Point', 'coordinates': [20.8, 30.9]}
point = Point.from_dict(point_dict)
```

Please refer to the GeoJSON specification about how to properly format the dictionaries to be given the factory methods 


### `Point` class

A point is a couple of geographic coordinates: longitude and latitude

```python
from pyowm.utils import geo
lon = 20.8
lat = 30.9
point = geo.Point(lon, lat)
coords = point.lon, point.lat  # 20.8, 30.9 
```

As circle shapes are not part of the GeoJSON specification, you can approximate the circle having a specific `Point` instance
at its center with a square polygon: we call it bounding square polygon. You just need to provide the radius of the
circle you want to approximate (in kms):

```python
from pyowm.utils import geo
point = geo.Point(20.8, 30.9)
polygon = point.bounding_square_polygon(inscribed_circle_radius_km=2.0)   # default radius: 10 km
```

Please, notice that if you specify big values for the radius you need to take care about the projection of geographic
coordinates on a proper geoid: this means that if you don't, the polygon will only _approximate_ a square.


### From City IDs to `Point` objects

The City ID Registry class can return the geopoints that correspond to one or more named cities:

```python
import pyowm
owm = pyowm.OWM('your-API-key')
reg = owm.city_id_registry()
list_of_geopoints = reg.geopoints_for('London', country='GB')
```

This, in combination with the `bounding_square_polygon` method, makes it possible to easily get polygons to cover large 
squared areas centered on largely spread city areas - such as London,GB itself: 

```python
london_city_centre = geopoints[0]
london_city_bounding_polygon = london_city_centre.bounding_square_polygon(inscribed_circle_radius_km=12)
```

### `MultiPoint` class

A `MultiPoint` object represent a set of `Point` objects

```python
from pyowm.utils.geo import Point, MultiPoint
point_1 = Point(20.8, 30.9)
point_2 = Point(1.2, 0.4)

# many ways to instantiate
multipoint = MultiPoint.from_points([point_1, point_2])
multipoint = MultiPoint([20.8, 30.9], [1.2, 0.4])

multipoint.longitudes  # [20.8, 1.2]
multipoint.latitudes   # [30.9, 0.4]
```


### `Polygon` class

A `Polygon` object represents a shape made by a set of geopoints, connected by lines. Polygons are allowed to have "holes".
Each line of a polygon must be closed upon itself: this means that the last geopoint defined for the line _must_ coincide 
with its first one.

```python
from pyowm.utils.geo import Polygon, Point
point_1_coords = [2.3, 57.32]
point_2_coords = [23.19, -20.2]
point_3_coords = [-120.4, 19.15]
point_1 = Point(point_1_coords)
point_2 = Point(point_2_coords)
point_3 = Point(point_3_coords)


# many ways to instantiate
line = [point_1_coords, point_2_coords, point_3_coords , point_1_coords]  # last point equals the first point
polygon = Polygon([line])
line = [point_1, point_2, point_3, point_1]  # last point equals the first point
polygon = Polygon.from_points([line])
```

### `MultiPolygon` class

A `MultiPolygon` object represent a set of `Polygon` objects
Same philosophy here as for `MultiPoint` class, polygons can cross:

```python
from pyowm.utils.geo import Point, Polygon, MultiPolygon
point_1 = Point(20.8, 30.9)
point_2 = Point(1.2, 0.4)
point_3 = Point(49.9, 17.4)
point_4 = Point(178.4, 78.3)
polygon_1 = Polygon.from_points([point_1, point_2, point_3, point_1])
polygon_2 = Polygon.from_points([point_3, point_4, point_2, point_3])

multipoint = MultiPolygon.from_polygons([polygon_1, polygon_2])
```

### Building geometries

There is a useful factory method for geometry types, which you can use to turn a geoJSON-formatted dictionary into the
corresponding topology type:

```python
from pyowm.utils.geo import GeometryBuilder
point_dict = {
    "type": "Point",
    "coordinates": [53, 37]
}
point = GeometryBuilder.build(point_dict)      # this is a `Point` instance

wrongly_formatted_dict = {"a": 1, "b": 99}
GeometryBuilder.build(wrongly_formatted_dict)  # you get an exception
```


## `measurables` module
This module provides utilities numeric conversions

### Temperature
You have a `dict` whose values represent temperature units in Kelvin: you can convert them to Fahrenheit and Celsius.

```python
from pyowm.utils import measurables

fahrenheit_temperature_dict = measurables.kelvin_dict_to(kelvin_temperature_dict, 'fahrenheit')
celsius_temperature_dict = measurables.kelvin_dict_to(kelvin_temperature_dict, 'celsius')
```

### Wind
On the same line as temperatures, you can convert wind values among meters/sec, kilometers/hour, miles/hour, knots and
the Beaufort scale. The pivot unit of measure for wind is meters/sec


```python
from pyowm.utils import measurables

kmhour_wind_dict = measurables.metric_wind_dict_to_km_h(msec_wind_dict)
mileshour_wind_dict = measurables.metric_wind_dict_to_imperial(msec_wind_dict)
knots_wind_dict = measurables.metric_wind_dict_to_knots(msec_wind_dict)
beaufort_wind_dict = measurables.metric_wind_dict_to_beaufort(msec_wind_dict)
```

### Pressure
OWM gives barometric pressure in hPa values, in a 
[dict of three pressure items](https://openweathermap.org/weather-data). You can convert these to inHg, which is a 
common unit of measurement in the United States.

```python
from pyowm.utils import measurables

hpa_pressure_dict = {'press': 1000, 'sea_level': 1000, 'grnd_level': 1000}
inhg_pressure_dict = measurables.metric_pressure_dict_to_inhg(hpa_pressure_dict)
```

### Visibility
A typical API response contains a single visibility distance value. This is described as the average visibility in
meters. You can convert this value (from meters) using the function provided to either kms or miles.

```python
from pyowm.utils import measurables

visibility = 1000

# the default return value is in kilometers
visibility_kms = measurables.visibility_distance_to(visibility)
visibility_miles = measurables.visibility_distance_to(visibility, 'miles')
```

## `timestamps` module

All `datetime.datetime` objects returned by PyOWM are UTC offset-aware

```python
from pyowm.utils import timestamps

timestamps.now()                                         # Current time in `datetime.datetime` object (default)
timestamps.now('unix')                                   # epoch
timestamps.now('iso')                                    # ISO8601-formatted str (YYYY-MM-DD HH:MM:SS+00:00)

timestamps.tomorrow()                                    # Tomorrow at this time
timestamps.tomorrow(18, 7)                               # Tomorrow at 6:07 PM
timestamps.yesterday(11, 27)                             # Yesterday at 11:27 AM

timestamps.next_three_hours()                            # 3 hours from now
timestamps.last_three_hours(date=timestamps.tomorrow())  # tomorrow but 3 hours before this time

timestamps.next_hour()
timestamps.last_hour(date=timestamps.yesterday())        # yesterday but 1 hour before this time


# And so on with: next_week/last_week/next_month/last_month/next_year/last_year
```
