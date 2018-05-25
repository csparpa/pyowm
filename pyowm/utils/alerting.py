from pyowm.utils import timeformatutils


class WeatherParametersEnum:
    """
    Allowed weather parameters for condition checking

    """
    TEMPERATURE = 'temp'  # Kelvin
    PRESSURE = 'pressure'
    HUMIDITY = 'humidity'
    WIND_SPEED = 'wind_speed'
    WIND_DIRECTION = 'wind_direction'
    CLOUDS = 'clouds'  # Coverage %

    def items(self):
        """
        All values for this enum
        :return: list of tuples

        """
        return [
            ('TEMPERATURE', self.TEMPERATURE),
            ('PRESSURE', self.PRESSURE),
            ('HUMIDITY', self.HUMIDITY),
            ('WIND_SPEED', self.WIND_SPEED),
            ('WIND_DIRECTION', self.WIND_DIRECTION),
            ('CLOUDS', self.CLOUDS)
        ]


class OperatorsEnum:
    """
    Allowed comparison operators for condition checking upon weather parameters

    """
    GREATER_THAN = '$gt'
    GREATER_THAN_EQUAL = '$gte'
    LESS_THAN = '$lt'
    LESS_THAN_EQUAL = '$lte'
    EQUAL = '$eq'
    NOT_EQUAL = '$ne'

    def items(self):
        """
        All values for this enum
        :return: list of tuples

        """
        return [
            ('GREATER_THAN', self.GREATER_THAN),
            ('GREATER_THAN_EQUAL', self.GREATER_THAN_EQUAL),
            ('LESS_THAN', self.LESS_THAN),
            ('LESS_THAN_EQUAL', self.LESS_THAN_EQUAL),
            ('EQUAL', self.EQUAL),
            ('NOT_EQUAL', self.NOT_EQUAL)
        ]


class Condition:
    """
    Object representing a condition to be checked on a specific weather parameter. A condition is given when comparing
    the weather parameter against a numerical value with respect to an operator.
    Allowed weather params and operators are specified by the `pyowm.utils.alerting.WeatherParametersEnum` and
    `pyowm.utils.alerting.OperatorsEnum` enumerator classes.
    :param weather_param: the weather variable to be checked (eg. TEMPERATURE, CLOUDS, ...)
    :type weather_param: str
    :param operator: the comparison operator to be applied to the weather variable (eg. GREATER_THAN, EQUAL, ...)
    :type operator: str
    :param amount: comparison value
    :type amount: int or float
    :param id: optional unique ID for this Condition instance
    :type id: str
    :returns:  a *Condition* instance
    :raises: *ValueError* when either the weather param has wrong type or is not allowed, or the operator has wrong type
    or is not allowed, or the amount has wrong type

    """
    def __init__(self, weather_param, operator, amount, id=None):
        assert isinstance(weather_param, str)
        try:
            self.weather_param = getattr(WeatherParametersEnum, weather_param.upper())
        except AttributeError as e:
            raise ValueError(e)

        assert isinstance(operator, str)
        try:
            self.operator = getattr(OperatorsEnum, operator.upper())
        except AttributeError as e:
            raise ValueError(e)

        assert amount is not None
        assert isinstance(amount, int) or isinstance(amount, float)
        self.amount = amount
        self.id = id


class AlertChannel:
    """
    Base class representing a channel through which one can acknowledge that a weather alert has been issued.
    Examples: OWM API polling, push notifications, email notifications, etc.
    This feature is yet to be implemented by the OWM API.
    :param name: name of the channel
    :type name: str
    :returns:  an *AlertChannel* instance

    """
    def __init__(self, name):
        self.name = name


class AlertChannelsEnum:
    """
    Allowed alert channels

    """
    OWM_API_POLLING = AlertChannel('OWM API POLLING')

    def items(self):
        """
        All values for this enum
        :return: list of tuples

        """
        return [
            ('OWM_API_POLLING', self.OWM_API_POLLING)
        ]


class Trigger:
    """
    Object representing a the check if a set of weather conditions are met on a given geographical area: each condition
    is a rule on the value of a given weather parameter (eg. humidity, temperature, etc). Whenever a condition from a
    `Trigger` is met, the OWM API crates an alert and binds it to the the `Trigger`.
    A `Trigger` is the local proxy for the corresponding entry on the OWM API, therefore it can get ouf of sync as
    time goes by and conditions are met: it's up to you to "refresh" the local trigger by using a
    `pyowm.utils.alerting.AlertManager` instance.
    :param start: time object representing the time when the trigger begins to be checked
    :type start: int, ``datetime.datetime`` or ISO8601-formatted string
    :param end: time object representing the time when the trigger ends to be checked
    :type end: int, ``datetime.datetime`` or ISO8601-formatted string
    :param alerts: the `Alert` objects representing the alerts that have been fired for this `Trigger` so far. Defaults
    to `None`
    :type alerts: list of `pyowm.utils.alerting.Alert` instances
    :param conditions: the `Condition` objects representing the set of checks to be done on weather variables
    :type conditions: list of `pyowm.utils.alerting.Condition` instances
    :param area: the geographic are over which conditions are checked: it can be composed by multiple geoJSON types
    :type area: list of geoJSON types (str)
    :param alert_channels: the alert channels through which alerts originating from this `Trigger` can be consumed.
    Defaults to OWM API polling
    :type alert_channels: list of `pyowm.utils.alerting.AlertChannel` instances
    :param id: optional unique ID for this `Trigger` instance
    :type id: str
    :returns:  a *Trigger* instance
    :raises: *ValueError* when start or end epochs are `None` or when end precedes start or when conditions or area
    are empty collections

    """
    def __init__(self, start, end, conditions, area, alerts=None, alert_channels=None, id=None):
        assert start is not None
        assert end is not None
        unix_start = timeformatutils.to_UNIXtime(start)
        unix_end = timeformatutils.to_UNIXtime(end)
        if unix_start >= unix_end:
            raise ValueError("Error: the start epoch must precede the end epoch")
        self.start = unix_start
        self.end = unix_end
        assert conditions is not None
        if len(conditions) == 0:
            raise ValueError('A trigger must contain at least one condition: you provided none')
        assert area is not None
        if len(area) == 0:
            raise ValueError('The area for a trigger must contain at least one geoJSON type: you provided none')
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
        return self.alerts

    def get_alert(self, alert_id):
        for alert in self.alerts:
            if alert.id == alert_id:
                return alert
        return None