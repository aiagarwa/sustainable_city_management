from main_project.Bike_API.graphvalues_bike import GraphValuesBike
from main_project.Bike_API import fetch_bikeapi
from main_project.Bike_API.store_bikedata_to_database import StoreBikeDataToDatabase
from main_project.Bike_API.store_processed_bikedata_to_db import StoreProcessedBikeDataToDB
from main_project.Bike_API.fetch_bikeapi import FetchBikeApi
from django.test import TestCase
from unittest.mock import MagicMock
import datetime
from freezegun import freeze_time


@freeze_time("2021-03-11 17")
class TestGraphValuesBike(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_graphvalue_call_locationbased_returns_error_with_days_historical_0(self):
        graph_values_bike = GraphValuesBike()

        with self.assertRaises(ValueError) as context:
            graph_values_bike.graphvalue_call_locationbased(days_historical=0)
        assert str(context.exception) == 'Assign days_historic parameter >= 2.'

    def test_graphvalue_call_locationbased_returns_error_with_days_historical_1(self):
        graph_values_bike = GraphValuesBike()

        with self.assertRaises(ValueError) as context:
            graph_values_bike.graphvalue_call_locationbased(days_historical=1)
        assert str(context.exception) == 'Assign days_historic parameter >= 2.'

    def test_graphvalue_call_locationbased(self):
        graph_values_bike = GraphValuesBike()

        store_processed_bike_data_to_database = StoreProcessedBikeDataToDB()

        mocked_fetch_processed_data = [
            {
                "name": "test_abcd",
                "data": [
                    {
                        "day": datetime.datetime(2021, 3, 15, 16, 45, 0),
                        "in_use": 10,
                        "total_stands": 50
                    }
                ]
            },
            {
                "name": "test_abcdef",
                "data": [
                    {
                        "day": datetime.datetime(2021, 3, 15, 16, 45, 0),
                        "in_use": 15,
                        "total_stands": 20
                    }
                ]
            }
        ]

        mocked_fetch_predicted_data = [
            {
                "name": "test_abcd",
                "data": {
                    "in_use": 11
                }
            },
            {
                "name": "test_abcdef",
                "data": {
                    "in_use": 12
                }
            }
        ]

        store_processed_bike_data_to_database.fetch_processed_data = MagicMock(
            return_value=mocked_fetch_processed_data)
        store_processed_bike_data_to_database.fetch_predicted_data = MagicMock(
            return_value=mocked_fetch_predicted_data)

        expected_result = {
            'test_abcd': {
                'TOTAL_STANDS': 50,
                'IN_USE': {
                    '2021-03-12': 11,
                    '2021-03-15': 10
                }
            },
            'test_abcdef': {
                'TOTAL_STANDS': 20,
                'IN_USE': {
                    '2021-03-12': 12,
                    '2021-03-15': 15
                }
            }
        }

        result = graph_values_bike.graphvalue_call_locationbased(days_historical=2,
                                                                 store_processed_bike_data_to_db=store_processed_bike_data_to_database)

        self.assertDictEqual(result, expected_result)

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

    def test_graphvalue_call_overall(self):
        graph_values_bike = GraphValuesBike()

        store_processed_bike_data_to_database = StoreProcessedBikeDataToDB()

        mocked_fetch_processed_data = [
            {
                "name": "test_abcd",
                "data": [
                    {
                        "day": datetime.datetime(2021, 3, 15, 16, 45, 0),
                        "in_use": 10,
                        "total_stands": 50
                    }
                ]
            },
            {
                "name": "test_abcdef",
                "data": [
                    {
                        "day": datetime.datetime(2021, 3, 15, 16, 45, 0),
                        "in_use": 15,
                        "total_stands": 20
                    }
                ]
            }
        ]

        mocked_fetch_predicted_data = [
            {
                "name": "test_abcd",
                "data": {
                    "in_use": 11
                }
            },
            {
                "name": "test_abcdef",
                "data": {
                    "in_use": 12
                }
            }
        ]

        store_processed_bike_data_to_database.fetch_processed_data = MagicMock(
            return_value=mocked_fetch_processed_data)
        store_processed_bike_data_to_database.fetch_predicted_data = MagicMock(
            return_value=mocked_fetch_predicted_data)

        expected_result = {
            'ALL_LOCATIONS': {
                'TOTAL_STANDS': 20,
                'IN_USE': {
                    '2021-03-12': 12,
                    '2021-03-15': 15
                }
            }
        }

        result = graph_values_bike.graphvalue_call_overall(days_historical=2,
                                                           store_processed_bike_data_to_db=store_processed_bike_data_to_database)

        self.assertDictEqual(result, expected_result)
