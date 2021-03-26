from main_project.Bike_API.store_bikedata_to_database import StoreBikeDataToDatabase
from main_project.Bike_API.bike_collections_db import BikesStandsLocation, BikeStands, BikeAvailability
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

    def tearDown(self):
        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        BikesStandsLocation.objects().delete()
        BikeStands.objects().delete()

    @mock.patch('requests.get', side_effect=mocked_requests_bike_stands_location)
    def test_save_bike_stands_location(self, mock_get):
        store_bike_data_to_database = StoreBikeDataToDatabase()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        store_bike_data_to_database.save_bike_stands_location()

        fetch_bike_stand_location = BikesStandsLocation.objects(
            name="test_st_val").first()

        assert fetch_bike_stand_location["name"] == "test_st_val"
        self.assertAlmostEqual(
            fetch_bike_stand_location["latitude"], Decimal(1.1), None, None, 0.001)
        self.assertAlmostEqual(
            fetch_bike_stand_location["longitude"], Decimal(2.2), None, None, 0.001)

    @mock.patch('requests.get', side_effect=mocked_requests_bike_stands_location)
    def test_get_bikedata_day(self, mock_get):
        store_bike_data_to_database = StoreBikeDataToDatabase()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        bikedata_day = store_bike_data_to_database.get_bikedata_day(1)
        requests.get.assert_called_once_with(
            config_vals['location_api_url'] +
            '?dfrom=202103131515&dto=202103141515',
            headers={}, data={})

        assert bikedata_day == json.loads(mocked_result)

    @mock.patch('requests.get', side_effect=mocked_requests_bike_stands_location)
    def test_get_bikedata_live(self, mock_get):
        store_bike_data_to_database = StoreBikeDataToDatabase()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        bikedata_live = store_bike_data_to_database.get_bikedata_live(15)

        requests.get.assert_called_once_with(
            config_vals['location_api_url'] +
            '?dfrom=202103151500&dto=202103151515',
            headers={}, data={})

        assert bikedata_live == json.loads(mocked_result)

    def test_bike_usage_save_locations(self):
        store_bike_data_to_database = StoreBikeDataToDatabase()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        mocked_result = [
            {
                "name": "test_name_1"
            },
            {
                "name": "test_name_2"
            }
        ]

        store_bike_data_to_database.get_bikedata_day = MagicMock(
            return_value=mocked_result)
        store_bike_data_to_database.bike_usage_save_locations(1)

        fetch_bike_stand_1 = BikeStands.objects(name="test_name_1").first()
        fetch_bike_stand_2 = BikeStands.objects(name="test_name_2").first()

        assert fetch_bike_stand_1["name"] == "test_name_1"
        assert fetch_bike_stand_2["name"] == "test_name_2"

    def test_bikedata_day(self):
        store_bike_data_to_database = StoreBikeDataToDatabase()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        mocked_result = [
            {
                "name": "already_present_in_db",
                "historic": [
                    {
                        "time": "2021-03-15T15:15:15Z",
                        "bike_stands": 40,
                        "available_bike_stands": 10
                    }
                ]
            },
            {
                "name": "not_present_in_db"
            }
        ]
        BikeStands(name='already_present_in_db').save()

        store_bike_data_to_database.get_bikedata_day = MagicMock(
            return_value=mocked_result)

        store_bike_data_to_database.bikedata_day(15)

        fetch_bike_stand_1 = BikeStands.objects(
            name="not_present_in_db").first()
        assert fetch_bike_stand_1 is None

        fetch_bike_stand_2 = BikeStands.objects(
            name="already_present_in_db").first()
        assert fetch_bike_stand_2 is not None
        assert len(fetch_bike_stand_2.historical) == 1
        assert fetch_bike_stand_2.historical[0].bike_stands == 40
        assert fetch_bike_stand_2.historical[0].available_bike_stands == 10
        assert str(
            fetch_bike_stand_2.historical[0].time) == "2021-03-15 15:15:15"

    def test_save_historic_data_in_db(self):
        store_bike_data_to_database = StoreBikeDataToDatabase()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        store_bike_data_to_database.bike_usage_save_locations = MagicMock()
        store_bike_data_to_database.bikedata_day = MagicMock()

        store_bike_data_to_database.save_historic_data_in_db(3)

        assert store_bike_data_to_database.bike_usage_save_locations.call_count == 3
        assert store_bike_data_to_database.bikedata_day.call_count == 3

    def test_fetch_bike_stands_location(self):
        store_bike_data_to_database = StoreBikeDataToDatabase()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        BikesStandsLocation(name="name", latitude=12.2, longitude=1.1).save()

        json_bike_stands_location = store_bike_data_to_database.fetch_bike_stands_location()

        expected_result = [
            {
                "name": "name",
                "latitude": 12.2,
                "longitude": 1.1
            }
        ]

        assert len(json_bike_stands_location) == 1
        assert json_bike_stands_location[0]['name'] == 'name'
        assert json_bike_stands_location[0]['latitude'] == 12.2
        assert json_bike_stands_location[0]['longitude'] == 1.1

    def test_bikedata_minutes(self):
        store_bike_data_to_database = StoreBikeDataToDatabase()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        mocked_result = [
            {
                "name": "already_present_in_db_1",
                "historic": [
                    {
                        "time": "2021-03-15T14:15:15Z",
                        "bike_stands": 40,
                        "available_bike_stands": 10
                    }
                ]
            },
            {
                "name": "not_present_in_db"
            }
        ]
        BikeStands(name='already_present_in_db_1').save()

        store_bike_data_to_database.get_bikedata_live = MagicMock(
            return_value=mocked_result)

        store_bike_data_to_database.bikedata_minutes(15)

        fetch_bike_stand_1 = BikeStands.objects(
            name="not_present_in_db").first()
        assert fetch_bike_stand_1 is None

        fetch_bike_stand_2 = BikeStands.objects(
            name="already_present_in_db_1").first()
        assert fetch_bike_stand_2 is not None
        assert len(fetch_bike_stand_2.historical) == 1
        assert fetch_bike_stand_2.historical[0].bike_stands == 40
        assert fetch_bike_stand_2.historical[0].available_bike_stands == 10
        assert str(
            fetch_bike_stand_2.historical[0].time) == "2021-03-15 14:15:15"

        # We try to store the same data again, the data in the database should not change as we
        # should not be able to insert the same record twice
        store_bike_data_to_database.bikedata_minutes(15)

        fetch_bike_stand_2 = BikeStands.objects(
            name="already_present_in_db_1").first()
        assert fetch_bike_stand_2 is not None
        assert len(fetch_bike_stand_2.historical) == 1
        assert fetch_bike_stand_2.historical[0].bike_stands == 40
        assert fetch_bike_stand_2.historical[0].available_bike_stands == 10
        assert str(
            fetch_bike_stand_2.historical[0].time) == "2021-03-15 14:15:15"

        mocked_result = [
            {
                "name": "already_present_in_db_1",
                "historic": [
                    {
                        "time": "2021-03-15T15:15:15Z",
                        "bike_stands": 40,
                        "available_bike_stands": 12
                    }
                ]
            },
            {
                "name": "not_present_in_db"
            }
        ]
        store_bike_data_to_database.get_bikedata_live = MagicMock(
            return_value=mocked_result)

        # We try to store the different data now, so we should get 2 datapoints in historical
        store_bike_data_to_database.bikedata_minutes(15)

        fetch_bike_stand_2 = BikeStands.objects(
            name="already_present_in_db_1").first()
        assert fetch_bike_stand_2 is not None
        assert len(fetch_bike_stand_2.historical) == 2

        assert fetch_bike_stand_2.historical[0].bike_stands == 40
        assert fetch_bike_stand_2.historical[0].available_bike_stands == 10
        assert str(
            fetch_bike_stand_2.historical[0].time) == "2021-03-15 14:15:15"

        assert fetch_bike_stand_2.historical[1].bike_stands == 40
        assert fetch_bike_stand_2.historical[1].available_bike_stands == 12
        assert str(
            fetch_bike_stand_2.historical[1].time) == "2021-03-15 15:15:15"

    def test_fetch_data_from_db_for_minutes(self):
        store_bike_data_to_database = StoreBikeDataToDatabase()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        BikeStands(name='bike_stand_1').save()
        BikeStands(name='bike_stand_2').save()

        bike_stand_1 = BikeStands.objects(name='bike_stand_1').first()
        bike_stand_2 = BikeStands.objects(name='bike_stand_2').first()

        bike_stand_1.historical.append(
            BikeAvailability(
                bike_stands=40,
                available_bike_stands=10,
                time='2021-03-15 13:15:15')
        )
        bike_stand_1.save()

        bike_stand_2.historical.append(
            BikeAvailability(
                bike_stands=40,
                available_bike_stands=20,
                time='2021-03-15 14:15:15')
        )
        bike_stand_2.historical.append(
            BikeAvailability(
                bike_stands=40,
                available_bike_stands=30,
                time='2021-03-15 15:15:15')
        )
        bike_stand_2.save()

        result = store_bike_data_to_database.fetch_data_from_db_for_minutes()

        expected_result = [
            {
                'historical': [
                    {
                        'bike_stands': 40,
                        'available_bike_stands': 10,
                        'time': FakeDatetime(2021, 3, 15, 13, 15, 15)
                    }
                ],
                'name': 'bike_stand_1'
            },
            {
                'historical': [
                    {
                        'bike_stands': 40,
                        'available_bike_stands': 30,
                        'time': FakeDatetime(2021, 3, 15, 15, 15, 15)
                    }
                ],
                'name': 'bike_stand_2'
            }
        ]

        assert expected_result == result

    def test_fetch_data_from_db_for_day(self):
        store_bike_data_to_database = StoreBikeDataToDatabase()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        BikeStands(name='bike_stand_1').save()
        BikeStands(name='bike_stand_2').save()

        bike_stand_1 = BikeStands.objects(name='bike_stand_1').first()
        bike_stand_2 = BikeStands.objects(name='bike_stand_2').first()

        bike_stand_1.historical.append(
            BikeAvailability(
                bike_stands=40,
                available_bike_stands=10,
                time='2021-03-15 13:15:15')
        )
        bike_stand_1.historical.append(
            BikeAvailability(
                bike_stands=40,
                available_bike_stands=10,
                time='2021-03-14 13:15:15')
        )
        bike_stand_1.save()

        bike_stand_2.historical.append(
            BikeAvailability(
                bike_stands=40,
                available_bike_stands=20,
                time='2021-03-15 14:15:15')
        )
        bike_stand_2.historical.append(
            BikeAvailability(
                bike_stands=40,
                available_bike_stands=30,
                time='2021-03-15 15:15:15')
        )
        bike_stand_2.save()

        result = store_bike_data_to_database.fetch_data_from_db_for_day(
            datetime.now())

        expected_result = [
            {
                'historical': [
                    {
                        'bike_stands': 40,
                        'available_bike_stands': 10,
                        'time': FakeDatetime(2021, 3, 15, 13, 15, 15)
                    }
                ],
                'name': 'bike_stand_1'
            },
            {
                'historical': [
                    {
                        'bike_stands': 40,
                        'available_bike_stands': 20,
                        'time': FakeDatetime(2021, 3, 15, 14, 15, 15)
                    },
                    {
                        'bike_stands': 40,
                        'available_bike_stands': 30,
                        'time': FakeDatetime(2021, 3, 15, 15, 15, 15)
                    }
                ],
                'name': 'bike_stand_2'
            }
        ]

        assert expected_result == result
