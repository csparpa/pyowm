## Carbon Monoxide (CO) Index

You can query the OWM API for Carbon Monoxide (CO) measurements in the surroundings of specific geocoordinates.

Please refer to the official API docs for [CO](http://openweathermap.org/api/pollution/v1/co) data consumption for details about how the search radius is influenced by the decimal digits on the provided lat/lon values.

Queries return the latest CO Index values available since the specified
`start` date and across the specified `interval` timespan. If you don't
specify any value for `interval` this is defaulted to: `'year'`.
Eg:

  - `start='2016-07-01 15:00:00Z'` and `interval='hour'`: searches from 3 to 4 PM of day 2016-07-01
  - `start='2016-07-01'` and `interval='day'`: searches on the day 2016-07-01
  - `start='2016-07-01'` and `interval='month'`: searches on the month of July 2016
  - `start='2016-07-01'` and `interval='year'`: searches from day 2016-07-01 up to the end of year 2016

Please be aware that also data forecasts can be returned, depending on the search query.


### Querying CO index

Getting the data is easy:
```
from pyowm import OWM
from pyowm.utils import timestamps

owm = OWM('apikey')

# get an air pollution manager object
mgr = owm.airpollution_manager()

# Get latest CO Index on geocoordinates
coi = mgr.coindex_around_coords(lat, lon)

# Get available CO Index in the last 24 hours
coi = mgr.coindex_around_coords(lat, lon,
    start=timestamps.yesterday(), interval='day')

# Get available CO Index in the last ...
coi = mgr.coindex_around_coords(
    lat, lon,
    start=start_datetime,  # iso-8601, unix or datetime
    interval=span)         # can be: 'minute', 'hour', 'day', 'month', 'year'
```


### `COIndex` entity
`COIndex` is an entity representing a set of CO measurements on a certain geopoint.
Each CO measurement is taken at a certain air pressure value and has a VMR (Volume Mixing Ratio) value
for CO. Here are some of the methods:

```
list_of_samples = coi.get_co_samples()
location = coi.get_location()
coi.get_reference_time()
coi.get_reception_time()

max_sample = coi.get_co_sample_with_highest_vmr()
min_sample = coi.get_co_sample_with_lowest_vmr()
```

If you want to know if a COIndex refers to the future - aka: is a forecast - with respect to the
current timestamp, then use the `is_forecast()` method


## Ozone (O3)

You can query the OWM API for Ozone measurements in the surroundings of specific geocoordinates.

Please refer to the official API docs for [O3](http://openweathermap.org/api/pollution/v1/o3) data consumption for details about how the search radius is influenced by the decimal digits on the provided lat/lon values.

Queries return the latest Ozone values available since the specified
`start` date and across the specified `interval` timespan. If you don't
specify any value for `interval` this is defaulted to: `'year'`.
Eg:

  - `start='2016-07-01 15:00:00Z'` and `interval='hour'`: searches from 3 to 4 PM of day 2016-07-01
  - `start='2016-07-01'` and `interval='day'`: searches on the day 2016-07-01
  - `start='2016-07-01'` and `interval='month'`: searches on the month of July 2016
  - `start='2016-07-01'` and `interval='year'`: searches from day 2016-07-01 up to the end of year 2016

Please be aware that also data forecasts can be returned, depending on the search query.

### Querying Ozone data

Getting the data is easy:
```
from pyowm import OWM
from pyowm.utils import timestamps

owm = OWM('apikey')

# get an air pollution manager object
mgr = owm.airpollution_manager()

# Get latest O3 value on geocoordinates
o3 = mgr.ozone_around_coords(lat, lon)

# Get available O3 value in the last 24 hours
oz = mgr.ozone_around_coords(lat, lon,
         start=timestamps.yesterday(), interval='day')

# Get available O3 value in the last ...
oz = mgr.ozone_around_coords(
       lat, lon,
        start=start_datetime,  # iso-8601, unix or datetime
        interval=span)         # can be: 'minute', 'hour', 'day', 'month', 'year'
```

### `Ozone` entity
`Ozone` is an entity representing a set of CO measurements on a certain geopoint.
Each ozone value is expressed in [Dobson Units](http://www.theozonehole.com/dobsonunit.htm).
Here are some of the methods:

```
location = oz.get_location()
oz = get_du_value()
oz.get_reference_time()
oz.get_reception_time()
```

If you want to know if an Ozone measurement refers to the future - aka: is a forecast - with respect to the
current timestamp, then use the `is_forecast()` method


### Querying Nitrogen dioxide (NO2) and Sulfur Dioxide (SO2) data
This works exactly as for O2 data - please refer to that bit of the docs