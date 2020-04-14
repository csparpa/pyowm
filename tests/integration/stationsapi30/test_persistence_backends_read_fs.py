#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import tempfile
import json
from pyowm.stationsapi30.measurement import Measurement
from pyowm.stationsapi30.buffer import Buffer
from pyowm.stationsapi30.persistence_backend import JSONPersistenceBackend


class TestJSONPersistenceBackendsReadFS(unittest.TestCase):

    basepath = os.path.dirname(os.path.abspath(__file__))
    data_dict = dict(station_id='mytest', timestamp=1378459200,
                       temperature=dict(min=0, max=100), wind_speed=2.1,
                       wind_gust=67, humidex=77, weather_other=dict(key='val'))
    measurement = Measurement.from_dict(data_dict)

    def test_json_persistence_backend_with_no_station_id_specified(self):
        be = JSONPersistenceBackend(
            self.basepath + os.sep + 'measurements.json', None)
        with self.assertRaises(ValueError):
            be.load_to_buffer()

    def test_json_persistence_backend_reads(self):
        be = JSONPersistenceBackend(
            self.basepath + os.sep + 'measurements.json', 'mytest')
        buf = be.load_to_buffer()
        self.assertTrue(3, len(buf))
        for item in buf:
            self.assertTrue(isinstance(item, Measurement))

    def test_json_persistence_backend_writes(self):
        with tempfile.NamedTemporaryFile() as tmp:
            # write file
            target_file = os.path.abspath(tmp.name)
            be = JSONPersistenceBackend(target_file, 'mytest')
            buffer = Buffer('mytest')
            buffer.append(self.measurement)
            be.persist_buffer(buffer)

            # check data
            with open(target_file, 'r') as f:
                data = f.read()
                items = json.loads(data)
                self.assertEqual(1, len(items))
                msmt = items[0]
                self.assertTrue(all(item in msmt.items()
                                    for item in self.data_dict.items()))


if __name__ == "__main__":
    unittest.main()

