#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.alertapi30.alert import Alert
from pyowm.alertapi30.trigger import Trigger
from pyowm.alertapi30.uris import ROOT_ALERT_API_URL, TRIGGERS_URI, NAMED_TRIGGER_URI, ALERTS_URI, NAMED_ALERT_URI
from pyowm.commons.http_client import HttpClient
from pyowm.constants import ALERT_API_VERSION
from pyowm.utils import formatting, timestamps


class AlertManager:

    """
    A manager objects that provides a full interface to OWM Alert API. It implements CRUD methods on Trigger entities
    and read/deletion of related Alert objects

    :param API_key: the OWM Weather API key
    :type API_key: str
    :param config: the configuration dictionary
    :type config: dict
    :returns: an *AlertManager* instance
    :raises: *AssertionError* when no API Key is provided

    """

    def __init__(self, API_key, config):
        assert API_key is not None, 'You must provide a valid API Key'
        self.API_key = API_key
        assert isinstance(config, dict)
        self.http_client = HttpClient(API_key, config, ROOT_ALERT_API_URL)

    def alert_api_version(self):
        return ALERT_API_VERSION

    # TRIGGER methods

    def create_trigger(self,  start, end, conditions, area, alert_channels=None):
        """
        Create a new trigger on the Alert API with the given parameters
        :param start: time object representing the time when the trigger begins to be checked
        :type start: int, ``datetime.datetime`` or ISO8601-formatted string
        :param end: time object representing the time when the trigger ends to be checked
        :type end: int, ``datetime.datetime`` or ISO8601-formatted string
        :param conditions: the `Condition` objects representing the set of checks to be done on weather variables
        :type conditions: list of `pyowm.utils.alertapi30.Condition` instances
        :param area: the geographic are over which conditions are checked: it can be composed by multiple geoJSON types
        :type area: list of geoJSON types
        :param alert_channels: the alert channels through which alerts originating from this `Trigger` can be consumed.
        Defaults to OWM API polling
        :type alert_channels: list of `pyowm.utils.alertapi30.AlertChannel` instances
        :returns:  a *Trigger* instance
        :raises: *ValueError* when start or end epochs are `None` or when end precedes start or when conditions or area
        are empty collections
        """
        assert start is not None
        assert end is not None

        # prepare time period
        unix_start = formatting.to_UNIXtime(start)
        unix_end = formatting.to_UNIXtime(end)
        unix_current = timestamps.now(timeformat='unix')
        if unix_start >= unix_end:
            raise ValueError("The start timestamp must precede the end timestamp")
        delta_millis_start = timestamps.millis_offset_between_epochs(unix_current, unix_start)
        delta_millis_end = timestamps.millis_offset_between_epochs(unix_current, unix_end)
        the_time_period = {
            "start": {
                "expression": "after",
                "amount": delta_millis_start
            },
            "end": {
                "expression": "after",
                "amount": delta_millis_end
            }
        }

        assert conditions is not None
        if len(conditions) == 0:
            raise ValueError('A trigger must contain at least one condition: you provided none')
        the_conditions = [dict(name=c.weather_param, expression=c.operator, amount=c.amount) for c in conditions]

        assert area is not None
        if len(area) == 0:
            raise ValueError('The area for a trigger must contain at least one geoJSON type: you provided none')
        the_area = [a.to_dict() for a in area]

        # >>> for the moment, no specific handling for alert channels

        status, payload = self.http_client.post(
            TRIGGERS_URI,
            params={'appid': self.API_key},
            data=dict(time_period=the_time_period, conditions=the_conditions, area=the_area),
            headers={'Content-Type': 'application/json'})
        return Trigger.from_dict(payload)

    def get_triggers(self):
        """
        Retrieves all of the user's triggers that are set on the Weather Alert API.

        :returns: list of `pyowm.alertapi30.trigger.Trigger` objects

        """
        status, data = self.http_client.get_json(
            TRIGGERS_URI,
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})
        return [Trigger.from_dict(item) for item in data]

    def get_trigger(self, trigger_id):
        """
        Retrieves the named trigger from the Weather Alert API.

        :param trigger_id: the ID of the trigger
        :type trigger_id: str
        :return: a `pyowm.alertapi30.trigger.Trigger` instance
        """
        assert isinstance(trigger_id, str), "Value must be a string"
        status, data = self.http_client.get_json(
            NAMED_TRIGGER_URI % trigger_id,
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})
        return Trigger.from_dict(data)

    def update_trigger(self, trigger):
        """
        Updates on the Alert API the trigger record having the ID of the specified Trigger object: the remote record is
        updated with data from the local Trigger object.

        :param trigger: the Trigger with updated data
        :type trigger: `pyowm.alertapi30.trigger.Trigger`
        :return: ``None`` if update is successful, an error otherwise
        """
        assert trigger is not None
        assert isinstance(trigger.id, str), "Value must be a string"
        the_time_period = {
            "start": {
                "expression": "after",
                "amount": trigger.start_after_millis
            },
            "end": {
                "expression": "after",
                "amount": trigger.end_after_millis
            }
        }
        the_conditions = [dict(name=c.weather_param, expression=c.operator, amount=c.amount) for c in trigger.conditions]
        the_area = [a.to_dict() for a in trigger.area]

        status, _ = self.http_client.put(
            NAMED_TRIGGER_URI % trigger.id,
            params={'appid': self.API_key},
            data=dict(time_period=the_time_period, conditions=the_conditions, area=the_area),
            headers={'Content-Type': 'application/json'})

    def delete_trigger(self, trigger):
        """
        Deletes from the Alert API the trigger record identified by the ID of the provided
        `pyowm.alertapi30.trigger.Trigger`, along with all related alerts

        :param trigger: the `pyowm.alertapi30.trigger.Trigger` object to be deleted
        :type trigger: `pyowm.alertapi30.trigger.Trigger`
        :returns: `None` if deletion is successful, an exception otherwise
        """
        assert trigger is not None
        assert isinstance(trigger.id, str), "Value must be a string"
        status, _ = self.http_client.delete(
            NAMED_TRIGGER_URI % trigger.id,
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})

    # ALERTS methods

    def get_alerts_for(self, trigger):
        """
        Retrieves all of the alerts that were fired for the specified Trigger
        :param trigger: the trigger
        :type trigger: `pyowm.alertapi30.trigger.Trigger`
        :return: list of `pyowm.alertapi30.alert.Alert` objects
        """
        assert trigger is not None
        assert isinstance(trigger.id, str), "Value must be a string"
        status, data = self.http_client.get_json(
            ALERTS_URI % trigger.id,
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})
        return [Alert.from_dict(item) for item in data]

    def get_alert(self, alert_id, trigger):
        """
        Retrieves info about the alert record on the Alert API that has the specified ID and belongs to the specified
        parent Trigger object
        :param trigger: the parent trigger
        :type trigger: `pyowm.alertapi30.trigger.Trigger`
        :param alert_id: the ID of the alert
        :type alert_id `pyowm.alertapi30.alert.Alert`
        :return: an `pyowm.alertapi30.alert.Alert` instance
        """
        assert trigger is not None
        assert alert_id is not None
        assert isinstance(alert_id, str), "Value must be a string"
        assert isinstance(trigger.id, str), "Value must be a string"
        status, data = self.http_client.get_json(
            NAMED_ALERT_URI % (trigger.id, alert_id),
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})
        return Alert.from_dict(data)

    def delete_all_alerts_for(self, trigger):
        """
        Deletes all of the alert that were fired for the specified Trigger
        :param trigger: the trigger whose alerts are to be cleared
        :type trigger: `pyowm.alertapi30.trigger.Trigger`
        :return: `None` if deletion is successful, an exception otherwise
        """
        assert trigger is not None
        assert isinstance(trigger.id, str), "Value must be a string"
        status, _ = self.http_client.delete(
            ALERTS_URI % trigger.id,
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})

    def delete_alert(self, alert):
        """
        Deletes the specified alert from the Alert API
        :param alert: the alert to be deleted
        :type alert: pyowm.alertapi30.alert.Alert`
        :return: ``None`` if the deletion was successful, an error otherwise
        """
        assert alert is not None
        assert isinstance(alert.id, str), "Value must be a string"
        assert isinstance(alert.trigger_id, str), "Value must be a string"
        status, _ = self.http_client.delete(
            NAMED_ALERT_URI % (alert.trigger_id, alert.id),
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)