#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyowm.commons.exceptions
from pyowm.alertapi30.alert import Alert
from pyowm.alertapi30.condition import Condition
from pyowm.alertapi30.enums import AlertChannelsEnum
from pyowm.utils import formatting
from pyowm.utils.geo import GeometryBuilder


class Trigger:
    """
    Object representing a the check if a set of weather conditions are met on a given geographical area: each condition
    is a rule on the value of a given weather parameter (eg. humidity, temperature, etc). Whenever a condition from a
    `Trigger` is met, the OWM API crates an alert and binds it to the the `Trigger`.
    A `Trigger` is the local proxy for the corresponding entry on the OWM API, therefore it can get ouf of sync as
    time goes by and conditions are met: it's up to you to "refresh" the local trigger by using a
    `pyowm.utils.alertapi30.AlertManager` instance.
    :param start_after_millis: how many milliseconds after the trigger creation the trigger begins to be checked
    :type start_after_millis: int
    :param end_after_millis: how many milliseconds after the trigger creation the trigger ends to be checked
    :type end_after_millis: int
    :param alerts: the `Alert` objects representing the alerts that have been fired for this `Trigger` so far. Defaults
    to `None`
    :type alerts: list of `pyowm.utils.alertapi30.Alert` instances
    :param conditions: the `Condition` objects representing the set of checks to be done on weather variables
    :type conditions: list of `pyowm.utils.alertapi30.Condition` instances
    :param area: the geographic are over which conditions are checked: it can be composed by multiple geoJSON types
    :type area: list of geoJSON types
    :param alert_channels: the alert channels through which alerts originating from this `Trigger` can be consumed.
    Defaults to OWM API polling
    :type alert_channels: list of `pyowm.utils.alertapi30.AlertChannel` instances
    :param id: optional unique ID for this `Trigger` instance
    :type id: str
    :returns:  a *Trigger* instance
    :raises: *ValueError* when start or end epochs are `None` or when end precedes start or when conditions or area
    are empty collections

    """
    def __init__(self, start_after_millis, end_after_millis, conditions, area, alerts=None, alert_channels=None, id=None):
        assert start_after_millis is not None
        assert end_after_millis is not None
        assert isinstance(start_after_millis, int)
        assert isinstance(end_after_millis, int)
        if start_after_millis > end_after_millis:
            raise ValueError("Error: trigger start time must precede trigger end time")
        self.start_after_millis = start_after_millis
        self.end_after_millis = end_after_millis
        assert conditions is not None
        if len(conditions) == 0:
            raise ValueError('A trigger must contain at least one condition: you provided none')
        self.conditions = conditions
        assert area is not None
        if len(area) == 0:
            raise ValueError('The area for a trigger must contain at least one geoJSON type: you provided none')
        self.area = area
        if alerts is None or len(alerts) == 0:
            self.alerts = list()
        else:
            self.alerts = alerts
        if alert_channels is None or len(alert_channels) == 0:
            self.alert_channels = [AlertChannelsEnum.OWM_API_POLLING]
        else:
            self.alert_channels = alert_channels
        self.id = id

    def get_alerts(self):
        """
        Returns all of the alerts for this `Trigger`
        :return: a list of `Alert` objects
        """
        return self.alerts

    def get_alert(self, alert_id):
        """
        Returns the `Alert` of this `Trigger` having the specified ID
        :param alert_id: str, the ID of the alert
        :return: `Alert` instance
        """
        for alert in self.alerts:
            if alert.id == alert_id:
                return alert
        return None

    def get_alerts_since(self, timestamp):
        """
        Returns all the `Alert` objects of this `Trigger` that were fired since the specified timestamp.
        :param timestamp: time object representing the point in time since when alerts have to be fetched
        :type timestamp: int, ``datetime.datetime`` or ISO8601-formatted string
        :return: list of `Alert` instances
        """
        unix_timestamp = formatting.to_UNIXtime(timestamp)
        result = []
        for alert in self.alerts:
            if alert.last_update >= unix_timestamp:
                result.append(alert)
        return result

    def get_alerts_on(self, weather_param):
        """
        Returns all the `Alert` objects of this `Trigger` that refer to the specified weather parameter (eg. 'temp',
        'pressure', etc.). The allowed weather params are the ones enumerated by class
        `pyowm.alertapi30.enums.WeatherParametersEnum`
        :param weather_param: str, values in `pyowm.alertapi30.enums.WeatherParametersEnum`
        :return: list of `Alert` instances
        """
        result = []
        for alert in self.alerts:
            for met_condition in alert.met_conditions:
                if met_condition['condition'].weather_param == weather_param:
                    result.append(alert)
                    break
        return result

    @classmethod
    def from_dict(cls, the_dict):
        if the_dict is None:
            raise pyowm.commons.exceptions.ParseAPIResponseError('Data is None')
        try:
            # trigger id
            trigger_id = the_dict.get('_id', None)

            # start timestamp
            start_dict = the_dict['time_period']['start']
            expr = start_dict['expression']
            if expr != 'after':
                raise ValueError('Invalid time expression: "%s" on start timestamp. Only: "after" is supported' % expr)
            start = start_dict['amount']

            # end timestamp
            end_dict = the_dict['time_period']['end']
            expr = end_dict['expression']
            if expr != 'after':
                raise ValueError('Invalid time expression: "%s" on end timestamp. Only: "after" is supported' % expr)
            end = end_dict['amount']

            # conditions
            conditions = [Condition.from_dict(c) for c in the_dict['conditions']]

            # alerts
            alerts_dict = the_dict['alerts']
            alerts = list()
            for key in alerts_dict:
                alert_id = key
                alert_data = alerts_dict[alert_id]
                alert_last_update = alert_data['last_update']
                alert_met_conds = list()
                for c in alert_data['conditions']:
                    if isinstance(c['current_value'], int):
                        cv = c['current_value']
                    else:
                        cv = c['current_value']['min']
                    item = dict(current_value=cv, condition=Condition.from_dict(c['condition']))
                    alert_met_conds.append(item)
                alert_coords = alert_data['coordinates']
                alert = Alert(alert_id, trigger_id, alert_met_conds, alert_coords, last_update=alert_last_update)
                alerts.append(alert)

            # area
            area_list = the_dict['area']
            area = [GeometryBuilder.build(a_dict) for a_dict in area_list]

            # alert channels
            alert_channels = None  # defaulting

        except ValueError as e:
            raise pyowm.commons.exceptions.ParseAPIResponseError('Impossible to parse JSON: %s' % e)
        except KeyError as e:
            raise pyowm.commons.exceptions.ParseAPIResponseError('Impossible to parse JSON: %s' % e)

        return Trigger(start, end, conditions, area=area, alerts=alerts, alert_channels=alert_channels, id=trigger_id)

    def to_dict(self):
        return {
            "start_after_millis": self.start_after_millis,
            "end_after_millis": self.end_after_millis,
            "conditions": [c.to_dict() for c in self.conditions],
            "area": [g.to_dict() for g in self.area],
            "alerts": [alert.to_dict() for alert in self.alerts],
            "alert_channels": [ac.to_dict() for ac in self.alert_channels],
            "id": self.id
        }

    def __repr__(self):
        return "<%s.%s - id=%s, start_after_mills=%s, end_after_mills=%s, alerts=%s>" % (
                    __name__,
                    self.__class__.__name__,
                    self.id if self.id is not None else 'None',
                    self.start_after_millis,
                    self.end_after_millis,
                    str(len(self.alerts)))
