from django.test import TestCase
from unittest.mock import MagicMock
from rest_framework.request import Request
from django.http import HttpRequest
from main_project.Bus_API.views_bus_api.show_bus_delays import BusTripDelays
from main_project.Bus_API.process_bus_delays import ProcessBusDelays
import json


class TestShowBusApi(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_show_live_bus_delays(self):
        show_bus_delays = BusTripDelays()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['type'] = 'live'

        request_wrapper = Request(request)

        fetch_bus_delays = ProcessBusDelays()
        expected_result = {"test": "test_value"}
        fetch_bus_delays.get_delay_for_trip_live = MagicMock(return_value=expected_result)

        response = show_bus_delays.get(request_wrapper, fetch_bus_delays)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'DATA' in content
        data = content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result