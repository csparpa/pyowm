# Tiles client

OWM provides tiles for a few map layers displaying world-wide features such as global temperature, pressure, wind speed,
and precipitation amount.

Each tile is a PNG image that is referenced by a triplet: the (x, y) coordinates and a zoom level

The zoom level might depend on the type of layers: 0 means no zoom (full globe covered), while usually you can get up
to a zoom level of 18.

Available map layers are specified by the `pyowm.tiles.enums.MapLayerEnum` values.


## OWM website technical reference
 - [http://openweathermap.org/api/weathermaps](http://openweathermap.org/api/weathermaps)


## Usage examples

Tiles can be fetched this way:

```python
from pyowm import OWM
from pyowm.tiles.enums import MapLayerEnum

owm = OWM('my-API-key')

# Choose the map layer you want tiles for (eg. temeperature
layer_name = MapLayerEnum.TEMPERATURE

# Obtain an instance to a tile manager object
tm = owm.tile_manager(layer_name)

# Now say you want tile at coordinate x=5 y=2 at a zoom level of 6
tile = tm.get_tile(5, 2, 6)

# You can now save the tile to disk
tile.persist('/path/to/file.png')

# Wait! but now I need the pressure layer tile at the very same coordinates and zoom level! No worries...
# Just change the map layer name on the TileManager and off you go!
tm.map_layer = MapLayerEnum.PRESSURE
tile = tm.get_tile(5, 2, 6)
```


## Tile object

A `pyowm.commons.tile.Tile` object is a wrapper for the tile coordinates and the image data, which is a
`pyowm.commons.image.Image` object instance.

You can save a tile to disk by specifying a target file:

```python
tile.persist('/path/to/file.png')
```

## Use cases

### I have the lon/lat of a point and I want to get the tile that contains that point at a given zoom level

Turn the lon/lat couple to a `pyowm.utils.geo.Point` object and pass it

```python
from pyowm.utils.geo import Point
from pyowm.commons.tile import Tile

geopoint = Point(lon, lat)
x_tile, y_tile = Tile.tile_coords_for_point(geopoint, zoom_level):
```

### I have a tile and I want to know its bounding box in lon/lat coordinates

Easy! You'll get back a `pyowm.utils.geo.Polygon` object, from which you can extract lon/lat coordinates this way

```python
polygon = tile.bounding_polygon()
geopoints = polygon.points
geocoordinates = [(p.lon, p.lat) for p in geopoints]  # this gives you tuples with lon/lat
```
