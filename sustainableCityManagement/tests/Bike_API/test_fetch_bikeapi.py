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

    def test_bikeapi_locations_false(self):
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

        #fetch_bikeapi.datetime.date = NewDate

        store_bike_data_to_database.fetch_data_from_db_for_minutes = MagicMock(return_value=mocked_result)

        expected_result = {
            'MOUNT STREET LOWER': {'TOTAL_STANDS': 40, 'IN_USE': 31, 'TIME': '2021-03-11 17:00'},
            'SOUTH DOCK ROAD': {'TOTAL_STANDS': 30, 'IN_USE': 11, 'TIME': '2021-03-11 17:00'}
            }
        
        result = fetch_bike_api_class.bikeapi(locations=False, store_bike_data_to_database=store_bike_data_to_database)
        self.assertDictEqual(result, expected_result)

def lol_fun():
    return 'lol'