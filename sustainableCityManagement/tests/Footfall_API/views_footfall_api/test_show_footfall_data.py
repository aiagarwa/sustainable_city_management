from main_project.Footfall_API.views_footfall_api.show_footfall_data import FootfallDatebasedData, FootfallOverallData
from django.test import TestCase
from unittest.mock import MagicMock
from rest_framework.request import Request
from django.http import HttpRequest
from main_project.Footfall_API.fetch_footfallapi import FootfallApi
import json


class TestShowFootfallApi(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_show_footfall_prediction(self):
        show_footfall_data = FootfallDatebasedData()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['days_interval'] = '20'
        request.GET['location'] = 'Aston Quay'

        request_wrapper = Request(request)

        fetch_footfall_api = FootfallApi()
        expected_result = {"test": "test_value"}
        fetch_footfall_api.footfall_datebased_graphvalues_predictions = MagicMock(
            return_value=expected_result)

        response = show_footfall_data.get(request_wrapper, fetch_footfall_api)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'DATA' in content
        data = content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result


class TestFootfallOverallData(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_show_footfall_location(self):
        show_footfall_data = FootfallOverallData()

        request = HttpRequest()
        request.method = 'GET'

        request_wrapper = Request(request)

        fetch_footfall_api = FootfallApi()
        expected_result = {"test": "test_value"}
        fetch_footfall_api.footfall_overall = MagicMock(
            return_value=expected_result)

        response = show_footfall_data.get(request_wrapper, fetch_footfall_api)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'DATA' in content
        data = content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result
