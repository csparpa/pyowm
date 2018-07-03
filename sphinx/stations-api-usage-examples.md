# Stations API 3.0 usage examples


## Meteostations

Managing meteostations is easy!

Just get a reference to the `stationsapi30..stations_manager.StationsManager` 
object that proxies the OWM Stations API, and then work on it

You can issue CRUD (Create Read Update Delete) actions on the `StationsManager`
and data is passed in/out in the form of `stationsapi30.stations.Station` objects

Here are some examples:

```python
import pyowm
owm = pyowm.OWM('your-API-key')
mgr = owm.stations_manager()        # Obtain the Stations API client

# Create a new station
station = mgr.create_station("SF_TEST001", "San Francisco Test Station",
                                 37.76, -122.43, 150)
# Get all your stations
all_stations = mgr.get_stations()

# Get a station named by id
id = '583436dd9643a9000196b8d6'
retrieved_station = mgr.get_station(id)

# Modify a station by editing its "local" proxy object
retrieved_station.name = 'A different name'
mgr.modify_station(retrieved_station)

# Delete a station and all its related measurements
mgr.delete_station(retrieved_station)

```

## Measurements

Each meteostation tracks datapoints, each one represented by an object.
Datapoints that you submit to the OWM Stations API (also called "raw
measurements") are of type: `stationsapi30.measurement.Measurement`, while 
datapoints that you query against the API come in the form of:
 `stationsapi30.measurement.AggregatedMeasurement` objects.


Each `stationsapi30.measurement.Measurement` cointains a reference to the
`Station` it belongs to:

```python
measurement.station_id
```
  
Create such objects with the class constructor or using the
`stationsapi30.measurement.Measurement.from_dict()` utility method.


Once you have a raw measurement or a list of raw measurements (even belonging
to mixed stations), you can submit them to the OWM Stations API via 
the `StationsManager` proxy:


```python

# Send a new raw measurement for a station
mgr.send_measurement(raw_measurement_obj)

# Send a list of new raw measurements, belonging to multiple stations
mgr.send_measurements(list_of_raw_measurement_objs)
```

Reading measurements from the OWM Stations API can be easily done using the
`StationsManager` as well. As sad, they come in the form of 
`stationsapi30.measurement.AggregatedMeasurement` instances. Each of such
objects represents an *aggregation of measurements* for the station that you
specified, with an aggregation time granularity of *day*, *hour* or *minute* -
you tell what. You can query aggregated measurements in any time window.

So when querying for measurements, you need to specify:
  - the reference station ID
  - the aggregation granularity (as sai, among: `d`, `h` and `m`)
  - the time window (start-end Unix timestamps)
  - how many results you want

Example:

```python
# Read aggregated measurements (on day, hour or minute) for a station in a given
# time interval
aggr_msmts = mgr.get_measurements(station_id, 'h', 1505424648, 1505425648, limit=5)

```

## Buffers

As usually a meteostation tracks a lot of datapoints over time and it is expensive
(eg. in terms of battery and bandwidth usage) to submit them one by one to the
OWM Stations API, a good abstraction tool to work with with measurements is 
`stationsapi30.buffer.Buffer` objects.

A buffer is basically a "box" that collects multiple measurements for a station.
You can use the buffer to store measurements over time and to send all of the 
measurements to the API at once.

Examples:


```python
from pyowm.stationsapi30.buffer import Buffer

# Create a buffer for a station...
buf = Buffer(station_id)

# ...and append measurement objects to it
buf.append(msmt_1)
buf.append(msmt_2)
buf.append(msmt_3)

# ... or read data from other formats
# -- a dict
# (as you would pass to Measurement.from_dict method)
buf.append_from_dict(msmt_dict)
# -- a JSON string
# that string must be parsable as a dict that you can feed to
# Measurement.from_dict method
with open('my-msmts.json') as j:
    buf.append_from_json(j.read())

# buffers are nice objects
# -- they are iterable
print(len(buf))
for measurement in buf:
    print(measurement)

# -- they can be joined
new_buf = buf + another_buffer

# -- they can be emptied
buf.empty()

# -- you can order measurements in a buffer by their creation time
buf.sort_chronologically()
buf.sort_reverse_chronologically()


# Send measurements stored in a buffer to the API using the StationManager object
mgr.send_buffer(buf)
```

You can load/save measurements into/from Buffers from/tom any persistence backend:
  - *Saving*: persist data to the filesystem or to custom data persistence 
    backends that you can provide (eg. databases)
  - *Loading*: You can also pre-load a buffer with (or append to it) measurements 
    stored on the file system or read from custom data persistence backends

The default persistence backend is: `stationsapi30.persistence_backend.JSONPersistenceBackend` 
and allows to read/write buffer data from/to JSON files

As said, you can use your own *custom data backends*: they must be
subclasses of `stationsapi30.persistence_backend.PersistenceBackend`


Examples:

```python

from pyowm.stationsapi30 import persistence_backend

# instantiate the default JSON-based backend: you need to provide the ID of the 
# stations related to measurements...
json_be = persistence_backend.JSONPersistenceBackend('/home/myfile.json', station_id)


# ... and use it to load a buffer
buf = json_be.load_to_buffer()


# ... and to save buffers
json_be.persist_buffer(buf)


# You can use your own persistence backends
my_custom_be = MyCustomPersistenceBackend()
buf = my_custom_be.load_to_buffer()
my_custom_be.persist_buffer(buf)
```