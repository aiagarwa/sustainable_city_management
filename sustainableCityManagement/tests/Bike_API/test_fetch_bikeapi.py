from main_project.Bike_API import fetch_bikeapi 
from main_project.Bike_API.store_bikedata_to_database import StoreBikeDataToDatabase
from django.test import TestCase
from unittest.mock import MagicMock
from mock import patch
import json
import datetime
from freezegun import freeze_time

@freeze_time("2021-03-11 17")
class TestFetchBikeApi(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_bikeapi_locations_false_one_value_per_location_multiple_locations(self):
        fetch_bike_api_class = fetch_bikeapi.FetchBikeApi()

        store_bike_data_to_database = StoreBikeDataToDatabase()

        mocked_result = [
                            {'historical': [
                                    {
                                        'bike_stands': 40,
                                        'available_bike_stands': 31,
                                        'time': datetime.datetime(2021, 3, 11, 16, 40, 3)
                                    }
                                ], 'name': 'MOUNT STREET LOWER'
                            },
                            {'historical': [
                                    {
                                        'bike_stands': 30, 
                                        'available_bike_stands': 11,
                                        'time': datetime.datetime(2021, 3, 11, 16, 40, 3)
                                    }
                                ], 'name': 'SOUTH DOCK ROAD'
                            }
                        ]
        store_bike_data_to_database.fetch_data_from_db_for_minutes = MagicMock(return_value=mocked_result)

        expected_result = {
            'MOUNT STREET LOWER': {'TOTAL_STANDS': 40, 'IN_USE': 31, 'TIME': '2021-03-11 17:00'},
            'SOUTH DOCK ROAD': {'TOTAL_STANDS': 30, 'IN_USE': 11, 'TIME': '2021-03-11 17:00'}
            }
        
        result = fetch_bike_api_class.bikeapi(locations=False, store_bike_data_to_database=store_bike_data_to_database)
        self.assertDictEqual(result, expected_result)

    def test_bikeapi_locations_false_more_than_one_value_per_location(self):
        fetch_bike_api_class = fetch_bikeapi.FetchBikeApi()

        store_bike_data_to_database = StoreBikeDataToDatabase()

        mocked_result = [
                            {'historical': [
                                    {
                                        'bike_stands': 40,
                                        'available_bike_stands': 30,
                                        'time': datetime.datetime(2021, 3, 11, 16, 45, 3)
                                    },
                                    {
                                        'bike_stands': 40,
                                        'available_bike_stands': 20,
                                        'time': datetime.datetime(2021, 3, 11, 16, 40, 3)
                                    }
                                ], 'name': 'MOUNT STREET LOWER'
                            },
                            {'historical': [
                                    {
                                        'bike_stands': 30, 
                                        'available_bike_stands': 20,
                                        'time': datetime.datetime(2021, 3, 11, 16, 45, 3)
                                    },
                                    {
                                        'bike_stands': 30, 
                                        'available_bike_stands': 10,
                                        'time': datetime.datetime(2021, 3, 11, 16, 40, 3)
                                    }
                                ], 'name': 'SOUTH DOCK ROAD'
                            }
                        ]
        store_bike_data_to_database.fetch_data_from_db_for_minutes = MagicMock(return_value=mocked_result)

        expected_result = {
            'MOUNT STREET LOWER': {'TOTAL_STANDS': 40, 'IN_USE': 25, 'TIME': '2021-03-11 17:00'},
            'SOUTH DOCK ROAD': {'TOTAL_STANDS': 30, 'IN_USE': 15, 'TIME': '2021-03-11 17:00'}
            }
        
        result = fetch_bike_api_class.bikeapi(locations=False, store_bike_data_to_database=store_bike_data_to_database)
        self.assertDictEqual(result, expected_result)

    def test_bikeapi_locations_true(self):
        fetch_bike_api_class = fetch_bikeapi.FetchBikeApi()

        store_bike_data_to_database = StoreBikeDataToDatabase()

        mocked_result = [
                            {
                                "name": "test_name_1",
                                "latitude": 1,
                                "longitude": 2
                            },
                            {
                                "name": "test_name_2",
                                "latitude": 3,
                                "longitude": 4
                            }
                        ]
        store_bike_data_to_database.fetch_bike_stands_location = MagicMock(return_value=mocked_result)

        expected_result = {
                            "test_name_1": {
                                "LATITUDE": 1,
                                        "LONGITUDE": 2
                            },
                            "test_name_2": {
                                "LATITUDE": 3,
                                        "LONGITUDE": 4
                            }
                        }
        
        result = fetch_bike_api_class.bikeapi(locations=True, store_bike_data_to_database=store_bike_data_to_database)
        self.assertDictEqual(result, expected_result)