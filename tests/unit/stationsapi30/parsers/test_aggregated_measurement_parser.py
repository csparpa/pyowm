import unittest
import json
from pyowm.stationsapi30.parsers.aggregated_measurement_parser import AggregatedMeasurementParser
from pyowm.stationsapi30.measurement import AggregatedMeasurement
from pyowm.exceptions import parse_response_error


class TestAggregatedMeasurementParser(unittest.TestCase):

    test_msmt_json = '''{"station_id": "mytest","date": 123456789,
        "type": "m",
        "temp": {"min": 0, "max": 100},
        "humidity": {"min": 10, "max": 110},
        "wind": {"speed": 2.1, "gust": 67},
        "pressure": {},
        "precipitation": {}}
        '''

    test_msmt = AggregatedMeasurement('mytest', 123456789, 'm',
                                       temp=dict(min=0, max=100),
                                       humidity=dict(min=10, max=110),
                                       wind=dict(speed=2.1, gust=67),
                                       pressure=None,
                                       precipitation=None)

    def test_parse_JSON(self):
        instance = AggregatedMeasurementParser()
        result = instance.parse_JSON(self.test_msmt_json)
        self.assertTrue(isinstance(result, AggregatedMeasurement))
        self.assertEqual(self.test_msmt.station_id, result.station_id)
        self.assertEqual(self.test_msmt.timestamp, result.timestamp)
        self.assertEqual(self.test_msmt.aggregated_on, result.aggregated_on)
        self.assertEqual(self.test_msmt.temp, result.temp)
        self.assertEqual(self.test_msmt.humidity, result.humidity)
        self.assertEqual(self.test_msmt.wind, result.wind)
        self.assertEqual(self.test_msmt.pressure, result.pressure)
        self.assertEqual(self.test_msmt.precipitation, result.precipitation)

    def test_parse_JSON_fails_with_none_input(self):
        instance = AggregatedMeasurementParser()
        with self.assertRaises(parse_response_error.ParseResponseError):
            instance.parse_JSON(None)

    def test_parse_dict(self):
        data_dict = json.loads(self.test_msmt_json)
        instance = AggregatedMeasurementParser()
        result = instance.parse_dict(data_dict)
        self.assertTrue(isinstance(result, AggregatedMeasurement))
        self.assertEqual(self.test_msmt.station_id, result.station_id)
        self.assertEqual(self.test_msmt.timestamp, result.timestamp)
        self.assertEqual(self.test_msmt.aggregated_on, result.aggregated_on)
        self.assertEqual(self.test_msmt.temp, result.temp)
        self.assertEqual(self.test_msmt.humidity, result.humidity)
        self.assertEqual(self.test_msmt.wind, result.wind)
        self.assertEqual(self.test_msmt.pressure, result.pressure)
        self.assertEqual(self.test_msmt.precipitation, result.precipitation)

    def test_parse_dict_fails_with_wrong_input(self):
        instance = AggregatedMeasurementParser()
        with self.assertRaises(AssertionError):
            instance.parse_dict(1234)

