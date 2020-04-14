#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.alertapi30.condition import Condition
from pyowm.commons import exceptions
from pyowm.utils import formatting


class AlertChannel:
    """
    Base class representing a channel through which one can acknowledge that a weather alert has been issued.
    Examples: OWM API polling, push notifications, email notifications, etc.
    This feature is yet to be implemented by the OWM API.
    :param name: name of the channel
    :type name: str
    :returns: an *AlertChannel* instance

    """
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return dict(name=self.name)

    def __repr__(self):
        return '<%s.%s - name: %s>' % (__name__, self.__class__.__name__, self.name)


class Alert:
    """
    Represents the situation happening when any of the conditions bound to a `Trigger` is met. Whenever this happens, an
    `Alert` object is created (or updated) and is bound to its parent `Trigger`. The trigger can then be polled to check
    what alerts have been fired on it.
    :param id: unique alert identifier
    :type name: str
    :param trigger_id: link back to parent `Trigger`
    :type trigger_id: str
    :param met_conditions: list of dict, each one referring to a `Condition` obj bound to the parent `Trigger` and reporting
    the actual measured values that made this `Alert` fire
    :type met_conditions: list of dict
    :param coordinates: dict representing the geocoordinates where the `Condition` triggering the `Alert` was met
    :type coordinates: dict
    :param last_update: epoch of the last time when this `Alert` has been fired
    :type last_update: int

    """
    def __init__(self, id, trigger_id, met_conditions, coordinates, last_update=None):
        assert id is not None
        assert isinstance(id, str), "Value must be a string"
        self.id = id

        assert trigger_id is not None
        assert isinstance(trigger_id, str), "Value must be a string"
        self.trigger_id = trigger_id

        assert met_conditions is not None
        assert isinstance(met_conditions, list)
        self.met_conditions = met_conditions

        assert coordinates is not None
        assert isinstance(coordinates, dict)
        self.coordinates = coordinates

        if last_update is not None:
            assert isinstance(last_update, int)
        self.last_update = last_update

    @classmethod
    def from_dict(cls, the_dict):
        """
        Parses a *Alert* instance out of a data dictionary. Only certain properties of the data dictionary
        are used: if these properties are not found or cannot be parsed, an exception is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: a *Alert* instance or ``None`` if no data is available
        :raises: *ParseAPIResponseError* if it is impossible to find or parse the data needed to build the result

        """
        if the_dict is None:
            raise exceptions.ParseAPIResponseError('Data is None')
        try:
            alert_id = the_dict['_id']
            t = the_dict['last_update'].split('.')[0].replace('T', ' ') + '+00'
            alert_last_update = formatting.ISO8601_to_UNIXtime(t)
            alert_trigger_id = the_dict['triggerId']
            alert_met_conds = [
                dict(current_value=c['current_value']['min'], condition=Condition.from_dict(c['condition']))
                    for c in the_dict['conditions']
            ]
            alert_coords = the_dict['coordinates']
            return Alert(alert_id, alert_trigger_id, alert_met_conds, alert_coords, last_update=alert_last_update)
        except ValueError as e:
            raise exceptions.ParseAPIResponseError('Impossible to parse JSON: %s' % e)
        except KeyError as e:
            raise exceptions.ParseAPIResponseError('Impossible to parse JSON: %s' % e)

    def to_dict(self):
        """Dumps object to a dictionary

        :returns: a `dict`

        """
        return {
            'id': self.id,
            'trigger_id': self.trigger_id,
            'met_conditions': self.met_conditions,
            'coordinates': self.coordinates,
            'last_update': self.last_update}

    def __repr__(self):
        return "<%s.%s - id=%s, trigger id=%s, last update=%s>" % (
            __name__,
            self.__class__.__name__,
            self.id,
            self.trigger_id,
            formatting.to_ISO8601(self.last_update))
