#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from pyowm import owm
from pyowm.agroapi10.polygon import Polygon, GeoPolygon


class IntegrationTestsPolygonsAPISubset(unittest.TestCase):

    __owm = owm.OWM(os.getenv('OWM_API_KEY', None))

    def test_polygons_CRUD(self):

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
        pol1 = mgr.create_polygon(geopol1, 'polygon_1')

        # create pol2
        geopol2 = GeoPolygon([[
            [-141.1958, 27.6683],
            [-141.1779, 27.6687],
            [-141.1773, 27.6792],
            [-141.1958, 27.6792],
            [-141.1958, 27.6683]
        ]])
        pol2 = mgr.create_polygon(geopol2, 'polygon_2')

        # Read all
        polygons = mgr.get_polygons()
        self.assertEqual(n_old_polygons + 2, len(polygons))
        self.assertTrue(all([isinstance(p, Polygon) for p in polygons]))

        # Read one by one
        result = mgr.get_polygon(pol1.id)
        self.assertEqual(pol1.id, result.id)
        self.assertEqual(pol1.name, pol1.name)
        self.assertEqual(pol1.area, result.area)
        self.assertEqual(pol1.user_id, result.user_id)
        self.assertEqual(pol1.center.lon, result.center.lon)
        self.assertEqual(pol1.center.lat, result.center.lat)
        self.assertEqual(pol1.geopolygon.geojson(), result.geopolygon.geojson())

        result = mgr.get_polygon(pol2.id)
        self.assertEqual(pol2.id, result.id)
        self.assertEqual(pol2.name, result.name)
        self.assertEqual(pol2.area, result.area)
        self.assertEqual(pol2.user_id, result.user_id)
        self.assertEqual(pol2.center.lon, result.center.lon)
        self.assertEqual(pol2.center.lat, result.center.lat)
        self.assertEqual(pol2.geopolygon.geojson(), result.geopolygon.geojson())

        # Update a polygon
        pol2.name = 'a better name'
        mgr.update_polygon(pol2)
        result = mgr.get_polygon(pol2.id)
        self.assertEqual(pol2.id, result.id)
        self.assertEqual(pol2.area, result.area)
        self.assertEqual(pol2.user_id, result.user_id)
        self.assertEqual(pol2.center.lon, result.center.lon)
        self.assertEqual(pol2.center.lat, result.center.lat)
        self.assertEqual(pol2.geopolygon.geojson(), result.geopolygon.geojson())
        self.assertNotEqual(pol2.name, pol1.name)  # of course, the name has changed

        # Delete polygons one by one
        mgr.delete_polygon(pol1)
        polygons = mgr.get_polygons()
        self.assertEqual(n_old_polygons + 1, len(polygons))

        mgr.delete_polygon(pol2)
        polygons = mgr.get_polygons()
        self.assertEqual(n_old_polygons, len(polygons))


if __name__ == "__main__":
    unittest.main()

