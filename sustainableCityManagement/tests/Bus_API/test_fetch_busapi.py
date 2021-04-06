from main_project.Bus_API import fetch_busapi
from main_project.Bus_API.store_bus_routes_data_in_database import StoreBusRoutesData
from django.test import TestCase
from unittest.mock import MagicMock
from mock import patch
import json
import datetime
from freezegun import freeze_time


@freeze_time("2021-03-11 17")
class TestFetchBusApi(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_busapi_locations(self):
        fetch_bus_api_class = fetch_busapi.FetchBusApi()

        store_bus_data_to_database = StoreBusRoutesData()

        mocked_result = [
            {
                "stop_id": "stop_0",
                "stop_name": "test_name_1",
                "stop_lat": 1,
                "stop_lon": 2
            },
            {
                "stop_id": "stop_1",
                "stop_name": "test_name_2",
                "stop_lat": 3,
                "stop_lon": 4
            }
        ]
        store_bus_data_to_database.fetch_busstops_location = MagicMock(
            return_value=mocked_result)

        expected_result = {
            "stop_0": {
                "STOP_ID": "stop_0",
                "STOP_NAME": "test_name_1",
                "STOP_LAT": 1,
                "STOP_LON": 2
            },

            "stop_1": {
                "STOP_ID": "stop_1",
                "STOP_NAME": "test_name_2",
                "STOP_LAT": 3,
                "STOP_LON": 4
            }
        }

        result = fetch_bus_api_class.bus_stand_locations(
            busRoutesObj=store_bus_data_to_database)
        self.assertDictEqual(result, expected_result)

    def test_busapi_timings(self):
        fetch_bus_api_class = fetch_busapi.FetchBusApi()
        store_bus_data_to_database = StoreBusRoutesData()
        mocked_result_bus_trips = [
            {
                "trip_id": "315_IJ",
                "route_id": "route_0",
                "stops": []
            },
            {
                "trip_id": "315_IJ",
                "route_id": "route_1",
                "stops": []
            }
        ]
        store_bus_data_to_database.fetch_bustrips = MagicMock(
            return_value=mocked_result_bus_trips)


        mocked_result_routes = [
            {
                "route_name": "route_name_0",
                "route_id": "route_0",
            },
            {
                "route_name": "route_name_1",
                "route_id": "route_1",
            }
        ]
        store_bus_data_to_database.fetch_busroutes = MagicMock(
            return_value=mocked_result_routes)

        expected_result = {
            "trip_0": {
                "TRIP_ID": "315_IJ",
                "ROUTE_ID": "route_0",
                "ROUTE_NAME": "route_name_0",
                "STOP_INFO": []
            },

            "trip_1": {
                "TRIP_ID": "315_IJ",
                "ROUTE_ID": "route_1",
                "ROUTE_NAME": "route_name_1",
                "STOP_INFO": []
            }
        }
        result = fetch_bus_api_class.bus_trips_timings(
            busRoutesObj=store_bus_data_to_database)
        self.assertDictEqual(result, expected_result)
