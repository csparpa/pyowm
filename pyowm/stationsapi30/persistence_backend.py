#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from abc import ABCMeta, abstractmethod
from pyowm.stationsapi30.buffer import Buffer


class PersistenceBackend:   # pragma: no cover

    """
    A global abstract class representing an I/O manager for buffer objects containing
    raw measurements.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def load_to_buffer(self):
        """
        Reads meteostation measurement data into a *pyowm.stationsapi30.buffer.Buffer*
        object.

        :returns: a *pyowm.stationsapi30.buffer.Buffer* instance

        """
        pass

    @abstractmethod
    def persist_buffer(self, buffer):
        """
        Saves data contained into a *pyowm.stationsapi30.buffer.Buffer* object
        in a durable form.

        :param buffer: the Buffer object to be persisted
        :type buffer:  *pyowm.stationsapi30.buffer.Buffer* instance

        """
        pass

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)


class JSONPersistenceBackend(PersistenceBackend):

    """
    A `PersistenceBackend` loading/saving data to a JSON file. Data will be
    saved as a JSON list, each element being representing data of a
    *pyowm.stationsapi30.measurement.Measurement* object.

    :param json_file_path: path to the JSON file
    :type json_file_path: str
    :param station_id: unique OWM-provided ID of the station whose data is read/saved
    :type station_id: str
    """

    _file_path = None
    _station_id = None

    def __init__(self, json_file_path, station_id):
        assert json_file_path is not None
        self._station_id = station_id
        assert os.path.isfile(json_file_path)
        self._file_path = json_file_path

    def load_to_buffer(self):
        if self._station_id is None:
            raise ValueError('No station ID specified')
        result = Buffer(self._station_id)
        with open(self._file_path, 'r') as f:
            list_of_dicts = json.load(f)
            for _dict in list_of_dicts:
                result.append_from_dict(_dict)
            return result

    def persist_buffer(self, buffer):
        with open(self._file_path, 'w') as f:
            data = [msmt.to_JSON() for msmt in buffer]
            f.write('[%s]' % ','.join(data))
