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

    def test_point_as_dict(self):
        expected = {
            "coordinates": [34, -56.3],
            "type": "Point"
        }
        point = geo.Point(34, -56.3)
        self.assertEqual(expected, point.as_dict())

    def test_point_properties(self):
        lon = -56.3
        lat = 34
        point = geo.Point(lon, lat)
        self.assertEqual(lon, point.lon)
        self.assertEqual(lat, point.lat)

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

    def test_multipoint_as_dict(self):
        expected = {"coordinates": [[-155.5, 19.6], [-156.2, 20.7], [-157.9, 21.4]],
                    "type": "MultiPoint"}
        mp = geo.MultiPoint([[-155.5, 19.6], [-156.2, 20.7], [-157.9, 21.4]])
        self.assertEqual(expected, mp.as_dict())

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
        self.assertEqual(expected.as_dict(), result.as_dict())

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

    def test_polygon_as_dict(self):
        expected = {"coordinates": [[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]],
                    "type": "Polygon"}
        p = geo.Polygon([[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]])
        self.assertEqual(expected, p.as_dict())

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
        self.assertEqual(expected.as_dict(), result.as_dict())

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

    def test_multipolygon_as_dict(self):
        expected = {"coordinates": [
            [[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]],
            [[[6.3, 77.32], [13.19, -30.2], [-110.4, 17.15], [6.3, 77.32]]]
        ], "type": "MultiPolygon"}
        mp = geo.MultiPolygon([
            [[[2.3, 57.32], [23.19, -20.2], [-120.4, 19.15], [2.3, 57.32]]],
            [[[6.3, 77.32], [13.19, -30.2], [-110.4, 17.15], [6.3, 77.32]]]
        ])
        self.assertEqual(expected, mp.as_dict())

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
        self.assertEqual(expected.as_dict(), result.as_dict())