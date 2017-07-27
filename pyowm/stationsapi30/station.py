from datetime import datetime as dt
from pyowm.utils.timeformatutils import UTC


class Station:

    def __init__(self, id, created_at, updated_at, external_id, name,
                 lon, lat, alt, rank):
        assert id is not None
        assert external_id is not None
        assert lon is not None
        assert lat is not None
        assert alt is not None
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        self._lon = float(lon)
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        if alt < 0.0:
            raise ValueError("'alt' value must not be negative")
        self.id = id
        self.created_at = created_at
        if self.created_at is not None:
            self.created_at = dt.strptime(created_at,
                                          '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=UTC())
        self.updated_at = updated_at
        if self.updated_at is not None:
            self.updated_at = dt.strptime(updated_at,
                                          '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=UTC())
        self.external_id = external_id
        self.name = name
        self.lon = lon
        self.lat = lat
        self.alt = alt
        self.rank = rank
