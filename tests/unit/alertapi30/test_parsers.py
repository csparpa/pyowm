import unittest
from pyowm.alertapi30.parsers import TriggerParser, AlertParser
from pyowm.alertapi30.trigger import Trigger
from pyowm.alertapi30.alert import Alert
from pyowm.exceptions import parse_response_error


class TestStationsParser(unittest.TestCase):

    test_trigger_json = '''{"_id":"5852816a9aaacb00153134a3","__v":0,"alerts":{"8b48b2cd21c23d2894466caccba1ed1f":{"conditions":[
        {"current_value":{"min":263.576,"max":263.576},"condition":{"name":"temp","expression":"$lt","amount":273,
        "_id":"5852816a9aaacb00153134a5"}}],"last_update":1481802090232,"date":1482181200000,"coordinates":{"lon":37,
        "lat":53}}},"area":[{"type":"Point","_id":"5852816a9aaacb00153134a4","coordinates":[37,53]}],"conditions":
        [{"name":"temp","expression":"$lt","amount":273,"_id":"5852816a9aaacb00153134a5"}],"time_period":{"end":{
        "amount":432060000,"expression":"after"},"start":{"amount":432000000,"expression":"after"}}}'''

    test_trigger_wrong_operator_json = '''{"_id":"5852816a9aaacb00153134a3","__v":0,"alerts":{"8b48b2cd21c23d2894466caccba1ed1f":{"conditions":[
        {"current_value":{"min":263.576,"max":263.576},"condition":{"name":"temp","expression":"$lt","amount":273,
        "_id":"5852816a9aaacb00153134a5"}}],"last_update":1481802090232,"date":1482181200000,"coordinates":{"lon":37,
        "lat":53}}},"area":[{"type":"Point","_id":"5852816a9aaacb00153134a4","coordinates":[37,53]}],"conditions":
        [{"name":"temp","expression":"$lt","amount":273,"_id":"5852816a9aaacb00153134a5"}],"time_period":{"end":{
        "amount":432000000,"expression":"exact"},"start":{"amount":132000000,"expression":"before"}}}'''

    def test_parse_JSON_fails_with_none_input(self):
        instance = TriggerParser()
        with self.assertRaises(parse_response_error.ParseResponseError):
            instance.parse_JSON(None)

    def test_parse_JSON(self):
        instance = TriggerParser()
        result = instance.parse_JSON(self.test_trigger_json)
        self.assertTrue(isinstance(result, Trigger))

    def test_parse_JSON_when_wrong_time_operator(self):
        instance = TriggerParser()
        with self.assertRaises(parse_response_error.ParseResponseError):
            instance.parse_JSON(self.test_trigger_wrong_operator_json)


class TestAlertParser(unittest.TestCase):

    test_alert_json = '''{"_id": "5853dbe27416a400011b1b77","date": "2016-12-17T00:00:00.000Z","last_update": 
    "2016-12-16T11:19:46.352Z","triggerId": "5852816a9aaacb00153134a3","__v": 0,"conditions": [{"current_value": 
    {"max": 258.62,"min": 258.62},"_id": "5853dbe27416a400011b1b78","condition": {"amount": 273,"expression": 
    "$lt","name": "temp"}}],"coordinates": {"lat": "53","lon": "37"}}'''

    def test_parse_JSON_fails_with_none_input(self):
        instance = AlertParser()
        with self.assertRaises(parse_response_error.ParseResponseError):
            instance.parse_JSON(None)

    def test_parse_JSON(self):
        instance = AlertParser()
        result = instance.parse_JSON(self.test_alert_json)
        self.assertTrue(isinstance(result, Alert))
