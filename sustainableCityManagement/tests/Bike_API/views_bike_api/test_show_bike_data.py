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

    def test_show_historical_bike_data(self):
        show_bike_data = ShowBikeApi()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['type'] = 'historical'
        request.GET['days_historic'] = 1

        request_wrapper = Request(request)

        fetch_bike_api = FetchBikeApi()
        expected_result = {"test": "test_value"}
        fetch_bike_api.bikeapi = MagicMock(return_value=expected_result)

        response = show_bike_data.get(request_wrapper, fetch_bike_api)
        fetch_bike_api.bikeapi.assert_called_with(
            historical=True, days_historical=1)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'DATA' in content
        data = content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result

    def test_show_historical_bike_data_without_days_historical(self):
        show_bike_data = ShowBikeApi()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['type'] = 'historical'

        request_wrapper = Request(request)

        fetch_bike_api = FetchBikeApi()
        expected_result = {"test": "test_value"}
        fetch_bike_api.bikeapi = MagicMock(return_value=expected_result)

        response = show_bike_data.get(request_wrapper, fetch_bike_api)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'ERROR' in content
        assert content['ERROR'] == 'BIKE_INFO API not working, check fetch_bikeapi, and check the query parameters.'

    def test_show_historical_bike_data_with_days_historical_not_a_number(self):
        show_bike_data = ShowBikeApi()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['type'] = 'historical'
        request.GET['days_historic'] = 'test_value'

        request_wrapper = Request(request)

        fetch_bike_api = FetchBikeApi()
        expected_result = {"test": "test_value"}
        fetch_bike_api.bikeapi = MagicMock(return_value=expected_result)

        response = show_bike_data.get(request_wrapper, fetch_bike_api)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'ERROR' in content
        assert content['ERROR'] == 'BIKE_INFO API not working, check fetch_bikeapi, and check the query parameters.'

    def test_show_locations_bike_data(self):
        show_bike_data = ShowBikeApi()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['type'] = 'locations'

        request_wrapper = Request(request)

        fetch_bike_api = FetchBikeApi()
        expected_result = {"test": "test_value"}
        fetch_bike_api.bikeapi = MagicMock(return_value=expected_result)

        response = show_bike_data.get(request_wrapper, fetch_bike_api)
        fetch_bike_api.bikeapi.assert_called_with(locations=True)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'DATA' in content
        data = content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result

    def test_show_bike_data_with_invalid_type(self):
        show_bike_data = ShowBikeApi()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['type'] = 'invalid_type'

        request_wrapper = Request(request)

        fetch_bike_api = FetchBikeApi()
        expected_result = {"test": "test_value"}
        fetch_bike_api.bikeapi = MagicMock(return_value=expected_result)

        response = show_bike_data.get(request_wrapper, fetch_bike_api)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'ERROR' in content
        assert content['ERROR'] == 'Give valid query parameters.'
