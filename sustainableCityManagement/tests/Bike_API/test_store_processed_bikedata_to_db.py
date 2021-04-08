from main_project.Bike_API.store_bikedata_to_database import StoreBikeDataToDatabase
from main_project.Bike_API.store_processed_bikedata_to_db import StoreProcessedBikeDataToDB
from main_project.Bike_API.bike_collections_db import BikeProcessedData, BikeAvailabilityProcessedData, BikePredictedData, BikeAvailabilityPredictedData, BikeStands
from django.test import TestCase
from unittest.mock import MagicMock
from decimal import Decimal
import mongomock as mm
from mongoengine import get_connection
from main_project.Config.config_handler import read_config
import json
import mock
from datetime import datetime
import requests
from freezegun import freeze_time
from freezegun.api import FakeDatetime
from datetime import datetime, timedelta


@freeze_time("2021-03-31 15:15:15")
class TestStoreProcessedBikedataToDatabase(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_store_bikedata(self):
        store_bike_data_processed = StoreProcessedBikeDataToDB()
        # MongoDb test connection.
        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        mocked_result = [
            {
                "name": "info_1",
                "historical": [
                    {
                        "time": "2021-03-31T15:15:15Z",
                        "bike_stands": 26,
                        "available_bike_stands": 10
                    },
                    {
                        "time": "2021-03-31T15:15:15Z",
                        "bike_stands": 26,
                        "available_bike_stands": 30
                    }
                ]
            }
        ]
        store_bike_data_processed.fetch_bike_data = MagicMock(
            return_value=mocked_result)
        store_bike_data_processed.store_bikedata(1)
        fetch_bike_stand_2 = BikeProcessedData.objects(
            name="info_1").first()
        assert fetch_bike_stand_2 is not None
        assert len(fetch_bike_stand_2.data) == 1
        assert fetch_bike_stand_2.data[0].in_use == 20
        assert fetch_bike_stand_2.data[0].total_stands == 26
        assert str(
            fetch_bike_stand_2.data[0].day == "2021-03-31")
    # Testing function to store location of all bike stands.

    def test_store_bikedata_all_locations(self):
        store_bike_data_processed = StoreProcessedBikeDataToDB()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        BikeProcessedData(name='bike_info_location1').save()
        BikeProcessedData(name='bike_info_location2').save()

        bike_stand_1 = BikeProcessedData.objects(
            name='bike_info_location1').first()
        bike_stand_2 = BikeProcessedData.objects(
            name='bike_info_location2').first()

        bike_stand_1.data.append(
            BikeAvailabilityProcessedData(
                total_stands=40,
                in_use=10,
                day='2021-03-31 13:15:15')
        )
        bike_stand_1.save()

        bike_stand_2.data.append(
            BikeAvailabilityProcessedData(
                total_stands=32,
                in_use=30,
                day='2021-03-15 15:15:15')
        )
        bike_stand_2.save()
        # Call to orginal function[store_bikedata_all_locations]
        store_bike_data_processed.store_bikedata_all_locations(1)
        fetch_bike_stand_2 = BikeProcessedData.objects(
            name="ALL_LOCATIONS").first()
        assert fetch_bike_stand_2 is not None
        assert len(fetch_bike_stand_2.data) == 1
        assert fetch_bike_stand_2.data[0].in_use == 30
        assert fetch_bike_stand_2.data[0].total_stands == 66
        assert str(
            fetch_bike_stand_2.data[0].day == "2021-03-31")

    # Testing the function that creates list of location
    def test_create_location_list(self):
        store_bike_data_processed = StoreProcessedBikeDataToDB()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        BikeProcessedData(name='bike_info_location3').save()

        bike_stand_3 = BikeProcessedData.objects(
            name='bike_info_location3').first()

        bike_stand_3.data.append(
            BikeAvailabilityProcessedData(
                total_stands=40,
                in_use=10,
                day='2021-03-30 00:00:00')
        )
        bike_stand_3.save()
        # Call to orginal function[create_location_list]
        result = store_bike_data_processed.create_location_list()
        expected_result = [
            {
                'name': 'bike_info_location3',
                'in_use': [],
                'total': 40
            }
        ]
        assert expected_result == result
    # Testing function that creates a dictionary with in use array empty.

    def test_get_in_use_arr(self):
        store_bike_data_processed = StoreProcessedBikeDataToDB()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        mocked_result = [
            {
                'name': 'bike_info_location3',
                'in_use': [],
                'total': 40
            }
        ]
        store_bike_data_processed.create_location_list = MagicMock(
            return_value=mocked_result)
        # Call to orginal function[get_in_use_arr]
        result = store_bike_data_processed.get_in_use_arr(2)
        expected_result = [
            {
                'name': 'bike_info_location3',
                'in_use': [10],
                'total': 40
            }
        ]
        assert expected_result == result

    # Testing store function that stores predicted data into database.
    def test_store_predict_data_in_db(self):
        store_bike_data_processed = StoreProcessedBikeDataToDB()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        mocked_result = [
            {
                'name': 'bike_info_location3',
                'in_use': [10, 20, 30, 15],
                'total': 40
            }
        ]
        store_bike_data_processed.get_in_use_arr = MagicMock(
            return_value=mocked_result)
        # Call to orginal function [store_predict_data_in_db()]
        store_bike_data_processed.store_predict_data_in_db(1)
        fetch_bike_stand_2 = BikePredictedData.objects(
            name="bike_info_location3").first()
        assert fetch_bike_stand_2 is not None
        assert len(fetch_bike_stand_2.data) == 1
        assert fetch_bike_stand_2.data[0].in_use == 23
        assert fetch_bike_stand_2.data[0].total_stands == 40
        assert str(
            fetch_bike_stand_2.data[0].day == "2021-04-01")

    # Testing fetch function that retrieves processed data for the specified number of daya in past.
    def test_fetch_processed_data(self):
        store_bike_data_processed = StoreProcessedBikeDataToDB()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        # Call to orginal function [fetch_processed_data]
        result = store_bike_data_processed.fetch_processed_data(2)
        expected_result = [
            {
                'data': [
                    {
                        'total_stands': 40,
                        'in_use': 10,
                        'day': FakeDatetime(2021, 3, 30, 0, 0)
                    }
                ],
                'name': 'bike_info_location3'
            }
        ]
        assert expected_result == result

    # Testing fetch function that retrieves prediction for one day in future.
    def test_fetch_predicted_data(self):
        store_bike_data_processed = StoreProcessedBikeDataToDB()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        BikePredictedData(name='bike_predict1').save()
        day_ahead = "2021-04-1 15:15:15"

        bike_predict_1 = BikePredictedData.objects(
            name='bike_predict1').first()

        bike_predict_1.data.append(
            BikeAvailabilityPredictedData(
                total_stands=40,
                in_use=10,
                day=FakeDatetime(2021, 4, 1, 0, 0))
        )
        bike_predict_1.save()
        # call to orginal function.[fetch predicted_data]
        result = store_bike_data_processed.fetch_predicted_data(day_ahead)
        expected_result = {'total_stands': 40, 'in_use': 10,
                           'day': FakeDatetime(2021, 4, 1, 0, 0)}
        assert result[0]['data'] == expected_result
