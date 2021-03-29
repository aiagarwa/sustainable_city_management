from main_project.Emergency_Service_API.views_emergency_service_api.show_emergency_service_data import FireStations, HealthCenters, GardaStations, Hospitals
from django.test import TestCase
from unittest.mock import MagicMock
from rest_framework.request import Request
from django.http import HttpRequest
from main_project.Emergency_Service_API.fetch_emergency_service import FetchEmergencyServiceApi
import json


class TestEmergencyService(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_show_fire_service_data(self):
        show_fire_service_data = FireStations()

        request = HttpRequest()
        request.method = 'GET'

        request_wrapper = Request(request)

        fetch_fire_service_api = FetchEmergencyServiceApi()
        expected_result = {"test": "test_value"}
        fetch_fire_service_api.fire_stations_data=MagicMock(return_value=expected_result)

        response=show_fire_service_data.get(
                request_wrapper, fetch_fire_service_api)
        fetch_fire_service_api.fire_stations_data.assert_called_with()

        assert response.status_code == 200
        content=json.loads(response.content)
        assert 'DATA' in content
        data=content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result

    def test_show_garda_stations(self):
        show_garda_stations=GardaStations()

        request=HttpRequest()
        request.method='GET'

        request_wrapper=Request(request)

        fetch_garda_stations_api=FetchEmergencyServiceApi()
        expected_result={"test": "test_value"}
        fetch_garda_stations_api.garda_stations_data=MagicMock(
            return_value=expected_result)

        response=show_garda_stations.get(
            request_wrapper, fetch_garda_stations_api)
        fetch_garda_stations_api.garda_stations_data.assert_called_with()

        assert response.status_code == 200
        content=json.loads(response.content)
        assert 'DATA' in content
        data=content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result

    def test_show_hospital_centers(self):
        show_hospitals=Hospitals()

        request=HttpRequest()
        request.method='GET'

        request_wrapper=Request(request)

        fetch_hospital_api=FetchEmergencyServiceApi()
        expected_result={"test": "test_value"}
        fetch_hospital_api.hospitals_data=MagicMock(
            return_value=expected_result)

        response=show_hospitals.get(
            request_wrapper, fetch_hospital_api)
        fetch_hospital_api.hospitals_data.assert_called_with()

        assert response.status_code == 200
        content=json.loads(response.content)
        assert 'DATA' in content
        data=content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == expected_result
