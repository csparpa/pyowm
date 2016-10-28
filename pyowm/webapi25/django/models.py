import json
from django.db import models
from pyowm.utils import timeformatutils
from pyowm.webapi25.location import Location as LocationEntity
from pyowm.webapi25.weather import Weather as WeatherEntity
from pyowm.webapi25.observation import Observation as ObservationEntity


class Location(models.Model):
    """
    Model allowing a Location entity object to be saved to a persistent datastore
    """
    name = models.CharField(max_length=255,
                            verbose_name='Toponym of the place',
                            help_text='Name')
    lon = models.FloatField(verbose_name='Longitude of the place',
                            help_text='Longitude')
    lat = models.FloatField(verbose_name='Latitude of the place',
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
    def from_entity(cls, location_obj):
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


class Weather(models.Model):
    """
    Model allowing a Weather entity object to be saved to a persistent datastore
    """
    reference_time = models.DateTimeField(null=True, blank=True)
    sunrise_time = models.DateTimeField(null=True, blank=True)
    sunset_time = models.DateTimeField(null=True, blank=True)
    clouds = models.PositiveIntegerField(null=True, blank=True)
    rain = models.CharField(max_length=255, null=True, blank=True)
    snow = models.CharField(max_length=255, null=True, blank=True)
    wind = models.CharField(max_length=255, null=True, blank=True)
    humidity = models.PositiveIntegerField(null=True, blank=True)
    pressure = models.CharField(max_length=255, null=True, blank=True)
    temperature = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255)
    detailed_status = models.CharField(max_length=255)
    weather_code = models.IntegerField()
    weather_icon_name = models.CharField(max_length=255, null=True, blank=True)
    visibility_distance = models.FloatField(null=True, blank=True)
    dewpoint = models.FloatField(null=True, blank=True)
    humidex = models.FloatField(null=True, blank=True)
    heat_index = models.FloatField(null=True, blank=True)

    def to_entity(self):
        """
        Generates a Weather object out of the current model
        :return: a pyowm.webapi25.weather.Weather instance
        """
        return WeatherEntity(
            self.reference_time,
            self.sunrise_time,
            self.sunset_time,
            self.clouds,
            json.loads(self.rain),
            json.loads(self.snow),
            json.loads(self.wind),
            self.humidity,
            json.loads(self.pressure),
            json.loads(self.temperature),
            self.status,
            self.detailed_status,
            self.weather_code,
            self.weather_icon_name,
            self.visibility_distance,
            self.dewpoint,
            self.humidex,
            self.heat_index)

    @classmethod
    def from_entity(cls, weather_obj):
        """
        Creates a model instance out of a Weather model object
        :param weather_obj: the Weather object
        :type weather_obj: pyowm.webapi25.weather.Weather
        :return: a Weather model instance
        """
        assert isinstance(weather_obj, WeatherEntity)
        return Weather(
            reference_time=weather_obj.get_reference_time(timeformat='date'),
            sunrise_time=weather_obj.get_sunrise_time(timeformat='date'),
            sunset_time=weather_obj.get_sunset_time(timeformat='date'),
            clouds=weather_obj.get_clouds(),
            rain=json.dumps(weather_obj.get_rain()),
            snow=json.dumps(weather_obj.get_snow()),
            wind=json.dumps(weather_obj.get_wind()),
            humidity=weather_obj.get_humidity(),
            pressure=json.dumps(weather_obj.get_pressure()),
            temperature=json.dumps(weather_obj.get_temperature()),
            status=weather_obj.get_status(),
            detailed_status=weather_obj.get_detailed_status(),
            weather_code=weather_obj.get_weather_code(),
            weather_icon_name=weather_obj.get_weather_icon_name(),
            visibility_distance=weather_obj.get_visibility_distance(),
            dewpoint=weather_obj.get_dewpoint(),
            humidex=weather_obj.get_humidex(),
            heat_index=weather_obj.get_heat_index())


class Observation(models.Model):
    """
    Model allowing an Observation entity object to be saved to a persistent datastore
    """
    reception_time = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True,
                                 on_delete=models.DO_NOTHING)
    weather = models.ForeignKey(Weather, null=True, blank=True,
                                on_delete=models.DO_NOTHING)

    def to_entity(self):
        """
        Generates an Observation object out of the current model
        :return: a pyowm.webapi25.observation.Observation instance
        """
        return ObservationEntity(
            timeformatutils.timeformat(self.reception_time, 'unix'),
            self.location.to_entity(),
            self.weather.to_entity())

    @classmethod
    def from_entity(cls, observation_obj):
        """
        Creates a model instance out of an Observation model object
        :param observation_obj: the Observation object
        :type observation_obj: pyowm.webapi25.observation.Observation
        :return: an Observation model instance
        """
        assert isinstance(observation_obj, ObservationEntity)
        location_entity = observation_obj.get_location()
        weather_entity = observation_obj.get_weather()
        loc = Location.from_entity(location_entity)
        weat = Weather.from_entity(weather_entity)
        return Observation(
            reception_time=observation_obj.get_reception_time(timeformat='date'),
            location=loc,
            weather=weat)


    def save(self, *args, **kwargs):
        # TBD: need to save related objects before the current one!
        pass