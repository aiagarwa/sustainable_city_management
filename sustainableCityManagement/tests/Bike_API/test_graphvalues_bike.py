from main_project.Bike_API.graphvalues_bike import GraphValuesBike
from main_project.Bike_API.store_bikedata_to_database import StoreBikeDataToDatabase
from main_project.Bike_API.store_processed_bikedata_to_db import StoreProcessedBikeDataToDB
from django.test import TestCase
from unittest.mock import MagicMock
import datetime
from freezegun import freeze_time

@freeze_time("2021-03-11 17")
class TestGraphValuesBike(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_graphvalue_call_overall_returns_error_with_days_historical_0(self):
        graph_values_bike = GraphValuesBike()

        with self.assertRaises(ValueError) as context:
            graph_values_bike.graphvalue_call_overall(days_historical=0)
        assert str(context.exception) == 'Assign days_historic parameter >= 2.'


    def test_graphvalue_call_overall_returns_error_with_days_historical_1(self):
        graph_values_bike = GraphValuesBike()

        with self.assertRaises(ValueError) as context:
            graph_values_bike.graphvalue_call_overall(days_historical=1)
        assert str(context.exception) == 'Assign days_historic parameter >= 2.'


    def test_graphvalue_call_locationbased(self):
        graph_values_bike = GraphValuesBike()

        fetch_bike_api_class = fetch_bikeapi.FetchBikeApi()

        store_processed_bike_data_to_database = StoreBikeDataToDatabase()
        store_predicted_bike_data_to_database = StoreProcessedBikeDataToDB()
        # fetched_data = store_processed_bike_data_to_database.fetch_processed_data(days_historical)
        # fetched_predicted = store_processed_bike_data_to_database.fetch_predicted_data(day_ahead_tmp)
        mocked_result_historical = [
                            {'historical': [
                                    {
                                        'TOTAL_STANDS': 40,
                                        'IN_USE': 31,
                                        'time': datetime.datetime(2021, 3, 30, 16, 40, 3)
                                    }
                                ], 'name': 'MOUNT STREET LOWER'
                            },
                            {'historical': [
                                    {
                                        'TOTAL_STANDS': 30, 
                                        'IN_USE': 11,
                                        'time': datetime.datetime(2021, 3, 30, 16, 40, 3)
                                    }
                                ], 'name': 'SOUTH DOCK ROAD'
                            }
                        ]

        mocked_result_predicted = [
                            {'historical': [
                                    {
                                        'TOTAL_STANDS': 40,
                                        'IN_USE': 31,
                                        'time': datetime.datetime(2021, 3, 30, 16, 40, 3)
                                    }
                                ], 'name': 'MOUNT STREET LOWER'
                            },
                            {'historical': [
                                    {
                                        'TOTAL_STANDS': 30, 
                                        'IN_USE': 11,
                                        'time': datetime.datetime(2021, 3, 30, 16, 40, 3)
                                    }
                                ], 'name': 'SOUTH DOCK ROAD'
                            }
                        ]

        store_processed_bike_data_to_database.fetch_processed_data = MagicMock(return_value=mocked_result_historical)
        store_predicted_bike_data_to_database.fetch_predicted_data = MagicMock(return_value=mocked_result_predicted)

        expected_result = {
            'MOUNT STREET LOWER': {'TOTAL_STANDS': 40, 'IN_USE': 31, 'TIME': '2021-03-11 17:00'},
            'SOUTH DOCK ROAD': {'TOTAL_STANDS': 30, 'IN_USE': 11, 'TIME': '2021-03-11 17:00'}
            }
        
        result = fetch_bike_api_class.bikeapi(locations=False, store_processed_bike_data_to_database=store_processed_bike_data_to_database)
        print(result)
        self.assertDictEqual(result, expected_result)


        # with self.assertRaises(ValueError) as context:
        #     graph_values_bike.graphvalue_call_overall(days_historical=1)
        # assert str(context.exception) == 'Assign days_historic parameter >= 2.'

