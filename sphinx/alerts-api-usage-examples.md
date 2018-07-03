# Weather Alert API

You can use the OWM API to create triggers. Each trigger represents the check if a set of conditions on certain weather 
parameter values are met over certain geographic areas.

Whenevere a condition is met, an alert is fired and stored, and can be retrieved by polling the API.

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

Attributes:
  - coordinates: list of lists (each sublist representing a point)

Any of the geometry subtypes found in `pyowm.utils.geo` module (point, multipoint, polygon, multipolygon) are fine to use.

Topology is set out as stated by [GeoJSON](https://github.com/frewsxcv/python-geojson)

There is a useful factory for Areas: `pyowm.utils.geo.GeometryBuilder.build()`


### Condition

Attributes:
  - id: str, unique condition identifier
  - target_param: weather parameters to be checked. Can be: `temp, pressure, humidity, wind_speed, wind_direction, clouds`.
  - expression: str, operator for the comparison. Can be: `$gt`, $gte, $lt, $lte, $eq, $ne`
  - amount: number, the comparison value

Conditions are bound to Triggers, as they are set on Trigger instantiation.

As Conditions can be only set on a limited number of meteo variables and can be expressed only through a closed set of 
value comparison operators, convenient **enumerators** are offered in module `pyowm.alertapi30.enums`:

  - `WeatherParametersEnum` --> what meteo variable to set triggers on
  - `OperatorsEnum` --> what comparison operator to use on the meteo variable
  - `AlertChannelsEnum` --> what channels should alerts of

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
