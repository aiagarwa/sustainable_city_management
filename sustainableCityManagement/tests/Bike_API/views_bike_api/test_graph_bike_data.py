from main_project.Bike_API.views_bike_api.graph_bike_data import GraphBikeData
from main_project.Bike_API.graphvalues_bike import GraphValuesBike
import time as processTiming
from django.test import TestCase
from unittest.mock import MagicMock
from rest_framework.request import Request
from django.http import HttpRequest
import json

class TestGraphBikeData(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_graph_bike_data_error_if_location_based_not_set_correctly(self):
        graph_bike_data = GraphBikeData()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['location_based'] = 'wrong_location_based_parameter'
        request.GET['days_historic'] = '1'

        request_wrapper = Request(request)

        graphvalues_bike = GraphValuesBike()

        response = graph_bike_data.get(request_wrapper, graphvalues_bike = graphvalues_bike)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'ERROR' in content
        assert content['ERROR'] == 'Give valid query parameters.'

    def test_graph_bike_data_if_location_based_is_set_to_no(self):
        graph_bike_data = GraphBikeData()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['location_based'] = 'no'
        request.GET['days_historic'] = '1'

        request_wrapper = Request(request)

        graphvalues_bike = GraphValuesBike()
        expected_result = {"test": "test_val"}
        graphvalues_bike.graphvalue_call_overall = MagicMock(return_value=expected_result)

        response = graph_bike_data.get(request_wrapper, graphvalues_bike = graphvalues_bike)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'DATA' in content
        data = content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result

    def test_graph_bike_data_if_location_based_is_set_to_yes(self):
        graph_bike_data = GraphBikeData()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['location_based'] = 'yes'
        request.GET['days_historic'] = '1'

        request_wrapper = Request(request)

        graphvalues_bike = GraphValuesBike()
        expected_result = {"test": "test_val"}
        graphvalues_bike.graphvalue_call_locationbased = MagicMock(return_value=expected_result)

        response = graph_bike_data.get(request_wrapper, graphvalues_bike = graphvalues_bike)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'DATA' in content
        data = content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result

    def test_graph_bike_data_error_if_days_historic_not_passed(self):
        graph_bike_data = GraphBikeData()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['location_based'] = 'yes'

        request_wrapper = Request(request)

        with self.assertRaises(ValueError) as context:
            graph_bike_data.get(request_wrapper)
        assert str(context.exception) == 'days_historic must contain a number'

    def test_graph_bike_data_error_if_days_historic_not_a_number(self):
        graph_bike_data = GraphBikeData()

        request = HttpRequest()
        request.method = 'GET'
        request.GET['location_based'] = 'yes'
        request.GET['days_historic'] = 'test_val_not_number'

        request_wrapper = Request(request)

        with self.assertRaises(ValueError) as context:
            graph_bike_data.get(request_wrapper)
        assert str(context.exception) == 'days_historic must contain a number'
