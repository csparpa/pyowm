#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch

from pyowm.stationsapi30.measurement import Measurement
from pyowm.stationsapi30.persistence_backend import JSONPersistenceBackend
from pyowm.stationsapi30.buffer import Buffer


class TestJSONPersistenceBackend(unittest.TestCase):
    file = 'file'
    test_id = 'test_id'
    test_timestamp = 1468274766

    def test_init(self):
        with patch('os.path.isfile', return_value=True):
            test_instance = JSONPersistenceBackend(self.file, self.test_id)
            self.assertEqual(test_instance._file_path, self.file)
            self.assertEqual(test_instance._station_id, self.test_id)

        # None json_file_path
        with patch('os.path.isfile', return_value=True):
            with self.assertRaises(AssertionError):
                JSONPersistenceBackend(None, self.test_id)

        # json_file_path is not file
        with patch('os.path.isfile', return_value=False):
            with self.assertRaises(AssertionError):
                JSONPersistenceBackend(self.file, self.test_id)

    def test_load_to_buffer(self):
        with patch('os.path.isfile', return_value=True):
            mocked_file_data = '[{"station_id": "test_id", "timestamp":142332322}]'
            with patch('builtins.open', unittest.mock.mock_open(read_data=mocked_file_data)) as mocked_open:
                test_instance = JSONPersistenceBackend(self.file, self.test_id)
                test_instance.load_to_buffer()
                mocked_open.assert_called_once_with(self.file, 'r')

            with self.assertRaises(ValueError):
                test_instance._station_id = None
                test_instance.load_to_buffer()

    def test_persist_buffer(self):
        with patch('os.path.isfile', return_value=True):
            mocked_file_data = '[{"station_id": "test_id", "timestamp":142332322}]'
            with patch('builtins.open', unittest.mock.mock_open(read_data=mocked_file_data)) as mocked_open:
                test_instance = JSONPersistenceBackend(self.file, self.test_id)
                test_buffer = Buffer(self.test_id)
                test_measurement = Measurement(self.test_id, self.test_timestamp)
                test_buffer.measurements = [test_measurement]
                test_instance.persist_buffer(test_buffer)
                mocked_open.assert_called_once_with(self.file, 'w')
