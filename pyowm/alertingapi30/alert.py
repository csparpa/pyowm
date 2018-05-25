
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