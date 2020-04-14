#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pyowm.agroapi10.polygon import Polygon, GeoPoint, GeoPolygon


class TestPolygon(unittest.TestCase):

    geopoint= GeoPoint(34, -56.3)
    geopolygon = GeoPolygon([
        [[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]
    ])

    def test_polygon_fails_with_wrong_parameters(self):

        self.assertRaises(AssertionError, Polygon, None, 'polygon', self.geopolygon, self.geopoint, 123.4, 'user')
        self.assertRaises(AssertionError, Polygon, 'id', 'polygon', 'wrong', self.geopoint, 123.4, 'user')
        self.assertRaises(AssertionError, Polygon, None, 'polygon', self.geopolygon, 'wrong', 123.4, 'user')
        self.assertRaises(AssertionError, Polygon, None, 'polygon', self.geopolygon, self.geopoint, None, 'user')
        self.assertRaises(AssertionError, Polygon, None, 'polygon', self.geopolygon, self.geopoint, -77, 'user')

    def test_area_kilometers_property(self):
        area_hs = 456.78
        expected = area_hs * 0.01
        instance = Polygon('id', 'polygon', self.geopolygon, self.geopoint, area_hs, 'user')
        self.assertEqual(expected, instance.area_km)
        instance = Polygon('id', 'polygon', self.geopolygon, self.geopoint, None, 'user')
        self.assertIsNone(instance.area_km)

    def test_from_dict(self):
        _id = "5abb9fb82c8897000bde3e87"
        name = "Polygon Sample"
        coords = [121.1867, 37.6739]
        geopolygon = GeoPolygon([[
            [-121.1958, 37.6683],
            [-121.1779, 37.6687],
            [-121.1773, 37.6792],
            [-121.1958, 37.6792],
            [-121.1958, 37.6683]]])
        center = GeoPoint(coords[0], coords[1])
        area = 190.6343
        user_id = "557066d0ff7a7e3897531d94"
        the_dict = {
            "id": _id,
            "geo_json": {
                "type": "Feature",
                "properties": {

                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-121.1958, 37.6683],
                            [-121.1779, 37.6687],
                            [-121.1773, 37.6792],
                            [-121.1958, 37.6792],
                            [-121.1958, 37.6683]
                        ]
                    ]
                }
            },
            "name": name,
            "center": coords,
            "area": area,
            "user_id": user_id
        }
        expected = Polygon(_id, name, geopolygon, center, area, user_id)
        result = Polygon.from_dict(the_dict)
        self.assertEqual(expected.id, result.id)
        self.assertEqual(expected.name, result.name)
        self.assertEqual(expected.area, result.area)
        self.assertEqual(expected.user_id, result.user_id)
        self.assertEqual(expected.center.lat, result.center.lat)
        self.assertEqual(expected.center.lon, result.center.lon)
        self.assertEqual(expected.geopolygon.geojson(), result.geopolygon.geojson())

        # now testing with dirty data
        self.assertRaises(AssertionError, Polygon.from_dict, None)

        the_dict['center'] = ['no_lon', 'no_lat']
        self.assertRaises(ValueError, Polygon.from_dict, the_dict)
        the_dict['center'] = coords

        del the_dict['id']
        self.assertRaises(AssertionError, Polygon.from_dict, the_dict)

    def test_repr(self):
        instance = Polygon('id', 'polygon', self.geopolygon, self.geopoint, 1.2, 'user')
        repr(instance)
        instance = Polygon('id')
        repr(instance)

