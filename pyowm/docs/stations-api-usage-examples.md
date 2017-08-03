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

TBD