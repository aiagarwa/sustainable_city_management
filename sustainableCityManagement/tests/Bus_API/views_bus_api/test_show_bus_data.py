from main_project.Bus_API.views_bus_api.show_bus_info import BusStopsLocations, BusTripsTimings
from django.test import TestCase
from unittest.mock import MagicMock
from rest_framework.request import Request
from django.http import HttpRequest
from main_project.Bus_API.fetch_busapi import FetchBusApi
import json


class TestBusStopsLocations(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_show_bus_location_data(self):
        show_bus_data = BusStopsLocations()

        request = HttpRequest()
        request.method = 'GET'

        request_wrapper = Request(request)

        fetch_bus_api = FetchBusApi()
        expected_result = {"test": "test_value"}
        fetch_bus_api.bus_stand_locations = MagicMock(
            return_value=expected_result)

        response = show_bus_data.get(request_wrapper, fetch_bus_api)
        fetch_bus_api.bus_stand_locations.assert_called_with()

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'DATA' in content
        data = content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result

    def test_show_bus_trip_timings(self):
        show_trip_timing = BusTripsTimings()

        request = HttpRequest()
        request.method = 'GET'

        request_wrapper = Request(request)

        fetch_bus_api = FetchBusApi()
        expected_result = {"test": "test_value"}
        fetch_bus_api.bus_trips_timings = MagicMock(
            return_value=expected_result)

        response = show_trip_timing.get(request_wrapper, fetch_bus_api)
        fetch_bus_api.bus_trips_timings.assert_called_with()

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'DATA' in content
        data = content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result
