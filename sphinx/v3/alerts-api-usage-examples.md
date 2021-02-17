# Weather Alert API

You can use the OWM API to create triggers.

Each trigger represents the check if a set of conditions on certain weather parameter values are met over certain geographic areas.

Whenever a condition is met, an alert is fired and stored, and can be retrieved by polling the API.

## OWM website technical reference
 - [https://openweathermap.org/triggers](https://openweathermap.org/triggers)
 - [http://openweathermap.org/triggers-struct](http://openweathermap.org/triggers-struct)

## A full example first

Hands-on! This is a full example of how to use the Alert API. Check further for details about the involved object types.


```python
from pyowm import OWM
from pyowm.utils import geo
from pyowm.alertapi30.enums import WeatherParametersEnum, OperatorsEnum, AlertChannelsEnum
from pyowm.alertapi30.condition import Condition

# obtain an AlertManager instance
owm = OWM('apikey')
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


# -- conditions --
condition_1 = Condition(WeatherParametersEnum.TEMPERATURE,
                        OperatorsEnum.GREATER_THAN,
                        313.15)  # kelvin
condition_2 = Condition(WeatherParametersEnum.CLOUDS,
                        OperatorsEnum.EQUAL,
                        80) # clouds % coverage

# -- triggers --

# create a trigger
trigger = am.create_trigger(start_after_millis_=355000, end_after_millis=487000,
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

## Alert API object model

This is the Alert API object model:

  - *Trigger*: collection of alerts to be met over specified areas and within a specified time frame according to specified weather params conditions
  - *Condition*: rule for matching a weather measurement with a specified threshold
  - *Alert*: whenever a condition is met, an alert is created (or updated) and can be polled to verify when it has been met and what the actual weather param value was.
  - *Area*: geographic area over which the trigger is checked
  - *AlertChannel*: as OWM plans to add push-oriented alert channels (eg. push notifications), we need to encapsulate this into a specific class

and then you have an *AlertManager* class that you will need to instantiate to operatively interact with the Alert API 


### Area

The area describes the geographic boundaries over which a trigger is evaluated. Don't be mislead by the term "area": this
can refer also to a specific geopoint or a set of them, besides - of course - polygons and set of polygons.

Any of the geometry subtypes found in `pyowm.utils.geo` module (point, multipoint, polygon, multipolygon) are fine to use.

Example:

```python
from pyowm.utils import geo
point = geo.Point(20.8, 30.9)  # available geometry types: Point, MultiPoint, Polygon, MultiPolygon
point.geojson()
'''
{
  "type": "Point",
  "coordinates":[ 20.8, 30.9 ]
}
'''
```


Defining complex geometries is sometimes difficult, but in most cases you just need to set triggers upon cities: that's
why we've added a method to the `pyowm.weatherapi25.cityidregistry.CityIDRegistry` registry that returns the geopoints 
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
centre = geopoints[0] # the list has only 1 geopoint
square_polygon = centre.bounding_square_polygon(inscribed_circle_radius_km=12) # radius of the inscribed circle in kms (defaults to: 10)
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

Here is an example of conditions:

```python
from pyowm.alertapi30.condition import Condition
from pyowm.alertapi30 import enums

# this condition checks if the temperature is bigger than 313.15 Kelvin degrees
condition = Condition(enums.WeatherParametersEnum.TEMPERATURE,
                      enums.OperatorsEnum.GREATER_THAN,
                      313.15)
```

Remember that each Condition is checked by the OWM Alert API on the geographic area that you need to specify!

You can bind multiple `pyowm.alertapi30.condition.Condition` objects to a Trigger: each Alert will be fired when
a specific Condition is met on the area.


### Alert

As said, whenever one or more conditions are met on a certain area, an alert is fired (this means that "the trigger triggers")

If the condition then keeps on being met, more and more alerts will be spawned by the OWM Alert API. You can retrieve
such alerts by polling the OWM API (see below about how to do it).

Each alert is represented by PyOWM as a `pyowm.alertapi30.alert.Alert` instance, having:
  - a unique identifier
  - timestamp of firing
  - a link back to the unique identifier of the parent `pyowm.alertapi30.trigger.Trigger` object instance
  - the list of met conditions (each one being a dict containing the `Condition` object and the weather parameter
    value that actually made the condition true)
  - the geocoordinates where the condition has been met (they belong to the area that had been specified for the Trigger)

Example:

```python
from pyowm.alertapi30.condition import Condition
from pyowm.alertapi30 import enums
from pyowm.alertapi30.alert import Alert

condition = Condition(enums.WeatherParametersEnum.TEMPERATURE,
                      enums.OperatorsEnum.GREATER_THAN,
                      356.15)

alert = Alert('alert-id',                   # alert id
              'parent-trigger-id',          # parent trigger's id
              [{                            # list of met conditions
                    "current_value": 326.4,
                    "condition": condition
               }],
               {"lon": 37, "lat": 53},      # coordinates
               1481802100000                # fired on
)
```

As you see, you're not meant to create alerts, but PyOWM is supposed to create them for you as they are fired by the
OWM API.


### AlertChannel
Something that OWM envisions, but still does not offer. Possibly, when you will setup a trigger you shall also specify 
the channels you want to be notified on: that's why we've added a reference to a list of `AlertChannel` instances
directly on the Trigger objects (the list now only points to the default channel)
 
A useful enumerator is offered in module `pyowm.alertapi30.enums`: `AlertChannelsEnum` (says what channels should the alerts
delivered to)
 
As of today, the default `AlertChannel` is: `AlertChannelsEnum.OWM_API_POLLING`, and is the only one available.


### Trigger
As said, each trigger represents the check if a set of conditions on certain weather parameter values are met over 
certain geographic areas.

A Trigger is the local proxy for the corresponding entry on the OWM API: Triggers can be operated through 
`pyowm.alertapi30.alertmanager.AlertManager` instances.

Each Trigger has these attributes:
  - start_after_millis: _with respect to the time when the trigger will be created on the Alert API_, how many milliseconds after should it begin to be checked for conditions matching
  - end_after_millis: _with respect to the time when the trigger will be created on the Alert API_, how many milliseconds after should it end to be checked for conditions matching
  - alerts: a list of `pyowm.alertapi30.alert.Alert` instances, which are the alerts that the trigger has fired so far
  - conditions: a list of `pyowm.alertapi30.condition.Condition` instances
  - area: a list of `pyowm.utils.geo.Geometry` instances, representing the geographic area on which the trigger's conditions need to be checked
  - alertChannels: list of `pyowm.alertapi30.alert.AlertChannel` objects, representing which channels this trigger is notifying to

**Notes on trigger's time period**
By design, PyOWM will only use the `after` operator to communicate time periods for Triggers to the Alert API.
will send them to the API using the `after` operator.

The millisecond start/end deltas will be calculated with respect to the time when the Trigger record is created on the
Alert API using `pyowm.alertapi30.alertmanager.AlertManager.create_trigger`


### AlertManager
The OWM main entry point object allows you to get an instance of an `pyowm.alertapi30.alert_manager.AlertManager` object:
use it to interact with the Alert API and create/read/update/delete triggers and read/delete the related alerts.

Here is how to instantiate an `AlertManager`:

```python
from pyowm import OWM

owm = OWM(API_Key='my-API-key')
am = owm.alert_manager()
```

Then you can do some nice things with it:

  - create a trigger
  - read all of your triggers
  - read a named trigger
  - modify a named trigger
  - delete a named trigger
  - read all the alerts fired by a named trigger
  - read a named alert
  - delete a named alert
  - delete all of the alerts for a named trigger