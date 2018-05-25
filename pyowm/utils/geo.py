import json
import geojson


def assert_is_lat(val):
    """
    Checks it the given value is a feasible latitude

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
    Checks it the given value is a feasible longitude

    :param val: value to be checked
    :type val: int of float
    :returns:  `None`
    :raises: *ValueError* if value is out of longitude boundaries, *AssertionError* if type is wrong

    """
    assert type(val) is float or type(val) is int, "Value must be a number"
    if val < -180.0 or val > 180.0:
        raise ValueError("Longitude value must be between -180 and 180")


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

    def as_dict(self):
        """
        Returns a dict representation of this geotype
        :return: dict
        """
        raise NotImplementedError()


class Point(Geometry):
    """
    A Point geotype. Represents a single geographic point

    :param lon: longitude for the geopoint
    :type lon: int of float
    :param lat: latitude for the geopoint
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

    def geojson(self):
        return geojson.dumps(self._geom)

    def as_dict(self):
        return json.loads(self.geojson())


class MultiPoint(Geometry):
    """
    A MultiPoint geotype. Represents a set of geographic points

    :param list_of_tuples: list of tuples, each one being the (lon, lat) coordinates of a geopoint
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
        List of longitudes of this MultiPoint instance
        :return: list of tuples
        """
        return [coords[0] for coords in self._geom['coordinates']]

    @property
    def latitudes(self):
        """
        List of latitudes of this MultiPoint instance
        :return: list of tuples
        """
        return [coords[1] for coords in self._geom['coordinates']]

    def geojson(self):
        return geojson.dumps(self._geom)

    def as_dict(self):
        return json.loads(self.geojson())


class Polygon(Geometry):
    """
    A Polygon geotype. Each Polygon is made up by one or more lines: a line represents a set of connected geographic
    points and is conveyed by a list of points, the last one of which must coincide with the its very first one.
    As said, Polygons can be also made up by multiple lines (therefore, Polygons with "holes" are allowed)
    :param list_of_lists: list of lists, each sublist being a line and being composed by tuples - each one being the
    (lon, lat) couple of a geopoint. The last point specified MUST coincide with the first one specified
    :type list_of_tuples: list
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
        if not first == last:
            raise ValueError("The start and end point of Polygon must coincide")
        self._geom = geojson.Polygon(list_of_lists)

    def geojson(self):
        return geojson.dumps(self._geom)

    def as_dict(self):
        return json.loads(self.geojson())

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
            curve = []
            for point in l:
                curve.append((point.lon, point.lat))
            result.append(curve)
        return Polygon(result)


class MultiPolygon(Geometry):
    """
    A MultiPolygon geotype. Each MultiPolygon represents a set of (also djsoint) Polygons. Each MultiPolygon is composed
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

    def as_dict(self):
        return json.loads(self.geojson())

    @classmethod
    def from_polygons(cls, iterable_of_polygons):
        """
        Creates a *MultiPolygon* instance out of an iterable of Polygon geotypes
        :param iterable_of_polygons: list of `pyowm.utils.geo.Point` instances
        :type iterable_of_polygons: iterable
        :returns:  a *MultiPolygon* instance

        """
        return MultiPolygon([polygon.as_dict()['coordinates'] for polygon in iterable_of_polygons])
