from main_project.Parkings_API.views_parkings_api.show_parkings_availability import ParkingsAvailability
from django.test import TestCase
from unittest.mock import MagicMock
from rest_framework.request import Request
from django.http import HttpRequest
from main_project.Parkings_API.fetch_parkingsapi import FetchParkingsApi
import json


class TestShowParkingAvailabilityApi(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_show_parking_availability(self):
        show_parking_availability = ParkingsAvailability()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['startdate'] = '2021-03-14'
        request.GET['enddate'] = '2021-03-12'

        request_wrapper = Request(request)

        fetch_parking_availability_api = FetchParkingsApi()
        expected_result = {"test": "test_val"}
        fetch_parking_availability_api.parkings_availability = MagicMock(
            return_value=expected_result)

        response = show_parking_availability.get(
            request_wrapper, fetch_parking_availability_api)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'DATA' in content
        data = content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result
