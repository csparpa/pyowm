import unittest
import os
from pyowm.constants import DEFAULT_API_KEY
from pyowm.weatherapi25.owm25 import OWM25
from pyowm.weatherapi25.configuration25 import parsers
from pyowm.agroapi10.polygon import Polygon, GeoPolygon
from pyowm.agroapi10.soil import Soil


class IntegrationTestsSoilData(unittest.TestCase):

    __owm = OWM25(parsers, os.getenv('OWM_API_KEY', DEFAULT_API_KEY))

    def test_call_soil_data(self):

        mgr = self.__owm.agro_manager()

        # check if any previous polygon exists on this account
        n_old_polygons = len(mgr.get_polygons())

        # create pol1
        geopol1 = GeoPolygon([[
            [-121.1958, 37.6683],
            [-121.1779, 37.6687],
            [-121.1773, 37.6792],
            [-121.1958, 37.6792],
            [-121.1958, 37.6683]
        ]])
        test_pol = mgr.create_polygon(geopol1, 'soil_data_test_pol')

        soil = mgr.soil_data(test_pol)

        self.assertTrue(isinstance(soil, Soil))
        self.assertEqual(test_pol.id, soil.polygon_id)

        # Delete test polygon
        mgr.delete_polygon(test_pol)
        polygons = mgr.get_polygons()
        self.assertEqual(n_old_polygons, len(polygons))


if __name__ == "__main__":
    unittest.main()

