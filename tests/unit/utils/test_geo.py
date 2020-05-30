#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
from pyowm.utils import geo


class TestGeo(unittest.TestCase):

    def test_assert_is_lat(self):
        self.assertRaises(AssertionError, geo.assert_is_lat, '23.7')
        self.assertRaises(ValueError, geo.assert_is_lat, -100.0)
        self.assertRaises(ValueError, geo.assert_is_lat, 100.0)
        geo.assert_is_lat(90)
        geo.assert_is_lat(-90)
        geo.assert_is_lat(-45.6)

    def test_assert_is_lon(self):
        self.assertRaises(AssertionError, geo.assert_is_lon, '23.7')
        self.assertRaises(ValueError, geo.assert_is_lon, -200.0)
        self.assertRaises(ValueError, geo.assert_is_lon, 200.0)
        geo.assert_is_lon(180)
        geo.assert_is_lon(-180)
        geo.assert_is_lon(-45.6)

    # -- Point --

    def test_point_geojson(self):
        expected = {
            "coordinates": [34, -56.3],
            "type": "Point"
        }
        point = geo.Point(34, -56.3)
        self.assertEqual(sorted(json.dumps(expected)),
                         sorted(point.geojson()))

    def test_point_to_dict(self):
        expected = {
            "coordinates": [34, -56.3],
            "type": "Point"
        }
        point = geo.Point(34, -56.3)
        self.assertEqual(expected, point.to_dict())

    def test_point_properties(self):
        lon = -56.3
        lat = 34
        point = geo.Point(lon, lat)
        self.assertEqual(lon, point.lon)
        self.assertEqual(lat, point.lat)

    def test_point_from_dict(self):
        the_dict = {
            "coordinates": [34, -56.3],
            "type": "Point"
        }
        expected = geo.Point(34, -56.3)
        result = geo.Point.from_dict(the_dict)
        self.assertIsInstance(result, geo.Point)
        self.assertEqual(expected.lat, result.lat)
        self.assertEqual(expected.lon, result.lon)

    def test_bounding_square_polygon_fails_with_wrong_input(self):
        the_dict = {
            "type": "Point",
            "coordinates": [-0.098040, 51.513844]  # St. Paul's Cathedral, London, GB
        }
        centre = geo.Point.from_dict(the_dict)
        self.assertRaises(AssertionError, centre.bounding_square_polygon, 'not-a-number')
        self.assertRaises(AssertionError, centre.bounding_square_polygon, -67.9)
        self.assertRaises(AssertionError, centre.bounding_square_polygon, 0.)

    def test_bounding_square_polygon(self):
        the_dict = {
            "type": "Point",
            "coordinates": [-0.098040, 51.513844]  # St. Paul's Cathedral, London, GB
        }
        centre = geo.Point.from_dict(the_dict)
        result = centre.bounding_square_polygon(inscribed_circle_radius_km=15.0)
        self.assertIsInstance(result, geo.Polygon)

        the_dict = {
            "type": "Point",
            "coordinates": [0.0, 89.8]  # Almost at the North Pole
        }
        centre = geo.Point.from_dict(the_dict)
        result = centre.bounding_square_polygon(inscribed_circle_radius_km=1000.0)
        self.assertIsInstance(result, geo.Polygon)

    # -- Multipoint --

    def test_multipoint_with_wrong_inputs(self):
        self.assertRaises(AssertionError, geo.MultiPoint,
                          [[-155.5, 'x'], [-156.2, 20.7], [-157.9, 21.4]])
        self.assertRaises(ValueError, geo.MultiPoint,
                          [[-155.5, 19.6], [-156.2, -420.7], [-157.9, 21.4]])
        self.assertRaises(ValueError, geo.MultiPoint,
                          [[-155.5, 19.6], [-156.2, -20.7], [957.9, 21.4]])
        self.assertRaises(ValueError, geo.MultiPoint, [])

    def test_multipoint_geojson(self):
        expected = {"coordinates": [[-155.5, 19.6], [-156.2, 20.7], [-157.9, 21.4]],
                    "type": "MultiPoint"}
        mp = geo.MultiPoint([[-155.5, 19.6], [-156.2, 20.7], [-157.9, 21.4]])
        self.assertEqual(sorted(json.dumps(expected)),
                         sorted(mp.geojson()))

    def test_multipoint_to_dict(self):
        expected = {"coordinates": [[-155.5, 19.6], [-156.2, 20.7], [-157.9, 21.4]],
                    "type": "MultiPoint"}
        mp = geo.MultiPoint([[-155.5, 19.6], [-156.2, 20.7], [-157.9, 21.4]])
        self.assertEqual(expected, mp.to_dict())

    def test_multipoint_properties(self):
        expected_longitudes = [-155.5, -156.2, -157.9]
        expected_latitudes = [19.6, 20.7, 21.4]
        mp = geo.MultiPoint([[-155.5, 19.6], [-156.2, 20.7], [-157.9, 21.4]])
        self.assertEqual(expected_longitudes, mp.longitudes)
        self.assertEqual(expected_latitudes, mp.latitudes)

    def test_multipoint_from_points(self):
        expected = geo.MultiPoint([(34, -56.3), (35, 8), (36, 12)])
        list_of_points = [
            geo.Point(34, -56.3),
            geo.Point(35, 8),
            geo.Point(36, 12)]
        result = geo.MultiPoint.from_points(list_of_points)
        self.assertIsInstance(result, geo.MultiPoint)
        self.assertEqual(expected.to_dict(), result.to_dict())

    def test_multipoint_from_dict(self):
        the_dict = {"coordinates": [[-155.5, 19.6], [-156.2, 20.7], [-157.9, 21.4]],
                    "type": "MultiPoint"}
        expected = geo.MultiPoint([[-155.5, 19.6], [-156.2, 20.7], [-157.9, 21.4]])
        result = geo.MultiPoint.from_dict(the_dict)
        self.assertIsInstance(result, geo.MultiPoint)
        self.assertEqual(expected.latitudes.sort(), result.latitudes.sort())
        self.assertEqual(expected.longitudes.sort(), result.longitudes.sort())

    # -- Polygon --

    def test_polygon_with_wrong_inputs(self):
        self.assertRaises(AssertionError, geo.Polygon,
                          [[[-155.5, 'x'], [-156.2, 20.7], [-157.9, 21.4]]])
        self.assertRaises(ValueError, geo.Polygon,
                          [[[-155.5, 19.6], [-156.2, -420.7], [-157.9, 21.4]]])
        self.assertRaises(ValueError, geo.Polygon,
                          [[[-155.5, 19.6], [-156.2, -20.7], [957.9, 21.4]]])
        self.assertRaises(ValueError, geo.Polygon, [])

    def test_polygon_must_be_closed(self):
        self.assertRaises(ValueError, geo.Polygon,
                          [[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [18, 27.32]]])

    def test_polygon_geojson(self):
        expected = {"coordinates": [
            [[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]
        ], "type": "Polygon"}
        polygon = geo.Polygon([
            [[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]
        ])
        self.assertEqual(sorted(json.dumps(expected)),
                         sorted(polygon.geojson()))

    def test_polygon_to_dict(self):
        expected = {"coordinates": [[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]],
                    "type": "Polygon"}
        p = geo.Polygon([[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]])
        self.assertEqual(expected, p.to_dict())

    def test_polygon_points(self):
        p = geo.Polygon([[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]])
        result = p.points
        self.assertTrue(result)
        self.assertTrue(all([isinstance(p, geo.Point) for p in result]))

    def test_polygon_points(self):
        p = geo.Polygon([[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]])
        result = p.points
        self.assertTrue(result)
        self.assertTrue(all([isinstance(p, geo.Point) for p in result]))

    def test_polygon_from_points(self):
        expected = geo.Polygon([[[2.3, 57.32], [23.19, -20.2], [2.3, 57.32]]])
        list_of_lists = [
            [
                geo.Point(2.3, 57.32),
                geo.Point(23.19, -20.2),
                geo.Point(2.3, 57.32)
            ]
        ]
        result = geo.Polygon.from_points(list_of_lists)
        self.assertIsInstance(result, geo.Polygon)
        self.assertEqual(expected.to_dict(), result.to_dict())

    def test_polygon_from_dict(self):
        the_dict = {"coordinates": [
            [[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]
        ], "type": "Polygon"}
        result = geo.Polygon.from_dict(the_dict)
        self.assertIsInstance(result, geo.Polygon)

    # -- MultiPolygon --

    def test_multipolygon_with_wrong_inputs(self):
        self.assertRaises(AssertionError, geo.MultiPolygon,
                          [[[[-155.5, 'x'], [-156.2, 20.7], [-157.9, 21.4]]]])
        self.assertRaises(ValueError, geo.MultiPolygon,
                          [[[[-155.5, 19.6], [-156.2, -420.7], [-157.9, 21.4]]]])
        self.assertRaises(ValueError, geo.MultiPolygon,
                          [[[[-155.5, 19.6], [-156.2, -20.7], [957.9, 21.4]]]])
        self.assertRaises(ValueError, geo.MultiPolygon, [])

    def test_multipolygon_geojson(self):
        expected = {"coordinates": [
            [[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]],
            [[[6.3, 77.32], [13.19, -30.2], [-110.4, 17.15], [6.3, 77.32]]]
        ], "type": "MultiPolygon"}
        mp = geo.MultiPolygon([
            [[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]],
            [[[6.3, 77.32], [13.19, -30.2], [-110.4, 17.15], [6.3, 77.32]]]
        ])
        self.assertEqual(sorted(json.dumps(expected)),
                         sorted(mp.geojson()))

    def test_multipolygon_to_dict(self):
        expected = {"coordinates": [
            [[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]],
            [[[6.3, 77.32], [13.19, -30.2], [-110.4, 17.15], [6.3, 77.32]]]
        ], "type": "MultiPolygon"}
        mp = geo.MultiPolygon([
            [[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]],
            [[[6.3, 77.32], [13.19, -30.2], [-110.4, 17.15], [6.3, 77.32]]]
        ])
        self.assertEqual(expected, mp.to_dict())

    def test_multipolygon_from_dict(self):
        the_dict = {"coordinates": [
            [[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]],
            [[[6.3, 77.32], [13.19, -30.2], [-110.4, 17.15], [6.3, 77.32]]]
        ], "type": "MultiPolygon"}
        result = geo.MultiPolygon.from_dict(the_dict)
        self.assertIsInstance(result, geo.MultiPolygon)

    def test_from_polygons(self):
        expected = geo.MultiPolygon([
            [[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]],
            [[[6.3, 77.32], [13.19, -30.2], [-110.4, 17.15], [6.3, 77.32]]]
        ])
        iterable_of_polygons = [
            geo.Polygon([[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]]),
            geo.Polygon([[[6.3, 77.32], [13.19, -30.2], [-110.4, 17.15], [6.3, 77.32]]])
        ]
        result = geo.MultiPolygon.from_polygons(iterable_of_polygons)
        self.assertIsInstance(result, geo.MultiPolygon)
        self.assertEqual(expected.to_dict(), result.to_dict())


class TestGeometryBuilder(unittest.TestCase):

    def test_unrecognized_geom_type(self):
        self.assertRaises(AssertionError, geo.GeometryBuilder.build, None)
        self.assertRaises(ValueError, geo.GeometryBuilder.build, {"type": "Unknown"})
        self.assertRaises(ValueError, geo.GeometryBuilder.build, {})

    def test_bulding_points(self):
        the_dict = {
            "coordinates": [34, -56.3],
            "type": "Point"
        }
        expected = geo.Point(34, -56.3)
        result = geo.GeometryBuilder.build(the_dict)
        self.assertIsInstance(result, geo.Point)
        self.assertEqual(expected.lat, result.lat)
        self.assertEqual(expected.lon, result.lon)

    def test_building_multipoints(self):
        the_dict = {"coordinates": [[-155.5, 19.6], [-156.2, 20.7], [-157.9, 21.4]],
                    "type": "MultiPoint"}
        expected = geo.MultiPoint([[-155.5, 19.6], [-156.2, 20.7], [-157.9, 21.4]])
        result = geo.GeometryBuilder.build(the_dict)
        self.assertIsInstance(result, geo.MultiPoint)
        self.assertEqual(expected.latitudes.sort(), result.latitudes.sort())
        self.assertEqual(expected.longitudes.sort(), result.longitudes.sort())

    def test_building_polygons(self):
        the_dict = {"coordinates": [
            [[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]
        ], "type": "Polygon"}
        result = geo.GeometryBuilder.build(the_dict)
        self.assertIsInstance(result, geo.Polygon)

    def test_building_multipolygons(self):
        the_dict = {"coordinates": [
            [[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]],
            [[[6.3, 77.32], [13.19, -30.2], [-110.4, 17.15], [6.3, 77.32]]]
        ], "type": "MultiPolygon"}
        result = geo.GeometryBuilder.build(the_dict)
        self.assertIsInstance(result, geo.MultiPolygon)