You can query the OWM API for current Ultra Violet (UV) intensity data in the surroundings of
specific geocoordinates.

Please refer to the official API docs for [UV](http://openweathermap.org/api/uvi)


### Querying UV index observations

Getting the data is easy:

```python
from pyowm import OWM
owm = OWM('apikey')
mgr = owm.uvindex_manager()
uvi = mgr.uvindex_around_coords(lat, lon)
```

The query returns an UV Index value entity instance


### Querying UV index forecasts

As easy as:

```python
uvi_list = mgr.uvindex_forecast_around_coords(lat, lon)
```

### Querying UV index history

As easy as: 

```python
uvi_history_list = mgr.uvindex_history_around_coords(
    lat, lon,
    datetime.datetime(2017, 8, 1, 0, 0, 0, timezone.utc),
    end=datetime.datetime(2018, 2, 15, 0, 0, 0, timezone.utc))
```

`start` and `end` can be ISO-8601 date strings, unix timestamps or Python datetime
objects.

In case `end` is not provided, then UV historical values will be retrieved
dating back to `start` up to the current timestamp.


### `UVIndex` entity
`UVIndex` is an entity representing a UV intensity measurement on a certain geopoint.
Here are some of the methods:

```python
uvi.get_value()
uvi.get_reference_time()
uvi.get_reception_time()
uvi.get_exposure_risk()
```

The `get_exposure_risk()` methods returns a string estimating the risk of harm from 
unprotected sun exposure if an average adult was exposed to a UV intensity such as the on
in this measurement. [This is the source mapping](https://en.wikipedia.org/wiki/Ultraviolet_index)
for the statement.
