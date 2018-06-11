class AlertManager:

    def __init__(self):
        raise NotImplementedError()

    def alert_api_version(self):
        raise NotImplementedError()

    # TRIGGER methods

    def create_trigger(self):
        raise NotImplementedError()

    def get_triggers(self):
        raise NotImplementedError()

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

