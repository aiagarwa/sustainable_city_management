from main_project.Bike_API.store_bikedata_to_database import StoreBikeDataToDatabase
from main_project.Bike_API.store_bikedata_to_database import BikesStandsLocation
from django.test import TestCase
from unittest.mock import MagicMock
from decimal import Decimal
import mongomock as mm
from mongoengine import get_connection
from main_project.Config.config_handler import read_config
import json
import mock
import requests
from freezegun import freeze_time

mocked_result = '[{"st_NAME" : "test_st_val","st_LATITUDE": 1.1,"st_LONGITUDE": 2.2}]'
config_vals = read_config("Bike_API")

def mocked_requests_bike_stands_location(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.text = json_data
            self.status_code = status_code

        def json(self):
            return self.text

    return MockResponse(mocked_result, 200)

@freeze_time("2021-03-15 15:15:15")
class TestStoreBikedataToDatabase(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    @mock.patch('requests.get', side_effect=mocked_requests_bike_stands_location)
    def test_save_bike_stands_location(self, mock_get):
        store_bike_data_to_database = StoreBikeDataToDatabase()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        store_bike_data_to_database.save_bike_stands_location()
        
        fetch_bike_stand_location = BikesStandsLocation.objects(name="test_st_val").first()

        assert fetch_bike_stand_location["name"] == "test_st_val"
        self.assertAlmostEqual(fetch_bike_stand_location["latitude"],Decimal(1.1),None,None,0.001)
        self.assertAlmostEqual(fetch_bike_stand_location["longitude"],Decimal(2.2),None,None,0.001)

    @mock.patch('requests.get', side_effect=mocked_requests_bike_stands_location)
    def test_get_bikedata_day(self, mock_get):
        store_bike_data_to_database = StoreBikeDataToDatabase()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        bikedata_day = store_bike_data_to_database.get_bikedata_day(1)
        requests.get.assert_called_once_with(
            config_vals['location_api_url'] + '?dfrom=202103131515&dto=202103141515',
            headers={}, data={})

        assert bikedata_day == json.loads(mocked_result)

    @mock.patch('requests.get', side_effect=mocked_requests_bike_stands_location)
    def test_get_bikedata_live(self, mock_get): 
        store_bike_data_to_database = StoreBikeDataToDatabase()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        bikedata_live = store_bike_data_to_database.get_bikedata_live(15)

        requests.get.assert_called_once_with(
            config_vals['location_api_url'] + '?dfrom=202103151500&dto=202103151515',
            headers={}, data={})
        
        assert bikedata_live == json.loads(mocked_result)

# mocked_result = [
#     {'historical': [
#             {
#                 'bike_stands': 40,
#                 'available_bike_stands': 31,
#                 'time': datetime.datetime(2021, 3, 11, 16, 40, 3)
#             }
#         ], 'name': 'MOUNT STREET LOWER'
#     },
#     {'historical': [
#             {
#                 'bike_stands': 30, 
#                 'available_bike_stands': 11,
#                 'time': datetime.datetime(2021, 3, 11, 16, 40, 3)
#             }
#         ], 'name': 'SOUTH DOCK ROAD'
#     }
# ]