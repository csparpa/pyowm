

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
    :returns:  an *AlertChannel* instance

    """
    def __init__(self, name):
        self.name = name


class AlertChannelsEnum:
    """
    Allowed alert channels

    """
    OWM_API = AlertChannel('OWM API')

    def items(self):
        """
        All values for this enum
        :return: list of tuples

        """
        return [
            ('OWM_API', self.OWM_API)
        ]