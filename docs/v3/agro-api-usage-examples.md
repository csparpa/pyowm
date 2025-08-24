# Agro API examples

OWM provides an API for Agricultural monitoring that provides soil data, satellite imagery, etc.

The first thing you need to do to get started with it is to create a *polygon* and store it on the OWM Agro API.
PyOWM will give you this new polygon's ID and you will use it to invoke data queries upon that polygon.

Eg: you can look up satellite imagery, weather data, historical NDVI for that specific polygon.

Read further on to get more details.


## OWM website technical reference
 - [https://agromonitoring.com/api](hhttps://agromonitoring.com/api)


## AgroAPI Manager object

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
in acres, but you can also get it in squared kilometers:

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


## Soil data API Operations

Once you've defined a polygon, you can easily get soil data upon it. Just go with:

```python
soil = mgr.soil_data(polygon)
```

`Soil` is an entity of type `pyowm.agro10.soil.Soil` and is basically a wrapper around a Python dict reporting
the basic soil information on that polygon:
```python
soil.polygon_id                         # str           
soil.reference_time(timeformat='unix')  # can be: int for UTC Unix time ('unix'), 
                                        # ISO8601-formatted str for 'iso' or 
                                        # datetime.datetime for 'date'
soil.surface_temp(unit='kelvin')        # float (unit can be: 'kelvin', 'celsius' or 'fahrenheit')
soil.ten_cm_temp(unit='kelvin')         # float (Kelvins, measured at 10 cm depth) - unit same as for above
soil.moisture                           # float (m^3/m^3)
```

Soil data is updated twice a day.


## Satellite Imagery API Operations

This is the real meat in Agro API: the possibility to obtain **satellite imagery** right upon your polygons!

### Overview

Satellite Imagery comes in 3 formats:
  - **PNG images**
  - **PNG tiles** (variable zoom level)
  - **GeoTIFF images**

Tiles can be retrieved by specifying a proper set of tile coordinates (x, y) and a zoom level: please refer to PyOWM's 
Map Tiles client documentation for further insights.

When we say that imagery is upon a polygon we mean that the polygon is fully contained in the scene that was acquired by
the satellite.

Each image comes with a **preset**: a preset tells how the acquired scene has been post-processed, eg: image has been
put in false colors or image contains values of the Enhanced Vegetation Index (EVI) calculated on the scene

Imagery is provided by the Agro API for different **satellites** 

Images that you retrieve from the Agro API are `pyowm.agroapi10.imagery.SatelliteImage` instances, and they **contain both
image's data and metadata**.

You can download NDVI images using several **color palettes** provided by the Agro API, for easier processing on your side.


### Operations summary

Once you've defined a polygon, you can:
  - **search for available images** upon the polygon and taken in a specific time frame. The search can be performed with 
     multiple filters (including: satellite symbol, image type, image preset, min/max resolution, minx/max cloud coverage, ...)
     and returns search results, each one being *metadata* for a specific image.
  - from those metadata, **download an image**, be it a regular scene or a tile, optionally specifying a color palette for NDVI ones
  - if your image has EVI or NDVI presets, you can **query for its statistics**: these include min/max/median/p25/p75 values
    for the corresponding index
    
**A concrete example**: we want to acquire all NDVI GeoTIFF images acquired by Landsat 8 from July 18, 2017 to October 26, 2017;
then we want to get stats for one such image and to save it to a local file.


```python
from pyowm.commons.enums import ImageTypeEnum
from pyowm.agroapi10.enums import SatelliteEnum, PresetEnum

pol_id = '5abb9fb82c8897000bde3e87'  # your polygon's ID
acq_from = 1500336000                # 18 July 2017
acq_to = 1508976000                  # 26 October 2017
img_type = ImageTypeEnum.GEOTIFF     # the image format type
preset = PresetEnum.NDVI    # the preset
sat = SatelliteEnum.LANDSAT_8.symbol # the satellite


# the search returns images metadata (in the form of `MetaImage` objects)
results = mgr.search_satellite_imagery(pol_id, acq_from, acq_to, img_type=img_type, preset=preset, None, None, acquired_by=sat)

# download all of the images
satellite_images = [mgr.download_satellite_image(result) for result in results]

# get stats for the first image
sat_img = satellite_images[0]
stats_dict = mgr.stats_for_satellite_image(sat_img)

# ...satellite images can be saved to disk
sat_img.persist('/path/to/my/folder/sat_img.tif')
```

Let's see in detail all of the imagery-based operations.


### Searching images

Search available imagery upon your polygon by specifying at least a mandatory time window, with from and to timestamps
expressed as UNIX UTC timestamps:

```python

pol_id = '5abb9fb82c8897000bde3e87'  # your polygon's ID
acq_from = 1500336000                # 18 July 2017
acq_to = 1508976000                  # 26 October 2017

# the most basic search ever: search all available images upon the polygon in the specified time frame 
metaimages_list = mgr.search_satellite_imagery(pol_id, acq_from, acq_to)

```

What you will get back is actually metadata for the actual imagery, not data.

The function call will return **a list of `pyowm.agroapi10.imagery.MetaImage` instances, each
one being a bunch of metadata relating to one single satellite image**.

Keep these objects, as you will need them in order to download the corresponding satellite images from the Agro API:
think of them such as descriptors for the real images.

But let's get back to search! Search is a parametric affair... **you can specify many more filters**:
  
  - the image format type (eg. PNG, GEOTIFF)
  - the image preset (eg. false color, EVI)
  - the satellite that acquired the image (you need to specify its symbol)
  - the px/m resolution range for the image (you can specify a minimum value, a maximum value or both of them)
  - the % of cloud coverage on the acquired scene (you can specify a minimum value, a maximum value or both of them)
  - the % of valid data coverage on the acquired scene (you can specify a minimum value, a maximum value or both of them)

Sky is the limit...

As regards image type, image preset and satellite filters please refer to subsequent sections explaining the supported
values.

Examples of search:

```python
from pyowm.commons.enums import ImageTypeEnum
from pyowm.agroapi10.enums import SatelliteEnum, PresetEnum 


# search all Landsat 8 images in the specified time frame
results = mgr.search_satellite_imagery(pol_id, acq_from, acq_to, acquired_by=SatelliteEnum.LANDSAT_8.symbol)

# search all GeoTIFF images in the specified time frame                                     
results = mgr.search_satellite_imagery(pol_id, acq_from, acq_to, img_type=ImageTypeEnum.GEOTIFF)

# search all NDVI images acquired by Sentinel 2 in the specified time frame
results = mgr.search_satellite_imagery(pol_id, acq_from, acq_to, acquired_by=SatelliteEnum.SENTINEL_2.symbol,
                                       preset=PresetEnum.NDVI)

# search all PNG images in the specified time frame with a max cloud coverage of 1% and a min valid data coverage of 98%
results = mgr.search_satellite_imagery(pol_id, acq_from, acq_to, img_type=ImageTypeEnum.PNG, 
                                       max_cloud_coverage=1, min_valid_data_coverage=98)

# search all true color PNG images in the specified time frame, acquired by Sentinel 2, with a range of metric resolution
# from 4 to 16 px/m, and with at least 90% of valid data coverage
results = mgr.search_satellite_imagery(pol_id, acq_from, acq_to, img_type=ImageTypeEnum.PNG, preset=PresetEnum.TRUE_COLOR,
                                       min_resolution=4, max_resolution=16, min_valid_data_coverage=90)
```

So, what metadata can be extracted by a `MetaImage` object? Here we go:

```python
metaimage.polygon_id                 # the ID of the polygon upon which the image is taken
metaimage.url                        # the URL the actual satellite image can be fetched from
metaimage.preset                     # the satellite image preset
metaimage.image_type                 # the satellite image format type
metaimage.satellite_name             # the name of the satellite that acquired the image
metaimage.acquisition_time('unix')   # the timestamp when the image was taken (can be specified using: 'iso', 'unix' and 'date')        
metaimage.valid_data_percentage      # the percentage of valid data coverage on the image
metaimage.cloud_coverage_percentage  # the percentage of cloud coverage on the image
metaimage.sun_azimuth                # the sun azimuth angle at scene acquisition time
metaimage.sun_elevation              # the sun zenith angle at scene acquisition time
metaimage.stats_url                  # if the image is EVI or NDVI, this is the URL where index statistics can be retrieved (see further on for details)
```


### Download an image

Once you've got your metaimages ready, you can download the actual satellite images.

In order to download, you must specify to the Agro API manager object at least the desired metaimage to fetch. If you're
downloading a tile, you must specify tile coordinates (x, y, and zoom level): these are mandatory, and if you forget
to provide them you'll get an `AssertionError`.

Optionally, you can specify a color palette - but this will be significant only if you're downloading an image with NDVI 
preset (otherwise the palette parameter will be safely ignored) - please see further on for reference.

Once download is complete, you'll get back a `pyowm.agroapi10.imagery.SatelliteImage` object (more on this in a while).

Here are some examples:

```python
from pyowm.agroapi10.enums import PaletteEnum

# Download a NDVI image
ndvi_metaimage   # metaimage for a NDVI image
bnw_sat_image = mgr.download_satellite_image(ndvi_metaimage, preset=PaletteEnum.BLACK_AND_WHITE)
green_sat_image =  mgr.download_satellite_image(ndvi_metaimage, preset=PaletteEnum.GREEN)

# Download a tile
tile_metaimage   # metaimage for a tile
tile_image = mgr.download_satellite_image(tile_metaimage, x=2, y=3, zoom=5)
tile_image = mgr.download_satellite_image(tile_metaimage)   # AssertionError (x, y and zoom are missing!)
```

Downloaded satellite images contain both binary image data and and embed *the original `MetaImage` object describing
image metadata*. Furthermore, you can query for the download time of a satellite image, and for its related color palette:

```python

# Get satellite image download time - you can as usual specify: 'iso', 'date' and 'unix' time formats
bnw_sat_image.downloaded_on('iso')  #  '2017-07-18 14:08:23+00:00'

# Get its palette
bnw_sat_image.palette               #  '2'

# Get satellite image's data and metadata
bnw_sat_image.data                  # this returns a `pyowm.commons.image.Image` object or a
                                    # `pyowm.commons.tile.Tile` object depending on the satellite image
metaimage = bnw_sat_image.metadata  # this gives a `MetaImage` subtype object

# Use the Metaimage object as usual...
metaimage.polygon_id
metaimage.preset,
metaimage.satellite_name
metaimage.acquisition_time
```

You can also save satellite images to disk - it's as easy as:

```python
bnw_sat_image.persist('C:\myfolder\myfile.png')
```

### Querying for NDVI and EVI image stats

NDVI and EVI preset images have an extra blessing: you can query for statistics about the image index.

Once you've downloaded such satellite images, you can query for stats and get back a data dictionary for each of them:

```python
ndvi_metaimage   # metaimage for a NDVI image

# download it
bnw_sat_image = mgr.download_satellite_image(ndvi_metaimage, preset=PaletteEnum.BLACK_AND_WHITE)

# query for stats
stats_dict = mgr.stats_for_satellite_image(bnw_sat_image)
```

Stats dictionaries contain:
  - `std`: the standard deviation of the index
  - `p25`: the first quartile value of the index
  - `num`: the number of pixels in the current polygon
  - `min`: the minimum value of the index
  - `max`: the maximum value of the index
  - `median`: the median value of the index
  - `p75`: the third quartile value of the index
  - `mean`: the average value of the index

*What if you try to get stats for a non-NDVI or non-EVI image*? A `ValueError` will be raised!


### Supported satellites

Supported satellites are provided by the `pyowm.agroapi10.enums.SatelliteEnum` enumerator which returns
`pyowm.commons.databoxes.Satellite` objects:

```python
from pyowm.agroapi10.enums import SatelliteEnum

sat = SatelliteEnum.SENTINEL_2
sat.name   # 'Sentinel-2'
sat.symbol # 's2'
```

Currently only Landsat 8 and Sentinel 2 satellite imagery is available


### Supported presets
Supported presets are provided by the `pyowm.agroapi10.enums.PresetEnum` enumerator which returns strings, each
one representing an image preset:
 
 ```python
from pyowm.agroapi10.enums import PresetEnum

PresetEnum.TRUE_COLOR  # 'truecolor'
```

Currently these are the supported presets: true color, false color, NDVI and EVI


### Supported image types
Supported image types are provided by the `pyowm.commons.databoxes.ImageTypeEnum` enumerator which returns
`pyowm.commons.databoxes.ImageType` objects:
 
 ```python
from pyowm.agroapi10.enums import ImageTypeEnum

png_type = ImageTypeEnum.PNG
geotiff_type = ImageTypeEnum.GEOTIFF
png_type.name       # 'PNG'
png_type.mime_type  # 'image/png'
```

Currently only PNG and GEOTIFF imagery is available


### Supported color palettes
Supported color palettes are provided by the `pyowm.agroapi10.enums.PaletteEnum` enumerator which returns strings,
each one representing a color palette for NDVI images:

 ```python
from pyowm.agroapi10.enums import PaletteEnum

PaletteEnum.CONTRAST_SHIFTED  # '3'
```

As said, palettes only apply to NDVI images: if you try to specify palettes when downloading images with different
presets (eg. false color images), *nothing will happen*.

The default Agro API color palette is `PaletteEnum.GREEN` (which is `1`): if you don't specify any palette at all when 
downloading NDVI images, they will anyway be returned with this palette.

As of today green, black and white and two contrast palettes (one continuous and one continuous but shifted) are
supported by the Agro API. Please check the documentation for palettes' details, including control points.
