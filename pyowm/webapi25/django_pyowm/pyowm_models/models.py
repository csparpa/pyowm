import json
from django.db import models
from pyowm.utils import timeformatutils
from pyowm.webapi25.location import Location as LocationEntity
from pyowm.webapi25.weather import Weather as WeatherEntity
from pyowm.webapi25.observation import Observation as ObservationEntity
from pyowm.webapi25.forecast import Forecast as ForecastEntity
from pyowm.webapi25.station import Station as StationEntity
from pyowm.webapi25.stationhistory import StationHistory as StationHistoryEntity
from pyowm.webapi25.uvindex import UVIndex as UVIndexEntity


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

    def __repr__(self):
        return "<%s.%s - pk=%d>" % (
            __name__,
            self.__class__.__name__,
            self.pk if self.pk is not None else 'None')


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

    def __repr__(self):
        return "<%s.%s - pk=%d>" % (
            __name__,
            self.__class__.__name__,
            self.pk if self.pk is not None else 'None')


class Observation(models.Model):
    """
    Model allowing an Observation entity object to be saved to a persistent datastore
    """
    reception_time = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    weather = models.ForeignKey(Weather, null=True, blank=True)

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
            location=loc, weather=weat)

    def __repr__(self):
        return "<%s.%s - pk=%d>" % (
            __name__,
            self.__class__.__name__,
            self.pk if self.pk is not None else 'None')


class Forecast(models.Model):
    """
    Model allowing a Forecast entity object to be saved to a persistent datastore
    """
    INTERVAL_CHOICES = (
        (u'3h', u'Three hours'),
        (u'daily', u'Daily'))

    interval = models.CharField(max_length=255,
                                verbose_name='Time granularity of the forecast',
                                help_text='Interval',
                                choices=INTERVAL_CHOICES)
    reception_time = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Time the observation was received',
        help_text='Reception time')
    location = models.ForeignKey(
        Location, null=True, blank=True,
        verbose_name='Location of the forecast',
        help_text='Location')
    weathers = models.ManyToManyField(Weather,
                                      blank=True,
                                      related_name='forecasts',
                                      help_text="Weathers",
                                      verbose_name="Weathers of the forecast")

    def to_entity(self):
        """
        Generates a Forecast object out of the current model
        :return: a pyowm.webapi25.forecast.Forecast instance
        """
        return ForecastEntity(
            self.interval,
            timeformatutils.timeformat(self.reception_time, 'unix'),
            self.location.to_entity(),
            list(self.weathers.all()))

    @classmethod
    def from_entity(cls, forecast_obj):
        """
        Creates a model instance out of a Forecast model object
        :param forecast_obj: the Forecast object
        :type forecast_obj: pyowm.webapi25.forecast.Forecast
        :return: a Forecast model instance
        """
        assert isinstance(forecast_obj, ForecastEntity)
        location_entity = forecast_obj.get_location()
        weather_entities = forecast_obj.get_weathers()
        loc = Location.from_entity(location_entity)
        weats = [Weather.from_entity(w) for w in weather_entities]
        return Forecast(
            interval=forecast_obj.get_interval(),
            reception_time=forecast_obj.get_reception_time(timeformat='date'),
            location=loc,
            weathers=weats)

    def __repr__(self):
        return "<%s.%s - pk=%d>" % (
            __name__,
            self.__class__.__name__,
            self.pk if self.pk is not None else 'None')


class Station(models.Model):
    """
    Model allowing a Station entity object to be saved to a persistent datastore
    """
    name = models.CharField(max_length=255,
                            verbose_name='Name of the meteostation',
                            help_text='Name',
                            null=True, blank=True)
    station_id = models.IntegerField(verbose_name='OWM station ID',
                                     help_text='Station ID')
    station_type = models.IntegerField(verbose_name='Meteostation type',
                                       help_text='Type',
                                       null=True, blank=True)
    station_status = models.IntegerField(verbose_name='Meteostation status',
                                         help_text='Status',
                                         null=True, blank=True)
    lat = models.FloatField(verbose_name='Latitude of the meteostation',
                            help_text='Latitude')
    lon = models.FloatField(verbose_name='Longitude of the meteostation',
                            help_text='Longitude')
    distance = models.FloatField(
        verbose_name='Distance of station from lat/lon of search criteria',
        help_text='Distance',
        null=True, blank=True)
    last_weather = models.ForeignKey(
        Weather, null=True, blank=True,
        verbose_name='Last weather measured by the station',
        help_text='Last weather')

    def to_entity(self):
        """
        Generates a Station object out of the current model
        :return: a pyowm.webapi25.station.Station instance
        """
        return StationEntity(
            self.name,
            self.station_id,
            self.station_type,
            self.station_status,
            self.lat,
            self.lon,
            self.distance,
            self.last_weather.to_entity())

    @classmethod
    def from_entity(cls, station_obj):
        """
        Creates a model instance out of a Station model object
        :param station_obj: the Station object
        :type station_obj: pyowm.webapi25.station.Station
        :return: a Station model instance
        """
        assert isinstance(station_obj, StationEntity)
        weather_entity = Weather.from_entity(station_obj.get_last_weather())
        return Station(
            name=station_obj.get_name(),
            station_id=station_obj.get_station_ID(),
            station_type=station_obj.get_station_type(),
            station_status=station_obj.get_status(),
            lat=station_obj.get_lat(),
            lon=station_obj.get_lon(),
            distance=station_obj.get_distance(),
            last_weather=weather_entity)

    def __repr__(self):
        return "<%s.%s - pk=%d>" % (
            __name__,
            self.__class__.__name__,
            self.pk if self.pk is not None else 'None')


class StationHistory(models.Model):
    """
    Model allowing a StationHistory entity object to be saved to a persistent datastore
    """

    INTERVAL_CHOICES = (
        (u'tick', u'Tick'),
        (u'hour', u'One hour'),
        (u'day', u'One day'))

    station_id = models.IntegerField(verbose_name='OWM station ID',
                                     help_text='Station ID')
    interval = models.CharField(max_length=255,
                                verbose_name='Time granularity of the station history',
                                help_text='Interval',
                                choices=INTERVAL_CHOICES)
    reception_time = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Time the observation was received',
        help_text='Reception time')
    measurements = models.TextField(verbose_name='Measured data',
                                    help_text='Measurements')

    def to_entity(self):
        """
        Generates a StationHistory object out of the current model
        :return: a pyowm.webapi25.stationhistory.StationHistory instance
        """
        return StationHistoryEntity(
            self.station_id,
            self.interval,
            timeformatutils.timeformat(self.reception_time, 'unix'),
            json.loads(self.measurements))


    @classmethod
    def from_entity(cls, stationhistory_obj):
        """
        Creates a model instance out of a StationHistory model object
        :param stationhistory_obj: the StationHistory object
        :type stationhistory_obj: pyowm.webapi25.stationhistory.StationHistory
        :return: a StationHistory model instance
        """
        assert isinstance(stationhistory_obj, StationHistoryEntity)
        return StationHistory(
            station_id=stationhistory_obj.get_station_ID(),
            interval=stationhistory_obj.get_interval(),
            reception_time=stationhistory_obj.get_reception_time(timeformat='date'),
            measurements=json.dumps(stationhistory_obj.get_measurements()))

    def __repr__(self):
        return "<%s.%s - pk=%d>" % (
            __name__,
            self.__class__.__name__,
            self.pk if self.pk is not None else 'None')


class UVIndex(models.Model):
    """
    Model allowing a UVIndex entity object to be saved to a persistent datastore
    """
    reference_time = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Time the observation refers to',
        help_text='Reference time')
    location = models.ForeignKey(Location, null=True, blank=True,
                                 verbose_name='Location of the observation',
                                 help_text='Location')
    value = models.FloatField(verbose_name='Observed UV intensity',
                              help_text='Value')
    interval = models.CharField(max_length=255,
                                verbose_name='Time granularity of the observation',
                                help_text='Interval')
    reception_time = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Time the observation was received',
        help_text='Reception time')

    def to_entity(self):
        """
        Generates a UVIndex object out of the current model
        :return: a pyowm.webapi25.uvindex.UVIndex instance
        """
        return UVIndexEntity(
            timeformatutils.timeformat(self.reference_time, 'unix'),
            Location.to_entity(self.location),
            self.value,
            self.interval,
            timeformatutils.timeformat(self.reception_time, 'unix'))

    @classmethod
    def from_entity(cls, uvindex_obj):
        """
        Creates a model instance out of a UVIndex entity object
        :param uvindex_obj: the UVIndex object
        :type uvindex_obj: pyowm.webapi25.uvindex.UVIndex
        :return: a UVIndex model instance
        """
        assert isinstance(uvindex_obj, UVIndexEntity)
        loc = uvindex_obj.get_location()
        return UVIndex(
            reference_time=uvindex_obj.get_reference_time(timeformat='date'),
            location=Location.from_entity(loc),
            value=uvindex_obj.get_value(),
            interval=uvindex_obj.get_interval(),
            reception_time=uvindex_obj.get_reception_time(timeformat='date'))
