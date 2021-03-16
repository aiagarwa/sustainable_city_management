from main_project.Bike_API.store_bikedata_to_database import StoreBikeDataToDatabase
from main_project.Bike_API.store_bikedata_to_database import BikesStandsLocation
from django.test import TestCase
from unittest.mock import MagicMock
from decimal import Decimal
import mongomock as mm
from mongoengine import *
import json
import mock

def mocked_requests_bike_stands_location(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.text = json_data
            self.status_code = status_code

        def json(self):
            return self.text
    
    mocked_result = '[{"st_NAME" : "test_st_val","st_LATITUDE": 1.1,"st_LONGITUDE": 2.2}]'

    return MockResponse(mocked_result, 200)

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

        
        fetch_bike_stand_locaiton = BikesStandsLocation.objects(name="test_st_val").first()

        assert fetch_bike_stand_locaiton["name"] == "test_st_val"
        self.assertAlmostEqual(fetch_bike_stand_locaiton["latitude"],Decimal(1.1),None,None,0.001)
        self.assertAlmostEqual(fetch_bike_stand_locaiton["longitude"],Decimal(2.2),None,None,0.001)
