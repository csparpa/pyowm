from pyowm.alertapi30.alert import AlertChannel


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