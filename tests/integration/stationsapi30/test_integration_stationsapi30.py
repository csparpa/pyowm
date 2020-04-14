#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import copy
from pyowm import owm
from pyowm.stationsapi30.buffer import Buffer
from pyowm.stationsapi30.measurement import Measurement


class IntegrationTestsStationsAPI30(unittest.TestCase):

    __owm = owm.OWM(os.getenv('OWM_API_KEY', None))

    def test_stations_CRUD(self):

        mgr = self.__owm.stations_manager()

        # check if any previous station exists on this account
        n_old_stations = len(mgr.get_stations())

        # create stat1
        stat1 = mgr.create_station('PYOWM1', 'pyowm_test_station_1',
                                   45.0, 9.0, 189.0)

        # create stat2
        stat2 = mgr.create_station('PYOWM2', 'pyowm_test_station_2',
                                   46.0, 18.0, 50.0)

        # Read all
        stations = mgr.get_stations()
        self.assertEqual(n_old_stations + 2, len(stations))

        # Read one by one
        result = mgr.get_station(stat1.id)
        self.assertEqual(stat1.id, result.id)
        self.assertEqual(stat1.external_id, result.external_id)
        self.assertEqual(stat1.name, result.name)
        self.assertEqual(stat1.lat, result.lat)
        self.assertEqual(stat1.lon, result.lon)
        self.assertEqual(stat1.alt, result.alt)

        result = mgr.get_station(stat2.id)
        self.assertEqual(stat2.id, result.id)
        self.assertEqual(stat2.external_id, result.external_id)
        self.assertEqual(stat2.name, result.name)
        self.assertEqual(stat2.lat, result.lat)
        self.assertEqual(stat2.lon, result.lon)
        self.assertEqual(stat2.alt, result.alt)

        # Update a station
        modified_stat2 = copy.deepcopy(stat2)
        modified_stat2.eternal = 'modified_pyowm_test_station_2'
        modified_stat2.lat = 30.6
        mgr.update_station(modified_stat2)
        result = mgr.get_station(modified_stat2.id)
        self.assertEqual(modified_stat2.id, result.id)
        self.assertEqual(modified_stat2.external_id, result.external_id)
        self.assertEqual(modified_stat2.name, result.name)
        # of course, lat had been modified
        self.assertEqual(modified_stat2.lon, result.lon)
        self.assertEqual(modified_stat2.alt, result.alt)

        # Delete stations one by one
        mgr.delete_station(stat1)
        stations = mgr.get_stations()
        self.assertEqual(n_old_stations + 1, len(stations))

        mgr.delete_station(modified_stat2)
        stations = mgr.get_stations()
        self.assertEqual(n_old_stations, len(stations))

    def test_measurements_and_buffers(self):
        mgr = self.__owm.stations_manager()

        # check if any previous station exists on this account
        n_old_stations = len(mgr.get_stations())

        # create station
        test_station = mgr.create_station('PYOWM_TEST_BUFFERS', 'pyowm_test_buffers', 45.0, 9.0, 189.0)

        # create and bufferize some measurements for the test station
        buf = Buffer(test_station.id)
        buf.append_from_dict(dict(station_id=test_station.id, timestamp=1505231630,
                        temperature=100, wind_speed=2.1,
                        wind_gust=67, humidex=77))
        buf.append_from_dict(dict(station_id=test_station.id, timestamp=1505429694,
                        temperature=100, wind_speed=2.1,
                        wind_gust=67, humidex=77))
        mgr.send_buffer(buf)

        # now directly send measurements
        measurement = Measurement.from_dict(dict(station_id=test_station.id, timestamp=1505415230,
                        temperature=100, wind_speed=2.1,
                        wind_gust=67, humidex=77))
        measurements_list = [
            Measurement.from_dict(dict(station_id=test_station.id, timestamp=1505315230,
                        temperature=100, wind_speed=2.1,
                        wind_gust=67, humidex=77))
        ]
        mgr.send_measurement(measurement)
        mgr.send_measurements(measurements_list)

        # read the measurements for station
        msmts = mgr.get_measurements(test_station.id, 'd', 1505200000, 1505430000)
        for m in msmts:
            self.assertEqual(test_station.id, m.station_id)
            self.assertEqual('d', m.aggregated_on)

        # Delete stations one by one
        mgr.delete_station(test_station)
        stations = mgr.get_stations()
        self.assertEqual(n_old_stations, len(stations))


if __name__ == "__main__":
    unittest.main()

