# Weather Alert API

You can use the OWM API to create triggers.

Each trigger represents the check if a set of conditions on certain weather parameter values are met over certain geographic areas.

Whenever a condition is met, an alert is fired and stored, and can be retrieved by polling the API.

## OWM website technical reference
 - [https://openweathermap.org/triggers](https://openweathermap.org/triggers)
 - [http://openweathermap.org/triggers-struct](http://openweathermap.org/triggers-struct)

## PyOWM Object model

This is the descending object model:

  - *Trigger*: collection of alerts to be met over specified areas and within a specified time frame according to specified weather params conditions
  - *Condition*: rule for matching a weather measuerment with a specified threshold
  - *Alert*: whenever a condition is met, an alert is created (or updated) and can be polled to verify when it has been met and what the actual weather param value was.
  - *Area*: geographic area over which the trigger is checked
  - *AlertChannel*: as OWM plans to add push-oriented alert channels (eg. push notifications), we need to encapsulate this into a specific class

### Area

The area describes the geographic boundaries over which a trigger is evaluated. Don't be mislead by the term "area": this
can refer also to a specific geopoint or a set of them, besides - of course - polygons and set of polygons.

Any of the geometry subtypes found in `pyowm.utils.geo` module (point, multipoint, polygon, multipolygon) are fine to use.

Defining complex geometries is sometimes difficult, but in most cases you just need to set triggers upon cities: that's
why we've added a method to the `pyowm.webapi25.cityidregistry.CityIDRegistry` registry that returns the geopoints 
that correspond to one or more named cities:

```python
import pyowm
owm = pyowm.OWM('your-API-key')
reg = owm.city_id_registry()
geopoints = reg.geopoints_for('London', country='GB')
``` 

But still some very spread cities (think of London,GB or Los Angeles,CA) exist and therefore approximating a city to
a single point is not accurate at all: that's why we've added a nice method to get a _squared polygon that is circumscribed
to the circle having a specified geopoint as its centre_. This makes it possible to easily get polygons to cover large
squared areas and you would only need to specify the radius of the circle. Let's do it for London,GB in example: 

```python
geopoints = reg.geopoints_for('London', country='GB')
centre = geopoints[0]                                     # the list has only 1 geopoint
square_polygon = centre.square_circumscribed(radius=12)   # radius of the inscribed circle in kms (defaults to: 10)
```

Please, notice that if you specify big values for the radius you need to take care about the projection of geographic
coordinates on a proper geoid: this means that if you don't, the polygon will only _approximate_ a square.


Topology is set out as stated by [GeoJSON](https://github.com/frewsxcv/python-geojson)

Moreover, there is a useful factory for Areas: `pyowm.utils.geo.GeometryBuilder.build()`, that you can use to turn a geoJSON standard
dictionary into the corresponding topology type:


```python
from pyowm.utils.geo import GeometryBuilder
the_dict = {
    "type": "Point",
    "coordinates": [53, 37]
}
geom = GeometryBuilder.build(the_dict)
type(geom)  # <pyowm.utils.geo.Point>
```

You can bind multiple `pyowm.utils.geo` geometry types to a Trigger: a list of such geometries is considered to be
the area on which conditions of a Trigger are checked. 


### Condition
A condition is a numeric rule to be checked on a named weather variable. Something like:

```
  - VARIABLE X IS GREATER THAN AMOUNT_1
  - VARIABLE Y IS EQUAL TO AMOUNT_2
  - VARIABLE Z IS DIFFERENT FROM AMOUNT_3
```

`GREATER, EQUAL TO, DIFFERENT FROM` are called comparison expressions or operators; `VARIABLE X, Y, Z` are 
called target parameters. 

Each condition is then specified by:
  - target_param: weather parameter to be checked. Can be: `temp, pressure, humidity, wind_speed, wind_direction, clouds`.
  - expression: str, operator for the comparison. Can be: `$gt`, $gte, $lt, $lte, $eq, $ne`
  - amount: number, the comparison value

Conditions are bound to Triggers, as they are set on Trigger instantiation.

As Conditions can be only set on a limited number of weather variables and can be expressed only through a closed set of 
comparison operators, convenient **enumerators** are offered in module `pyowm.alertapi30.enums`:

  - `WeatherParametersEnum` --> what weather variable to set this condition on
  - `OperatorsEnum` --> what comparison operator to use on the weather parameter

Use enums so that you don't have to remember the syntax of operators and weather params that is specific to the OWM Alert API.
Here is how you use them:

```python
from pyowm.alertapi30 import enums
enums.WeatherParametersEnum.items()      # [('TEMPERATURE', 'temp'), ('WIND_SPEED', 'wind_speed'), ... ]
enums.WeatherParametersEnum.TEMPERATURE  # 'temp'
enums.WeatherParametersEnum.WIND_SPEED   # 'wind_speed'

enums.OperatorsEnum.items()              # [('GREATER_THAN', '$gt'), ('NOT_EQUAL', '$ne'), ... ]
enums.OperatorsEnum.GREATER_THAN         # '$gt'
enums.OperatorsEnum.NOT_EQUAL            # '$ne'

```

Remember that each Condition is checked by the OWM Alert API on the geographic area that you need to specify!

You can bind multiple `pyowm.alertapi30.condition.Condition` objects to a Trigger: each Alert will be fired when
a specific Condition is met on the area.


### Alert

Attributes:
  - id: str, unique alert identifier
  - trigger_id: str, link back to parent Trigger
  - met_conditions: list of dict, each one reports a link to a parent's Condition obj and the current values that made the Alert fire
  - last_update: epoch, last time when the alert has been fired
  - coordinates: dict representing the coordinates where the condition were met


### AlertChannel
Something that OWM envisions, but still does not offer. Possibly, when you will setup a trigger you shall also specify 
the channels you want to be notified on: that's why we've added a reference to a list of `AlertChannel` instances
 directly on the Trigger objects (the list now only points to the default channel)
 
A useful enumerator is offered in module `pyowm.alertapi30.enums`: `AlertChannelsEnum` (says what channels should the alerts
delivered to)
 
 
As of today, the default `AlertChannel` is: `AlertChannelsEnum.OWM_API_POLLING`, and is the only one available.


### Trigger

Attributes:
  - start: epoch when the trigger starts
  - end: epoch when the trigger ends
  - alerts: list of Alert objects
  - conditions: list of Condition objects
  - area: list of dicts, each one representing a geoJSON data structure
  - alertChannels: list of AlertChannel objects

**Notes on trigger's time period**: by design, PyOWM will only allow users to specify absolute datetimes for start/end and will send them to the API using `$exact`


### AlertManager
The OWM façade object allows to get an instance of a `AlertManager` object: use it to interact with the Alert API
and create/read/update/delete triggers and alerts.


## Code samples

```python
from pyowm import OWM
from pyowm.utils import geo
from pyowm.alertapi30.enums import WeatherParametersEnum, OperatorsEnum, AlertChannelsEnum
from pyowm.alertapi30.condition import Condition

# obtain an AlertManager instance
owm = OWM(API_Key='blablabla')
am = owm.alert_manager()

# -- areas --
geom_1 = geo.Point(lon, lat)  # available types: Point, MultiPoint, Polygon, MultiPolygon
geom_1.geojson()
'''
{
  "type": "Point",
  "coordinates":[ lon, lat ]
}
'''
geom_2 = geo.MultiPolygon([[lon1, lat1], [lon2, lat2], [lon3, lat3], [lon1, lat1]]
                          [[lon7, lat7], [lon8, lat8], [lon9, lat9], [lon7, lat7]])

# a very nice feature: look for city ID and get its corresponding geopoint!
reg = owm.city_id_registry()
geoms = reg.geopoints_for('London', country='GB')


# -- conditions --
condition_1 = Condition(WeatherParametersEnum.TEMPERATURE,
                        OperatorsEnum.GREATER_THAN,
                        313.15)  # kelvin
condition_2 = Condition(WeatherParametersEnum.CLOUDS,
                        OperatorsEnum.EQUAL,
                        80) # clouds % coverage

# -- triggers --

# create a trigger
trigger = am.create_trigger(start_ts=1234567890, end_ts=1278654300,
                            conditions=[condition_1, condition_2],
                            area=[geom_1, geom_2],
                            alert_channel=AlertChannelsEnum.OWM_API)

# read all triggers
triggers_list = am.get_triggers()

# read one named trigger
trigger_2 = am.get_trigger('trigger_id')

# update a trigger
am.update_trigger(trigger_2)

# delete a trigger
am.delete_trigger(trigger_2)

# -- alerts --

# retrieved from the local parent Trigger obj...
alerts_list = trigger.get_alerts()
alerts_list = trigger.get_alerts_since('2018-01-09T23:07:24Z')  # useful for polling alerts
alerts_list = trigger.get_alerts_on(WeatherParametersEnum.TEMPERATURE)
alert = trigger.get_alert('alert_id')

# ...or retrieved from the remote API
alerts_list_alternate = am.get_alerts_for(trigger)
alert_alternate = am.get_alert('alert_id')


# delete all or one alert
am.delete_all_alerts_for(trigger)
am.delete_alert_for(trigger, alert)
```
