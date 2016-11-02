import json
from datetime import datetime
from django.test import TestCase
from pyowm.utils.timeformatutils import UTC
from pyowm.webapi25.django_pyowm.pyowm_models.models import Location, \
    LocationEntity, Weather, WeatherEntity, Observation, ObservationEntity, \
    Forecast, ForecastEntity, Station, StationEntity, StationHistory, \
    StationHistoryEntity, UVIndex, UVIndexEntity, COIndex, COIndexEntity, \
    Ozone, OzoneEntity


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

    reception_time_unix = 1378459200
    reception_time = datetime.strptime(
        "2013-09-06 09:20:00+00",
        '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
    reference_time_unix = 1378459200
    reference_time = datetime.strptime(
        "2013-09-06 09:20:00+00",
        '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
    sunset_time_unix = 1378496400
    sunset_time = datetime.strptime(
        "2013-09-06 19:40:00+00",
        '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
    sunrise_time_unix = 1378449600
    sunrise_time = datetime.strptime(
        "2013-09-06 06:40:00+00",
        '%Y-%m-%d %H:%M:%S+00').replace(tzinfo=UTC())
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
        reference_time_unix, sunset_time_unix,
        sunrise_time_unix, clouds, rain,
        snow, wind, humidity,
        pressure, temperature,
        status, detailed_status,
        weather_code, weather_icon_name,
        visibility_distance, dewpoint,
        humidex, heat_index)

    # observation
    observation = ObservationEntity(reception_time_unix, location, weather)

    # forecast
    interval = '3h'
    weathers = [weather, weather]
    forecast = ForecastEntity(interval, reception_time_unix, location, weathers)

    # station
    station_name = 'KNGU'
    station_id = 2685
    station_type = 1
    station_status = 50
    station_distance = 18.56
    station = StationEntity(station_name, station_id, station_type,
                            station_status, lat, lon, station_distance, weather)

    # station history
    station_history_interval = "tick"
    station_history_measurements = {
        1362933983: {
            "temperature": 266.25,
            "humidity": 27.3,
            "pressure": 1010.02,
            "rain": None,
            "wind": 4.7
        },
        1362934043: {
            "temperature": 266.85,
            "humidity": 27.7,
            "pressure": 1010.09,
            "rain": None,
            "wind": 4.7
        }
    }
    station_history = StationHistoryEntity(
        station_id,
        station_history_interval,
        reception_time_unix,
        station_history_measurements)

    # UV Index
    uvindex_intensity = 6.8
    uvindex_interval = 'day'
    uvindex = UVIndexEntity(reference_time_unix, location, uvindex_interval,
                            uvindex_intensity, reception_time_unix)

    # CO Index
    co_samples = [
        {
            "precision": -4.999999987376214e-7,
            "pressure": 1000,
            "value": 8.168363052618588e-8
        },
        {
            "precision": -4.999999987376214e-7,
            "pressure": 681.2920532226562,
            "value": 8.686949115599418e-8
        }
    ]
    coindex_interval = 'month'
    coindex = COIndexEntity(
        reference_time_unix, location, coindex_interval, co_samples,
        reception_time_unix)

    # Ozone
    du_value = 6.8
    ozone_interval = 'year'
    ozone = OzoneEntity(reference_time_unix, location, ozone_interval, du_value,
                        reception_time_unix)


class Asserter():

    @staticmethod
    def assertLocationModelsEqual(testcase, expected, result):
        testcase.assertEqual(result.name, expected.name)
        testcase.assertEqual(result.lon, expected.lon)
        testcase.assertEqual(result.lat, expected.lat)
        testcase.assertEqual(result.city_id, expected.city_id)
        testcase.assertEqual(result.country, expected.country)

    @staticmethod
    def assertLocationEntitiesEqual(testcase, expected, result):
        testcase.assertEqual(result.get_name(), expected.get_name())
        testcase.assertEqual(result.get_lon(), expected.get_lon())
        testcase.assertEqual(result.get_lat(), expected.get_lat())
        testcase.assertEqual(result.get_ID(), expected.get_ID())
        testcase.assertEqual(result.get_country(), expected.get_country())

    @staticmethod
    def assertWeatherModelsEqual(testcase, expected, result):
        testcase.assertEquals(expected.reference_time, result.reference_time)
        testcase.assertEquals(expected.sunset_time, result.sunset_time)
        testcase.assertEquals(expected.sunrise_time, result.sunrise_time)
        testcase.assertEquals(expected.clouds, result.clouds)
        testcase.assertEquals(json.loads(expected.rain), json.loads(result.rain))
        testcase.assertEquals(json.loads(expected.snow), json.loads(result.snow))
        testcase.assertEquals(json.loads(expected.wind), json.loads(result.wind))
        testcase.assertEquals(expected.humidity, result.humidity)
        testcase.assertEquals(json.loads(expected.pressure), json.loads(result.pressure))
        testcase.assertEquals(json.loads(expected.temperature),
                          json.loads(result.temperature))
        testcase.assertEquals(expected.status, result.status)
        testcase.assertEquals(expected.detailed_status, result.detailed_status)
        testcase.assertEquals(expected.weather_code, result.weather_code)
        testcase.assertEquals(expected.weather_icon_name, result.weather_icon_name)
        testcase.assertEquals(expected.visibility_distance, result.visibility_distance)
        testcase.assertEquals(expected.dewpoint, result.dewpoint)
        testcase.assertEquals(expected.humidex, result.humidex)
        testcase.assertEquals(expected.heat_index, result.heat_index)

    @staticmethod
    def assertWeatherEntitiesEqual(testcase, expected, result):
        testcase.assertEquals(expected.get_reference_time(), result.get_reference_time())
        testcase.assertEquals(expected.get_sunset_time(), result.get_sunset_time())
        testcase.assertEquals(expected.get_sunrise_time(), result.get_sunrise_time())
        testcase.assertEquals(expected.get_clouds(), result.get_clouds())
        testcase.assertEquals(expected.get_rain(), result.get_rain())
        testcase.assertEquals(expected.get_snow(), result.get_snow())
        testcase.assertEquals(expected.get_wind(), result.get_wind())
        testcase.assertEquals(expected.get_humidity(), result.get_humidity())
        testcase.assertEquals(expected.get_pressure(), result.get_pressure())
        testcase.assertEquals(expected.get_temperature(), result.get_temperature())
        testcase.assertEquals(expected.get_status(), result.get_status())
        testcase.assertEquals(expected.get_detailed_status(), result.get_detailed_status())
        testcase.assertEquals(expected.get_weather_code(), result.get_weather_code())
        testcase.assertEquals(expected.get_weather_icon_name(), result.get_weather_icon_name())
        testcase.assertEquals(expected.get_visibility_distance(), result.get_visibility_distance())
        testcase.assertEquals(expected.get_dewpoint(), result.get_dewpoint())
        testcase.assertEquals(expected.get_humidex(), result.get_humidex())
        testcase.assertEquals(expected.get_heat_index(), result.get_heat_index())


class TestLocationModel(TestCase):

    def test_from_entity(self):
        expected = Location(name=Databox.location_name,
                                  lon=Databox.lon, lat=Databox.lat,
                                  city_id=Databox.city_id,
                                  country=Databox.country)
        result = Location.from_entity(Databox.location)
        Asserter.assertLocationModelsEqual(self, expected, result)

    def test_to_entity(self):
        model = Location(name=Databox.location_name, lon=Databox.lon,
                         lat=Databox.lat, city_id=Databox.city_id,
                         country=Databox.country)
        expected = Databox.location
        result = model.to_entity()
        Asserter.assertLocationEntitiesEqual(self, expected, result)


class TestWeatherModel(TestCase):

    def test_from_entity(self):
        expected = Weather(
            reference_time=Databox.reference_time,
            sunset_time=Databox.sunset_time,
            sunrise_time=Databox.sunrise_time,
            clouds=Databox.clouds,
            rain=json.dumps(Databox.rain),
            snow=json.dumps(Databox.snow),
            wind=json.dumps(Databox.wind),
            humidity=Databox.humidity,
            pressure=json.dumps(Databox.pressure),
            temperature=json.dumps(Databox.temperature),
            status=Databox.status,
            detailed_status=Databox.detailed_status,
            weather_code=Databox.weather_code,
            weather_icon_name=Databox.weather_icon_name,
            visibility_distance=Databox.visibility_distance,
            dewpoint=Databox.dewpoint,
            humidex=Databox.humidex,
            heat_index=Databox.heat_index)
        result = Weather.from_entity(Databox.weather)
        Asserter.assertWeatherModelsEqual(self, expected, result)

    def test_to_entity(self):
        model = Weather(
            reference_time=Databox.reference_time,
            sunset_time=Databox.sunset_time,
            sunrise_time=Databox.sunrise_time,
            clouds=Databox.clouds,
            rain=json.dumps(Databox.rain),
            snow=json.dumps(Databox.snow),
            wind=json.dumps(Databox.wind),
            humidity=Databox.humidity,
            pressure=json.dumps(Databox.pressure),
            temperature=json.dumps(Databox.temperature),
            status=Databox.status,
            detailed_status=Databox.detailed_status,
            weather_code=Databox.weather_code,
            weather_icon_name=Databox.weather_icon_name,
            visibility_distance=Databox.visibility_distance,
            dewpoint=Databox.dewpoint,
            humidex=Databox.humidex,
            heat_index=Databox.heat_index)
        expected = Databox.weather
        result = model.to_entity()
        Asserter.assertWeatherEntitiesEqual(self, expected, result)


class TestObservationModel(TestCase):

    def test_from_entity(self):
        location = Location.from_entity(Databox.location)
        weather = Weather.from_entity(Databox.weather)
        expected = Observation(reception_time=Databox.reception_time,
                               location=location,
                               weather=weather)
        result = Observation.from_entity(Databox.observation)
        self.assertEquals(expected.reception_time, result.reception_time)
        Asserter.assertLocationModelsEqual(self, expected.location, result.location)
        Asserter.assertWeatherModelsEqual(self, expected.weather, result.weather)

    def test_to_entity(self):
        location = Location.from_entity(Databox.location)
        weather = Weather.from_entity(Databox.weather)
        model = Observation(reception_time=Databox.reception_time,
                            location=location,
                            weather=weather)
        result = model.to_entity()
        expected = Databox.observation
        self.assertEquals(expected.get_reception_time(), result.get_reception_time())
        Asserter.assertLocationEntitiesEqual(self, expected.get_location(),
                                           result.get_location())
        Asserter.assertWeatherEntitiesEqual(self, expected.get_weather(),
                                          result.get_weather())


class TestForecastModel(TestCase):

    def test_from_entity(self):
        location = Location.from_entity(Databox.location)
        expected = Forecast(interval=Databox.interval,
                            reception_time=Databox.reception_time,
                            location=location)
        result = Forecast.from_entity(Databox.forecast)
        self.assertEquals(expected.interval, result.interval)
        self.assertEquals(expected.reception_time, result.reception_time)
        Asserter.assertLocationModelsEqual(self, expected.location, result.location)

    def test_to_entity(self):
        weats = [Weather.from_entity(w) for w in Databox.weathers]
        for w in weats:
            w.save()
        loc = Location.from_entity(Databox.location)
        loc.save()
        model = Forecast(interval=Databox.interval,
                         reception_time=Databox.reception_time,
                         location=loc)
        model.save()
        for w in weats:
            model.weathers.add(w)
        result = model.to_entity()
        expected = Databox.forecast
        self.assertEquals(expected.get_interval(), result.get_interval())
        self.assertEquals(expected.get_reception_time(), result.get_reception_time())
        Asserter.assertLocationEntitiesEqual(self, expected.get_location(),
                                           result.get_location())
        for ex_w, res_w in zip(expected.get_weathers(), result.get_weathers()):
            Asserter.assertWeatherEntitiesEqual(self, ex_w, res_w)


class TestStationModel(TestCase):

    def test_from_entity(self):
        expected = Station(name=Databox.station_name,
                           station_id=Databox.station_id,
                           station_type=Databox.station_type,
                           station_status=Databox.station_status,
                           lat=Databox.lat, lon=Databox.lon,
                           distance=Databox.station_distance,
                           last_weather=Weather.from_entity(Databox.weather))
        result = Station.from_entity(Databox.station)
        self.assertEquals(expected.name, result.name)
        self.assertEquals(expected.station_id, result.station_id)
        self.assertEquals(expected.station_type, result.station_type)
        self.assertEquals(expected.station_status, result.station_status)
        self.assertEquals(expected.lat, result.lat)
        self.assertEquals(expected.lon, result.lon)
        self.assertEquals(expected.distance, result.distance)
        Asserter.assertWeatherModelsEqual(self, expected.last_weather,
                                          result.last_weather)

    def test_to_entity(self):
        model = Station(name=Databox.station_name,
                        station_id=Databox.station_id,
                        station_type=Databox.station_type,
                        station_status=Databox.station_status,
                        lat=Databox.lat, lon=Databox.lon,
                        distance=Databox.station_distance,
                        last_weather=Weather.from_entity(Databox.weather))
        result = model.to_entity()
        expected = Databox.station
        self.assertEquals(expected.get_name(), result.get_name())
        self.assertEquals(expected.get_station_ID(), result.get_station_ID())
        self.assertEquals(expected.get_station_type(), result.get_station_type())
        self.assertEquals(expected.get_status(), result.get_status())
        self.assertEquals(expected.get_lat(), result.get_lat())
        self.assertEquals(expected.get_lon(), result.get_lon())
        self.assertEquals(expected.get_distance(), result.get_distance())
        Asserter.assertWeatherEntitiesEqual(self, expected.get_last_weather(),
                                            result.get_last_weather())


class TestStationHistoryModel(TestCase):

    def test_from_entity(self):
        expected = StationHistory(
            station_id=Databox.station_id,
            interval=Databox.station_history_interval,
            reception_time=Databox.reception_time,
            measurements=json.dumps(Databox.station_history_measurements))
        result = StationHistory.from_entity(Databox.station_history)
        self.assertEquals(expected.station_id, result.station_id)
        self.assertEquals(expected.interval, result.interval)
        self.assertEquals(expected.reception_time, result.reception_time)
        self.assertEquals(expected.measurements, result.measurements)

    def test_to_entity(self):
        model = StationHistory(
            station_id=Databox.station_id,
            interval=Databox.station_history_interval,
            reception_time=Databox.reception_time,
            measurements=json.dumps(Databox.station_history_measurements))
        result = model.to_entity()
        expected = Databox.station_history
        self.assertEquals(expected.get_station_ID(), result.get_station_ID())
        self.assertEquals(expected.get_interval(), result.get_interval())
        self.assertEquals(expected.get_reception_time(), result.get_reception_time())
        self.assertEquals(expected.get_measurements(), result.get_measurements())


class TestUVIndexModel(TestCase):

    def test_from_entity(self):
        expected = UVIndex(
            reference_time=Databox.reference_time,
            location=Location.from_entity(Databox.location),
            value=Databox.uvindex_intensity,
            interval=Databox.uvindex_interval,
            reception_time=Databox.reception_time)
        result = UVIndex.from_entity(Databox.uvindex)
        self.assertEquals(expected.reference_time, result.reference_time)
        self.assertEquals(expected.value, result.value)
        self.assertEquals(expected.interval, result.interval)
        self.assertEquals(expected.reception_time, result.reception_time)
        Asserter.assertLocationModelsEqual(self, expected.location, result.location)

    def test_to_entity(self):
        model = UVIndex(
            reference_time=Databox.reference_time,
            location=Location.from_entity(Databox.location),
            value=Databox.uvindex_intensity,
            interval=Databox.uvindex_interval,
            reception_time=Databox.reception_time)
        result = model.to_entity()
        expected = Databox.uvindex
        self.assertEquals(expected.get_reference_time(), result.get_reference_time())
        self.assertEquals(expected.get_value(), result.get_value())
        self.assertEquals(expected.get_interval(), result.get_interval())
        self.assertEquals(expected.get_reception_time(), result.get_reception_time())
        Asserter.assertLocationEntitiesEqual(self, expected.get_location(),
                                             result.get_location())


class TestCOIndexModel(TestCase):

    def test_from_entity(self):
        expected = COIndex(
            reference_time=Databox.reference_time,
            location=Location.from_entity(Databox.location),
            interval=Databox.coindex_interval,
            reception_time=Databox.reception_time,
            co_samples=json.dumps(Databox.co_samples))
        result = COIndex.from_entity(Databox.coindex)
        self.assertEquals(expected.reference_time, result.reference_time)
        self.assertEquals(expected.interval, result.interval)
        self.assertEquals(expected.reception_time, result.reception_time)
        self.assertEquals(sorted(expected.co_samples), sorted(result.co_samples))
        Asserter.assertLocationModelsEqual(self, expected.location, result.location)

    def test_to_entity(self):
        model = COIndex(
            reference_time=Databox.reference_time,
            location=Location.from_entity(Databox.location),
            interval=Databox.coindex_interval,
            reception_time=Databox.reception_time,
            co_samples=json.dumps(Databox.co_samples))
        result = model.to_entity()
        expected = Databox.coindex
        self.assertEquals(expected.get_reference_time(), result.get_reference_time())
        self.assertEquals(expected.get_co_samples(), result.get_co_samples())
        self.assertEquals(expected.get_interval(), result.get_interval())
        self.assertEquals(expected.get_reception_time(), result.get_reception_time())
        Asserter.assertLocationEntitiesEqual(self, expected.get_location(),
                                             result.get_location())


class TestOzoneModel(TestCase):

    def test_from_entity(self):
        expected = Ozone(
            reference_time=Databox.reference_time,
            location=Location.from_entity(Databox.location),
            du_value=Databox.du_value,
            interval=Databox.ozone_interval,
            reception_time=Databox.reception_time)
        result = Ozone.from_entity(Databox.ozone)
        self.assertEquals(expected.reference_time, result.reference_time)
        self.assertEquals(expected.interval, result.interval)
        self.assertEquals(expected.reception_time, result.reception_time)
        self.assertEquals(expected.du_value, result.du_value)
        Asserter.assertLocationModelsEqual(self, expected.location, result.location)

    def test_to_entity(self):
        model = Ozone(
            reference_time=Databox.reference_time,
            location=Location.from_entity(Databox.location),
            du_value=Databox.du_value,
            interval=Databox.ozone_interval,
            reception_time=Databox.reception_time)
        result = model.to_entity()
        expected = Databox.ozone
        self.assertEquals(expected.get_reference_time(), result.get_reference_time())
        self.assertEquals(expected.get_du_value(), result.get_du_value())
        self.assertEquals(expected.get_interval(), result.get_interval())
        self.assertEquals(expected.get_reception_time(), result.get_reception_time())
        Asserter.assertLocationEntitiesEqual(self, expected.get_location(),
                                             result.get_location())
