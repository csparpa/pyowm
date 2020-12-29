#!/usr/bin/env python
# -*- coding: utf-8 -*-

import geojson
import json
import math


EARTH_RADIUS_KM = 6378.1


# utilities

def assert_is_lat(val):
    """
    Checks it the given value is a feasible decimal latitude

    :param val: value to be checked
    :type val: int of float
    :returns:  `None`
    :raises: *ValueError* if value is out of latitude boundaries, *AssertionError* if type is wrong

    """
    assert type(val) is float or type(val) is int, "Value must be a number"
    if val < -90.0 or val > 90.0:
        raise ValueError("Latitude value must be between -90 and 90")


def assert_is_lon(val):
    """
    Checks it the given value is a feasible decimal longitude

    :param val: value to be checked
    :type val: int of float
    :returns:  `None`
    :raises: *ValueError* if value is out of longitude boundaries, *AssertionError* if type is wrong

    """
    assert type(val) is float or type(val) is int, "Value must be a number"
    if val < -180.0 or val > 180.0:
        raise ValueError("Longitude value must be between -180 and 180")


# classes

class Geometry:
    """
    Abstract parent class for geotypes

    """
    def geojson(self):
        """
        Returns a GeoJSON string representation of this geotype, compliant to
        RFC 7946 (https://tools.ietf.org/html/rfc7946)
        :return: str
        """
        raise NotImplementedError()

    def to_dict(self):
        """
        Returns a dict representation of this geotype
        :return: dict
        """
        raise NotImplementedError()


class Point(Geometry):
    """
    A Point geotype. Represents a single geographic point

    :param lon: decimal longitude for the geopoint
    :type lon: int of float
    :param lat: decimal latitude for the geopoint
    :type lat: int of float
    :returns:  a *Point* instance
    :raises: *ValueError* when negative values are provided

    """
    def __init__(self, lon, lat):
        assert_is_lon(lon)
        assert_is_lat(lat)
        self._geom = geojson.Point((lon, lat))

    @property
    def lon(self):
        return self._geom['coordinates'][0]

    @property
    def lat(self):
        return self._geom['coordinates'][1]

    def bounding_square_polygon(self, inscribed_circle_radius_km=10.0):
        """
         Returns a square polygon (bounding box) that circumscribes the circle having this geopoint as centre and 
         having the specified radius in kilometers.
         The polygon's points calculation is based on theory exposed by: http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
         by Jan Philip Matuschek, owner of the intellectual property of such material.
         In short:
         - locally to the geopoint, the Earth's surface is approximated to a sphere with radius = Earth's radius
         - the calculation works fine also when the bounding box contains the Earth's poles and the 180 deg meridian

         :param inscribed_circle_radius_km: the radius of the inscribed circle, defaults to 10 kms
         :type inscribed_circle_radius_km: int or float
         :return: a `pyowm.utils.geo.Polygon` instance
         """
        assert isinstance(inscribed_circle_radius_km, (int, float))
        assert inscribed_circle_radius_km > 0., 'Radius must be greater than zero'

        # turn metric distance to radians on the approximated local sphere
        rad_distance = float(inscribed_circle_radius_km) / EARTH_RADIUS_KM

        # calculating min/max lat for bounding box
        bb_min_lat_deg = self.lat * math.pi/180. - rad_distance
        bb_max_lat_deg = self.lat * math.pi/180. + rad_distance

        # now checking for poles...
        if bb_min_lat_deg > math.radians(-90) and bb_max_lat_deg < math.radians(90):  # no poles in the bounding box
            delta_lon = math.asin(math.sin(rad_distance) / math.cos(math.radians(self.lat)))

            bb_min_lon_deg = math.radians(self.lon) - delta_lon
            if bb_min_lon_deg < math.radians(-180):
                bb_min_lon_deg += 2 * math.pi

            bb_max_lon_deg = math.radians(self.lon) + delta_lon
            if bb_max_lon_deg > math.radians(180):
                bb_max_lon_deg -= 2 * math.pi
        else:   # a pole is contained in the bounding box
            bb_min_lat_deg = max(bb_min_lat_deg, math.radians(-90))
            bb_max_lat_deg = min(bb_max_lat_deg, math.radians(90))
            bb_min_lon_deg = math.radians(-180)
            bb_max_lon_deg = math.radians(180)

        # turn back from radians to decimal
        bb_min_lat = bb_min_lat_deg * 180./math.pi
        bb_max_lat = bb_max_lat_deg * 180./math.pi
        bb_min_lon = bb_min_lon_deg * 180./math.pi
        bb_max_lon = bb_max_lon_deg * 180./math.pi

        return Polygon([[
            [bb_min_lon, bb_max_lat],
            [bb_max_lon, bb_max_lat],
            [bb_max_lon, bb_min_lat],
            [bb_min_lon, bb_min_lat],
            [bb_min_lon, bb_max_lat]
        ]])

    def geojson(self):
        return geojson.dumps(self._geom)

    def to_dict(self):
        return json.loads(self.geojson())

    @classmethod
    def from_dict(cls, the_dict):
        """
        Builds a Point instance out of a geoJSON compliant dict
        :param the_dict: the geoJSON dict
        :return: `pyowm.utils.geo.Point` instance
        """
        geom = geojson.loads(json.dumps(the_dict))
        result = Point(0, 0)
        result._geom = geom
        return result

    def __repr__(self):
        return "<%s.%s - lon=%s, lat=%s>" % (__name__, self.__class__.__name__, self.lon, self.lat)


class MultiPoint(Geometry):
    """
    A MultiPoint geotype. Represents a set of geographic points

    :param list_of_tuples: list of tuples, each one being the decimal (lon, lat) coordinates of a geopoint
    :type list_of_tuples: list
    :returns:  a *MultiPoint* instance

    """
    def __init__(self, list_of_tuples):
        if not list_of_tuples:
            raise ValueError("A MultiPoint cannot be empty")
        for t in list_of_tuples:
            assert_is_lon(t[0])
            assert_is_lat(t[1])
        self._geom = geojson.MultiPoint(list_of_tuples)

    @classmethod
    def from_points(cls, iterable_of_points):
        """
        Creates a MultiPoint from an iterable collection of `pyowm.utils.geo.Point` instances
        :param iterable_of_points: iterable whose items are `pyowm.utils.geo.Point` instances
        :type iterable_of_points: iterable
        :return: a *MultiPoint* instance
        """
        return MultiPoint([(p.lon, p.lat) for p in iterable_of_points])

    @property
    def longitudes(self):
        """
        List of decimal longitudes of this MultiPoint instance
        :return: list of tuples
        """
        return [coords[0] for coords in self._geom['coordinates']]

    @property
    def latitudes(self):
        """
        List of decimal latitudes of this MultiPoint instance
        :return: list of tuples
        """
        return [coords[1] for coords in self._geom['coordinates']]

    def geojson(self):
        return geojson.dumps(self._geom)

    def to_dict(self):
        return json.loads(self.geojson())

    @classmethod
    def from_dict(cls, the_dict):
        """
        Builds a MultiPoint instance out of a geoJSON compliant dict
        :param the_dict: the geoJSON dict
        :return: `pyowm.utils.geo.MultiPoint` instance
        """
        geom = geojson.loads(json.dumps(the_dict))
        result = MultiPoint([(0, 0), (0, 0)])
        result._geom = geom
        return result


class Polygon(Geometry):
    """
    A Polygon geotype. Each Polygon is made up by one or more lines: a line represents a set of connected geographic
    points and is conveyed by a list of points, the last one of which must coincide with the its very first one.
    As said, Polygons can be also made up by multiple lines (therefore, Polygons with "holes" are allowed)
    :param list_of_lists: list of lists, each sublist being a line and being composed by tuples - each one being the
    decimal (lon, lat) couple of a geopoint. The last point specified MUST coincide with the first one specified
    :type list_of_lists: list
    :returns:  a *MultiPoint* instance
    :raises: *ValueError* when last point and fist point do not coincide or when no points are specified at all

    """
    def __init__(self, list_of_lists):
        for l in list_of_lists:
            for t in l:
                assert_is_lon(t[0])
                assert_is_lat(t[1])
        if not list_of_lists:
            raise ValueError("A Polygon cannot be empty")
        first, last = list_of_lists[0][0], list_of_lists[0][-1]
        if first != last:
            raise ValueError("The start and end point of Polygon must coincide")
        self._geom = geojson.Polygon(list_of_lists)

    def geojson(self):
        return geojson.dumps(self._geom)

    def to_dict(self):
        return json.loads(self.geojson())

    @property
    def points(self):
        """
        Returns the list of *Point* instances representing the points of the polygon
        :return: list of *Point* objects
        """
        feature = geojson.Feature(geometry=self._geom)
        points_coords = list(geojson.utils.coords(feature))
        return [Point(p[0], p[1]) for p in points_coords]

    @classmethod
    def from_dict(cls, the_dict):
        """
        Builds a Polygon instance out of a geoJSON compliant dict
        :param the_dict: the geoJSON dict
        :return: `pyowm.utils.geo.Polygon` instance
        """
        geom = geojson.loads(json.dumps(the_dict))
        result = Polygon([[[0, 0], [0, 0]]])
        result._geom = geom
        return result

    @classmethod
    def from_points(cls, list_of_lists):
        """
        Creates a *Polygon* instance out of a list of lists, each sublist being populated with
        `pyowm.utils.geo.Point` instances
        :param list_of_lists: list
        :type: list_of_lists: iterable_of_polygons
        :returns:  a *Polygon* instance

        """
        result = []
        for l in list_of_lists:
            curve = [(point.lon, point.lat) for point in l]
            result.append(curve)
        return Polygon(result)


class MultiPolygon(Geometry):
    """
    A MultiPolygon geotype. Each MultiPolygon represents a set of (also djsjoint) Polygons. Each MultiPolygon is composed
    by an iterable whose elements are the list of lists defining a Polygon geotype. Please refer to the
    `pyowm.utils.geo.Point` documentation for details

    :param iterable_of_list_of_lists: iterable whose elements are list of lists of tuples
    :type iterable_of_list_of_lists: iterable
    :returns:  a *MultiPolygon* instance
    :raises: *ValueError* when last point and fist point do not coincide or when no points are specified at all

    """
    def __init__(self, iterable_of_list_of_lists):
        if not iterable_of_list_of_lists:
            raise ValueError("A MultiPolygon cannot be empty")
        for list_of_lists in iterable_of_list_of_lists:
            Polygon(list_of_lists)
        self._geom = geojson.MultiPolygon(iterable_of_list_of_lists)

    def geojson(self):
        return geojson.dumps(self._geom)

    def to_dict(self):
        return json.loads(self.geojson())

    @classmethod
    def from_dict(cls, the_dict):
        """
        Builds a MultiPolygoninstance out of a geoJSON compliant dict
        :param the_dict: the geoJSON dict
        :return: `pyowm.utils.geo.MultiPolygon` instance
        """
        geom = geojson.loads(json.dumps(the_dict))
        result = MultiPolygon([
            [[[0, 0], [0, 0]]],
            [[[1, 1], [1, 1]]]
        ])
        result._geom = geom
        return result

    @classmethod
    def from_polygons(cls, iterable_of_polygons):
        """
        Creates a *MultiPolygon* instance out of an iterable of Polygon geotypes
        :param iterable_of_polygons: list of `pyowm.utils.geo.Point` instances
        :type iterable_of_polygons: iterable
        :returns:  a *MultiPolygon* instance

        """
        return MultiPolygon([polygon.to_dict()['coordinates'] for polygon in iterable_of_polygons])


class GeometryBuilder:

    @classmethod
    def build(cls, the_dict):
        """
        Builds a `pyowm.utils.geo.Geometry` subtype based on the geoJSON geometry type specified on the input dictionary
        :param the_dict: a geoJSON compliant dict
        :return: a `pyowm.utils.geo.Geometry` subtype instance
        :raises `ValueError` if unable to the geometry type cannot be recognized
        """
        assert isinstance(the_dict, dict), 'Geometry must be a dict'
        geom_type = the_dict.get('type', None)
        if geom_type == 'Point':
            return Point.from_dict(the_dict)
        elif geom_type == 'MultiPoint':
            return MultiPoint.from_dict(the_dict)
        elif geom_type == 'Polygon':
            return Polygon.from_dict(the_dict)
        elif geom_type == 'MultiPolygon':
            return MultiPolygon.from_dict(the_dict)
        else:
            raise ValueError('Unable to build a GeoType object: unrecognized geometry type')
