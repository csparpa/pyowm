"""
Object that can read/write meteostations metadata and extract related
measurements
"""

from pyowm.commons.http_client import HttpClient
from pyowm.stationsapi30.station_parser import StationParser


class StationsManager(object):

    STATIONS_API_VERSION = (3, 0, 0)

    """
    A manager objects that provides a full interface to OWM Stations API. Mainly
    it implements CRUD methods on Station entities and the corresponding
    measured datapoints.

    :param API_key: the OWM web API key (defaults to ``None``)
    :type API_key: str
    :returns: a *StationsManager* instance
    :raises: *AssertionError* when no API Key is provided

    """

    def __init__(self, API_key):
        assert API_key is not None, 'You must provide a valid API Key'
        self.API_key = API_key
        self.stations_parser = StationParser()
        self.http_client = HttpClient()

    def stations_api_version(self):
        return self.STATIONS_API_VERSION

    # STATIONS Methods

    def get_stations(self):
        """
        Retrieves all of the user's stations registered on the Stations API.

        :returns: list of *pyowm.stationsapi30.station.Station* objects

        """

        status, data = self.http_client.get_json(
            'http://api.openweathermap.org/data/3.0/stations',
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})
        return [self.stations_parser.parse_dict(item) for item in data]

    def get_station(self, id):
        """
        Retrieves a named station registered on the Stations API.

        :param id: the ID of the station
        :type id: str
        :returns: a *pyowm.stationsapi30.station.Station* object

        """
        status, data = self.http_client.get_json(
            'http://api.openweathermap.org/data/3.0/stations/%s' % str(id),
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})
        return self.stations_parser.parse_dict(data)

    def create_station(self, external_id, name, lat, lon, alt=None):
        """
        Create a new station on the Station API with the given parameters

        :param external_id: the user-given ID of the station
        :type external_id: str
        :param name: the name of the station
        :type name: str
        :param lat: latitude of the station
        :type lat: float
        :param lon: longitude of the station
        :type lon: float
        :param alt: altitude of the station
        :type alt: float
        :returns: the new *pyowm.stationsapi30.station.Station* object
        """
        assert external_id is not None
        assert name is not None
        assert lon is not None
        assert lat is not None
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        if alt is not None:
            if alt < 0.0:
                raise ValueError("'alt' value must not be negative")
        status, payload = self.http_client.post(
            'http://api.openweathermap.org/data/3.0/stations',
            params={'appid': self.API_key},
            data=dict(external_id=external_id, name=name, lat=lat,
                      lon=lon, alt=alt),
            headers={'Content-Type': 'application/json'})
        return self.stations_parser.parse_dict(payload)

    def update_station(self, station):
        """
        Updates the Station API record identified by the ID of the provided
        *pyowm.stationsapi30.station.Station* object with all of its fields

        :param station: the *pyowm.stationsapi30.station.Station* object to be updated
        :type station: *pyowm.stationsapi30.station.Station*
        :returns: `None` if update is successful, an exception otherwise
        """
        assert station.id is not None
        status, _ = self.http_client.put(
            'http://api.openweathermap.org/data/3.0/stations/%s' % str(station.id),
            params={'appid': self.API_key},
            data=dict(external_id=station.external_id, name=station.name,
                      lat=station.lat, lon=station.lon, alt=station.alt),
            headers={'Content-Type': 'application/json'})

    def delete_station(self, station):
        """
        Deletes the Station API record identified by the ID of the provided
        *pyowm.stationsapi30.station.Station*, along with all its related
        measurements

        :param station: the *pyowm.stationsapi30.station.Station* object to be deleted
        :type station: *pyowm.stationsapi30.station.Station*
        :returns: `None` if deletion is successful, an exception otherwise
        """
        assert station.id is not None
        status, _ = self.http_client.delete(
            'http://api.openweathermap.org/data/3.0/stations/%s' % str(station.id),
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})

    # Measurements-related methods

    def send_measurement(self, measurement):
        raise NotImplementedError()

    def send_measurements(self, list_of_raw_measurements):
        raise NotImplementedError()

    def get_measurements(self, station_id, interval, limit=None):
        raise NotImplementedError()

    def send_buffer(self, buffer):
        raise NotImplementedError()
