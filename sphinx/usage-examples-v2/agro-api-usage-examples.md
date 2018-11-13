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
am = owm.agro_manager()
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

### Creating Polygons
TBD



roughly

```python
from pyowm.agro10.agro_manager import AgroManager
agro = AgroManager(API_key)
agro.agro_api_version
polygon = agro.create_polygon(...)
polygons_list = agro.get_polygons()
retrieved_polygon = agro.get_polygon(id)
agro.update_polygon(polygon)
agro.delete_polygon(polygon)
```