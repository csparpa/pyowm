from pyowm.constants import ALERT_API_VERSION
from pyowm.commons.http_client import HttpClient
from pyowm.alertapi30.parsers import TriggerParser
from pyowm.alertapi30.uris import TRIGGERS_URI


class AlertManager:

    """
    A manager objects that provides a full interface to OWM Alert API. It implements CRUD methods on Trigger entities
    and read/deletion of related Alert objects

    :param API_key: the OWM web API key
    :type API_key: str
    :returns: an *AlertManager* instance
    :raises: *AssertionError* when no API Key is provided

    """

    def __init__(self, API_key):
        assert API_key is not None, 'You must provide a valid API Key'
        self.API_key = API_key
        self.trigger_parser = TriggerParser()
        self.http_client = HttpClient()

    def alert_api_version(self):
        return ALERT_API_VERSION

    # TRIGGER methods

    def create_trigger(self):
        raise NotImplementedError()

    def get_triggers(self):
        """
        Retrieves all of the user's triggers that are set on the Weather Alert API.

        :returns: list of `pyowm.alertapi30.trigger.Trigger` objects

        """
        status, data = self.http_client.get_json(
            TRIGGERS_URI,
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})
        return [self.trigger_parser.parse_dict(item) for item in data]

    def get_trigger(self, trigger_id):
        raise NotImplementedError()

    def refresh_trigger(self, trigger):
        raise NotImplementedError()

    def update_trigger(self, trigger):
        raise NotImplementedError()

    def delete_trigger(self, trigger):
        raise NotImplementedError()

    # ALERTS methods

    def delete_all_alerts_for(self, trigger):
        raise NotImplementedError()

    def delete_alert_for(self, alert, trigger):
        raise NotImplementedError()

