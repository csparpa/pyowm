"""
URIs templates for resources exposed by the Stations API 3.0
"""

ROOT_ALERT_API_URL = 'http://api.openweathermap.org/data/3.0'

# Stations
STATIONS_URI = ROOT_ALERT_API_URL + '/stations'
NAMED_STATION_URI = ROOT_ALERT_API_URL + '/stations/%s'

# Measurements
MEASUREMENTS_URI = ROOT_ALERT_API_URL + '/measurements'
