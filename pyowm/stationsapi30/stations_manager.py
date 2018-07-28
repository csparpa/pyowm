"""
Object that can read/write meteostations metadata and extract related
measurements
"""

from pyowm.commons.http_client import HttpClient
from pyowm.stationsapi30.parsers.station_parser import StationParser
from pyowm.stationsapi30.parsers.aggregated_measurement_parser import AggregatedMeasurementParser
from pyowm.stationsapi30.uris import STATIONS_URI, NAMED_STATION_URI, MEASUREMENTS_URI
from pyowm.constants import STATIONS_API_VERSION


class StationsManager(object):

    """
    A manager objects that provides a full interface to OWM Stations API. Mainly
    it implements CRUD methods on Station entities and the corresponding
    measured datapoints.

    :param API_key: the OWM web API key
    :type API_key: str
    :returns: a *StationsManager* instance
    :raises: *AssertionError* when no API Key is provided

    """

    def __init__(self, API_key):
        assert API_key is not None, 'You must provide a valid API Key'
        self.API_key = API_key
        self.stations_parser = StationParser()
        self.aggregated_measurements_parser = AggregatedMeasurementParser()
        self.http_client = HttpClient()

    def stations_api_version(self):
        return STATIONS_API_VERSION

    # STATIONS Methods

    def get_stations(self):
        """
        Retrieves all of the user's stations registered on the Stations API.

        :returns: list of *pyowm.stationsapi30.station.Station* objects

        """

        status, data = self.http_client.get_json(
            STATIONS_URI,
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
            NAMED_STATION_URI % str(id),
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
            STATIONS_URI,
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
            NAMED_STATION_URI % str(station.id),
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
            NAMED_STATION_URI % str(station.id),
            params={'appid': self.API_key},
            headers={'Content-Type': 'application/json'})

    # Measurements-related methods

    def send_measurement(self, measurement):
        """
        Posts the provided Measurement object's data to the Station API.

        :param measurement: the *pyowm.stationsapi30.measurement.Measurement*
          object to be posted
        :type measurement: *pyowm.stationsapi30.measurement.Measurement* instance
        :returns: `None` if creation is successful, an exception otherwise
        """
        assert measurement is not None
        assert measurement.station_id is not None
        status, _ = self.http_client.post(
            MEASUREMENTS_URI,
            params={'appid': self.API_key},
            data=[measurement.to_dict()],
            headers={'Content-Type': 'application/json'})

    def send_measurements(self, list_of_measurements):
        """
        Posts data about the provided list of Measurement objects to the
        Station API. The objects may be related to different station IDs.

        :param list_of_measurements: list of *pyowm.stationsapi30.measurement.Measurement*
          objects to be posted
        :type list_of_measurements: list of *pyowm.stationsapi30.measurement.Measurement*
          instances
        :returns: `None` if creation is successful, an exception otherwise
        """
        assert list_of_measurements is not None
        assert all([m.station_id is not None for m in list_of_measurements])
        msmts = [m.to_dict() for m in list_of_measurements]
        status, _ = self.http_client.post(
            MEASUREMENTS_URI,
            params={'appid': self.API_key},
            data=msmts,
            headers={'Content-Type': 'application/json'})

    def get_measurements(self, station_id, aggregated_on, from_timestamp,
                         to_timestamp, limit=100):
        """
        Reads measurements of a specified station recorded in the specified time
        window and aggregated on minute, hour or day. Optionally, the number of
        resulting measurements can be limited.

        :param station_id: unique station identifier
        :type station_id: str
        :param aggregated_on: aggregation time-frame for this measurement
        :type aggregated_on: string between 'm','h' and 'd'
        :param from_timestamp: Unix timestamp corresponding to the beginning of
          the time window
        :type from_timestamp: int
        :param to_timestamp: Unix timestamp corresponding to the end of the
          time window
        :type to_timestamp: int
        :param limit: max number of items to be returned. Defaults to 100
        :type limit: int
        :returns: list of *pyowm.stationsapi30.measurement.AggregatedMeasurement*
          objects
        """
        assert station_id is not None
        assert aggregated_on is not None
        assert from_timestamp is not None
        assert from_timestamp > 0
        assert to_timestamp is not None
        assert to_timestamp > 0
        if to_timestamp < from_timestamp:
            raise ValueError("End timestamp can't be earlier than begin timestamp")
        assert isinstance(limit, int)
        assert limit >= 0
        query = {'appid': self.API_key,
                 'station_id': station_id,
                 'type': aggregated_on,
                 'from': from_timestamp,
                 'to': to_timestamp,
                 'limit': limit}
        status, data = self.http_client.get_json(
            MEASUREMENTS_URI,
            params=query,
            headers={'Content-Type': 'application/json'})
        return [self.aggregated_measurements_parser.parse_dict(item) for item in data]

    def send_buffer(self, buffer):
        """
        Posts to the Stations API data about the Measurement objects contained
        into the provided Buffer instance.

        :param buffer: the *pyowm.stationsapi30.buffer.Buffer* instance whose
          measurements are to be posted
        :type buffer: *pyowm.stationsapi30.buffer.Buffer* instance
        :returns: `None` if creation is successful, an exception otherwise
        """
        assert buffer is not None
        msmts = []
        for x in buffer.measurements:
            m = x.to_dict()
            item = dict()
            item['station_id'] = m['station_id']
            item['dt'] = m['timestamp']
            item['temperature'] = m['temperature']
            item['wind_speed'] = m['wind_speed']
            item['wind_gust'] = m['wind_gust']
            item['wind_deg'] = m['wind_deg']
            item['pressure'] = m['pressure']
            item['humidity'] = m['humidity']
            item['rain_1h'] = m['rain_1h']
            item['rain_6h'] = m['rain_6h']
            item['rain_24h'] = m['rain_24h']
            item['snow_1h'] = m['snow_1h']
            item['snow_6h'] = m['snow_6h']
            item['snow_24h'] = m['snow_24h']
            item['dew_point'] = m['dew_point']
            item['humidex'] = m['humidex']
            item['heat_index'] = m['heat_index']
            item['visibility_distance'] = m['visibility_distance']
            item['visibility_prefix'] = m['visibility_prefix']
            item['clouds'] = [dict(distance=m['clouds_distance']),
                              dict(condition=m['clouds_condition']),
                              dict(cumulus=m['clouds_cumulus'])]
            item['weather'] = [
                dict(precipitation=m['weather_precipitation']),
                dict(descriptor=m['weather_descriptor']),
                dict(intensity=m['weather_intensity']),
                dict(proximity=m['weather_proximity']),
                dict(obscuration=m['weather_obscuration']),
                dict(other=m['weather_other'])]
            msmts.append(item)
        status, _ = self.http_client.post(
            MEASUREMENTS_URI,
            params={'appid': self.API_key},
            data=msmts,
            headers={'Content-Type': 'application/json'})
