import json
from datetime import datetime
from django.test import TestCase
from pyowm.utils.timeformatutils import UTC
from .models import Location, \
    LocationEntity, Weather, WeatherEntity, Observation, ObservationEntity, \
    Forecast, ForecastEntity, Station, StationEntity


class Databox():
    """
    Test data container
    """
    # location
    location_name = 'London'
    lat = 43.7
    lon = 12.3
    city_id = 1234
    country = 'UK'
    location = LocationEntity(location_name, lon, lat, city_id, country)

    reception_time = datetime.strptime(
        "2013-09-07 09:20:00+00",
        '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
    reference_time = datetime.strptime(
        "2013-09-06 09:20:00+00",
        '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
    sunset_time = 1378496400
    iso_sunset_time = "2013-09-06 19:40:00+00"
    sunrise_time = 1378449600
    iso_sunrise_time = "2013-09-06 06:40:00+00"
    clouds = 67
    rain = {"all": 20}
    snow = {"all": 0}
    wind = {"deg": 252.002, "speed": 1.100}
    humidity = 57
    pressure = {"press": 1030.119, "sea_level": 1038.589}
    temperature = {"temp": 294.199, "temp_kf": -1.899,
                   "temp_max": 296.098, "temp_min": 294.199}
    celsius_temperature = {"temp": 21.049, "temp_kf": -1.899,
                           "temp_max": 22.948, "temp_min": 21.049}
    fahrenheit_temperature = {"temp": 69.888, "temp_kf": -1.899,
                              "temp_max": 73.306, "temp_min": 69.888}
    status = "Clouds"
    detailed_status = "Overcast clouds"
    weather_code = 804
    weather_icon_name = "04d"
    visibility_distance = 1000
    dewpoint = 300.0
    humidex = 298.0
    heat_index = 40.0

    # weather
    weather = WeatherEntity(
        reference_time, sunset_time,
        sunrise_time, clouds, rain,
        snow, wind, humidity,
        pressure, temperature,
        status, detailed_status,
        weather_code, weather_icon_name,
        visibility_distance, dewpoint,
        humidex, heat_index)

    # observation
    observation = ObservationEntity(reception_time, location, weather)

    # forecast
    interval = '3h'
    weathers = [weather, weather]
    forecast = ForecastEntity(interval, reception_time, location, weathers)

    # station
    station_name = 'KNGU'
    station_id = 2685
    station_type = 1
    station_status = 50
    station_distance = 18.56
    station = StationEntity(station_name, station_id, station_type,
                            station_status, lat, lon, station_distance, weather)


class TestLocationModel(TestCase):

    def test_from_entity(self):
        expected_model = Location(name=Databox.location_name,
                                  lon=Databox.lon, lat=Databox.lat,
                                  city_id=Databox.city_id,
                                  country=Databox.country)
        result_model = Location.from_entity(Databox.location)
        self.assertEquals(expected_model, result_model)

    def test_to_entity(self):
        model = Location(name=Databox.location_name, lon=Databox.lon,
                         lat=Databox.lat, city_id=Databox.city_id,
                         country=Databox.country)
        result = model.to_entity()
        self.assertEquals(Databox.location, result)


class TestWeatherModel(TestCase):

    def test_from_entity(self):
        expected_model = Weather(
            reference_time=self.reference_time,
            sunset_time=self.sunset_time,
            sunrise_time=self.sunrise_time,
            clouds=json.dumps(self.clouds),
            rain=json.dumps(self.rain),
            snow=json.dumps(self.snow),
            wind=json.dumps(self.wind),
            humidity=self.humidity,
            pressure=json.dumps(self.pressure),
            temperature=json.dumps(self.temperature),
            status=self.status,
            detailed_status=self.detailed_status,
            weather_code=self.weather_code,
            weather_icon_name=self.weather_icon_name,
            visibility_distance=self.visibility_distance,
            dewpoint=self.dewpoint,
            humidex=self.humidex,
            heat_index=self.heat_index)
        result_model = Weather.from_entity(Databox.weather)
        self.assertEquals(expected_model, result_model)

    def test_to_entity(self):
        model = Weather(
            reference_time=self.reference_time,
            sunset_time=self.sunset_time,
            sunrise_time=self.sunrise_time,
            clouds=json.dumps(self.clouds),
            rain=json.dumps(self.rain),
            snow=json.dumps(self.snow),
            wind=json.dumps(self.wind),
            humidity=self.humidity,
            pressure=json.dumps(self.pressure),
            temperature=json.dumps(self.temperature),
            status=self.status,
            detailed_status=self.detailed_status,
            weather_code=self.weather_code,
            weather_icon_name=self.weather_icon_name,
            visibility_distance=self.visibility_distance,
            dewpoint=self.dewpoint,
            humidex=self.humidex,
            heat_index=self.heat_index)
        result = model.to_entity()
        self.assertEquals(Databox.weather, result)


class TestObservationModel(TestCase):

    def test_from_entity(self):
        expected_model = Observation(reception_time=Databox.reception_time,
                                     location=Databox.location,
                                     weather=Databox.weather)
        result_model = Observation.from_entity(Databox.observation)
        self.assertEquals(expected_model, result_model)

    def test_to_entity(self):
        model = Observation(reception_time=Databox.reception_time,
                            location=Databox.location,
                            weather=Databox.weather)
        result = model.to_entity()
        self.assertEquals(Databox.observation, result)


class TestForecastModel(TestCase):

    def test_from_entity(self):
        expected_model = Forecast(interval=Databox.interval,
                                  reception_time=Databox.reception_time,
                                  location=Databox.location,
                                  weathers=Databox.weathers)
        result_model = Forecast.from_entity(Databox.forecast)
        self.assertEquals(expected_model, result_model)

    def test_to_entity(self):
        model = Forecast(interval=Databox.interval,
                         reception_time=Databox.reception_time,
                         location=Databox.location,
                         weathers=Databox.weathers)
        result = model.to_entity()
        self.assertEquals(Databox.forecast, result)


class TestStationModel(TestCase):

    def test_from_entity(self):
        expected_model = Station(name=Databox.station_name,
                                 station_id=Databox.station_id,
                                 station_type=Databox.station_type,
                                 station_status=Databox.station_status,
                                 lat=Databox.lat, lon=Databox.lon,
                                 distance=Databox.station_distance,
                                 last_weather=Databox.weather)
        result_model = Station.from_entity(Databox.station)
        self.assertEquals(expected_model, result_model)

    def test_to_entity(self):
        model = Station(name=Databox.station_name,
                        station_id=Databox.station_id,
                        station_type=Databox.station_type,
                        station_status=Databox.station_status,
                        lat=Databox.lat, lon=Databox.lon,
                        distance=Databox.station_distance,
                        last_weather=Databox.weather)
        result = model.to_entity()
        self.assertEquals(Databox.station, result)
