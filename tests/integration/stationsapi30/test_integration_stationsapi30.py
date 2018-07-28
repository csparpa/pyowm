import unittest
import os
import copy
from pyowm.constants import DEFAULT_API_KEY
from pyowm.webapi25.configuration25 import parsers
from pyowm.webapi25.owm25 import OWM25
from pyowm.stationsapi30.buffer import Buffer


class IntegrationTestsStationsAPI30(unittest.TestCase):

    __owm = OWM25(parsers, os.getenv('OWM_API_KEY', DEFAULT_API_KEY))

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

        # create and bufferize some measurements for station n.1
        buf = Buffer(stat1.id)
        buf.append_from_dict(dict(station_id=stat1.id, timestamp=1505231630,
                        temperature=100, wind_speed=2.1,
                        wind_gust=67, humidex=77))
        buf.append_from_dict(dict(station_id=stat1.id, timestamp=1505415230,
                        temperature=100, wind_speed=2.1,
                        wind_gust=67, humidex=77))
        buf.append_from_dict(dict(station_id=stat1.id, timestamp=1505429694,
                        temperature=100, wind_speed=2.1,
                        wind_gust=67, humidex=77))
        mgr.send_buffer(buf)
        buf.empty()

        # read the measurements for station 1
        msmts = mgr.get_measurements(stat1.id, 'd', 1505200000, 1505430000)
        for m in msmts:
            self.assertEquals(m.station_id, stat1.id)

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


if __name__ == "__main__":
    unittest.main()