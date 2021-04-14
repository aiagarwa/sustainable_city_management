from main_project.Parkings_API.views_parkings_api.show_parkings_locations import ParkingsLocations
from django.test import TestCase
from unittest.mock import MagicMock
from rest_framework.request import Request
from django.http import HttpRequest
from main_project.Parkings_API.fetch_parkingsapi import FetchParkingsApi
import json


class TestShowParkingLocationApi(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_show_parking_location(self):
        show_parking_location = ParkingsLocations()

        request = HttpRequest()
        request.method = 'GET'

        request_wrapper = Request(request)

        fetch_parking_location_api = FetchParkingsApi()
        expected_result = {"test": "test_value"}
        fetch_parking_location_api.parkings_locations = MagicMock(
            return_value=expected_result)

        response = show_parking_location.get(
            request_wrapper, fetch_parking_location_api)
        fetch_parking_location_api.parkings_locations.assert_called_with()

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'DATA' in content
        data = content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result
