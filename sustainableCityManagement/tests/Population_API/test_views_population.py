from main_project.Population_API.store_population import StorePopulation
from main_project.Population_API.views_population import IrelandPopulationView, DublinPopulationView
from django.test import TestCase
from unittest.mock import MagicMock
from mock import patch
import json
import datetime
from rest_framework.request import Request
from django.http import HttpRequest
from freezegun import freeze_time


@freeze_time("2021-03-11 17")
class TestViewsPopulationApi(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_ireland_population_data(self):
        fetch_population = IrelandPopulationView()
        store_population = StorePopulation()
        mocked_result = [
            {
                "year": "1960",
                "population": "1"
            },
            {
                "year": "1961",
                "population": "2"
            }
        ]
        store_population.fetch_irish_population = MagicMock(return_value=mocked_result)

        request = HttpRequest()
        request.method = 'GET'

        request_wrapper = Request(request)

        response = fetch_population.get(request_wrapper, fetch_population=store_population)

        assert response.status_code == 200
        content=json.loads(response.content)
        assert 'DATA' in content
        data=content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == mocked_result

    def test_dublin_population_data(self):
        fetch_population = DublinPopulationView()
        store_population = StorePopulation()
        mocked_result = [
            {
                "year": "1960",
                "population": "1"
            },
            {
                "year": "1961",
                "population": "2"
            }
        ]
        store_population.fetch_dublin_population = MagicMock(return_value=mocked_result)

        request = HttpRequest()
        request.method = 'GET'

        request_wrapper = Request(request)

        response = fetch_population.get(request_wrapper, fetch_population=store_population)

        assert response.status_code == 200
        content=json.loads(response.content)
        assert 'DATA' in content
        data=content['DATA']
        assert 'RESULT' in data
        assert data['RESULT'] == mocked_result
