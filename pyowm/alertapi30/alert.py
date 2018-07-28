from pyowm.utils import timeformatutils, stringutils


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
        stringutils.assert_is_string_or_unicode(id)
        self.id = id

        assert trigger_id is not None
        stringutils.assert_is_string_or_unicode(trigger_id)
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

    def __repr__(self):
        return "<%s.%s - id=%s, trigger id=%s, last update=%s>" % (
                    __name__,
                    self.__class__.__name__,
                    self.id,
                    self.trigger_id,
                    timeformatutils.to_ISO8601(self.last_update))
