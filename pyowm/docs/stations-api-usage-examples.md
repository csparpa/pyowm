# Stations API 3.0 usage examples

As regards meteo stations:

```python
import pyowm
owm = pyowm.OWM('your-API-key')
mgr = owm.stations_manager()        # Obtain the Stations API client

# Get all your stations
# GET http://samples.openweathermap.org/data/3.0/stations?appid=b1b15e88fa797225412429c1c50c122a1
stats = mgr.get_stations()

# Get one named station
# GET http://api.openweathermap.org/data/3.0/stations/583436dd9643a9000196b8d6?appid=b1b15e88fa797225412429c1c50c122a1
stat = mgr.get_station('583436dd9643a9000196b8d6')

# Create a new station?appid=b1b15e88fa797225412429c1c50c122a1
# POST http://api.openweathermap.org/data/3.0/stations
stat = mgr.create_station("SF_TEST001", "San Francisco Test Station", 37.76, -122.43, 150)

# Modify a named station
# PUT http://api.openweathermap.org/data/3.0/stations/583436dd9643a9000196b8d6?appid=b1b15e88fa797225412429c1c50c122a1
mgr.modify_station(stat)

# Delete a named station and related measurements
# DELETE http://api.openweathermap.org/data/3.0/stations/583436dd9643a9000196b8d6?appid=b1b15e88fa797225412429c1c50c122a1
mgr.delete_station(stat)

```

As regards measurements:

```python

# Send a new raw measurement for a station
mgr.send_measurement(measurement_obj)

# Send new raw measurements for multiple stations
msmsts = mgr.send_measurements(list_of_raw_measurement_objs)

# Read aggregated measurements for a station
aggr_msmts = mgr.get_measurements(station_id, interval, limit=None)

```

A good tool to work with with measurements is Buffers:

```python
# Create a buffer for a station...
buf = Buffer(station_id)

# ...and append measurement objects to it
buf.append(msmt_1_of_station)
buf.append(msmt_2_of_station)
buf.append(msmt_3_of_station)


# ... or read data from other data formats
buf.append_from_dict(data_dict)
buf.append_from_json(json_string)

# iterate over the buffer
print(len(buf))
for measurement in buf:
    print(measurement)

# join buffers
buf = buf + another_buffer

# send buffered data to the API
mgr.send_buffer(buf)

# empty a buffer
buf.empty()

# order a buffer by the creation time of its samples (straight/reverse)
buf.sort_chronologically()
buf.sort_reverse_chronologically()
```

You can load/save data in Buffers to/from any persistent datastore:

```python

from pyowm.stationsapi30 import persistence_backend

# PyOWM provides pre-configured persistence backends...
json_be = persistence_backend.JSONPersistenceBackend('/home/myfile.json', station_id)
my_custom_be = YourCustomPersistenceBackend()

# ..which you can use to load buffers...
buf = json_be.load_to_buffer()
buf = my_custom_be.load_to_buffer()

# ...and save buffers
json_be.persist_buffer(buf)
my_custom_be.persist_buffer(buf)
```