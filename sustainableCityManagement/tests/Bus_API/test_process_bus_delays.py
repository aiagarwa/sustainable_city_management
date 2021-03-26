from django.test import TestCase
from unittest.mock import MagicMock
import mock
from mongoengine import *
import mongomock as mm
from main_project.Bus_API.process_bus_delays import ProcessBusDelays
import requests
import json

mocked_result = '{"header": {"gtfs_realtime_version": "1.0","timestamp": 1616682839},"entity":[{"id": "1.1a","trip_update": {"trip": {"trip_id": "1.1a","start_time": "09:15:00","route_id":"11-4e"},"stop_time_update": [{"stop_sequence":"1","departure": {"delay":"0"},"stop_id": "24B","schedule_relationship": "SCHEDULED"}]}}]}'
# config_vals = read_config("Bike_API")

def mocked_requests_bus_trips(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.text = json_data
            self.status_code = status_code

        def json(self):
            return self.text

    return MockResponse(mocked_result, 200)

class TestProcessBusDelays(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    @mock.patch('requests.get', side_effect=mocked_requests_bus_trips)
    def test_get_data_from_bus_api(self, mock_get):
        get_bus_trips_data = ProcessBusDelays()

        bus_trip = get_bus_trips_data.get_data_from_bus_api()
        headers = {get_bus_trips_data.config_vals["api_key_name"]:get_bus_trips_data.config_vals["api_key_value"]}
        requests.get.assert_called_once_with(
            get_bus_trips_data.config_vals['api_url'],
            headers=headers)
        assert bus_trip == json.loads(mocked_result)["entity"]

    def test_get_delay_for_trip_live_case1(self):
        delay_data_for_trip = ProcessBusDelays()
        mocked_result = [
            {"id": "1.1a",
            "trip_update": {"trip": {"trip_id": "1.1a",
                                    "start_time": "09:15:00",
                                    "route_id":"11-4e",
                                    "schedule_relationship": "CANCELED"
                                    },
                            "stop_time_update": [{"stop_sequence":"1",
                                                "departure": {"delay":"0"},
                                                "stop_id": "24B",
                                                "schedule_relationship": "SCHEDULED"}]
                            }
            }
            ]

        delay_data_for_trip.get_data_from_bus_api= MagicMock(return_value=mocked_result)
        response_result = delay_data_for_trip.get_delay_for_trip_live()
        assert response_result['1.1a']['STATUS'] == 'CANCELED'

    def test_get_delay_for_trip_live_case2(self):
        delay_data_for_trip = ProcessBusDelays()
        mocked_result = [
            {"id": "1.1a",
            "trip_update": {"trip": {"trip_id": "1.1a",
                                    "start_time": "09:15:00",
                                    "route_id":"11-4e",
                                    "schedule_relationship": "SCHEDULED"
                                    },
                            "stop_time_update": [{"stop_sequence":"1",
                                                "arrival": {},
                                                "stop_id": "24B",
                                                "schedule_relationship": "SCHEDULED"}]
                            }
            }
            ]

        delay_data_for_trip.get_data_from_bus_api= MagicMock(return_value=mocked_result)
        response_result = delay_data_for_trip.get_delay_for_trip_live()
        assert response_result['1.1a']['DELAY'] == 'Not Available'

    def test_get_delay_for_trip_live_case3(self):
        delay_data_for_trip = ProcessBusDelays()
        mocked_result = [
            {"id": "1.1a",
            "trip_update": {"trip": {"trip_id": "1.1a",
                                    "start_time": "09:15:00",
                                    "route_id":"11-4e",
                                    "schedule_relationship": "SCHEDULED"
                                    },
                            "stop_time_update": [{"stop_sequence":"1",
                                                "arrival": {"delay":"20"},
                                                "stop_id": "24B",
                                                "schedule_relationship": "SCHEDULED"}]
                            }
            }
            ]

        delay_data_for_trip.get_data_from_bus_api= MagicMock(return_value=mocked_result)
        response_result = delay_data_for_trip.get_delay_for_trip_live()
        assert response_result['1.1a']['DELAY'] == '20'

    def test_get_delay_for_trip_live_case4(self):
        delay_data_for_trip = ProcessBusDelays()
        mocked_result = [
            {"id": "1.1a",
            "trip_update": {"trip": {"trip_id": "1.1a",
                                    "start_time": "09:15:00",
                                    "route_id":"11-4e",
                                    "schedule_relationship": "SCHEDULED"
                                    },
                            "stop_time_update": [{"stop_sequence":"1",
                                                "departure": {},
                                                "stop_id": "24B",
                                                "schedule_relationship": "SCHEDULED"}]
                            }
            }
            ]

        delay_data_for_trip.get_data_from_bus_api= MagicMock(return_value=mocked_result)
        response_result = delay_data_for_trip.get_delay_for_trip_live()
        assert response_result['1.1a']['DELAY'] == 'Not Available'

    def test_get_delay_for_trip_live_case4(self):
        delay_data_for_trip = ProcessBusDelays()
        mocked_result = [
            {"id": "1.1a",
            "trip_update": {"trip": {"trip_id": "1.1a",
                                    "start_time": "09:15:00",
                                    "route_id":"11-4e",
                                    "schedule_relationship": "SCHEDULED"
                                    },
                            "stop_time_update": [{"stop_sequence":"1",
                                                "departure": {"delay":"40"},
                                                "stop_id": "24B",
                                                "schedule_relationship": "SCHEDULED"}]
                            }
            }
            ]

        delay_data_for_trip.get_data_from_bus_api= MagicMock(return_value=mocked_result)
        response_result = delay_data_for_trip.get_delay_for_trip_live()
        assert response_result['1.1a']['DELAY'] == '40'