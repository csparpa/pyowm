from django.db import models
from .validators import validate_latitude, validate_longitude
from pyowm.webapi25.location import Location as LocationEntity


class Location(models.Model):
    """
    Model allowing a Location entity object to be saved to a persistent datastore
    """
    name = models.CharField(max_length=255,
                            verbose_name='Toponym of the place',
                            help_text='Name')
    lon = models.FloatField(validators=[validate_longitude],
                            verbose_name='Longitude of the place',
                            help_text='Longitude')
    lat = models.FloatField(validators=[validate_latitude],
                            verbose_name='Latitude of the place',
                            help_text='Latitude')
    city_id = models.IntegerField(verbose_name='City ID related to the place',
                                  help_text='City ID')
    country = models.CharField(max_length=255,
                               verbose_name='Country of the place',
                               help_text="Country")

    def to_entity(self):
        """
        Generates a Location object out of the current model
        :return: a pyowm.webapi25.location.Location instance
        """
        return LocationEntity(self.name, self.lon, self.lat, self.city_id,
                              self.country)

    @classmethod
    def from_entity(self, location_obj):
        """
        Creates a model instance out of a Location model object
        :param location_obj: the Location object
        :type location_obj: pyowm.webapi25.location.Location
        :return: a Location model instance
        """
        assert isinstance(location_obj, LocationEntity)
        return Location(
            name=location_obj.get_name(),
            lon=location_obj.get_lon(),
            lat=location_obj.get_lat(),
            city_id=location_obj.get_ID(),
            country=location_obj.get_country())
