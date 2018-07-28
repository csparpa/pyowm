from pyowm.utils import stringutils


class Condition:
    """
    Object representing a condition to be checked on a specific weather parameter. A condition is given when comparing
    the weather parameter against a numerical value with respect to an operator.
    Allowed weather params and operators are specified by the `pyowm.utils.alertapi30.WeatherParametersEnum` and
    `pyowm.utils.alertapi30.OperatorsEnum` enumerator classes.
    :param weather_param: the weather variable to be checked (eg. TEMPERATURE, CLOUDS, ...)
    :type weather_param: str
    :param operator: the comparison operator to be applied to the weather variable (eg. GREATER_THAN, EQUAL, ...)
    :type operator: str
    :param amount: comparison value
    :type amount: int or float
    :param id: optional unique ID for this Condition instance
    :type id: str
    :returns:  a *Condition* instance
    :raises: *AssertionError* when either the weather param has wrong type or the operator has wrong type or the
    amount has wrong type

    """
    def __init__(self, weather_param, operator, amount, id=None):
        assert weather_param is not None
        stringutils.assert_is_string_or_unicode(weather_param)
        self.weather_param = weather_param

        assert operator is not None
        stringutils.assert_is_string_or_unicode(operator)
        self.operator = operator

        assert amount is not None
        assert isinstance(amount, int) or isinstance(amount, float)
        self.amount = amount
        self.id = id

    @classmethod
    def from_dict(cls, the_dict):
        assert isinstance(the_dict, dict)
        weather_param = the_dict['name']
        operator = the_dict['expression']
        amount = the_dict['amount']
        the_id = the_dict.get('_id', None)
        return Condition(weather_param, operator, amount, id=the_id)
