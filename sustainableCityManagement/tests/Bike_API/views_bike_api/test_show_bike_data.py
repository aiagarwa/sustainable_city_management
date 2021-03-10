from main_project.Bike_API.views_bike_api.show_bike_data import ShowBikeApi
from django.test import TestCase
from unittest.mock import MagicMock
from rest_framework.request import Request
from django.http import HttpRequest
from main_project.Bike_API.fetch_bikeapi import FetchBikeApi
import json

class TestShowBikeApi(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_show_live_bike_data(self):
        show_bike_data = ShowBikeApi()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['type'] = 'live'

        request_wrapper = Request(request)

        fetch_bike_api = FetchBikeApi()
        expected_result = {"test": "test_value"}
        fetch_bike_api.bikeapi = MagicMock(return_value=expected_result)

        response = show_bike_data.get(request_wrapper, fetch_bike_api)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'DATA' in content
        data = content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result
