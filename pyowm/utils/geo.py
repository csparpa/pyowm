import json
import geojson


def assert_is_lat(val):
    assert type(val) is float or type(val) is int, "Value must be a number"
    if val < -90.0 or val > 90.0:
        raise ValueError("Latitude value must be between -90 and 90")


def assert_is_lon(val):
    assert type(val) is float or type(val) is int, "Value must be a number"
    if val < -180.0 or val > 180.0:
        raise ValueError("Longitude value must be between -180 and 180")


class Geometry:
    def geojson(self):
        raise NotImplementedError()

    def as_dict(self):
        raise NotImplementedError()


class Point(Geometry):

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
    def __init__(self, list_of_tuples):
        if not list_of_tuples:
            raise ValueError("A MultiPoint cannot be empty")
        for t in list_of_tuples:
            assert_is_lon(t[0])
            assert_is_lat(t[1])
        self._geom = geojson.MultiPoint(list_of_tuples)

    @classmethod
    def from_points(cls, iterable_of_points):
        return MultiPoint([(p.lon, p.lat) for p in iterable_of_points])

    @property
    def longitudes(self):
        return [coords[0] for coords in self._geom['coordinates']]

    @property
    def latitudes(self):
        return [coords[1] for coords in self._geom['coordinates']]

    def geojson(self):
        return geojson.dumps(self._geom)

    def as_dict(self):
        return json.loads(self.geojson())


class Polygon(Geometry):
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
        result = []
        for l in list_of_lists:
            curve = []
            for point in l:
                curve.append((point.lon, point.lat))
            result.append(curve)
        return Polygon(result)


class MultiPolygon(Geometry):
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
        return MultiPolygon([polygon.as_dict()['coordinates'] for polygon in iterable_of_polygons])
