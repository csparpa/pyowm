"""
Module containing a concrete implementation for JSONParser abstract class,
returning a Station instance
"""

import json
from pyowm.abstractions import jsonparser
from pyowm.exceptions import parse_response_error
from pyowm.alertapi30.trigger import Trigger
from pyowm.alertapi30.condition import Condition
from pyowm.alertapi30.alert import Alert
from pyowm.utils.geo import GeometryBuilder
from pyowm.utils import timeformatutils


class TriggerParser(jsonparser.JSONParser):

    """
    Concrete *JSONParser* implementation building a
    `pyowm.alertapi30.trigger.Trigger` instance out of raw JSON data

    """

    def __init__(self):
        pass

    def parse_dict(self, data_dict):
        """
        Parses a dictionary representing the attributes of a `pyowm.alertapi30.trigger.Trigger` entity
        :param data_dict: dict
        :return: `pyowm.alertapi30.trigger.Trigger`
        """
        assert isinstance(data_dict, dict)
        string_repr = json.dumps(data_dict)
        return self.parse_JSON(string_repr)

    def parse_JSON(self, JSON_string):
        """
        Parses a `pyowm.alertapi30.trigger.Trigger` instance out of raw JSON
        data. As per OWM documentation, start and end times are expressed with
        respect to the moment when you create/update the Trigger. By design,
        PyOWM will only allow users to specify *absolute* datetimes - which is, with the `exact` expression -
        for start/end timestamps (will otherwise result in a `ParseResponseError` be raised)

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :return: a `pyowm.alertapi30.trigger.Trigger` instance or ``None``
            if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        try:
            # trigger id
            trigger_id = d.get('_id', None)

            # start timestamp
            start_dict = d['time_period']['start']
            expr = start_dict['expression']
            if expr != 'after':
                raise ValueError('Invalid time expression: "%s" on start timestamp. Only: "after" is supported' % expr)
            start = start_dict['amount']

            # end timestamp
            end_dict = d['time_period']['end']
            expr = end_dict['expression']
            if expr != 'after':
                raise ValueError('Invalid time expression: "%s" on end timestamp. Only: "after" is supported' % expr)
            end = end_dict['amount']

            # conditions
            conditions = [Condition.from_dict(c) for c in d['conditions']]

            # alerts
            alerts_dict = d['alerts']
            alerts = list()
            for key in alerts_dict:
                alert_id = key
                alert_data = alerts_dict[alert_id]
                alert_last_update = alert_data['last_update']
                alert_met_conds = [
                    dict(current_value=c['current_value']['min'], condition=Condition.from_dict(c['condition']))
                        for c in alert_data['conditions']
                ]
                alert_coords = alert_data['coordinates']
                alert = Alert(alert_id, trigger_id, alert_met_conds, alert_coords, last_update=alert_last_update)
                alerts.append(alert)

            # area
            area_list = d['area']
            area = [GeometryBuilder.build(a_dict) for a_dict in area_list]

            # alert channels
            alert_channels = None  # defaulting

        except ValueError as e:
            raise parse_response_error.ParseResponseError('Impossible to parse JSON: %s' % e)
        except KeyError as e:
            raise parse_response_error.ParseResponseError('Impossible to parse JSON: %s' % e)

        return Trigger(start, end, conditions, area=area, alerts=alerts, alert_channels=alert_channels, id=trigger_id)


class AlertParser(jsonparser.JSONParser):

    """
    Concrete *JSONParser* implementation building a `pyowm.alertapi30.alert.Alert` instance out of raw JSON data

    """

    def __init__(self):
        pass

    def parse_dict(self, data_dict):
        """
        Parses a dictionary representing the attributes of a `pyowm.alertapi30.alert.Alert entity
        :param data_dict: dict
        :return: `pyowm.alertapi30.alert.Alert`
        """
        assert isinstance(data_dict, dict)
        string_repr = json.dumps(data_dict)
        return self.parse_JSON(string_repr)

    def parse_JSON(self, JSON_string):
        """
        Parses a `pyowm.alertapi30.alert.Alert` instance out of raw JSON data.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :return: a `pyowm.alertapi30.alert.Alert` instance or ``None``
            if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        try:
            alert_id = d['_id']
            t = d['last_update'].split('.')[0].replace('T', ' ') + '+00'
            alert_last_update = timeformatutils._ISO8601_to_UNIXtime(t)
            alert_trigger_id = d['triggerId']
            alert_met_conds = [
                dict(current_value=c['current_value']['min'], condition=Condition.from_dict(c['condition']))
                    for c in d['conditions']
            ]
            alert_coords = d['coordinates']
            return Alert(alert_id, alert_trigger_id, alert_met_conds, alert_coords, last_update=alert_last_update)

        except ValueError as e:
            raise parse_response_error.ParseResponseError('Impossible to parse JSON: %s' % e)
        except KeyError as e:
            raise parse_response_error.ParseResponseError('Impossible to parse JSON: %s' % e)
