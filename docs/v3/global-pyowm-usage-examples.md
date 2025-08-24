# Global PyOWM library usage examples

The PyOWM library has one main entry point: the `OWM` class. You just need to instantiate it to get started!

Please refer to the `Code Recipes` page, section: `Library initialization`, to get info about how to instantiate 
the PyOWM library



## Dumping PyOWM objects to Python dictionaries
PyOWM object instances (eg. `Weather` or `Location` objects) can be dumped to `dict`s:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
mgr = owm.weather_manager()
weather = mgr.weather_at_place('London,GB').weather  # get the weather at London,GB now
dump_dict = weather.to_dict()
```

This is useful as you can save the dump dictionaries to files (eg. using Python `json` or `pickle` modules)

## Printing objects
Most of PyOWM objects can be pretty-printed for a quick introspection:

```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
print(owm)   # <pyowm.weatherapi30.owm25.OWM25 - API key=*******i-key, subscription type=free, PyOWM version=3.0.0>
```

