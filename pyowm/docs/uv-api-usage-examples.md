You can query the OWM API for current Ultra Violet (UV) intensity data in the surroundings of
specific geocoordinates.

Please refer to the official API docs for [UV](http://openweathermap.org/api/uvi)


### Querying UV index observations

Getting the data is easy:

```
uvi = owm.uvindex_around_coords(lat, lon)
```

The query returns an UV Index value entity instance


### `UVIndex` entity
`UVIndex` is an entity representing a UV intensity measurement on a certain geopoint.
Here are some of the methods:

```
uvi.get_value()
uvi.get_reference_time()
uvi.get_reception_time()
uvi.get_exposure_risk()
```

The `get_exposure_risk()` methods returns a string estimating the risk of harm from 
unprotected sun exposure if an average adult was exposed to a UV intensity such as the on
in this measurement. [This is the source mapping](https://en.wikipedia.org/wiki/Ultraviolet_index)
for the statement.