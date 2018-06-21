"""
URIs templates for resources exposed by the Alert API 3.0
"""

ROOT_ALERT_API_URL = 'http://api.openweathermap.org/data/3.0'

# Triggers
TRIGGERS_URI = ROOT_ALERT_API_URL + '/triggers'
NAMED_TRIGGER_URI = ROOT_ALERT_API_URL + '/triggers/%s'

# Alerts
ALERTS_URI = ROOT_ALERT_API_URL + '/triggers/%s/history'
NAMED_ALERT_URI = ROOT_ALERT_API_URL + '/triggers/%s/history/%s'
