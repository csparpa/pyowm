# Agro API examples

OWM provides an API for Agricultural monitoring that provides soil data, satellite imagery, etc.

The first thing you need to do to get started with it is to create a *polygon* and store it on the OWM Agro API.
PyOWM will give you this new polygon's ID and you will use it to invoke data queries upon that polygon.

Eg: you can look up satellite imagery, weather data, historical NDVI for that specific polygon.

Read further on to get more details.


## OWM website technical reference
 - [https://agromonitoring.com/api](hhttps://agromonitoring.com/api)


### AgroAPI Manager object

In order to do any kind of operations against the OWM Agro API, you need to obtain a `pyowm.agro10.agro_manager.AgroManager`
instance from the main OWM. You'll need your API Key for that:

```python
import pyowm
owm = pyowm.OWM('your-API-key')
mgr = owm.agro_manager()
```

Read on to discover what you can do with it.


## Polygon API operations

A polygon represents an area on a map upon which you can issue data queries. Each polygon has a unique ID, an optional
name and links back to unique OWM ID of the User that owns that polygon. Each polygon has an area that is expressed 
in hacres, but you can also get it in squared kilometers:

```python
pol                  # this is a pyowm.agro10.polygon.Polygon instance
pol.id               # ID
pol.area             # in hacres
pol.area_km          # in sq kilometers
pol.user_id          # owner ID
```

Each polygon also carries along the `pyowm.utils.geo.Polygon` object that represents the geographic polygon and the
`pyowm.utils.geo.Point` object that represents the baricentre of the polygon:

```python
geopol = pol.geopolygon   # pyowm.utils.geo.Polygon object
point = pol.center        # pyowm.utils.geo.Point object
```

### Reading Polygons
You can either get all of the Polygons you've created on the Agro API or easily get single polygons by specifying
their IDs:

```python
list_of_polygons = mgr.get_polygons()
a_polygon = mgr.get_polygon('5abb9fb82c8897000bde3e87')
```


### Creating Polygons
Creating polygons is easy: you just need to create a `pyowm.utils.geo.Polygon` instance that describes the coordinates
of the polygon you want to create on the Agro API. Then you just need to pass it (along with an optional name) to the
Agro Manager object:

```python

# first create the pyowm.utils.geo.Polygon instance that represents the area (here, a triangle)
from pyowm.utils.geo import Polygon as GeoPolygon
gp = GeoPolygon([[
        [-121.1958, 37.6683],
        [-121.1779, 37.6687],
        [-121.1773, 37.6792],
        [-121.1958, 37.6683]]])

# use the Agro Manager to create your polygon on the Agro API 
the_new_polygon = mgr.create_polygon(gp, 'my new shiny polygon')

# the new polygon has an ID and a user_id
the_new_polygon.id
the_new_polygon.user_id

```

You get back a `pyowm.agro10.polygon.Polygon` instance and you can use its ID to operate this new polygon on all the
other Agro API methods! 

### Updating a Polygon
Once you've created a polygon, you can only change its mnemonic name, as the rest of its parameters cannot
be changed by the user. In order to do it:

```python
my_polygon.name  # "my new shiny polygon"
my_polygon.name = "changed name"
mgr.update_polygon(my_polygon)
```

### Deleting a Polygon
Delete a polygon with

```python
mgr.delete_polygon(my_polygon)
```

Remember that when you delete a polygon, there is no going back!