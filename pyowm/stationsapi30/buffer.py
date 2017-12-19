import json
import copy
from pyowm.stationsapi30.measurement import Measurement
from pyowm.utils import timeutils, timeformatutils


class Buffer:

    station_id = None
    created_at = None
    measurements = None

    def __init__(self, station_id):
        assert station_id is not None
        self.station_id = station_id
        self.created_at = timeutils.now(timeformat='unix')
        self.measurements = list()

    def creation_time(self, timeformat='unix'):
        """Returns the UTC time of creation of this aggregated measurement

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time, '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00`` or `date` for
            a ``datetime.datetime`` object
        :type timeformat: str
        :returns: an int or a str or a ``datetime.datetime`` object or None
        :raises: ValueError

        """
        if self.created_at is None:
            return None
        return timeformatutils.timeformat(self.created_at, timeformat)

    def append(self, measurement):
        """
        Appends the specified ``Measurement`` object to the buffer
        :param measurement: a ``measurement.Measurement`` instance

        """
        assert isinstance(measurement, Measurement)
        assert measurement.station_id == self.station_id
        self.measurements.append(measurement)

    def append_from_dict(self, the_dict):
        """
        Creates a ``measurement.Measurement`` object from the supplied dict
        and then appends it to the buffer
        :param the_dict: dict

        """
        m = Measurement.from_dict(the_dict)
        self.append(m)

    def append_from_json(self, json_string):
        """
        Creates a ``measurement.Measurement`` object from the supplied JSON string
        and then appends it to the buffer
        :param json_string: the JSON formatted string

        """
        a_dict = json.loads(json_string)
        self.append_from_dict(a_dict)

    def empty(self):
        """
        Drops all measurements of this buffer instance

        """
        self.measurements = list()

    def sort_chronologically(self):
        """
        Sorts the measurements of this buffer in chronological order

        """
        self.measurements.sort(key=lambda m: m.timestamp)

    def sort_reverse_chronologically(self):
        """
        Sorts the measurements of this buffer in reverse chronological order

        """
        self.measurements.sort(key=lambda m: m.timestamp, reverse=True)

    # Magic methods

    def __len__(self):
        return len(self.measurements)

    def __iter__(self):
        return (m for m in self.measurements)

    def __add__(self, other):
        assert all([i.station_id == self.station_id for i in other])
        result = copy.deepcopy(self)
        for m in other.measurements:
            result.append(m)
        return result

    def __contains__(self, measurement):
        return measurement in self.measurements

    def __repr__(self):
        return '<%s.%s - station_id=%s, n_samples=%s>' \
               % (__name__, self.__class__.__name__,
                  self.station_id, len(self))
